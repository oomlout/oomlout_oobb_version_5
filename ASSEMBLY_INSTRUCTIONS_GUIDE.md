# OOBB assembly instructions guide

Style version 4: an eight-page, signature-padded assembly book with four pictorial panels on each landscape A4 instruction page. This supersedes the earlier standalone sheets. The [wave-drive manual](../oomlout_oobb_part_motor_gearbox_wave_drive_version_5/parts/oobb_part_motor_gearbox_wave_drive_version_5_12_to_1_reduction/assembly/assembly_instructions.pdf) is the reference implementation.

## Page and typography

- A4 landscape: 297 x 210 mm, 6 mm outer margins, 4 mm gutters.
- Four panels in a 2 x 2 grid, read left to right, then top to bottom. Each panel is 140.5 x 97 mm.
- The landscape A4 page is the default presentation unit in both the PDF and HTML viewer. Show steps 1-4 together, then 5-8, then 9-12. Do not substitute one-step screens for these pages. A final incomplete instruction page retains the same grid with unused positions blank; covers, details, the completed view and inventories remain separate pages.
- White paper, heavy 3 pt pure-black (#000000) outer borders and 1.1 pt pure-black component-box borders, 3 mm outer corner radius. All text is black. Do not draw insertion arrows. Do not use teal or yellow for typography.
- A plain 27 pt Consolas black step number is the only heading. No title, action sentence, captions, legend, parts-box heading, page footer or other explanatory text on the panels. Put preparation, numbered actions, step illustrations and notices under Assembly in the project, version or part's main README.
- Use Segoe UI Semibold for part names and cover headings, Consolas for step numbers and URL prefixes, and Consolas Bold for URL codes. Use Helvetica and Courier fallbacks where needed. Part names remain 7 pt. URL codes are smaller at 6.4 pt bold, with a still smaller 4.8 pt regular prefix. Quantities are 5.8 pt regular. Step thumbnails are 8.5 mm high, reduced from 10 mm.
- Place the large assembly diagram to the left. The small parts box sits at the top right, 34 mm wide. Its height follows the number of part types, up to four.
- Each parts entry shows its image first. Overlay the small black quantity at the image's clear bottom-right corner, shifted 1 mm to the right only when the quantity exceeds one: `x2`, `x12`. Omit `x1`. Use no spaces, no badge, and no coloured or oversized quantity.
- Put the part name just below the thumbnail. Only hardware gets a compact `oom.lt/a/{md5_6_alpha}` line below it. Printed components have names and quantities only: no shortlinks, alpha codes or printed QR codes. Measure the wrapped name height and leave only 0.65 mm before the URL text box. Keep the URL on a shared baseline: the prefix is small and regular; the code is larger and bold, with optical emphasis comparable to the heavier part name above it. Preserve thread, length and head form in screw names. Include spacer dimensions in its visible name: `Spacer 7mm OD 12mm depth`. Keep other secondary dimensions in companion notes.
- Keep text at the specified readable size. Split overfull operations rather than squeezing or clipping text. Hardware thumbnails identify parts; they are not to a common scale.

## Assembly diagrams and step grouping

Use actual current OpenSCAD production meshes rendered in Blender, with orthographic projection and soft lighting. Preserve the established material colours in the CAD, including the previously assembled parts. The black-text rule does not recolour the physical parts.

Keep the complete assembly-so-far in every panel. Its motor, base, installed fasteners and other fitted parts stay in their proper positions, even when naturally hidden by later parts. Do not repeatedly switch to isolated parts or omit the motor. Keep the camera consistent. Use a supplementary inset only when the cumulative view cannot show an essential operation clearly.

Combine related actions. For example, load the cage's twelve captive nuts and lower the cage in one panel: draw the cage exploded above the assembly, and the nuts exploded underneath that cage. Show every instance, not one representative roller with an implied quantity. The inventory box counts each newly added physical item once.

Align each fastener with its hole. Show direction through alignment and clear separation, without arrows. Multiply the authored explosion offsets by 1.35 by default, and use tighter camera framing to keep the parts readable. Expose the nuts below the receiving part before that part is lowered; preserve radial alignment for side-loading clamp nuts and screws.

Do not combine steps that conceal required access. Tighten cage screws before fitting the output bearing. Load base nuts before closing the case. For this drive, the six M3 x 30 case socket caps enter from the top, into nuts underneath the base; the four motor screws are M3 x 8 countersunk, flush with the plate. Cage screws are now M2 x 20; their raised seats leave 1.6 mm nominal tip clearance above the lower cage face.

## OOM.LT part links

For purchased hardware only, use OOMP's `md5_6_alpha` convention: MD5 of the UTF-8 identity, take the first six hexadecimal characters, and encode that integer as lower-case base36. The visible label is `oom.lt/a/{code}` and the PDF link target is `https://oom.lt/a/{code}`. This replaces the old BIP39 label entirely.

Reuse an exact existing OOMP identity where available. Printed parts retain their source IDs for regeneration, but have no short URLs or alpha codes in the manifest, CSV or booklet. Hardware without an exact matching catalogue record uses an explicitly project-local identity. Preserve the full ID, MD5, alpha code, URL and identity provenance in the manifest and CSV. Generating a code or a PDF hyperlink does not register a redirect with oom.lt. Do not claim local codes are already published; keep redirect verification separate from code generation. Never substitute a different screw head or drive just to get a catalogue match.

Identical physical specifications in different roles may share a code, such as the motor and shaft-clamp M3 x 8 countersunk screws. Reject only collisions between different full identities. Count one complete motor, not its six render meshes.

## Editable source and regeneration

Author the style, part labels and complete step sequence in `working_oomp_populate.py`, using explicit multiline dictionaries. Continue through `working_oomp.py` and `working_scad.py`. Reusable helpers use `copy.deepcopy`, `kwargs.setdefault` and `**kwargs`. Do not edit generated PDF or PNG files by hand.

The reference functions are `define_assembly_card_style()`, `define_assembly_part_labels()` and `define_assembly_cards()`. The panel recipe has:

- Use `title` and `action` for the main README's written sequence. Keep the print panels pictorial.
- `add`: named CAD instances consumed for the first time in this step.
- `move`: XYZ explosion offsets in millimetres from final assembly coordinates.
- `targets`: optional retained intermediate insertion offsets for mechanical explanation; version 4 does not render arrows.
- `eye` or `underside`: optional camera changes when genuinely required.

The renderer includes the cumulative set of added instances automatically. `components/wave_drive/assembly_cards.py` audits inventory, resolves alpha labels, stages Blender, composes the PDF and renders review PNGs. `render_studio.py` uses the production meshes and renders the cumulative views plus an assembled book-cover image.

Store everything under `parts/<configuration-id>/assembly/`: `assembly_instructions.pdf`, `assembly_manifest.json`, `parts.csv`, `cards/`, `pages/`, `contact_sheet.png`, `validation.json`, and `render/` for mesh cache, raw renders and editable scenes. Keep old styles under `parts/_archive/`; do not create a root presentation folder.

`python working.py` regenerates geometry, validation, renders and instructions. `python working.py --assembly-only` rebuilds instructions from validated current meshes and rejects mechanical changes that need a full build. `--scad-only` and `--no-renders` skip graphical manuals. The print pack includes the current PDF, inventory, manifest and individual panels.

## Book structure and printing

Define book text and options in `define_assembly_book()` in populate. A separate reusable `assembly_booklet.py` composes the book from the audited production inventory and rendered diagrams.

Use reading order: front cover, technical project-details verso, instruction pages, a full-page boxed finished-assembly view numbered as the next step, any required blank spacer pages, boxed printed and hardware inventories, and back cover. The first instruction page is page 3. Insert blank pages immediately before the summary until the total page count is divisible by four. The summary must always be the penultimate page, and the back cover the last page.

For twelve assembly operations, the eight-page sequence is: cover; project details; steps 1-4; steps 5-8; steps 9-12; full-page step 13 showing the completed assembly; parts inventories; back cover. The spacer is genuinely blank: no page number, notice or border.

Use a print-oriented cover with a heavy perimeter rule, the solid black Oomlout symbol without lettering, a clear title, one technical subtitle and the GitHub project name. The reference title is `Wave drive`, with `{reduction}:1 reduction / NEMA 17 drive` underneath. Centre the actual assembled CAD below the header rule. The back cover contains the same symbol and border, without repeating the title and subtitle.

Use the unshaded vector artwork from `C:/gh/oomlout_media/logos/logo_vector_unshaded/oomlout-LOGO-unshaded-vector.svg`. Keep an unchanged source copy inside the project. The source symbol occupies the first three compound subpaths; the later subpaths form lettering. Preserve those first three paths, remove lettering and render the symbol in pure black. Save the derived vector in the part's assembly/assets folder and track the source hash. This is vector processing, not an AI-generated substitute logo.

Write the inner-cover details as an editable default list in populate. Review every list entry and turn it into a direct technical bullet: reduction, motor body/shaft sizes, roller size, bearing sizes, screw joints, build command and brief verification status. Remove marketing language, repeated headings and long explanations.

On the penultimate page, put printed parts and purchased hardware in separate outlined boxes. Use their images, names and actual quantities, omitting x1. Add links only to hardware. Do not add a sentence stating the total printed-part count. Derive both inventories from the same production manifest, and merge identical purchased hardware by full identity across different roles. Count the complete motor once. Reconcile the combined quantities against the physical assembly inventory.

The full-page summary is a numbered boxed view of the finished assembly, not another parts-loading step: introduce no additional inventory and do not double-count any parts. Keep the motor visible. Its image is included in cards/step_13.png for the reference build.

The PDF contains landscape A4 logical pages in reading order, not pre-imposed printer spreads. Apply booklet imposition only once in the print workflow. The multiple-of-four padding ensures correct cover/summary placement; printer paper size and scaling still determine the folded booklet size. To preserve the full A4 instruction-page size, choose a suitable larger sheet or print the logical pages as a bound document at 100%.

## Review

Audit that every printed part, bearing, roller and fastener is introduced exactly once. Confirm all previous instances persist in every following panel. Check insertion directions, underside nut pockets, screw head forms and screw length conventions against the CAD.

Render every PDF sheet and inspect at its actual printed size. Check all four panels, inventory text, quantities, links, thumbnail overlays and visibility of the receiving parts. Automated checks must reject overflow, wrong paper orientation, coloured text, unexpected prose, missing part codes and stale geometry hashes. Keep a page contact sheet and individual panel PNGs.

Written notes retain the AI-generated notice and physical validation status. The panels intentionally omit those extra words at the user's request. A digital fit check does not establish a successful physical build.

![Four-panel landscape A4 instruction page](../oomlout_oobb_part_motor_gearbox_wave_drive_version_5/parts/oobb_part_motor_gearbox_wave_drive_version_5_12_to_1_reduction/assembly/pages/page_03.png)

## Standalone instruction viewer

Use [the reusable page-viewer template](presentation/templates/assembly_page_viewer.html). Populate `__TITLE__`, `__PROJECT_URL__` and `__DATA__` from the same audited book manifest. The payload contains `slides` (page ID, label, number, kind, step numbers, image key and normalized link rectangles), embedded `images`, `start`, `layout`, `paper_mm` and `step_count`. `start` is the first instruction page; `layout` is `a4-landscape-four-step`. The KALLAX `components/kallax/assembly_viewer.py` is a working page-export adapter.

Generate assembly_instructions.html beside the PDF. Embed the exact rendered PDF pages as data URIs, with inline CSS and JavaScript and no CDN dependencies. Start at the first instruction page, showing steps 1-4 together in their 2 x 2 landscape A4 layout. Navigate by whole pages, using labels such as "Steps 1-4" and "Steps 5-8". Keep the same page order, borders, typography, inventories and spacing as the PDF. Extract PDF hyperlink rectangles into clickable HTML overlays so hardware links remain usable. Printed parts have no URLs or codes.

Provide previous/next page controls, arrow keys, touch swipes, a page selector, zoom and a user-activated full-screen button. Include cover, details, completed view and parts-list pages once in reading order. On narrow screens retain the landscape sheet and provide zoom/pan; do not reflow the four panels into single-step screens. Individual panel PNGs remain secondary assets for written instructions and close inspection. Browser printing must produce the same A4 landscape pages, with navigation hidden. Verify the initial four-step page, page ranges, keyboard navigation, endpoints, zoom, hardware links and narrow layouts in a real browser.

On the cover use one technical subtitle, such as 12:1 reduction / NEMA 17. Put the full GitHub URL underneath the project name, with both inside the print margin. Link the catalogue name and thumbnail to the main README containing the complete written sequence. In that README offer the hosted viewer, PDF and downloadable standalone HTML as separately labelled formats. Publish only when authorized.
