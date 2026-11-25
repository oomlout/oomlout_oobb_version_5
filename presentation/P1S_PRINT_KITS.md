# P1S print kits

Publish one combined editable kit as `parts/<kit-id>/working.3mf`. Regeneration may overwrite the existing `working.3mf`; validate a temporary archive before replacing it. Use this canonical filename in the generator, README, assembly instructions and downloadable print pack. Keep individual catalogue STLs in their original folders. Give each a concise part README linking to its own geometry and to the kit. The kit README owns the quantities, illustrated assembly, PDF and standalone HTML viewer. Link both the kit name and its thumbnail on the project landing page to the kit README. Link the editable 3MF beside the print files.

## Start from the base project

Copy `three_d_printing_base/default.3mf` into the project as a versioned source input. Record its SHA-256. Inspect `Metadata/project_settings.config` for printer, nozzle, process, bed and filament slots. For the KALLAX example the source SHA-256 is `2dbe41cec9ed16e34dbe2c74a136f2b2d7bc7ec4a4ba0353d2cfd04c581c8d9e`. It selects Bambu Lab P1S, 0.4 mm, textured PEI, the oobb_base_layer_p1s process and black PLA in slot 1. Leave these settings intact when populating the empty project.

## Populate the plates

1. Use the same reviewed printable BOM as the instructions. Export millimetre meshes in print orientation. Seat each mesh on Z=0. Check mesh closure and connected components against the intended part.
2. Give each physical piece a separate build object, mesh volume and object-level filament assignment. Include the part name and copy number, such as `M3 nut cap (2 of 5)`. Cache the mesh geometry while building and use the [editable-copy helper](scripts/p1s_print_kit.py) for each placement. Keep all template filament definitions even for a single-colour kit. Match each component role to the requested colour; do not assign one colour to every object simply because they share a plate. Check both object and normal-part filament assignments. Group same-colour structural parts on plates where practical, keeping multicolour labels as aligned parts of one parent object.
3. Name each plate for its contents. Use local bed coordinates to check bounds, object spacing and the printer exclusion zone. On multicolour plates, reserve clearance for the base project's purge tower, including its brim and toolpaths; check the final slice for G-code conflicts after rearranging parts. Translate to the Bambu plate grid for the build transforms. The matching `model_instance` for each independently editable object has `instance_id=0` and a project-wide unique `identify_id`.
4. Use current plate silhouettes for thumbnails. Show the print orientation, actual quantities and assigned colour on a quiet light background. The booklet uses studio assembly views. The 3MF preview uses the actual bed arrangement. Remove empty-template previews and unrelated attribution from the new project.
5. Package the populated 3MF model, model settings, plate previews and relationships with the original project settings. Write through a temporary file, then replace `working.3mf` after validation. Reopen the ZIP and compare the settings bytes and BOM with their sources.
6. Slice all plates in Bambu Studio. For local CLI validation run `bambu-studio.exe --slice 0 --outputdir <temporary-directory> <parts/kit-id/working.3mf>`. Check its return code, per-plate warnings, number of G-code files and object quantities. Distribute the editable project and record the slicer result. Machine runs are separate from project validation.

7. The established editable-copy writer does not require a repeated manual filament-change/save/reopen test. Validate object/part/plate references and filament assignments programmatically, and slice the original deliverable with its intended defaults. Keep multicolour inlays as parts of their physical parent object so that their common coordinates are preserved.

## Generating editable copies

Vendor `scripts/p1s_print_kit.py` in standalone projects so that make_all can run from a clean checkout. Supply one millimetre mesh element per source shape. Call `add_printable_copy` for each physical placement with its mesh, project-wide serial starting at one, name, build transform, one-based filament slot, model resources, build node, model settings and target plate. The helper writes a distinct component object, matching normal part and zero-based plate instance for each piece.

After writing, reopen the archive and call `validate_editable_copies(model=model, settings=config, count=physical_count, filament_count=slot_count)` on the two parsed XML roots. It checks independent build IDs, component/part references, filament slots and plate assignments. Use its returned meshes to check dimensions against the production STLs.

In Bambu Studio 2.9.2.62, the former five-instance adapter layout sliced successfully and allowed filament changes on the parent object. Selecting an individual child instance in the Objects tab and assigning a filament crashed Studio. Separate object rows allow each copy to retain its own filament through a Studio save and slice.

The [KALLAX example builder](https://github.com/oomlout/three_d_printing_filament_storage_kallax_holder/blob/main/components/kallax/print_project.py) illustrates template reuse, plate mapping, mesh-derived previews and footprint checks. Apply the editable-copy workflow above when adapting its layout.

## Bulk filament changes in Prepare

For a kit of single-part objects, validate the **written archive** before replacing the published file. Pass the number of physical pieces from the BOM, including every copy. From the base repo run:

```powershell
python presentation/scripts/p1s_print_kit.py path/to/working.3mf --count 32
```

The original KALLAX archive had 32 placements, seven build object IDs and zero normal-part records. It sliced on all three plates, but bulk filament changes in Prepare were reported to crash Studio. The KALLAX generator now calls `add_printable_copy` per placement and `validate_kit_archive` on its temporary output. A 32-piece kit has 32 unique selectable objects, 32 matching mesh parts and 32 plate bindings. Each copy inherits its object's filament. Keep genuinely multipart objects together and use their project's multipart validator.

When investigating a reported editor regression, open a disposable copy in Prepare, select several pieces on the bed, choose another existing filament, save, and reopen. Check the selected pieces' assignments and any pieces outside the selection. Keep the release project in its intended colours. In the repaired KALLAX kit, selecting all 32 pieces in Prepare and pressing `2` changed them to teal. Studio saved and reopened the copy with all 32 objects assigned to slot 2. The release file retained black slot 1 and sliced on all three P1S plates without warnings.

## V9 rotary-divider colour example

The LEGO rotary-divider V9 combined project uses slot 1 black for both halves of the inner roller (`rotor_front_print` and `rotor_back_print`) and the bearing frame; slot 2 teal for the housing halves, bearing insert and three spacers; and slot 3 yellow for every half of both the single and double clamp options. Keep the two label objects multipart, with their black/teal/yellow inlays in shared coordinates. These are V9 component assignments; other projects should follow their own requested palette.

Publish all 17 physical objects (20 mesh volumes) in the part directory as `working.3mf`. Use three plates: teal shell/insert/spacers, black roller/frame, and yellow clamps with both labels. Update thumbnails, manifests, instructions, archive entries and the recorded slicer checksum when changing colours or filenames. The reviewed V9 orientations use object-level support disabling while retaining the original base project settings bytes. Record the known housing cantilever warning; do not describe it as a warning-free or physically proven print. The established writer needs no repeated manual filament-edit/save/reopen test.
