# Gridfinity tubs — .4 mm nozzle, current-enclosure fit

These are the corrected **16.5 mm total-height** tubs. The height includes the feet and, on the lipped version, the shallow alignment guide. Both versions fit fully inside the unchanged current V3 tray with its lid closed.

The two OOBB components are `gridfinity_tub_nozzle_04_no_lip` and `gridfinity_tub_nozzle_04_lipped`. The original Gridfinity library is unchanged. Both optimized nozzle families were intentionally corrected to this height; their earlier, too-tall exports are archived under `prototype_history/tubs_before_enclosure_height_correction` and are no longer active print parts.

## Why 16.5 mm, rather than 18 mm

The tray has 18 mm of internal height and uses standard reference bins about 17.74 mm tall. However, its lid locating rings descend to approximately **16.74 mm above the tray floor**. Whole-cell bin rims can surround those rings; fractional-bin rims cross them. Intersection checks found contact at 17.74 mm for the fractional sizes. A uniform nominal **16.5 mm** height leaves at least **0.24 mm beneath the locating tips**, plus 1.5 mm below the main roof. The ordinary rounded rims measure approximately 16.49 mm; the raised no-lip half-height receiver reaches 16.5 mm.

The lipped version retains the **full original upper 45-degree chamfer**, running from **1.9 mm wall thickness at Z=15.3 mm** to **0.7 mm at the nominal Z=16.5 mm top**. A second **45-degree slope underneath** returns to the 0.82 mm body wall, so there is no abrupt inward overhang or broad bearing shelf. The guide occupies 2.68 mm of nominal vertical height and projects 1.08 mm inward beyond the body wall. A **0.4 mm-high flat inner face**, from Z=14.9 to Z=15.3 mm, separates the two slopes so the ridge does not end in a sharp point. The lower slope starts beneath this flat. The standard feet remain unchanged. The label receiver is lowered on lipped tubs so that it does not obstruct the foot of a stacked tub. Its M3 countersink, screw bore and locating keys are retained; a 45-degree support transition keeps the original foot envelope clear below Z=5 mm. The no-lip version retains its original relative label position, including the short-end raised mount on 3×0.5.

## Nozzle optimization

- Wall: **.82 mm**; intended body lines: **two**.
- Efficient recessed floor: **.8 mm nominal**, plus the existing 0.01 mm Boolean allowance.
- Slice with **.44 mm nominal line widths**, **.28 mm layers** and **.24 mm first layer**.
- Arachne, two requested wall loops, three top/bottom layers, .8 mm minimum top/bottom shell thickness, 0% sparse infill, supports off, no automatic brim.
- The locally thicker receiver and guide receive the additional toolpaths they need. Use ordinary printing, not vase mode.

The profiles use the installed Bambu Lab A1 mini .4 nozzle and Generic PETG / textured PEI settings. Temperatures and flow limits are inherited from those profiles. The saved 2×1 sliced 3MFs and flattened profiles are in `slicer_check`. Check the printer/nozzle/material selection before printing.

The wall dimensions target the intended number of extrusion lines, accounting for line overlap rather than simply multiplying nozzle diameter. See [Prusa's perimeter and wall-thickness guidance](https://help.prusa3d.com/article/layers-and-perimeters_1748). The supplied G-code audits verify the actual resulting paths.

## Catalogue and normal pipeline

Seven footprints in 42 mm Gridfinity units: **1×1, 1×1.5, 1×0.75, 2×1, 3×1, 3×0.5, 3×0.75**. Both lip variants are provided, giving 14 tubs per nozzle family and 28 in total. The standard foot profiles, 0.5 mm total XY clearance and single M3 labeling hole remain. Quarter-unit footprints retain the project's existing mixed-foot extension.

The catalogue paths are `<size>x16.5/<variant>/tub.stl`. Print base-down as supplied. Keep the adjacent `scad_reference` directory with any moved SCAD source.

```powershell
# Both nozzle families through populate -> working_oomp -> working_scad:
python action_make_tubs_pipeline.py

# Only this nozzle family:
python action_make_tubs_nozzle_04_pipeline.py
python action_make_tubs_nozzle_04_pipeline.py --variant lipped
python action_make_tubs_nozzle_04_pipeline.py --no-stl

# Collect pipeline exports into the portable catalogue:
python action_make_tubs_nozzle_04.py --from-pipeline

# Or render the standalone catalogue directly:
python action_make_tubs_nozzle_04.py --catalogue
```

Edit `working_tubs_nozzle_04.py` for sizes/defaults. Pipeline records store **total depth in mm**. The SCAD adapter converts that to 7 mm units for the component API. `parts_source` gets source metadata; `parts` gets enriched OOMP metadata, `thing.yaml`, `3dpr.scad`, `3dpr.stl` and `3dpr.png`. Unfiltered make-all runs include both families. Packaging sets remain separate.

```python
oobb.append_full(thing, shape="gridfinity_tub_nozzle_04_lipped",
                 width=2, height=1, depth=16.5/7)
```

For these optimized components, `depth`/`gridfinity_depth` now means **total height including the lip**, in 7 mm units. This corrects the earlier body-height interpretation. The original raw Gridfinity components' API is untouched. `pos`, `rot` and the existing label-placement keys remain available. Lipped default `rim_lift_mm=-2.15` seats the label receiver below the stacking plane. The minimum supported total height is 16.5 mm. A taller custom override must be checked independently against the enclosure.

## Verification and estimates

Run `python check_tub_enclosure_fit.py` for direct intersections against the existing V3 bottom, baseplate and closed lid across all five case footprints that can contain each tub. It records results in `tubs_enclosure_fit.json`, including roof and locating-tip clearances. No enclosure source is altered.

Geometry tests check connected watertight meshes, exactly one through-hole, actual floor and wall thickness, standard feet, stacking and pipeline output agreement. Tests also check stacking between nozzle families. Slicer audits check the floor at both foot centres, the intended number of body wall paths and the clear screw axis. The 0.4 mm audit additionally checks the paths below the guide and material coverage through the enlarged ridge. Geometry checks verify that the guide clears a centred foot and contacts a foot shifted sideways by 0.4 mm.

```powershell
python tubs_nozzle_04/check_slicer.py
python tubs_nozzle_04/audit_toolpaths.py
python -m unittest discover -s tests -p "test_tubs_nozzle_0*.py" -v
python record_tub_verification.py
```

Current estimates and exact source hashes are in `slicer_check/report.json`. The baseline in that comparison is the earlier 18 mm no-lip tub; the corrected 16.5 mm tub changes both height and print geometry, so the improvement is not due to nozzle settings alone. Estimates are not measured print times. The original baseline meshes are comparison fixtures, not the corrected parts to print.

The original full-lip revision is retained in `prototype_history/tubs_before_shallow_guide`; the smaller 1.4 mm guide is retained in `prototype_history/tubs_small_guide`; the pointed full-angle prototype is retained in `prototype_history/tubs_pointed_full_angle_guide`. `slicer_check/guide_comparison.json` records the material and time comparison against that revision at the same 16.5 mm height and identical settings.

Physical fit, durability and labeling hardware still need a sample print. Start with one 2×1 tub before printing a full set.
