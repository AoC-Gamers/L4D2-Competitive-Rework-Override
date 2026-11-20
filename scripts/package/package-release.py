#!/usr/bin/env python3

import argparse
import shutil
from pathlib import Path
from tempfile import TemporaryDirectory

from artifact_contract import relative_path, validate, validate_zip


def main() -> None:
    parser = argparse.ArgumentParser(description="Package a validated SourceMod artifact into a ZIP.")
    parser.add_argument("--root", default=".", type=Path)
    parser.add_argument("--artifact", type=Path)
    parser.add_argument("--basename", required=True)
    args = parser.parse_args()

    root = args.root.resolve()
    artifact = (root / (args.artifact or "dist/sourcemod/artifact")).resolve()
    if relative_path(args.basename).parts != (args.basename,):
        parser.error("--basename must be a single filename without directories")

    validate(root, artifact)
    release_dir = root / "dist/release"
    release_dir.mkdir(parents=True, exist_ok=True)
    archive = release_dir / f"{args.basename}.zip"
    with TemporaryDirectory(dir=release_dir) as temp:
        candidate = Path(shutil.make_archive(str(Path(temp) / args.basename), "zip", root_dir=artifact))
        validate_zip(root, candidate)
        candidate.replace(archive)
    print(f"Release archive generated in: {archive}")


if __name__ == "__main__":
    main()
