# OOBB catalogue refresh standard

Status: implementation instructions, documented 14 November 2026. This document
does not execute a refresh, archive parts, change Git history or publish anything.

Use this standard when refreshing an OOBB version-five part catalogue. It captures
the finished plate repository's compact READMEs, folder-based discovery, original
CAD renders, reproducible generation and storage-conscious publication. The planned
work includes repairing the code that produces these outputs, not just editing
generated Markdown once.

Start with the [project rollout notes](CATALOGUE_REFRESH_PROJECTS.md). Use the
[history reset procedure](CATALOGUE_HISTORY_RESET.md) only after the catalogue is
complete and a history reset is included in the authorized work for that repository.
Read [STYLE.md](STYLE.md) and [RENDER_STYLE.md](../RENDER_STYLE.md) for the shared
visual conventions. Multipart mechanisms still use the [assembly workflow](README.md).

## 1. Scope and reference implementation

The initial targets are L plates, U plates and bearing holders. The 90-degree
plate and electronics catalogues are smaller follow-ons. Timing-belt storage is
a small native-CAD candidate with a separate Git-initialization requirement.
Timing pulleys, screwdrivers and gears need the additional review described in
the rollout notes. Motor holders and the cycloidal gearbox are separate projects,
with existing specialist assembly documentation to preserve.

The reference is `oomlout_oobb_part_plate_version_5`, at commit
`a2e37c3135baafa95e9cf3298dd39225dfadb643`:

