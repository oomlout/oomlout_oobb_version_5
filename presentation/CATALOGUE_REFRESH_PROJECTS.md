# Planned rollout across OOBB version-five projects

This is a planning snapshot from a read-only audit on 14 November 2026. No target
project is refreshed by these instructions. Recheck counts, Git state and output
conventions at implementation time. Sizes below are decimal logical file bytes,
rounded to MB/GB; they are not filesystem allocation or guaranteed reclaimable space.

Apply the [catalogue refresh standard](CATALOGUE_REFRESH.md), including focused
code repairs, one project at a time. Use the [Git procedure](CATALOGUE_HISTORY_RESET.md)
only as the final authorized phase, after all outputs are verified.

## First group: closest matches

| Folder under `C:/gh` | Active metadata records | Navigation asset bytes | Audit findings |
| --- | ---: | ---: | --- |
| `oomlout_oobb_part_plate_l_version_5` | 168 | 319,947,863 | No current root/part READMEs; every record has an STL; clean Git state |
| `oomlout_oobb_part_plate_u_version_5` | 136 | 268,743,792 | No current root/part READMEs; every record has an STL; clean Git state; `old/` is another 470,969,488 bytes |
| `oomlout_oobb_part_holder_bearing_version_5` | 44 | 420,223,584 | No current root/part READMEs; every record has an STL; 90 Git status entries require preservation/reconciliation |

Recommended order: L plates, U plates, bearing holders. These three navigation
trees hold about 1.009 GB of assets. Sampled large STLs matched canonical files by
SHA256, but several other navigation files did not match canonical name/size pairs.
Do a full mapping/hash audit before replacement; differences may be metadata,
older variants or navigation-only work.

### L plates

- Keep the actual `plate_l` taxonomy, including angle/max-angle and arc variants.
  Do not reduce every leaf to just width, height and depth.
- Inspect how the 168 source records are populated and rendered; capture the full
  expected ID set before an archive or pilot run.
- Use existing `3dpr.stl` as the initial render adapter; this project currently
  has no native SolidCraft build entry. Keep SCAD STL export enabled.
- Repair the old copying navigation implementation and its callers. Review the
  `action_make_all.py` orchestration rather than transplanting native plate flags.
- Render an L-shaped representative and extremes. A top view may need a side
  companion to make the bend and height clear.

### U plates

- Preserve the existing width/height/depth meanings and all 136 records.
- Retain `3dpr.stl` generation. Adapt descriptions and render framing to a U-shaped
  part; do not reuse the flat plate's single-plane explanation.
- Inventory `old/` separately. Its size does not establish that it is disposable
  or unused by imports/build scripts. Preserve necessary source and unique geometry.
- Test the smallest and widest/tallest brackets before a full render batch.
- Ensure the default full build cannot accidentally repopulate archived variants
  outside the agreed active set.

### Bearing holders

- First preserve/reconcile the existing worktree changes; do not use a reset or
  a wholesale generated-folder replacement to make them disappear.
- Keep bearing size, holder style, embedded-nut options and multi-bearing variants
  in the taxonomy and public detail fields.
- Inventory all meshes per record. There were 126 STL files across 44 records;
  do not assume every additional STL is a redundant copy.
- Keep working SCAD export. Render the printed holder alone for the catalogue;
  use a bearing/hardware assembly view only with actual reviewed geometry/positions.
- Existing tests/examples may encode fit decisions. Preserve and run the relevant
  tests if repairing the corresponding CAD or orchestration code.
- There was an older root `readme_old_1.md`; review useful content before generating
  the new canonical README.

## Second group: small follow-ons

| Folder under `C:/gh` | Records | Navigation assets | Implementation notes |
| --- | ---: | ---: | --- |
| `oomlout_oobb_part_plate_90_degree_version_5` | 13 | 13.03 MB | No READMEs; meshes exist; two Git status entries to inspect; keep SCAD exporter |
| `oomlout_oobb_electronic_version_5` | 28 | 30.04 MB | No READMEs; meshes exist; clean Git state; preserve 39.07 MB `old_version/` until reviewed |
| `oomlout_oobb_part_timing_belt_storage_version_5` | 4 | 91.36 MB | Native outputs already exist; no READMEs; not currently a Git repository |

