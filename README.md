# OOBB Generator

This repository is the working codebase behind the OOBB part generator.

It is the place where parts, variables, component definitions, documentation tooling, and generation workflows are developed before they are packaged into cleaner end-user releases. In other words: this is the workshop, not the showroom.

## What This Repo Contains

- Python code for building OOBB parts and shapes
- Shared dimensional variables and fit/tolerance settings
- Component-based object discovery under `components/`
- Documentation generation tools for JSON, HTML, and Markdown outputs
- Regression tests for part discovery, generation, and documentation

## Quick Tour

- [`oobb.py`](./oobb.py)  
  Core runtime for variables, object dispatch, and part-building helpers.

- [`oobb_variables.py`](./oobb_variables.py)  
  Central source of OOBB dimensions, hole sizes, bearing data, nut sizes, and print/laser variants.

- [`oobb_generate.py`](./oobb_generate.py)  
  Small generation helpers for common batches such as plates and circles.

- [`components/`](./components/)  
  Modular component definitions used by the discovery and documentation systems.

- [`tests/`](./tests/)  
  Regression coverage for generation, migration work, and documentation export.

- [`old/`](./old/)  
  Archived or compatibility-layer code kept around during the ongoing restructure.

## Working Model

The current codebase is in a transition from older generator logic toward a more structured component/discovery architecture.

That means this repo intentionally contains a mix of:

- active generator code
- compatibility shims
- migration scaffolding
- archived legacy logic

If you are looking for the cleanest outputs rather than the internals, the release repositories below are usually a better starting point.

## Related Repositories

### Generated Parts

- Generated parts repo: <https://github.com/oomlout/oomlout_oobb_version_4_generated_parts>

### More Organized Releases

- 3D printing files: <https://github.com/oomlout/oomlout_oobb_release_3d_print>
- Laser cutting files: <https://github.com/oomlout/oomlout_oobb_release_laser_cut>

### Bundles

- Basic plates: <https://github.com/oomlout/oomlout_oobe_bundle_plates_basic>
- Alphabet bunting: <https://github.com/oomlout/oomlout_oobb_bundle_bunting_alphabet>
- SMD magazines: <https://github.com/oomlout/oomlout_oobb_bundle_smd_magazine>
- Character decorations: <https://github.com/oomlout/oomlout_oobb_bundle_decorations>

## Getting Started

This project is Python-based and expects a local environment with the repo checked out.

Typical setup:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -U pip
```

Some tests also expect OpenSCAD to be installed and available on `PATH`.

## Running the Tests

```powershell
python -m unittest discover -s tests -p "test_*.py"
```

More detail on the test harness is available in [`tests/README.md`](./tests/README.md).

## Documentation Generation

The repository includes a documentation generator for discovered objects and part sets.

Examples:

```powershell
python components/documentation.py --markdown
```

```powershell
python components/documentation.py --json documentation_data.json
```

```powershell
python components/documentation.py --html-template templates/documentation_template.html --html-output documentation.html
```

## Notes

- The repo name may lag behind the current internal architecture and generated-output locations.
- Some hard-coded paths still reflect local development workflows.
- The codebase is actively being cleaned up, so structure is improving but not fully finished yet.

## Why This Repo Exists

This repository optimizes for making and evolving parts quickly. It is where new ideas get encoded, dimensions get tuned, and generators get refactored. It is intentionally practical, a bit experimental, and much closer to the machinery of OOBB than to a polished public release.
