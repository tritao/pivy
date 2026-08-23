"""Report typing-quality metrics for a generated Pivy stub file."""

from __future__ import annotations

import argparse
import ast
import json
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from tools.pivy_stub_typing_policy import (
    DYNAMIC_RUNTIME_SUBCATEGORIES,
    GEOMETRY_PARAMETER_AUDIT,
    INCOMPLETE_CATEGORIES,
    INCOMPLETE_CATEGORY_ACTIONS,
    INCOMPLETE_CATEGORY_POLICIES,
    OPAQUE_PARAMETER_FAMILY_ACTIONS,
    OPAQUE_RETURN_AUDIT,
    RAW_POINTER_AUDIT,
    classify_incomplete,
    classify_dynamic_runtime_site,
)
from tools.pivy_typing.resolved import resolve_stub


OPAQUE_PARAMETER_FAMILIES = (
    "geometry",
    "image/buffer",
    "action",
    "array/output",
    "callback/handle",
    "other",
)


@dataclass(frozen=True)
class AnnotationSite:
    """One parameter, return value, or class attribute annotation."""

    kind: str
    class_name: str
    method_name: str | None
    name: str
    annotation: ast.expr
    line: int


@dataclass(frozen=True)
class TypingReport:
    classes: int
    methods: int
    parameters: int
    annotation_sites: int
    concrete_annotations: int
    any_annotations: int
    incomplete_annotations: int
    incomplete_categories: Counter[str]
    dynamic_runtime_subcategories: Counter[str]
    opaque_parameter_families: Counter[str]
    incomplete_sites: tuple[tuple[AnnotationSite, str], ...]


@dataclass(frozen=True)
class TypingQualityBaseline:
    """Reviewed lower/upper bounds for the generated Coin typing surface."""

    min_concrete_annotations: int
    max_any_annotations: int
    max_incomplete_annotations: int
    max_incomplete_by_category: tuple[tuple[str, int], ...] = ()


# These values are intentionally explicit.  Improving the generated surface
# should make the relevant bound stricter in the same reviewed change; an
# accidental generator or dependency drift must not silently lower quality.
TYPING_QUALITY_BASELINE = TypingQualityBaseline(
    min_concrete_annotations=21842,
    max_any_annotations=0,
    max_incomplete_annotations=400,
    max_incomplete_by_category=(
        ("raw C pointers", 102),
        ("callbacks", 30),
        ("unknown output parameters", 0),
        ("function pointers", 36),
        ("dynamic/runtime API", 232),
        ("uncategorized", 0),
    ),
)


def quality_regressions(
    report: TypingReport,
    baseline: TypingQualityBaseline = TYPING_QUALITY_BASELINE,
) -> tuple[str, ...]:
    """Return human-readable violations of the reviewed typing baseline."""

    violations = []
    if report.concrete_annotations < baseline.min_concrete_annotations:
        violations.append(
            "concrete annotations dropped below %d (got %d)"
            % (baseline.min_concrete_annotations, report.concrete_annotations)
        )
    if report.any_annotations > baseline.max_any_annotations:
        violations.append(
            "Any annotations exceeded %d (got %d)"
            % (baseline.max_any_annotations, report.any_annotations)
        )
    if report.incomplete_annotations > baseline.max_incomplete_annotations:
        violations.append(
            "Incomplete annotations exceeded %d (got %d)"
            % (baseline.max_incomplete_annotations, report.incomplete_annotations)
        )
    for category, maximum in baseline.max_incomplete_by_category:
        actual = report.incomplete_categories[category]
        if actual > maximum:
            violations.append(
                "%s Incomplete sites exceeded %d (got %d)"
                % (category, maximum, actual)
            )
    return tuple(violations)


