#!/usr/bin/env python3

import argparse
import filecmp
import json
from pathlib import Path
from zipfile import ZipFile

MAP_PATH = Path("scripts/package/package-map.json")
SOURCEMOD = Path("addons/sourcemod")
SCRIPTING = SOURCEMOD / "scripting"
TRANSLATIONS = SOURCEMOD / "translations"
PLUGINS = SOURCEMOD / "plugins"
BUCKETS = ("root", "anticheat", "fixes", "optional")
PROJECT_FILES = (Path("README.md"), Path("LICENSE"), Path("NOTICES.md"))


def load_map(root: Path) -> dict:
    with (root / MAP_PATH).open(encoding="utf-8") as manifest:
        return json.load(manifest)


def relative_path(value: str) -> Path:
    path = Path(value)
    if not path.parts or path.is_absolute() or ".." in path.parts or any(char in value for char in ":\\"):
        raise ValueError(f"Invalid path in {MAP_PATH}: {value}")
    return path


def plugin_paths(manifest: dict) -> dict[Path, Path]:
    plugins = {}
    names_seen = set()
    for bucket, names in manifest["build"]["plugins"].items():
        if bucket not in BUCKETS:
            raise ValueError(f"Unknown plugin destination in {MAP_PATH}: {bucket}")
        destination = PLUGINS if bucket == "root" else PLUGINS / bucket
        for name in names:
            if relative_path(name).parts != (name,) or name.casefold() in names_seen:
                raise ValueError(f"Duplicate or invalid plugin name in {MAP_PATH}: {name}")
            names_seen.add(name.casefold())
            plugins[destination / f"{name}.smx"] = SCRIPTING / f"{name}.sp"
    if not plugins:
        raise ValueError(f"No product plugins in {MAP_PATH}")
    return plugins


def directory_files(root: Path, relative: Path):
    directory = root / relative
    if not directory.is_dir():
        raise FileNotFoundError(f"Missing declared directory: {directory}")
    yield from (path.relative_to(root) for path in sorted(directory.rglob("*")) if path.is_file())


def manifest_files(root: Path, tree: dict, prefix: Path = Path()):
    if tree.get("all"):
        yield from directory_files(root, prefix)
    for name in tree.get("files", []):
        path = prefix / relative_path(name)
        if not (root / path).is_file():
            raise FileNotFoundError(f"Missing declared file: {root / path}")
        yield path
    for name in tree.get("dirs", []):
        yield from directory_files(root, prefix / relative_path(name))
    for key, subtree in tree.items():
        if key not in {"all", "files", "dirs"}:
            yield from manifest_files(root, subtree, prefix / relative_path(key))


def product_files(root: Path, manifest: dict) -> set[Path]:
    files = list(manifest_files(root, manifest["artifact"]))
    if len({path.as_posix().casefold() for path in files}) != len(files):
        raise ValueError("Duplicate artifact paths, including case-insensitive collisions")
    for path in files:
        if path.is_relative_to(SCRIPTING) and path.suffix in {".sp", ".inc"}:
            continue
        if path.is_relative_to(TRANSLATIONS) and path.name.endswith(".phrases.txt"):
            continue
        raise ValueError(f"Unsupported product resource: {path}")

    entrypoints = {path for path in files if path.parent == SCRIPTING and path.suffix == ".sp"}
    if entrypoints != set(plugin_paths(manifest).values()):
        raise ValueError("Product sources in artifact and declared plugin entrypoints differ")
    return set(files)


def project_files(root: Path) -> tuple[Path, ...]:
    for path in PROJECT_FILES:
        if not (root / path).read_bytes().strip():
            raise ValueError(f"Required project file is empty: {path}")
    license_text = (root / "LICENSE").read_bytes()
    if not all(marker in license_text for marker in (
        b"GNU GENERAL PUBLIC LICENSE",
        b"Version 3, 29 June 2007",
        b"END OF TERMS AND CONDITIONS",
    )):
        raise ValueError("LICENSE must contain the full GNU GPL v3 text")
    return PROJECT_FILES


def check_inventory(expected: set[Path], actual: list[Path]) -> None:
    if len({p.as_posix().casefold() for p in actual}) != len(actual):
        raise ValueError("Artifact paths differ only by case or occur more than once")
    if unexpected := set(actual) - expected:
        raise ValueError(f"Unexpected packaged files: {sorted(map(str, unexpected))}")
    if missing := expected - set(actual):
        raise ValueError(f"Missing packaged files: {sorted(map(str, missing))}")


def validate(root: Path, artifact: Path, *, build_tree: bool = False) -> None:
    if not artifact.is_dir():
        raise FileNotFoundError(f"Missing artifact directory: {artifact}")

    manifest = load_map(root)
    sources = product_files(root, manifest)
    plugins = set(plugin_paths(manifest))
    documents = set() if build_tree else set(project_files(root))
    actual = []
    for path in artifact.rglob("*"):
        if path.is_symlink():
            raise ValueError(f"Unexpected symbolic link: {path}")
        if path.is_file():
            actual.append(path.relative_to(artifact))

    expected = sources | plugins | documents
    check_inventory(expected, actual)
    for path in sorted(sources | documents):
        if not filecmp.cmp(root / path, artifact / path, shallow=False):
            raise ValueError(f"Packaged file differs from its source: {path}")
    for path in sorted(plugins):
        with (artifact / path).open("rb") as binary:
            if binary.read(4) != b"FFPS":
                raise ValueError(f"Invalid SourcePawn plugin header: {path}")


def validate_zip(root: Path, archive: Path) -> None:
    manifest = load_map(root)
    expected = product_files(root, manifest) | set(plugin_paths(manifest)) | set(project_files(root))
    with ZipFile(archive) as package:
        check_inventory(expected, [relative_path(item.filename) for item in package.infolist() if not item.is_dir()])
        if bad_file := package.testzip():
            raise ValueError(f"Invalid ZIP member: {bad_file}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a staged SourceMod artifact.")
    parser.add_argument("--root", default=".", type=Path)
    parser.add_argument("--artifact", default=Path("dist/sourcemod/artifact"), type=Path)
    args = parser.parse_args()
    try:
        validate(args.root, args.artifact)
    except (OSError, ValueError) as error:
        parser.exit(1, f"{error}\n")
    print("ARTIFACT_VALIDATION_OK")


if __name__ == "__main__":
    main()