For 90-degree plates, inspect right-angle geometry in an angled/side view and
confirm the actual depth field/units. Keep all 13 variants unless the user changes
the catalogue scope.

For electronics, describe actual holder/connector function. Do not confuse this
OOBB repository with the separate `electronic_breakout_` adapter in the base
`oobb-present` command. Preserve meaningful connector/wire/header taxonomy. Do not
invent a board rendering or hardware compatibility from a folder name.

For timing-belt storage, inspect the mixed SCAD/native pipeline: make-all currently
defaults `run_solidcraft` to `working_scad`, exports native extras/STL and still
enables legacy SCAD STL. Verify native coverage and intended outputs before
disabling a duplicate exporter. Build cache was approximately 870 MB; treat it
separately from published parts. Initialize/publish Git only with a confirmed
destination in the authorized implementation scope; there is no old local history
to wipe here.

## Later catalogues requiring additional review

| Folder under `C:/gh` | Records | Navigation assets | Why it needs an adapted pass |
| --- | ---: | ---: | --- |
| `oomlout_oobb_part_timing_pulley_version_5` | 44 | 86.82 MB | Existing overview and family renders, no part READMEs, 480 Git status entries |
| `oomlout_oobb_tool_precision_screwdriver_version_5` | 79 | 60.96 MB | Existing assembly/build docs and one part README; native entry; 58 Git status entries; no origin configured |
| `oomlout_oobb_gear_version_5` | 50 metadata records in 52 folders | 105.44 MB | No root README; direct STLs in only 16 part folders; 156 Git status entries |

Timing pulleys already distinguish 35 pulleys and nine couplers. Keep belt profile,
tooth count, idler/basic style and coupler function. Its `make_all.py` is a different
entry point; do not assume the standard `action_make_all.py` filename. Preserve
existing comparison renders and resolve the local changes before replacing outputs.

The screwdriver includes printable parts, fit samples, labels, legacy generations
and a purchased hardware record. Classify these explicitly. A purchased screw
record should not get an invented printable render. Keep the reviewed assembly and
two-colour-printing instructions, full IDs and colour relationships. Confirm the
remote rather than deriving it from the folder name.

For gears, resolve the 52-folder/50-record mismatch and locate nested/alternative
meshes before declaring missing outputs. Repair incomplete generation where
possible. Keep the full requested source catalogue; do not shrink it to the 16
folders that happened to have a direct STL in the audit.

## Separate projects, outside the initial catalogue batch

| Project | Local total | Main storage groups | Treatment |
| --- | ---: | --- | --- |
| `oomlout_oobb_part_holder_motor_version_5` | 9.53 GB | Outputs 5.13 GB; navigation 1.45 GB; parts 1.40 GB; working backups 1.02 GB | Consolidate existing TT/servo/NEMA documentation and renderers; preserve specialist assembly/fit work |
| `oomlout_oobb_part_motor_gearbox_cycloidal_version_5` | 51.13 GB | Build 29.00 GB; Git 6.82 GB; parts 6.53 GB; releases 4.85 GB; outputs 1.92 GB; navigation 1.41 GB | Storage/lifecycle review, not a generic README/render replacement |

Motor holders had 24 metadata records, 71 Git status entries and no origin URL.
The cycloidal gearbox had 20 records, 18 part READMEs, existing studio/assembly
documentation and a clean Git worktree. Its animation frames, release bundles,
native version families and Git history need explicit retention decisions.

Do not route either project through the flat-plate template unchanged. The general
principles of canonical assets and text-only navigation still apply, but assembly
inventories, print transforms and mechanical versions require their own review.

The base `oomlout_oobb_version_5` is the shared library and guidance repository,
not a part catalogue. The already refreshed `oomlout_oobb_part_plate_version_5`
is the reference. Neither is another target of this planned rollout.

