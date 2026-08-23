"""Compare two stub producers through the canonical Pivy API manifest."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
import sys

from tools.pivy_typing.manifest import manifest_diff, manifest_from_stub


def classify_difference(difference):
    """Classify a manifest path without interpreting producer formatting."""

    if difference.startswith("$.boundaries"):
        return "intentional-boundary"
    if difference.startswith("$.callback_contracts"):
        return "binding-metadata"
    if difference.startswith("$.classes"):
        return "python-api"
    if difference.startswith("$.schema_version"):
        return "schema"
    return "manifest"


def compare_producers(reference: Path, candidate: Path):
    """Return a deterministic semantic comparison result."""

    reference_manifest = manifest_from_stub(reference)
    candidate_manifest = manifest_from_stub(candidate)
    differences = manifest_diff(reference_manifest, candidate_manifest)
    classified = tuple(
        {
            "category": classify_difference(difference),
            "difference": difference,
        }
        for difference in differences
    )
    return {
        "candidate": str(candidate),
        "categories": dict(sorted(Counter(item["category"] for item in classified).items())),
        "equivalent": not differences,
        "differences": list(classified),
        "reference": str(reference),
    }


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reference", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    return parser.parse_args()


def main():
    args = parse_args()
    result = compare_producers(args.reference, args.candidate)
    if args.as_json:
        json.dump(result, sys.stdout, indent=2, sort_keys=True)
        sys.stdout.write("\n")
    elif result["equivalent"]:
        print("Pivy typing producers are semantically equivalent")
    else:
        print("Pivy typing producers differ:")
        for category, count in result["categories"].items():
            print("  %s: %d" % (category, count))
        for item in result["differences"]:
            print("  [%s] %s" % (item["category"], item["difference"]))
    return 0 if result["equivalent"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
