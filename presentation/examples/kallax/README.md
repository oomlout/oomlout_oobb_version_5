# Worked example: KALLAX filament holders

**AI-generated reference.** The source scripts and images may contain mistakes; physical fit and load capacity have not been tested.

This example shows README layout 4: Summary, Details, Parts and Assembly. It includes an in-use image, assembled printed parts only, an exploded holder, a hardware-only table with OOMP IDs and short-code links, and linked 480 px assembly thumbnails. The complete printed/hardware BOM remains in the CSV and revision 3 PDF. Full technical notes are retained separately. This is a reference implementation; production meshes remain in the original project.

The delivered project is `three_d_printing_filament_storage_kallax_holder`, currently checked out at `C:/gh/three_d_printing_filament_storage_kallax_holder`. Reuse the structure, not that machine-specific path.

Files retained here:

- `project.json`: complete manifest and README content.
- `render_kallax.py`: Blender source. Copy to a downstream project root alongside its `scad_output/` folder.
- `build.py`: project-specific page composition. Copy to `presentation/scripts/` after adopting the reusable helpers.
- `readme_layout.py`: project-specific four-section text and hardware-link configuration. Copy beside `build.py`.
- `audit_scene.py`: read-only checks of frame counts and captive hardware positions. Copy beside `build.py`.
- `preview.png`: the generated manual's first page.
- `end-section.png`: the actual adjustment-end section from the example.

The renderer imports actual printed-part STL geometry, with illustrative furniture, reels and hardware. It requires `presentation/project.json`. The builder uses seven manual views plus four README views. Use `build.py --readme-only` to refresh the README and thumbnails without rebuilding the PDF. Add `--render --blender PATH` to regenerate the four README views. If adapting to another project, replace all KALLAX-specific geometry, narrative, file-copy rules and dimensional assertions. The rod's OOMP record is pending by user request.

Key mechanical lessons from this example: count all four frames per holder; distinguish the front and rear holders; seat both outer fasteners in their pockets; include the adjustment bolt's retaining nut; and make the nut cover plus slotted cover match the available span. One rail uses one coupling, two ordinary nuts and one fully threaded bolt.

The selected full-thread bolt is OOMP `hardware_set_screw_m6_25_mm_length`, not the partial-thread `hardware_bolt_m6_25_mm_length`. Seven millimetre full-hex and slotted covers are existing source parts. No production mesh was modified for this revision.
