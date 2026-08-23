"""Remediation ownership for Pivy typing boundaries and special contracts."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

try:
    from tools.pivy_stub_typing_policy import (
        OPAQUE_RETURN_AUDIT,
        RAW_POINTER_AUDIT,
        classify_dynamic_runtime_site,
    )
except ImportError:
    from pivy_stub_typing_policy import (
        OPAQUE_RETURN_AUDIT,
        RAW_POINTER_AUDIT,
        classify_dynamic_runtime_site,
    )


class RemediationClass(str, Enum):
    """Primary owner of the work needed to improve one API boundary."""

    TYPING = "A"
    PIVY_BINDING = "B"
    COIN_API = "C"
    INTENTIONALLY_NATIVE = "D"


REMEDIATION_CLASS_LABELS = {
    RemediationClass.TYPING: "typing/backend limitation",
    RemediationClass.PIVY_BINDING: "Pivy binding limitation",
    RemediationClass.COIN_API: "Coin API limitation",
    RemediationClass.INTENTIONALLY_NATIVE: "intentionally native",
}


@dataclass(frozen=True)
class RemediationRecord:
    """Ownership, confidence and next action for one semantic contract."""

    classification: RemediationClass
    confidence: str
    rationale: str
    next_action: str
    source: str

    @property
    def code(self) -> str:
        return self.classification.value

    @property
    def label(self) -> str:
        return REMEDIATION_CLASS_LABELS[self.classification]


POLICY_SOURCE = "tools/pivy_typing/remediation.py"
AUDIT_SOURCE = "tools/pivy_stub_typing_policy.py"


def boundary_key(boundary) -> tuple[str, str, str, str]:
    """Return the stable identity shared by reports and audit registries."""

    return (
        boundary.kind,
        boundary.class_name,
        boundary.method_name or "",
        boundary.name,
    )


def _record(
    classification: RemediationClass,
    *,
    confidence: str,
    rationale: str,
    next_action: str,
    source: str = POLICY_SOURCE,
) -> RemediationRecord:
    return RemediationRecord(
        classification=classification,
        confidence=confidence,
        rationale=rationale,
        next_action=next_action,
        source=source,
    )


def _raw_pointer_remediation(key, audit) -> RemediationRecord:
    if audit.disposition == "intentional native input boundary":
        return _record(
            RemediationClass.PIVY_BINDING,
            confidence="reviewed",
            rationale=(
                "The native input can potentially be made safe by a Pivy "
                "copying or owning adapter without changing Coin."
            ),
            next_action=(
                "Confirm the native layout and add a tested Python adapter."
            ),
            source=AUDIT_SOURCE,
        )
    if audit.disposition == "intentional ABI boundary":
        return _record(
            RemediationClass.INTENTIONALLY_NATIVE,
            confidence="reviewed",
            rationale=(
                "The boundary is an ABI-level handle, pointer-to-pointer, "
                "file descriptor or mutable native storage interface."
            ),
            next_action=(
                "Keep native unless a stable serialized or buffer API is "
                "needed by a supported Python workflow."
            ),
            source=AUDIT_SOURCE,
        )
    if audit.disposition == "intentional native output boundary":
        return _record(
            RemediationClass.COIN_API,
            confidence="reviewed",
            rationale=(
                "Coin exposes a native output sink rather than a value that "
                "a binding can type independently."
            ),
            next_action=(
                "Consider an additive Coin serialization or file-like API."
            ),
            source=AUDIT_SOURCE,
        )
    return _record(
        RemediationClass.COIN_API,
        confidence="reviewed",
        rationale=(
            "Coin returns borrowed native storage without an independent "
            "Python owner or lifetime contract."
        ),
        next_action=(
            "Add an owning copy or lifetime-bound view at the Coin/Pivy API "
            "boundary."
        ),
        source=AUDIT_SOURCE,
    )


def _opaque_return_remediation(key, audit) -> RemediationRecord:
    _, class_name, method_name, _ = key
    if class_name.startswith("SoMF") and method_name == "startEditing":
        return _record(
            RemediationClass.PIVY_BINDING,
            confidence="reviewed",
            rationale=(
                "Pivy can expose an owned snapshot or edit-session wrapper "
                "while preserving the native field storage internally."
            ),
            next_action=(
                "Add a typed snapshot/edit-session adapter with runtime tests."
            ),
            source=AUDIT_SOURCE,
        )
    return _record(
        RemediationClass.COIN_API,
        confidence="reviewed",
        rationale=(
            "The native API exposes borrowed geometry, cache or object "
            "storage without enough ownership or extent information for a "
            "safe generic binding adapter."
        ),
        next_action=(
            "Prefer an additive owning/copying Coin API, then expose it in "
            "Pivy."
        ),
        source=AUDIT_SOURCE,
    )


def remediation_for_boundary(boundary) -> RemediationRecord:
    """Classify one boundary using reviewed audits and conservative defaults."""

    key = boundary_key(boundary)
    if key in RAW_POINTER_AUDIT:
        return _raw_pointer_remediation(key, RAW_POINTER_AUDIT[key])
    if key in OPAQUE_RETURN_AUDIT:
        return _opaque_return_remediation(key, OPAQUE_RETURN_AUDIT[key])

    if boundary.category == "unknown output parameters":
        return _record(
            RemediationClass.TYPING,
            confidence="provisional",
            rationale=(
                "The native output shape needs a typed tuple or helper in "
                "the generated Python contract."
            ),
            next_action="Add a typed output policy and runtime assertion.",
        )
    if boundary.category == "callbacks":
        return _record(
            RemediationClass.PIVY_BINDING,
            confidence="provisional",
            rationale=(
                "A Pivy callback adapter may be able to provide Python "
                "lifecycle and userdata semantics."
            ),
            next_action="Confirm retention/removal behavior and model a callback contract.",
        )
    if boundary.category == "function pointers":
        return _record(
            RemediationClass.INTENTIONALLY_NATIVE,
            confidence="provisional",
            rationale=(
                "The boundary is a native C function-pointer ABI rather than "
                "a directly callable Python value."
            ),
            next_action="Keep native unless a supported Python callback adapter is justified.",
        )
    if boundary.category == "dynamic/runtime API":
        subcategory = classify_dynamic_runtime_site(
            kind=boundary.kind,
            method_name=boundary.method_name,
        )
        if subcategory == "opaque field storage":
            return _record(
                RemediationClass.PIVY_BINDING,
                confidence="provisional",
                rationale=(
                    "The runtime field value can likely be exposed through a "
                    "Pivy-owned protocol or snapshot."
                ),
                next_action="Define a field protocol or owned snapshot and test it.",
            )
        if subcategory == "runtime factory returns":
            return _record(
                RemediationClass.TYPING,
                confidence="provisional",
                rationale=(
                    "The runtime factory may already return a typed concrete "
                    "object; the missing piece is static downcast knowledge."
                ),
                next_action="Verify runtime downcast behavior and add a factory policy rule.",
            )
        return _record(
            RemediationClass.COIN_API,
            confidence="provisional",
            rationale=(
                "The public native API leaves object ownership, extent or "
                "parameter semantics opaque to a binding."
            ),
            next_action="Identify an additive Coin API or a narrowly scoped Pivy adapter.",
        )
    if boundary.category == "uncategorized":
        return _record(
            RemediationClass.TYPING,
            confidence="provisional",
            rationale="The site has not yet received a valid semantic boundary classification.",
            next_action="Classify the site before accepting it into the reviewed baseline.",
        )
    return _record(
        RemediationClass.TYPING,
        confidence="provisional",
        rationale="The boundary category is not recognized by the remediation policy.",
        next_action="Extend the remediation policy with an explicit owner.",
    )


def remediation_for_method_contract(contract) -> RemediationRecord:
    """Classify a policy-owned method contract."""

    return _record(
        RemediationClass.TYPING,
        confidence="reviewed",
        rationale=(
            "The runtime adapter is already represented; this contract "
            "controls the generated Python typing surface."
        ),
        next_action="Keep the policy contract synchronized with runtime tests.",
        source=contract.source,
    )


def remediation_for_callback_contract(contract) -> RemediationRecord:
    """Classify a Python-facing callback lifecycle contract."""

    return _record(
        RemediationClass.PIVY_BINDING,
        confidence="reviewed",
        rationale=(
            "Callback retention, userdata and removal semantics are supplied "
            "by the Pivy binding adapter."
        ),
        next_action="Retain independent callback lifetime tests as the contract evolves.",
        source=contract.source,
    )


__all__ = [
    "AUDIT_SOURCE",
    "POLICY_SOURCE",
    "REMEDIATION_CLASS_LABELS",
    "RemediationClass",
    "RemediationRecord",
    "boundary_key",
    "remediation_for_boundary",
    "remediation_for_callback_contract",
    "remediation_for_method_contract",
]
