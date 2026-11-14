# Technical presentation style

Use the object and its assembly as the primary visual information. This guidance supplements `RENDER_STYLE.md`.

## Page design

- White page, dark grey text, restrained teal for dimension lines and leaders. Keep the existing warm studio background within renders.
- One plain descriptive title per page. Use sentence case. Omit breadcrumb headers, slash-separated metadata bands, pills, dashboards, decorative cards and slogans.
- Default example size: 900 x 675 pt landscape, 42 pt margins. Title 28 pt, body 10.5-11 pt, captions 9.5 pt, footer 8 pt. Use a plain sans-serif font with one bold weight. Increase type size for a different output scale rather than squeezing text.
- Give each page one task: configuration, parts, main assembly, captive fastener detail, dimensional section or installation checks. A seven-page guide is a worked example, not a required page count.
- Use numbered actions with a specific verb and the part being handled. Put the relevant illustration next to the instructions. Explain access and order when hardware becomes inaccessible later.
- The manual and CSV may retain the complete printed/hardware BOM. The main README lists hardware only, with quantities, canonical OOMP IDs and verified alpha codes. Hardware names and IDs link to OOMP repository pages; codes link to `https://oom.lt/a/{code}`. Do not substitute supplier links or invent a missing record. Mark unresolved entries pending only when the user accepts that draft exception.
- Use figure captions and fine leaders. Label all hardware that can be mistaken for another type. Show a section through hidden recesses; do not imply visibility through solid plastic.
- Use only the page number and an AI notice in the footer. Put revision/date once near the front and in the manifest.

## README design

For compact OOBB part catalogues, apply the specific [catalogue refresh rules](CATALOGUE_REFRESH.md): keep the four sections and AI notices, show one representative example, link discovery and part choices to directories, and omit full catalogue/file/download tables. Store each finished catalogue render once beside its canonical mesh and reference it from navigation. These catalogue rules refine the general assembly-package image and download layout below; retain real hardware and assembly documentation for multipart projects.

Use the project title followed by the AI notice and exactly four level-two headings, in this order:

1. **Summary** — explain what the project is, what it does and where it is used in plain English. Assume the reader knows only the project name or a search result. Main image: the finished object in use.
2. **Details** — operating details and essential dimensions. Main image: only the printed parts in their assembled positions. Hide hardware, the setting and contents.
3. **Parts** — main image: exploded assembly. For a single-piece print, show the object; for a catalogue, show one named representative example. The table lists hardware, not printable parts. For one assembly, give a complete hardware list with quantities. For a catalogue sample, label the list representative and non-exhaustive; quantities must explicitly refer to the sample. Link hardware names and OOMP IDs to their OOMP pages, and verified short codes to `https://oom.lt/a/{code}`. Put printable downloads under Details or in the full BOM.
4. **Assembly** — no section hero. Use short numbered actions, each with its own small image linked to the full-size image. Include preparation, adjustment and installation in the sequence where needed.

Generate real thumbnail files, normally 480 px on the longest edge, under `presentation/images/thumbnails/`. Use `[![alt](thumbnail.png)](full-size.png)` so GitHub displays the small file and opens the full image on click. Do not merely reduce the displayed width of a full-size download. Use production CAD for staged assembly views; never invent fasteners to fill a step.

Use the supplied template. GitHub already provides an outline, so a repeated navigation menu is unnecessary. Use Markdown headings and tables, descriptive link text and relative local paths. Avoid badge rows, emoji metadata, centre-aligned prose and HTML card grids. Put source evidence and extended dimensions in the build notes rather than adding root headings.

Image captions must explain the view and its assumptions. Alternative text should identify the assembly and the fact that the image is generated. Keep images in `presentation/images/` at sufficient resolution for details. Avoid embedding repeated large hero images in every section.

## Summary writing

Write a short, self-contained introduction, usually two or three sentences, followed by a brief paragraph explaining the project's AI origin and purpose as a starting point. A person arriving from search, a discovering agent or a search engine should be able to identify the project from this introduction alone.

- Start with the kind of thing this is: for example, 3D-printable storage holders, a motor mount or a collection of circuit-board mounting plates. State its purpose and relevant setting or compatibility.
- Say what the repository provides when useful: printable files, CAD source or assembly instructions. Do not assume the title or image explains the object.
- Follow with the main arrangement or capability that helps someone decide whether the project suits their need. Keep dimensions, fastener choices and assembly steps in later sections.
- Use concrete nouns and ordinary language. Introduce unfamiliar terms briefly. Avoid unexplained abbreviations, slogans, keyword lists and repeating the project title without explaining it.
- Use relevant names naturally, such as IKEA KALLAX and 3D printer filament. Write for understanding; do not add search-engine claims or keyword stuffing.
- Before finishing, read the paragraph without its title or image. It should still answer: what is it, what is it for, and where does it fit?
- In Summary, explicitly state that this is an entirely AI-generated coding project. Explain that the generated outputs are included and usually work, while the main reason for publishing is to let others use it as a starting point for their own AI-assisted modifications. Keep the separate AI-generated image/instruction notice as well.

Example: "This project provides 3D-printable holders for storing 3D printer filament in an IKEA KALLAX shelving unit. Two holders store five reels at the front and five filament refills without spools on a raised row at the back."

Follow with: "This is an entirely AI-generated coding project. The generated outputs are included and usually work, but the main purpose of publishing it is to give others a starting point for modifying the project with their own AI tools."

## Writing

Use two writing passes. First, write the complete technical draft and retain it in source notes, including assumptions and validation evidence. Second, edit the public README, captions and manual aggressively: retain only the action, part identification and essential dimension. Remove rationale, repeated qualifications and testing commentary. Keep technical evidence in the agent handoff, not in assembly steps.

Keep the four README headings above. Other documents may use short headings such as "Adjustment" or "Installation"; never add "and checks". Use imperative sentences: "Seat H2 in the outer hex pocket." Delete sentences that do not change what the builder does. Keep actual actions such as measuring the cell or seating a nut; remove general reminders that instructions can be imperfect.

Use this notice near the start:

> AI-generated images and instructions. Errors possible.

Retain validation results in source notes and QA reports. Do not repeat them in the published instructions.

Published image footer:

> AI-generated CAD illustration. Errors possible.

Use "CAD render" for Blender output from production meshes, "section drawing" for a calculated diagram and "illustrative geometry" for generic rolls or hardware. Do not describe a render as a photograph or as evidence of a completed build.

## Review

Inspect the full-size PDF pages and a compact contact sheet. Large blank margins around a small assembly are not a substitute for legible details: adjust the render camera or aspect ratio. Review the README at desktop and narrow widths. A horizontally scrollable parts table is acceptable; essential instructions should not require horizontal scrolling.