## Per-project completion record

For each implemented project, append a dated result to its maintenance notes:

1. Original IDs/counts, branch/remote and preserved existing changes.
2. Code issues found, fixes made and the checks that establish the resulting behavior.
3. Source adapter, export policy, variant list and regeneration commands.
4. Parts/navigation archival manifests and navigation-only material disposition.
5. Generated IDs, mesh/render counts, link/hash results and visual review.
6. Published final tree and history-reset/fresh-clone results when authorized.
7. Before/after parts, navigation, Git and clean-clone sizes, plus retained local extras.

Update this plan's status only after the corresponding project is actually complete.
Do not treat recording a plan, passing one pilot, or producing a new root commit
without all required outputs as completion.

## Completed rollout — 14 November 2026

All nine catalogue projects above have now been refreshed, rebuilt, validated and given new single-root histories. Seven were synced to their verified GitHub remotes. Timing-belt storage and the precision screwdriver were explicitly kept local, with no remote configured. The motor-holder and cycloidal projects remain outside this batch.

| Project | Records | Studio sheets | Snapshot |
| --- | ---: | ---: | --- |
| `oomlout_oobb_part_plate_l_version_5` | 168 | 168 | [08e78453](https://github.com/oomlout/oomlout_oobb_part_plate_l_version_5/commit/08e78453d0da1098476cd3198ae3144ca9653883) |
| `oomlout_oobb_part_plate_u_version_5` | 136 | 136 | [d01e5b3e](https://github.com/oomlout/oomlout_oobb_part_plate_u_version_5/commit/d01e5b3e82f106493460566de870ae2c3504a26f) |
| `oomlout_oobb_part_holder_bearing_version_5` | 44 | 88 | [73071aa4](https://github.com/oomlout/oomlout_oobb_part_holder_bearing_version_5/commit/73071aa41cf6388e4862972014ce03887942ee00) |
| `oomlout_oobb_part_plate_90_degree_version_5` | 13 | 13 | [f99dbc47](https://github.com/oomlout/oomlout_oobb_part_plate_90_degree_version_5/commit/f99dbc471e5be3ef2c73420ddbb22eac35b11dd2) |
| `oomlout_oobb_electronic_version_5` | 28 | 28 | [062b5f18](https://github.com/oomlout/oomlout_oobb_electronic_version_5/commit/062b5f18be8d0c50a3733e931e18379414dac95e) |
| `oomlout_oobb_part_timing_belt_storage_version_5` | 4 | 8 | Local `8fa045b6` |
| `oomlout_oobb_part_timing_pulley_version_5` | 44 | 88 | [c7772880](https://github.com/oomlout/oomlout_oobb_part_timing_pulley_version_5/commit/c77728805101ccfd7a8b585e18e9c655359e0ca9) |
| `oomlout_oobb_tool_precision_screwdriver_version_5` | 79 | 156 | Local `052883b6` |
| `oomlout_oobb_gear_version_5` | 50 | 50 | [275960a7](https://github.com/oomlout/oomlout_oobb_gear_version_5/commit/275960a731905a48dbd91774bfe0a2b44fbafeda) |

The seven published trees fell from 3.013 GB to 0.788 GB (73.9%). Their local Git directories fell from 505.7 MB to 291.4 MB. Across all nine, navigation fell from 1.397 GB to 6.424 MB. Recovery copies and local build caches are retained separately and are not counted as freed disk space.

The complete measured report, per-file generated asset inventory, verified original worktree archives/history bundles and independent clone checks are under `C:/gh/_repository_recovery/catalogue_refresh_2026-11-14/`; start with `refresh_report.md`. Each refreshed project also contains CATALOGUE_BUILD.md and MAINTENANCE.md.

Implementation lessons: keep full IDs inside leaf README/text files rather than repeating them in long directory names; use a short `_part` leaf when a default part shares a taxonomy prefix with variants; retain generation markers; check exporter warnings and actual outputs; preserve version-specific mechanical contracts when shared libraries change; distinguish native/SCAD equivalence from merely having both exporters available.
