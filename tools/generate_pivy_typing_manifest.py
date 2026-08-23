"""Generate or compare a canonical manifest for a Pivy stub file."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from tools.pivy_typing.manifest import (
    manifest_diff,
    manifest_from_stub,
    render_manifest,
)
from tools.pivy_typing.baseline import manifest_baseline_issues


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stub", type=Path)
    parser.add_argument(
        "--compare",
        type=Path,
        help="compare the stub manifest with another stub instead of rendering it",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="write the manifest to this path instead of stdout",
    )
    parser.add_argument(
        "--check-baseline",
        action="store_true",
        help="check the input against the reviewed Coin manifest baseline",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = manifest_from_stub(args.stub)

    if args.compare is not None:
        differences = manifest_diff(manifest, manifest_from_stub(args.compare))
        if differences:
            print("Pivy typing manifests differ:")
            print("\n".join(differences))
            return 1
        print("Pivy typing manifests are semantically equivalent")
        return 0

    if args.check_baseline:
        issues = manifest_baseline_issues(manifest)
        if issues:
            print("Pivy typing manifest baseline mismatch:")
            print("\n".join(issues))
            return 1
        print("Pivy typing manifest matches the reviewed baseline")
        return 0

    output = render_manifest(manifest)
    if args.output is None:
        sys.stdout.write(output)
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(output, encoding="utf-8")
    print("Wrote Pivy typing manifest to %s" % args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
