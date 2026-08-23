"""Reviewed backend-neutral baseline for the current public Coin API."""

from __future__ import annotations

from hashlib import sha256

from .manifest import render_manifest


COIN_MANIFEST_BASELINE = {
    "module": "pivy.coin",
    "schema_version": 1,
    "classes": 842,
    "methods": 9598,
    "attributes": 2738,
    "boundaries": 417,
    "callback_contracts": 78,
    "sha256": "90d6e9643b1963f63f5e4c78b7d075567f2e8b43ace24771c4f9249ab2300c06",
}


def manifest_fingerprint(manifest):
    """Return the digest of the canonical rendered manifest."""

    return sha256(render_manifest(manifest).encode("utf-8")).hexdigest()


def manifest_summary(manifest):
    """Return stable structural counts used in baseline diagnostics."""

    return {
        "module": manifest["module"],
        "schema_version": manifest["schema_version"],
        "classes": len(manifest["classes"]),
        "methods": sum(
            len(class_manifest["methods"])
            for class_manifest in manifest["classes"].values()
        ),
        "attributes": sum(
            len(class_manifest["attributes"])
            for class_manifest in manifest["classes"].values()
        ),
        "boundaries": len(manifest["boundaries"]),
        "callback_contracts": len(manifest["callback_contracts"]),
    }


def manifest_baseline_issues(manifest):
    """Return actionable differences from the reviewed Coin baseline."""

    issues = []
    summary = manifest_summary(manifest)
    for key, expected in COIN_MANIFEST_BASELINE.items():
        if key == "sha256":
            actual = manifest_fingerprint(manifest)
        else:
            actual = summary.get(key)
        if actual != expected:
            issues.append("%s: expected %r, got %r" % (key, expected, actual))
    return tuple(issues)


__all__ = [
    "COIN_MANIFEST_BASELINE",
    "manifest_baseline_issues",
    "manifest_fingerprint",
    "manifest_summary",
]