- [Navigation and README generator](https://github.com/oomlout/oomlout_oobb_part_plate_version_5/blob/a2e37c3135baafa95e9cf3298dd39225dfadb643/working_navigation.py)
- [Presentation orchestrator](https://github.com/oomlout/oomlout_oobb_part_plate_version_5/blob/a2e37c3135baafa95e9cf3298dd39225dfadb643/render_plates.py)
- [Blender worker](https://github.com/oomlout/oomlout_oobb_part_plate_version_5/blob/a2e37c3135baafa95e9cf3298dd39225dfadb643/presentation/scripts/render_catalogue.py)
- [Build entry point](https://github.com/oomlout/oomlout_oobb_part_plate_version_5/blob/a2e37c3135baafa95e9cf3298dd39225dfadb643/action_make_all.py)
- [Build and audit notes](https://github.com/oomlout/oomlout_oobb_part_plate_version_5/blob/a2e37c3135baafa95e9cf3298dd39225dfadb643/presentation/README.md)

These are working examples, not a universal adapter. The plate scripts assume
plate descriptions, width/height/depth fields, two native STL variants and a
binary STL measurement reader. Adapt those assumptions for the destination.
Do not describe a bearing holder as a flat plate or reject a valid ASCII STL
because the reference renderer only measures binary STL files.

The existing base `oobb-present` command still uses the electronics-breakout
adapter described in [CATALOGUE.md](CATALOGUE.md). It is not yet an implementation
of this refresh standard for arbitrary OOBB catalogues. Its old file tables,
root catalogue index and duplicate image destinations must not be copied into
newly refreshed catalogues. This is a documentation specification; no shared
generator has been migrated by publishing this document.

## 2. Required end state

| Area | Required result |
| --- | --- |
| Canonical files | One active folder per full OOMP ID under `parts/` |
| Root README | Short introduction, one representative image, one discovery entry; no full catalogue or file table |
| Discovery | Relative directory links; skip the initial chain of single-child categories |
| Category selection | Natural numeric ordering; terminal choices open the canonical part folder |
| Navigation leaf | Exactly `README.md` and `oomp_id.txt`; no copied CAD, YAML, SVG or image files |
| Part README | Four sections, useful dimensions, full ID, rendered image, complete metadata; no generated download inventory |
| Images | Actual production geometry in the OOBB studio style, saved once beside the corresponding mesh |
| Build code | Repeatable full build, reliable explicit filtering, checked failures, docs generated after outputs finish |
| Regeneration | All active records in the agreed catalogue, not just a demonstration size |
| Storage | Generated intermediates ignored; archives accounted for separately; no redundant navigation assets |
| Git reset | When authorized: one new root commit, exact-lease push, verified fresh clone and honest size report |

Keep current geometry, variant identities, mechanical intent and manually written
technical notes. A refresh does not automatically authorize redesigning clearances,
selecting new bearings, changing hardware, deleting historical source material or
removing a necessary export format.

## 3. Public README design

Use the [catalogue root template](templates/CATALOGUE_ROOT.template.md) and
[canonical/leaf part template](templates/CATALOGUE_PART.template.md) as explicit
content contracts. They are new reference templates, not templates already wired
into the old `oobb-present` command. Implement substitution in the destination's
generator or generate equivalent Markdown directly. Resolve every `{{token}}`;
do not publish template placeholders.

Compute each URL relative to the actual output page. Directory URL tokens include
the trailing `/`; image tokens address canonical image files. Generate metadata
table rows with escaped values; generate the opening fence as a sufficiently long
backtick sequence followed by `yaml`, and the matching closing sequence. Reuse the
part content for a navigation leaf with URLs recomputed for that leaf. The leaf
can omit generated-block markers because its whole file is generated. For a
record without a real mesh/image, omit the image block and describe the available
record accurately instead of leaving a broken image token.

### Root README

Use a descriptive title, the notice below and exactly these level-two headings:
`Summary`, `Details`, `Parts`, `Assembly`.

Place this notice near the title:

> AI-generated images and instructions. Errors possible.

Summary explains the family in plain language and includes this coding-origin
paragraph, adjusted only if the user's project-specific instruction requires it:

> This is an entirely AI-generated coding project. The generated outputs are included and usually work, but the main purpose of publishing it is to give others a starting point for modifying the project with their own AI tools.

Show one named representative part using its canonical image path. Link its name
to its directory. Do not embed the same large image repeatedly in every section.

Details states the active catalogue count, gives the discovery directory link,
explains dimensions/units that apply across the family and gives short rebuild
commands. Put long implementation notes, QA records and migration logs in
`presentation/README.md` or a dedicated maintenance document.

Parts explains the available alternatives and any actually verified hardware
requirements. It is not a row for every printable option. Assembly is short for
a single-piece part; multipart holders retain real assembly instructions.
Do not invent assembly steps to fill a template.

Do not generate a complete part index, every OOMP ID, filenames, file sizes,
download tables or repeated file-navigation menus in the root README. GitHub's
directory interface already exposes the files.

### Canonical part README

Use the same four headings and notices. Include:

1. A family-appropriate description and a relative link to the final render.
2. The complete OOMP ID as text, for example `oobb_part_plate_basic_5_width_5_height_3_depth`.
3. A `Part folder` directory link and an `OOBB navigation` directory link.
4. A small table of decision-making metadata: dimensions with units, variant,
   bearing designation, angle, belt profile or other fields appropriate to the family.
5. All original part metadata in a collapsed `<details>` block, serialized as YAML.
6. Actual part/assembly instructions and retained hand-written technical notes.

No `### Downloads` inventory or `File | Bytes` table. Say which variant is for
printing when that distinction exists; the files themselves remain browsable in
the folder. An essential instruction may name a specific file without recreating
the entire file listing.

Preserve metadata types, full IDs and nested data. Escape Markdown table pipes.
Use a sufficiently long code fence if the serialized metadata itself contains
backticks. Display width/height in OOBB units only where that is the real unit;
do not silently treat them as millimetres.

### Generated-block ownership

Use one generated block in canonical/root READMEs:

```html
<!-- oobb-presentation:start -->
...generated content...
<!-- oobb-presentation:end -->
```

Preserve everything outside it, including existing user edits. On the first
adoption, prepend the generated block and review any pre-existing material for
duplication or obsolete links. Remove old text only when its disposition has been
decided. Reject missing, reversed or repeated markers before writing any pages.

Navigation is a wholly generated namespace, after the old content has been
inventoried and preserved. Canonical parts and project documentation are not.

## 4. Folder-based discovery

The existing directory name is `navigation_oobb`. Do not rename it to
`oobb_navigation` merely because that wording is used conversationally.

Example final tree:

```text
README.md
parts/
  <full-oomp-id>/
    working.yaml
    README.md
    <production CAD and meshes>
    3dpr_presentation.png
navigation_oobb/
  README.md
  oobb/part/<family>/
    README.md
    <width>/<height>/
      README.md
      <depth>/
        README.md
        oomp_id.txt
presentation/
  README.md
  catalogue.json
  scripts/
build/                         # ignored intermediates and QA
.archives/                     # ignored retained recovery data, if used
```

The placeholder family/width/height/depth tree is illustrative. Preserve the
project's real taxonomy; a bearing catalogue needs bearing size and mounting
variant, while a pulley catalogue needs belt profile, tooth count and style.

### Link contract

| Link source | Destination |
| --- | --- |
| Root discovery link | First navigation directory with more than one child |
| Nonterminal category option | Child navigation directory |
| Terminal category option | `parts/<full-oomp-id>/` directly |
| Navigation leaf `Part folder` link | Canonical `parts/<full-oomp-id>/` |
| Parent category link | Parent navigation directory (`../`) |
| Root representative example | Canonical part directory |
| Canonical part self-link | `./` |
| README image | Exact image file in the canonical part folder |

Never append `README.md` to a discovery, category or part link. Directory links
let GitHub show the README together with its file-navigation interface. Images
still target image files. Keep ordinary directory links relative and end them
with `/`; use `/` separators and URL-encode path components as needed.

For a singleton catalogue, descend to its sole canonical part directory. For an
empty catalogue, leave a valid navigation directory with a clear empty-state
message. Never dereference a nonexistent first part.

### First branching level algorithm

```text
node = navigation root
while node is not a part leaf:
    children = direct child category/leaf nodes
    if number of children != 1:
        break
    node = its sole child
if node is a part leaf:
    destination = canonical part directory
else:
    destination = navigation directory for node
```

Count child nodes, not files such as `README.md` or `oomp_id.txt`. Do not hard-code
the plate path `oobb/part/plate/basic`; different projects branch elsewhere.
Sort category values naturally (`1`, `2`, `9`, `10`, `11`), retaining stable folder
names. Define numeric parsing for decimal taxonomy values such as `14d2` when those
occur; do not change the underlying IDs to improve sorting.

### Leaf content

Each navigation leaf contains only:

- `README.md`: useful part details, image reference, full OOMP ID and canonical
  directory link. It may reuse the canonical page's generated body with relative
  links recalculated for the deeper location.
- `oomp_id.txt`: the complete part ID followed by a newline; no abbreviation or URL.

Keep these leaves even though normal terminal category links bypass them. They
support manual folder traversal and retain the user's requested ID text files.
Parent categories contain only their generated Markdown, plus child directories.

## 5. Inventory, archival and source selection

Before modifying a project, record its current branch/commit, remotes, dirty state,
tracked/untracked/ignored files, active metadata records, existing meshes, current
renders, generated-file sizes and README ownership. Read its local instructions.

Measure both the working directory and Git separately. Record every large group:
`parts`, `navigation_oobb`, `.git`, build/output directories, dependency environments,
archives and release bundles. For generated files, aggregate bytes and counts by
filename/variant and extension; make the output-retention decisions explicit.

Build an active-record inventory from the actual canonical metadata. Verify each
ID against its directory. Do not discover parts by recursively searching all of
the repository: that pulls in navigation copies, backups, tests and archived parts.
Inspect how `parts_source/` materializes `parts/`; archival of outputs does not
disable old source records. Preserve the full agreed catalogue by default.

If a parts archive is part of the authorized refresh, use a unique dated destination
under ignored `.archives/` or outside the repository. Store a manifest with relative
paths, byte sizes and SHA256 hashes. Verify the archive before replacing any original.
Ensure the source definitions can recreate the active part list before clearing it.
Do not substitute a pilot size for a later explicitly requested full rebuild.

### Removing copied navigation safely

1. Inventory every existing navigation file before replacement.
2. Match it to canonical parts by ID/path mapping and actual bytes. Matching only
   filename and length is useful for discovery but is not proof of duplication.
3. Hash candidate matches. Preserve unmatched/different files in a dated archive,
   with their original relative path and a migration report.
4. Review navigation-only CAD variants or notes for inclusion in canonical parts.
   Do not silently discard or overwrite a unique working variant.
5. Generate the complete new text navigation in a staging directory.
6. Validate IDs, taxonomy collisions, relative links and all generated content.
7. Replace only the generated navigation namespace after validation succeeds.

On Windows, Explorer may hold the directory open. Synchronizing staged files into
the existing navigation root with atomic file replacement can work where renaming
the entire tree fails. Remove obsolete entries only inside the resolved navigation
root, after their preservation decisions have been recorded.

Reject traversal segments, absolute paths, Windows reserved/path-invalid names,
symlinks/junctions and two IDs mapping to the same taxonomy leaf. Check the final
resolved target stays beneath the intended root before recursive removal or moves.
Use native PowerShell `-LiteralPath` operations end-to-end; do not feed enumerated
paths to another shell for deletion. If an automated action is blocked, retain the
files, report the exact action/reason and do not try a disguised deletion method.

## 6. Project adapter and code repairs

Create a written adapter specification before copying the reference code. Record:

| Adapter field | What to establish |
| --- | --- |
| Active metadata | Source directory, materialization rule, expected record count |
| Identity | Full OOMP ID field and folder consistency rule |
| Taxonomy | Ordered keys, fallback fields, missing-value rules and collision behavior |
| Public text | Correct family name, function, units and actual assembly requirements |
| Mesh variants | Explicit source filenames and what each represents |
| Backend | SCAD, native SolidCraft, or a documented mixture |
| Dependencies | Python interpreter, local libraries, tools and required versions |
| Build entry | Real public command and how it passes a single selection to all stages |
| Keep outputs | Printable STL, source, STEP/DXF where useful, metadata and final PNGs |
| Ignore outputs | Rebuildable raw renders, caches, QA sheets/logs and verified archives |

Do not invent a `true` variant or look for `3dpr_solidcraft.stl` in a repository
that only publishes `3dpr.stl`. Use the current working mesh as the render input.
Identify whether an STL is one part, several print-oriented pieces, or a complete
assembly; do not present a print layout as an assembled mechanism.

### Repairs included in the planned update

Fix demonstrated problems in the generation path while adopting this standard.
Avoid leaving a hand-edited README that the next build will overwrite.

| Problem to inspect | Expected repair | Evidence |
| --- | --- | --- |
| Navigation uses `xcopy`, `copytree` or full-folder mirroring | Replace the active implementation and all callers with text-only generation | Full build creates no nontext navigation assets |
| Make-all silently selects a pilot | Default to the approved full active set; keep an explicit filter | Expected IDs generated; filtered run leaves other parts unchanged |
| Filters reach only one backend | Propagate the same selection through population, actions, SCAD, native CAD, SVG and renders | Controlled entry-point test and one real filtered build |
| Population/actions run asynchronously | Wait for metadata and geometry to finish before consumers start | No stale/missing outputs or read/write races |
| Old export options override new policy | Normalize options once; remove stale `typ=all`/save-mode overrides | Intended STL outputs exist; disabled redundant exports do not recur |
| Failed tools appear successful | Check exit codes and required output files; fail with a useful log path | Controlled failure returns nonzero |
| Windows command quoting or executable selection breaks | Argument-list subprocess calls, explicit executable discovery and paths with spaces | Run from another working directory and a path containing spaces |
| Render caches ignore changed sources | Include mesh, worker/style/settings and tool version in invalidation | Changed source invalidates; unchanged complete batch reuses images |
| Broken or partial PNGs counted as cached | Verify readability/dimensions; publish atomically; keep a provenance manifest | Interrupted render resumes without publishing incomplete images |
| README generation drops hand-written notes | Generated markers and preflight validation | Manual content survives; malformed markers stop before replacement |
| Part IDs/taxonomy are inconsistent | Diagnose data source; fix the source or explicit mapping, not just output names | Unique canonical ID-to-leaf mapping |
| Obsolete output files survive regeneration | Remove/archive only known obsolete generated outputs in scope | Final manifest and folder contents agree |
| Unsupported/no-mesh records | Repair generation where possible; otherwise document the exact unsupported record | Never fabricate geometry or silently shrink the catalogue |
| Copy/hash changes caused by line endings | Set deliberate attributes and deterministic writes | Fresh-clone artifact hashes match |

Keep repairs focused on reproducibility, correctness and this refresh. Fix a
clear local generation bug with evidence. Do not turn a documentation refresh
into an unreviewed redesign of mechanical geometry or a broad dependency upgrade.
If a genuine CAD issue blocks a valid output, record it precisely and resolve the
required design decision before calling the full catalogue complete.

### STL export policy

For SCAD-only L/U/90-degree plates, electronics and bearing holders, retain
OpenSCAD STL export: it is currently the printable output. The plate repository
could disable its legacy `3dpr.stl` because verified native meshes replaced it.
Apply that optimization elsewhere only after the native exporter covers every
selected part/variant and its output has been checked.

For mixed/native projects, document which backend owns each file. Keep existing
SCAD/PNG/DXF generation when still required. A storage refresh is not a blanket
instruction to migrate every project to SolidCraft or to stop producing STL.

## 7. Studio renders

Use current production meshes. Apply satin teal PLA (`#00B1B7` sRGB converted to
linear shader values), metallic zero and roughness near 0.4. Use an orthographic
three-quarter camera, large soft lights and a quiet warm-white background.
Use black/yellow only where distinct real components have those presentation roles.

For single-piece catalogue parts, publish a 1600 × 1000 PNG sheet with an angled
view and top view. The reference renders each view at 1000 × 1000 and fits it
into a 720 × 720 panel. Use independently fitted views to keep thin/tall parts
visible; label them clearly and do not imply a shared scale where they differ.
Add a short part/variant title, measured mesh envelope in millimetres, and:

> AI-generated CAD illustration. Errors possible.

An envelope is not a hole-spacing drawing or a clearance guarantee. If the top
view conceals the function of a bent bracket or holder, add a relevant side or
underside view using the same real mesh. Multipart mechanisms need reviewed
assembly positions and may need the assembly workflow instead of this sheet.

Keep holes open against the background. Floor shadows through holes must not
look like inserted hardware. Do not smooth away holes, bevel or remesh production
geometry for a prettier picture. Render materials and camera transforms may change;
the source CAD/mesh bytes must not.

Publish one image per required variant directly under its canonical part folder,
for example `3dpr_presentation.png` or `true_presentation.png`. Store no second copy
under navigation or `presentation/images/` for the same catalogue sheet. Preserve
existing technical previews unless their retirement has been explicitly decided.

Use one canonical provenance manifest, such as `presentation/catalogue.json`:

```json
{
  "schema": 1,
  "renders": [{
    "id": "FULL_OOMP_ID",
    "variant": "3dpr",
    "source": "parts/FULL_OOMP_ID/3dpr.stl",
    "source_sha256": "MEASURED_SHA256",
    "image": "parts/FULL_OOMP_ID/3dpr_presentation.png",
    "image_sha256": "MEASURED_SHA256",
    "dimensions_mm": [74.0, 74.0, 3.0],
    "renderer_sha256": "MEASURED_SHA256",
    "blender": "ACTUAL_VERSION",
    "sheet_version": 1,
    "key": "DERIVED_CACHE_KEY"
  }]
}
```

Example dimensions are illustrative, never defaults for other projects. Include
every actual source if one render composes several meshes. Also invalidate a
published sheet when its title/metadata or sheet layout changes, even if the raw
views can be reused. This improves on the reference's manually incremented sheet
version. Record relevant dependencies and source revision in build notes.

The reference uses Cycles, 24 samples and denoising. On its RTX 4060, GPU denoising
materially reduced batch time. Detect supported hardware; keep a working CPU
fallback. One or two workers are sufficient unless measurements justify more.
Use unique jobs/logs per worker and prevent concurrent runs from sharing mutable
job/manifest files. Do not launch duplicate full builds from integration tests.

Keep raw views, jobs, logs, contact sheets and optional scene caches beneath
ignored `build/presentation/`. A missing cache is recoverable; published images
remain usable. A forced rebuild refreshes renders after driver/lighting changes.

## 8. Regeneration sequence

1. Read local instructions and inventory the project, Git state and output sizes.
2. Preserve dirty work, old parts when required, and navigation-only material.
3. Define active IDs, adapters, variants and keep/ignore decisions.
4. Repair generation code and wire the new workflow into the real build command.
5. Build one representative part; verify source geometry and inspect its README
   and studio sheet at GitHub reading width.
6. Exercise extreme shapes: smallest, largest, thin, tall, bent and multipart
   variants as applicable. Resolve framing/description problems before the batch.
7. Regenerate all approved active records and all selected variants.
8. Render finished meshes, assemble final sheets and write provenance.
9. Generate canonical/root READMEs and text-only navigation after publication of
   CAD and images. Do not finish with an earlier metadata-only navigation pass.
10. Run the audits and focused regression checks below; visually review contact
    sheets of all variants and full-size representative extremes.
11. Repeat an unchanged presentation/docs build to verify stable output and cache
    reuse. Do not rerun expensive CAD without a change or unresolved failure.
12. Produce the reviewed final tree and size report. If authorized, perform the
    separate history reset and publish it; otherwise leave a complete local result.

If a project already has valid geometry and the requested scope is only presentation,
reuse it. A full refresh that explicitly includes regeneration must run its CAD
pipeline; do not equate a README rerun with rebuilding the parts.

## 9. Validation and acceptance

The completion record must establish:

- Expected active IDs equal generated IDs; no archive/navigation records leaked in.
- Every declared variant exists and corresponds to its intended backend and source.
- STL files are readable and nonempty. Check mesh structure, bounds and available
  native validity measurements; do not rely on file existence alone.
- Published artifact manifests match their files, including after Git checkout.
- Every render has matching source/image hashes, dimensions and renderer identity.
- Every published PNG decodes and has the intended size; images are not placeholders.
- All root, canonical and navigation Markdown links resolve within the repository.
- Discovery/category/part links target directories, not `README.md` files.
- Terminal category choices target canonical `parts/<id>/` directories.
- The initial discovery link is computed from actual branching, not hard-coded.
- Every leaf has exactly two files; `oomp_id.txt` matches the canonical full ID.
- Navigation contains no copied CAD, image, YAML, archive or binary files.
- Root/part READMEs have the four headings, notices and preserved manual content.
- No full-catalogue table or generated file-size/download inventory has returned.
- Full metadata remains available in each canonical/leaf detail page.
- An unchanged rerun leaves published content stable and avoids rendering again.
- Build failures propagate and selection/filtering covers every applicable stage.
- Existing project-specific mechanical tests still pass after relevant code repairs.

Adapt the reference audit; do not hard-code 195 records, 390 images or binary STL
layout into another project's validator. Check expected sets, not only counts.
An integration test must mock every expensive backend, including the new renderer.
Use focused regression tests for repaired orchestration and preservation behavior;
do not introduce a large test framework merely for prose changes.

Record visual review results in maintenance notes: which samples and contact
sheets were inspected, what was fixed, and what remains a physical-build question.
On an authorized publish, verify the live root README, one part folder and the
discovery route. Confirm image loading and folder navigation at desktop and narrow
widths. Resolve failures before reporting completion.

## 10. Git attributes, ignored files and storage reports

The plate repository uses these attributes to preserve exact artifact hashes:

```gitattributes
/parts/** -text whitespace=cr-at-eol
/navigation_oobb/** text eol=lf
/presentation/scripts/render_catalogue.py -text whitespace=cr-at-eol
```

Adapt the renderer path. Preserve raw bytes of every file whose digest is recorded,
or define a consistent normalization scheme before hashing. Do not normalize hashed
STEP/JSON/SolidCraft text during staging and then publish a manifest for other bytes.
Use explicit LF writes for new generated navigation to avoid repeated Windows
line-ending warnings. `whitespace=cr-at-eol` affects whitespace checking, not hashes.

Ignore build caches and archives before creating them. `.gitignore` does not remove
already tracked files: review the index and intentionally remove obsolete generated
paths from tracking while preserving required local recovery material. Keep source
definitions, real production assets, source code, final sheets and provenance.

The report separates:

| Measurement | Meaning |
| --- | --- |
| Canonical parts | Published CAD, metadata, README and image bytes |
| Navigation | Text-only tree bytes and file count |
| Other published files | Source, code, docs, manifests and essential examples |
| Git data | Logical bytes under the actual Git directory |
| Clean clone total | New checked-out tree plus its Git data |
| Local extras | Ignored archives, dependencies, caches and temporary work |
| External recovery | Bundle, backups and any retained validation clone |

Use decimal MB/GB consistently or label binary MiB/GiB explicitly. Report both
absolute savings and `(before - after) / before * 100`. Logical file bytes differ
from filesystem allocation. A local folder can remain large because backups are
retained even when a new clone is small. A fresh clone does not prove immediate
physical removal of historical objects from GitHub's servers.

List all generated output families with count, bytes and share of `parts` so the
user can later choose export formats. Keep this maintenance inventory out of the
public README. Do not claim total savings from navigation size alone: final renders
add bytes, and unique files may be retained elsewhere.

## 11. Handoff template for the implementing agent

Fill these values for one repository before implementation:

```text
Repository and target branch:
Confirmed remote/push destination:
Authorized scope (code repair / CAD regeneration / rendering / history reset / push):
Existing changes and how they will be preserved:
Expected active IDs and metadata source:
Backend and explicit mesh variants:
Taxonomy keys and first branching category:
Representative and extreme samples:
Archive destination and manifest:
Navigation-only files to preserve:
Required code repairs and corresponding checks:
Required outputs / ignored intermediates:
Full-build command / filtered-build command / docs-only command:
Render command / audit command:
Before sizes, original refs and remote SHA:
Backup verification:
Regeneration / hash / link / visual review results:
Final tree, new root SHA and pushed remote SHA (if reset authorized):
Fresh-clone results and after sizes:
Retained local/external recovery files:
Remaining mechanical questions or concrete blockers:
```

When the user authorizes a named project refresh, proceed through the applicable
steps without asking again for routine reversible repairs. If the existing request
already includes history reset and publishing, that authorization persists. This
documentation-only request does not start those operations in any other project.
If a required action is outside the actual scope, prepare the concrete result first
and identify the specific missing decision; do not substitute repeated generic
permission prompts for doing the authorized work.
