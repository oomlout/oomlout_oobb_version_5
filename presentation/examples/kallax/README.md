# Worked example: KALLAX filament holders

**AI-generated reference.** The source scripts and images may contain mistakes; physical fit and load capacity have not been tested.

This example shows revision 3: one combined BOM with MD5 alpha links and short technical instructions. Full technical notes are retained separately before the publication edit. It is a reference implementation, not a standalone print package. Production meshes remain in the original project. The relative STL paths in `project.json` identify the required source parts.

The delivered project is `three_d_printing_filament_storage_kallax_holder`. The local checkout used during authoring was `C:/od/OneDrive/docs/three_d_printing_filament_storage_kallax_holder`. Reuse the structure, not that machine-specific path.

Files retained here:

- `project.json`: complete manifest and README content.
- `render_kallax.py`: Blender source. Copy to a downstream project root alongside its `scad_output/` folder.
- `build.py`: project-specific page composition. Copy to `presentation/scripts/` after adopting the reusable helpers.
- `audit_scene.py`: read-only checks of frame counts and captive hardware positions. Copy beside `build.py`.
- `preview.png`: the generated manual's first page.
- `end-section.png`: the actual adjustment-end section from the example.

The renderer imports actual printed-part STL geometry, but uses illustrative furniture, reels and hardware. It requires a manifest in `presentation/project.json`. The PDF builder expects seven raw shots in `presentation/raw/`, then creates the published package and copies PNGs beside the active parts. If adapting to another project, replace all KALLAX-specific geometry, narrative, file-copy rules and dimensional assertions.

Key mechanical lessons from this example: count all four frames per holder; distinguish the front and rear holders; seat both outer fasteners in their pockets; include the adjustment bolt's retaining nut; and make the nut cover plus slotted cover match the available span. One rail uses one coupling, two ordinary nuts and one fully threaded bolt.

The selected full-thread bolt is OOMP `hardware_set_screw_m6_25_mm_length`, not the partial-thread `hardware_bolt_m6_25_mm_length`. Seven millimetre full-hex and slotted covers are existing source parts. No production mesh was modified for this revision.
