"""Report typing-quality metrics for a generated Pivy stub file."""

from __future__ import annotations

import argparse
import ast
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from tools.pivy_stub_typing_policy import (
    INCOMPLETE_CATEGORIES,
    classify_incomplete,
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
    incomplete_sites: tuple[tuple[AnnotationSite, str], ...]


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
    for site in annotation_sites:
        if has_annotation_name(site.annotation, "Incomplete"):
            category = classify_incomplete(
                kind=site.kind,
                class_name=site.class_name,
                method_name=site.method_name,
                parameter_name=site.name,
                has_raw_pointer_note=has_raw_pointer_note(site, source_lines),
            )
            incomplete_sites.append((site, category))
            category_counts[category] += 1
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
        incomplete_sites=tuple(incomplete_sites),
    )


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
    ]
    for category in INCOMPLETE_CATEGORIES:
        count = report.incomplete_categories[category]
        lines.append(
            "%-30s %6d    %s"
            % (category, count, percentage(count, report.incomplete_annotations))
        )
    return "\n".join(lines)


def format_site(site: AnnotationSite) -> str:
    if site.kind == "attribute":
        return "%s.%s" % (site.class_name, site.name)
    if site.kind == "return":
        return "%s.%s() -> return" % (site.class_name, site.method_name)
    return "%s.%s(%s)" % (site.class_name, site.method_name, site.name)


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
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = collect_report(args.stub)
    output = format_report(report, args.stub)
    if args.show_uncategorized:
        output += format_uncategorized(report)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
