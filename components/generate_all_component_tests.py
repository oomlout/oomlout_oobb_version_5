from __future__ import annotations

import argparse
import importlib.util
import os
import sys
from pathlib import Path


def _load_module(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def generate_all_component_tests(
    objects_root: str | Path = "components",
    skip_existing_images: bool = False,
) -> int:
    root = Path(objects_root).resolve()
    working_files = sorted(
        path for path in root.glob("*/working.py") if path.parent.name != "__pycache__"
    )

    if skip_existing_images:
        os.environ["OOBB_SKIP_EXISTING_IMAGES"] = "1"

    attempted = 0
    completed = 0
    failures: list[tuple[str, str]] = []

    for working_file in working_files:
        component_name = working_file.parent.name
        try:
            module = _load_module(working_file, f"component_test_{component_name}")
            test_fn = getattr(module, "test", None)
            if not callable(test_fn):
                continue
            attempted += 1
            test_fn()
            completed += 1
            print(f"[ok] {component_name}")
        except Exception as exc:  # noqa: BLE001
            failures.append((component_name, f"{type(exc).__name__}: {exc}"))
            print(f"[fail] {component_name}: {type(exc).__name__}: {exc}")

    print("")
    print(f"Attempted: {attempted}")
    print(f"Completed: {completed}")
    print(f"Failed: {len(failures)}")
    if failures:
        print("Failures:")
        for component_name, message in failures:
            print(f" - {component_name}: {message}")

    return 0


def cli() -> int:
    parser = argparse.ArgumentParser(description="Generate all component test assets")
    parser.add_argument("--objects-root", default="components")
    parser.add_argument("--skip-existing-images", action="store_true")
    args = parser.parse_args()
    return generate_all_component_tests(
        objects_root=args.objects_root,
        skip_existing_images=args.skip_existing_images,
    )


if __name__ == "__main__":
    raise SystemExit(cli())