def method_parameters(method: ast.FunctionDef | ast.AsyncFunctionDef) -> list[ast.arg]:
    """Return public parameters, including *args and **kwargs when present."""

    parameters = [
        *method.args.posonlyargs,
        *method.args.args,
        *method.args.kwonlyargs,
    ]
    if method.args.vararg is not None:
        parameters.append(method.args.vararg)
    if method.args.kwarg is not None:
        parameters.append(method.args.kwarg)
    return [
        parameter
        for parameter in parameters
        if parameter.arg not in {"self", "cls"}
    ]


def annotation_names(annotation: ast.expr) -> set[str]:
    return {
        node.id
        for node in ast.walk(annotation)
        if isinstance(node, ast.Name)
    }


def has_annotation_name(annotation: ast.expr, name: str) -> bool:
    return name in annotation_names(annotation)


def is_comment_or_decorator(line: str) -> bool:
    stripped = line.strip()
    return not stripped or stripped.startswith("#") or stripped.startswith("@")


def has_raw_pointer_note(site: AnnotationSite, source_lines: list[str]) -> bool:
    """Recognize the generator's explicit note on intentionally raw surfaces."""

    index = site.line - 2
    while index >= 0 and is_comment_or_decorator(source_lines[index]):
        if "raw C pointers" in source_lines[index]:
            return True
        index -= 1
    return False


def iter_class_members(tree: ast.Module) -> Iterable[tuple[ast.ClassDef, ast.stmt]]:
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            for member in node.body:
                yield node, member


