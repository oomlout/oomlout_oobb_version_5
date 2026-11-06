# Catalogue presentation

AI-generated images and instructions. Errors possible.

Use this workflow for a repository with `parts/<id>/working.yaml` and exported mounting plates. Use the [assembly workflow](README.md) for multipart mechanisms requiring reviewed hardware positions and exploded views.

## Run

Install Python 3.10+, Blender 4.2+ and the Python dependencies:

```powershell
python -m pip install -r C:\gh\oomlout_oobb_version_5\presentation\requirements-catalogue.txt
```

Add `C:\gh\oomlout_oobb_version_5` to the user PATH. Open a new terminal. From any catalogue part folder:

```bat
oobb-present
```

From the catalogue repository root:

```bat
oobb-present --all
```

The default batch includes Git-tracked `parts/*/working.yaml` records only. It does not traverse `navigation_oobb`, regenerate CAD, commit or push. Use `--all --include-untracked` deliberately to include new local records. A single-folder build accepts an untracked record.

```bat
oobb-present "C:\path with spaces\repository\parts\part-id"
oobb-present --readme-only
oobb-present --all --force
```

Set `OOBB_PYTHON` to a Python executable or `BLENDER_EXE` to a Blender executable when they are not on PATH. Blender is also discovered under `C:\Program Files\Blender Foundation`. The launcher preserves the caller's working directory and returns a nonzero exit code on failure. Python entry point on other platforms: `python /path/to/base/presentation/scripts/catalogue.py`.

## Folder output

```text
parts/<id>/
  working.yaml                 # existing catalogue source, unchanged
  3dpr.stl                     # existing default mounting plate, unchanged
  working_oobb.stl             # existing OOBB variant, unchanged
  README.md                    # concise generated block
  3dpr_presentation.png         # final image beside source STL
  working_oobb_presentation.png
  presentation/
    config.json                # optional reviewed overrides; never overwritten
    manifest.json              # source hashes, dimensions, image paths
    README.md                  # full technical source notes
    images/3dpr.png
    images/working_oobb.png
```

At the repository root, `--all` creates a grouped README index and `presentation/catalogue.json`. The shared `presentation/.cache/` is ignored by Git. Render keys include both the STL hash and Blender worker hash; identical geometry reuses the same views. `--force` refreshes cached renders after a Blender, driver or lighting change. `--readme-only` requires existing presentation images or cached views for every mesh.

## Rules

1. Read `working.yaml` and inspect the source CAD. These two STL filenames identify mounting plates in this catalogue, not electronic boards. Add another explicit adapter before applying this script to a different file convention.
2. Render each available variant with an orthographic angled view and a top view. Use actual geometry, satin teal PLA, soft studio lighting and a warm background. Do not add a board, fastener or wire holder without its reviewed model and position.
3. Label the measured mesh bounding size in millimetres. Keep board dimensions separate. A dimensioned envelope is not a hole-spacing drawing. Do not infer mounting compatibility from the envelope.
4. Use one parts table with linked names, quantities and MD5 alpha codes. The board's code identifies the board record, not its plate. The two plates are alternatives. Link local STLs and catalogue metadata using relative paths. Do not invent a URL shortener; a verified code is compact link text.
5. Keep full source notes, then shorten the public copy. Use plain headings and the brief AI notice. Add Installation actions only when supported by reviewed source information. Omit generic testing sections. If no mesh exists, publish a reference page without a simulated plate.
6. Preserve user text outside the generated README markers. Store overrides in `presentation/config.json`. A malformed marker pair stops the build.
7. Inspect the example at GitHub reading width before running the whole catalogue. After an authorised sync, open the live README and example in a browser. Check wrapping, source links, image loading and small-screen layout; refine and sync again.

## Overrides

Optional `presentation/config.json`:

```json
{
  "title": "Raspberry Pi Pico",
  "hardware": [],
  "installation": [],
  "sources": [
    {"label": "Raspberry Pi documentation", "url": "https://www.raspberrypi.com/products/raspberry-pi-pico/"}
  ]
}
```

Each reviewed hardware row accepts `name`, `specification`, `quantity`, `url` and optional `md5_6_alpha`. Quantities are per board. Installation is an array of short actions. Codes and URLs must come from the exact hardware record; record your verification evidence in project handoff notes. The generator does not verify external URLs or select screws.

## Example

[Pico mounting plates](https://github.com/oomlout/oomp_electronic_breakout_version_5/tree/main/parts/electronic_breakout_microcontroller_rp2040_pico_without_headers_21_mm_width_51_mm_height_40_pin_raspberry_pi_pico) use board code `1owcj`. The legacy record has a 21 × 51 mm board envelope but no board mounting-hole specification. Its default STL measures 59 × 88.98 × 3 mm. The presentation lists the board and both alternative prints; no board screws or completed assembly are implied.

Keep source-review evidence and browser review results in the downstream `presentation/README.md`. Before committing, stage only owned generated files; other catalogue work may be in progress.
