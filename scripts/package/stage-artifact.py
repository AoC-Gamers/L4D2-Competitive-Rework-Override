#!/usr/bin/env python3

import argparse
import shutil
from pathlib import Path

from artifact_contract import BUCKETS, PLUGINS, SOURCEMOD, project_files, validate


def main() -> None:
    parser = argparse.ArgumentParser(description="Stage the SourceMod product for packaging.")
    parser.add_argument("root_dir", type=Path)
    parser.add_argument("build_dir", type=Path)
    parser.add_argument("compile_log", type=Path, help="Existing CLI input. The log stays outside the installer.")
    parser.add_argument("output_dir", type=Path, nargs="?")
    args = parser.parse_args()

    root = args.root_dir.resolve()
    source = args.build_dir.resolve()
    output = (args.output_dir or root / "dist/sourcemod/artifact").resolve()
    if source == output or source.is_relative_to(output) or output.is_relative_to(source):
        parser.error("Staging requires separate input and output trees")

    validate(root, source, build_tree=not (source / "README.md").exists())
    documents = project_files(root)
    if output.exists():
        shutil.rmtree(output)

    shutil.copytree(source / SOURCEMOD, output / SOURCEMOD)
    for bucket in BUCKETS[1:]:
        (output / PLUGINS / bucket).mkdir(parents=True, exist_ok=True)
    for path in documents:
        shutil.copy2(root / path, output / path)
    validate(root, output)
    print(f"SourceMod artifacts generated in {output}")


if __name__ == "__main__":
    main()