def collect_report(stub_path: Path) -> TypingReport:
    source = stub_path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(stub_path))
    resolved_model = resolve_stub(source, name=str(stub_path))
    semantic_boundaries = {
        (
            boundary.kind,
            boundary.class_name,
            boundary.method_name,
            boundary.name,
            boundary.line,
        ): boundary.category
        for boundary in resolved_model.incomplete_boundaries
    }
    source_lines = source.splitlines()
    classes = [node for node in tree.body if isinstance(node, ast.ClassDef)]
    methods = [
        member
        for _, member in iter_class_members(tree)
        if isinstance(member, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]

    parameters = sum(len(method_parameters(method)) for method in methods)
    annotation_sites: list[AnnotationSite] = []
    for class_node, member in iter_class_members(tree):
        if isinstance(member, ast.AnnAssign) and member.annotation is not None:
            if isinstance(member.target, ast.Name):
                annotation_sites.append(
                    AnnotationSite(
                        "attribute",
                        class_node.name,
                        None,
                        member.target.id,
                        member.annotation,
                        member.lineno,
                    )
                )
            continue

        if not isinstance(member, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for parameter in method_parameters(member):
            if parameter.annotation is not None:
                annotation_sites.append(
                    AnnotationSite(
                        "parameter",
                        class_node.name,
                        member.name,
                        parameter.arg,
                        parameter.annotation,
                        parameter.lineno,
                    )
                )
        if member.returns is not None:
            annotation_sites.append(
                AnnotationSite(
                    "return",
                    class_node.name,
                    member.name,
                    "return",
                    member.returns,
                    member.lineno,
                )
            )

    incomplete_sites: list[tuple[AnnotationSite, str]] = []
    status_counts = Counter()
    category_counts = Counter()
    # Keep the JSON/report shape stable even when a reviewed subcategory
    # reaches zero after an adapter lands.
    dynamic_subcategory_counts = Counter(
        {subcategory: 0 for subcategory in DYNAMIC_RUNTIME_SUBCATEGORIES}
    )
    opaque_parameter_family_counts = Counter(
        {family: 0 for family in OPAQUE_PARAMETER_FAMILIES}
    )
    for site in annotation_sites:
        if has_annotation_name(site.annotation, "Incomplete"):
            category = semantic_boundaries.get(
                (
                    site.kind,
                    site.class_name,
                    site.method_name,
                    site.name,
                    site.line,
                )
            )
            if category is None:
                category = classify_incomplete(
                    kind=site.kind,
                    class_name=site.class_name,
                    method_name=site.method_name,
                    parameter_name=site.name,
                    has_raw_pointer_note=has_raw_pointer_note(site, source_lines),
                )
            incomplete_sites.append((site, category))
            category_counts[category] += 1
            if category == "dynamic/runtime API":
                subcategory = classify_dynamic_runtime_site(
                    kind=site.kind,
                    method_name=site.method_name,
                )
                dynamic_subcategory_counts[subcategory] += 1
                if subcategory == "opaque parameter boundaries":
                    opaque_parameter_family_counts[
                        classify_opaque_parameter_family(site)
                    ] += 1
            status_counts["incomplete"] += 1
        elif has_annotation_name(site.annotation, "Any"):
            status_counts["any"] += 1
        else:
            status_counts["concrete"] += 1

    return TypingReport(
        classes=len(classes),
        methods=len(methods),
        parameters=parameters,
        annotation_sites=len(annotation_sites),
        concrete_annotations=status_counts["concrete"],
        any_annotations=status_counts["any"],
        incomplete_annotations=status_counts["incomplete"],
        incomplete_categories=category_counts,
        dynamic_runtime_subcategories=dynamic_subcategory_counts,
        opaque_parameter_families=opaque_parameter_family_counts,
        incomplete_sites=tuple(incomplete_sites),
    )


def classify_opaque_parameter_family(site: AnnotationSite) -> str:
    """Assign a conservative review bucket to an opaque parameter.

    These buckets are triage metadata, not typing decisions.  The classifier
    deliberately favors ``other`` when the native declaration does not make
    a safe Python representation obvious.
    """

    class_name = site.class_name.lower()
    method_name = (site.method_name or "").lower()
    parameter_name = site.name.lower()
    combined = " ".join((class_name, method_name, parameter_name))

    if any(token in combined for token in ("image", "pixel", "texture", "bitmap")):
        return "image/buffer"
    if "callback" in combined or parameter_name in {
        "cb",
        "callback",
        "closure",
        "data",
        "userdata",
    }:
        return "callback/handle"
    if "action" in class_name or "action" in method_name:
        return "action"
    if class_name.startswith(("sbvec", "sbmatrix", "sbplane", "sbsphere")):
        return "geometry"
    if any(
        token in parameter_name
        for token in ("array", "indices", "values", "out", "fp")
    ):
        return "array/output"
    return "other"


def percentage(value: int, total: int) -> str:
    return "0.0%" if total == 0 else "%.1f%%" % (100 * value / total)


def format_report(report: TypingReport, stub_path: Path) -> str:
    lines = [
        "Pivy typing quality",
        "===================",
        "",
        "Stub                            %s" % stub_path,
        "Classes                         %d" % report.classes,
        "Methods                         %d" % report.methods,
        "Parameters                      %d" % report.parameters,
        "Annotation sites                %d" % report.annotation_sites,
        "",
        "Concrete annotations            %d    %s"
        % (
            report.concrete_annotations,
            percentage(report.concrete_annotations, report.annotation_sites),
        ),
        "Any                              %d    %s"
        % (
            report.any_annotations,
            percentage(report.any_annotations, report.annotation_sites),
        ),
        "Incomplete                       %d    %s"
        % (
            report.incomplete_annotations,
            percentage(report.incomplete_annotations, report.annotation_sites),
        ),
        "",
        "Incomplete categories",
        "---------------------",
        "Category                        Status       Count    Share  Next action",
    ]
    for category in INCOMPLETE_CATEGORIES:
        count = report.incomplete_categories[category]
        lines.append(
            "%-30s %-12s %6d    %-6s  %s"
            % (
                category,
                INCOMPLETE_CATEGORY_POLICIES[category].disposition,
                count,
                percentage(count, report.incomplete_annotations),
                INCOMPLETE_CATEGORY_ACTIONS[category],
            )
        )
    lines.extend(
        [
            "",
            "Dynamic/runtime inventory",
            "-------------------------",
            "Subcategory                     Count    Next action",
        ]
    )
    for subcategory in DYNAMIC_RUNTIME_SUBCATEGORIES:
        lines.append(
            "%-30s %6d    %s"
            % (
                subcategory,
                report.dynamic_runtime_subcategories[subcategory],
                {
                    "runtime factory returns": "verify factory downcast behavior",
                    "opaque pointer/object returns": "add a Python adapter where stable",
                    "opaque parameter boundaries": "model or document the ABI boundary",
                    "opaque field storage": "replace raw storage with a field protocol",
                }[subcategory],
            )
        )
    lines.extend(
        [
            "",
            "Opaque parameter triage",
            "-----------------------",
            "Family                          Count",
        ]
    )
    for family in OPAQUE_PARAMETER_FAMILIES:
        lines.append(
            "%-30s %6d    %s"
            % (
                family,
                report.opaque_parameter_families[family],
                OPAQUE_PARAMETER_FAMILY_ACTIONS[family],
            )
        )
    return "\n".join(lines)


def report_to_dict(report: TypingReport, stub_path: Path) -> dict[str, object]:
    """Return stable, JSON-serializable typing-quality data."""

    incomplete_categories = {}
    for category in INCOMPLETE_CATEGORIES:
        count = report.incomplete_categories[category]
        incomplete_categories[category] = {
            "count": count,
            "share_percent": (
                0.0
                if report.incomplete_annotations == 0
                else round(100 * count / report.incomplete_annotations, 1)
            ),
            "disposition": INCOMPLETE_CATEGORY_POLICIES[category].disposition,
            "next_action": INCOMPLETE_CATEGORY_ACTIONS[category],
        }

    payload = {
        "schema_version": 6,
        "stub": str(stub_path),
        "classes": report.classes,
        "methods": report.methods,
        "parameters": report.parameters,
        "annotation_sites": report.annotation_sites,
        "concrete_annotations": report.concrete_annotations,
        "any_annotations": report.any_annotations,
        "incomplete_annotations": report.incomplete_annotations,
        "incomplete_categories": incomplete_categories,
        "dynamic_runtime_subcategories": {
            subcategory: report.dynamic_runtime_subcategories[subcategory]
            for subcategory in DYNAMIC_RUNTIME_SUBCATEGORIES
        },
        "opaque_parameter_families": {
            family: report.opaque_parameter_families[family]
            for family in OPAQUE_PARAMETER_FAMILIES
        },
        "opaque_parameter_family_actions": {
            family: OPAQUE_PARAMETER_FAMILY_ACTIONS[family]
            for family in OPAQUE_PARAMETER_FAMILIES
        },
    }
    if stub_path.name == "coin.pyi":
        payload["opaque_return_audit"] = opaque_return_audit_summary(report)
        payload["raw_pointer_audit"] = raw_pointer_audit_summary(report)
        payload["geometry_parameter_audit"] = geometry_parameter_audit_summary(
            report
        )
    return payload


def format_site(site: AnnotationSite) -> str:
    if site.kind == "attribute":
        return "%s.%s" % (site.class_name, site.name)
    if site.kind == "return":
        return "%s.%s() -> return" % (site.class_name, site.method_name)
    return "%s.%s(%s)" % (site.class_name, site.method_name, site.name)


def format_site_key(key: tuple[str, str, str, str]) -> str:
    kind, class_name, method_name, name = key
    if kind == "return":
        return "%s.%s() -> return" % (class_name, method_name)
    if kind == "attribute":
        return "%s.%s" % (class_name, name)
    return "%s.%s(%s)" % (class_name, method_name, name)


def opaque_return_sites(report: TypingReport) -> set[tuple[str, str, str, str]]:
    """Return the currently observed opaque pointer/object return keys."""

    return {
        (site.kind, site.class_name, site.method_name or "", site.name)
        for site, category in report.incomplete_sites
        if category == "dynamic/runtime API"
        and classify_dynamic_runtime_site(
            kind=site.kind,
            method_name=site.method_name,
        )
        == "opaque pointer/object returns"
    }


def raw_pointer_sites(report: TypingReport) -> set[tuple[str, str, str, str]]:
    """Return the unique sites classified as raw C-pointer boundaries."""

    return {
        (site.kind, site.class_name, site.method_name or "", site.name)
        for site, category in report.incomplete_sites
        if category == "raw C pointers"
    }


def geometry_parameter_sites(
    report: TypingReport,
) -> set[tuple[str, str, str, str]]:
    """Return the currently observed opaque geometry parameter sites."""

    return {
        (site.kind, site.class_name, site.method_name or "", site.name)
        for site, category in report.incomplete_sites
        if category == "dynamic/runtime API"
        and classify_opaque_parameter_family(site) == "geometry"
    }


def geometry_parameter_audit_issues(report: TypingReport) -> tuple[str, ...]:
    """Return missing or stale entries in the geometry boundary audit."""

    observed = geometry_parameter_sites(report)
    audited = set(GEOMETRY_PARAMETER_AUDIT)
    issues = []
    for key in sorted(observed - audited):
        issues.append(
            "geometry parameter is not audited: %s" % format_site_key(key)
        )
    for key in sorted(audited - observed):
        issues.append(
            "geometry parameter audit entry is stale: %s" % format_site_key(key)
        )
    return tuple(issues)


def geometry_parameter_audit_summary(report: TypingReport) -> dict[str, object]:
    """Return a compact machine-readable geometry-boundary audit summary."""

    observed = geometry_parameter_sites(report)
    dispositions = Counter(
        GEOMETRY_PARAMETER_AUDIT[key].disposition
        for key in observed
        if key in GEOMETRY_PARAMETER_AUDIT
    )
    return {
        "observed": len(observed),
        "audited": len(observed & set(GEOMETRY_PARAMETER_AUDIT)),
        "dispositions": dict(sorted(dispositions.items())),
    }


def raw_pointer_audit_issues(report: TypingReport) -> tuple[str, ...]:
    """Return missing or stale entries in the reviewed raw-pointer audit."""

    observed = raw_pointer_sites(report)
    audited = set(RAW_POINTER_AUDIT)
    issues = []
    for key in sorted(observed - audited):
        issues.append("raw pointer is not audited: %s" % format_site_key(key))
    for key in sorted(audited - observed):
        issues.append("raw pointer audit entry is stale: %s" % format_site_key(key))
    return tuple(issues)


def raw_pointer_audit_summary(report: TypingReport) -> dict[str, object]:
    """Return a compact machine-readable raw-pointer audit summary."""

    observed = raw_pointer_sites(report)
    dispositions = Counter(
        RAW_POINTER_AUDIT[key].disposition
        for key in observed
        if key in RAW_POINTER_AUDIT
    )
    return {
        "observed": len(observed),
        "audited": len(observed & set(RAW_POINTER_AUDIT)),
        "dispositions": dict(sorted(dispositions.items())),
    }


def opaque_return_audit_issues(report: TypingReport) -> tuple[str, ...]:
    """Return missing or stale entries in the reviewed opaque-return audit."""

    observed = opaque_return_sites(report)
    audited = set(OPAQUE_RETURN_AUDIT)
    issues = []
    for key in sorted(observed - audited):
        issues.append("opaque return is not audited: %s" % (key[1:3],))
    for key in sorted(audited - observed):
        issues.append("opaque return audit entry is stale: %s" % (key[1:3],))
    return tuple(issues)


def opaque_return_audit_summary(report: TypingReport) -> dict[str, object]:
    """Return a compact machine-readable summary of the opaque-return audit."""

    observed = opaque_return_sites(report)
    dispositions = Counter(
        OPAQUE_RETURN_AUDIT[key].disposition
        for key in observed
        if key in OPAQUE_RETURN_AUDIT
    )
    return {
        "observed": len(observed),
        "audited": len(observed & set(OPAQUE_RETURN_AUDIT)),
        "dispositions": dict(sorted(dispositions.items())),
    }


def format_opaque_return_audit(report: TypingReport) -> str:
    lines = ["", "Opaque pointer/object return audit", "---------------------------------"]
    for key in sorted(opaque_return_sites(report)):
        audit = OPAQUE_RETURN_AUDIT[key]
        lines.append(
            "%s: %s; %s; next: %s"
            % (
                format_site_key(key),
                audit.disposition,
                audit.rationale,
                audit.next_action,
            )
        )
    return "\n".join(lines)


def format_raw_pointer_audit(report: TypingReport) -> str:
    lines = ["", "Raw C-pointer audit", "--------------------"]
    for key in sorted(raw_pointer_sites(report)):
        audit = RAW_POINTER_AUDIT[key]
        lines.append(
            "%s: %s; %s; next: %s"
            % (
                format_site_key(key),
                audit.disposition,
                audit.rationale,
                audit.next_action,
            )
        )
    return "\n".join(lines)


def format_uncategorized(report: TypingReport) -> str:
    sites = [
        site
        for site, category in report.incomplete_sites
        if category == "uncategorized"
    ]
    if not sites:
        return ""
    lines = ["", "Uncategorized Incomplete sites", "-------------------------------"]
    lines.extend("%s (line %d)" % (format_site(site), site.line) for site in sites)
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stub", type=Path, help="path to a Pivy .pyi file")
    parser.add_argument(
        "--show-uncategorized",
        action="store_true",
        help="list the individual Incomplete sites left uncategorized",
    )
    parser.add_argument(
        "--show-category",
        choices=INCOMPLETE_CATEGORIES,
        help="list individual Incomplete sites in one category",
    )
    parser.add_argument(
        "--show-opaque-returns",
        action="store_true",
        help="list the reviewed opaque pointer/object return audit",
    )
    parser.add_argument(
        "--show-raw-pointers",
        action="store_true",
        help="list the reviewed raw C-pointer audit",
    )
    parser.add_argument(
        "--check-baseline",
        action="store_true",
        help="fail if the reviewed typing-quality baseline regresses",
    )
    parser.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="write a stable machine-readable JSON report",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = collect_report(args.stub)
    if args.as_json:
        print(json.dumps(report_to_dict(report, args.stub), indent=2, sort_keys=True))
    else:
        output = format_report(report, args.stub)
        if args.show_uncategorized:
            output += format_uncategorized(report)
        if args.show_category:
            sites = [
                site
                for site, category in report.incomplete_sites
                if category == args.show_category
            ]
            output += "\n\n%s Incomplete sites\n%s" % (
                args.show_category,
                "-" * (len(args.show_category) + len(" Incomplete sites")),
            )
            output += "\n" + "\n".join(
                "%s (line %d)" % (format_site(site), site.line) for site in sites
            )
        if args.show_opaque_returns:
            output += format_opaque_return_audit(report)
        if args.show_raw_pointers:
            output += format_raw_pointer_audit(report)
        print(output)
    uncategorized = report.incomplete_categories["uncategorized"]
    if uncategorized:
        print(
            "error: %d Incomplete sites are not classified" % uncategorized,
            file=sys.stderr,
        )
        return 1
    if args.stub.name == "coin.pyi":
        audit_issues = opaque_return_audit_issues(report)
        if audit_issues:
            for issue in audit_issues:
                print("error: typing audit: %s" % issue, file=sys.stderr)
            return 1
        raw_pointer_issues = raw_pointer_audit_issues(report)
        if raw_pointer_issues:
            for issue in raw_pointer_issues:
                print("error: typing audit: %s" % issue, file=sys.stderr)
            return 1
        geometry_issues = geometry_parameter_audit_issues(report)
        if geometry_issues:
            for issue in geometry_issues:
                print("error: typing audit: %s" % issue, file=sys.stderr)
            return 1
    if args.check_baseline:
        violations = quality_regressions(report)
        if violations:
            for violation in violations:
                print("error: typing baseline: %s" % violation, file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
