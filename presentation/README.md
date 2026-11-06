# OOBB project presentation workflow

Create a technical README, CAD illustrations and a short assembly manual for an OOBB project. This folder is a reusable repository template and agent handoff, not an installed Codex skill.

**AI-generated workflow and example.** The documentation, scripts and example images were created with AI assistance and may contain mistakes. Digital checks do not establish a successful physical build.

Read [STYLE.md](STYLE.md), [the research notes](research.md) and the parent [render rules](../RENDER_STYLE.md) before starting. The current reference implementation is [the KALLAX example](examples/kallax/README.md). Preserve user-specified colours and assembly details even when they differ from the default palette.

For a catalogue of individual mounting plates, use [the catalogue workflow](CATALOGUE.md). The root `oobb-present.bat` command runs from a part folder through PATH; `oobb-present --all` builds the tracked catalogue and its README index.

## Deliverables

Each downstream project has a `presentation/` directory:

```text
presentation/
  README.md                    # assumptions, status, rebuild commands
  project.json                 # reviewed quantities, paths, links and text
  assembly-guide.pdf           # published manual
  parts.csv                    # portable quantities and part references
  research.md                  # primary sources and resulting decisions
  images/                      # published PNGs, visibly labelled AI-generated
  raw/                         # unlabelled CAD render intermediates
  scenes/                      # editable Blender scenes
  scripts/                     # project build and assembly audit
    lib/                       # vendored helpers from this folder
  templates/README.template.md
  qa/                          # reports, logs and contact sheets
```

The root README uses relative image and STL paths so it works in a clone and on a branch. It contains one generated block between `<!-- oobb-presentation:start -->` and `<!-- oobb-presentation:end -->`. Content outside that block is preserved. A first build prepends the block; inspect the existing README and explicitly remove obsolete boilerplate or broken links during migration.

Keep production geometry in its existing folders. Copy the final relevant PNGs beside the actual catalogue STLs as required by the render rules. Treat `presentation/` as the published package; `raw/`, scenes and QA files are working assets.

## Agent procedure

1. Inspect the project, its `AGENTS.md`, the production STL/SCAD files, print-plate information and earlier user corrections. Record an assembly inventory. Count repeated pieces explicitly. Never infer a quantity from the number of part types.
2. Check how the fasteners seat. Measure hole axes, pocket depth, hex orientation and contact faces in source geometry. Write an axial or dimensional stack before rendering. Distinguish a rod, screw, bolt, ordinary nut and coupling nut. List what is confirmed by the user, derived from CAD, selected from a catalogue and still assumed.
3. Verify hardware links. Use local OOMP records for discovery, then inspect the public repository entry. Record the exact ID, URL, date and any mismatch. A reachable URL alone is insufficient. For M6 fully threaded hex-head fasteners, the current OOMP catalogue uses `hardware_set_screw_...`; `hardware_bolt_...` denotes partial thread. Never substitute a grub screw based on the phrase "set screw". Do not invent an OOMP ID when no suitable entry is found.
4. Research two or three relevant primary examples. Record what is adopted and why. Keep the writing specific to the build; avoid copying navigation chrome or marketing language from the reference websites.
5. Run `python presentation/scripts/adopt_template.py <project-directory>` from this base repository. It copies helpers and a README template; it does not replace CAD or the project README. Use `--update-tools` only when refreshing an existing vendored copy intentionally.
6. Create `presentation/project.json` using [the data contract](DATA.md) and the worked example. Add a project-specific CAD renderer and manual builder. Keep original meshes intact. Use generic hardware only when its assumed dimensions and simplifications are disclosed.
7. Render the assembled object, its setting, an empty assembly, an exploded assembly and a close detail of hidden fastening. Use an orthographic camera and actual source meshes. Adjust camera aspect ratio to the subject so small hardware is legible. Use a true section drawing where a render cannot show a captive nut.
8. Build the README, CSV, PDF and published image variants. Include the AI notice in the README, the manual, every published image and the build notes. Use the same part references and quantities throughout. Generate the BOM from the manifest rather than manually retyping it.
9. Audit the scene counts and hardware positions with a project-specific read-only script. Run the generic validator. Render every PDF page and visually inspect it at readable size. Check the actual README preview, image captions, table wrapping, long links and the mobile-width fallback. Fix defects and rebuild only what changed.
10. Hand off the local files, not a claim of physical validation. Document build commands, software versions, assumptions, superseded variants, source hashes and remaining checks. Do not commit, push or publish unless requested.

## Reusable commands

```powershell
python presentation/scripts/adopt_template.py 'C:/path/to/project'
python presentation/scripts/build_readme.py 'C:/path/to/project'
python presentation/scripts/validate_presentation.py 'C:/path/to/project'
```

`build_readme.py` and `adopt_template.py` use the Python standard library. `manual_layout.py` needs ReportLab. Validation needs Pillow and PyMuPDF. Blender runs the project renderer with its bundled Python. The example used Blender 5.2 with Cycles/OptiX and a Windows Segoe UI font; the manual helper falls back to Helvetica if Segoe UI is unavailable.

The published table combines printed parts and hardware with one quantity column and clickable MD5 alpha codes. State the quantity basis above the table. The CSV also includes the doubled quantity. Codes must be read from catalogue metadata; use the canonical URL when no short URL has been verified.

Write in two passes: retain the full technical draft as source notes, then reduce published text to short actions and essential dimensions. Use "Installation", not "Installation and checks". Keep validation records in the agent handoff; omit testing commentary from the public instructions.

## Review checklist

- Assembly quantities match the user-confirmed arrangement.
- Recessed heads, retaining nuts, spacers and couplings are geometrically present, not merely named in captions.
- Nominal, measured, inferred and tested statements are clearly distinguished.
- Purchased part identity, thread, head form and length are checked against the linked record.
- Published images carry an AI-generated notice; raw intermediates are not used as public README images.
- Every part link and local image target resolves. Catalogue links have recorded inspection evidence.
- Guide pages are visually checked, with no overlaps or clipping.
- No physical fit, torque, print strength or load claim is made without evidence.
- Scripts can run from a different working directory and return a nonzero exit code on failed validation.

## Updating an existing presentation

Make an assembly correction before a cosmetic revision if the correction affects the images. Update the manifest, renderer, diagrams and instructions together. Re-render all affected views; do not leave a visually unchanged hero based on an obsolete assembly. Preserve previous source files but mark superseded variants clearly. Refresh copied images in the active part folders and redirect old top-level build commands to the current workflow.
