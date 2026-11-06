# Technical presentation style

Use the object and its assembly as the primary visual information. This guidance supplements `RENDER_STYLE.md`.

## Page design

- White page, dark grey text, restrained teal for dimension lines and leaders. Keep the existing warm studio background within renders.
- One plain descriptive title per page. Use sentence case. Omit breadcrumb headers, slash-separated metadata bands, pills, dashboards, decorative cards and slogans.
- Default example size: 900 x 675 pt landscape, 42 pt margins. Title 28 pt, body 10.5-11 pt, captions 9.5 pt, footer 8 pt. Use a plain sans-serif font with one bold weight. Increase type size for a different output scale rather than squeezing text.
- Give each page one task: configuration, parts, main assembly, captive fastener detail, dimensional section or installation checks. A seven-page guide is a worked example, not a required page count.
- Use numbered actions with a specific verb and the part being handled. Put the relevant illustration next to the instructions. Explain access and order when hardware becomes inaccessible later.
- Combine printed parts and hardware in one table: reference, type, part, specification, quantity and MD5 alpha code. Link every part name where a target is available: STL for a print, OOMP record for hardware, or a verified supplier when no OOMP record exists. Also link verified `md5_6_alpha` codes. Show PDF links in the accent colour. Do not invent codes or short URL destinations.
- Use figure captions and fine leaders. Label all hardware that can be mistaken for another type. Show a section through hidden recesses; do not imply visibility through solid plastic.
- Use only the page number and an AI notice in the footer. Put revision/date once near the front and in the manifest.

## README design

Use the supplied template: purpose, AI notice, one assembled image, downloads, configuration, parts, preparation, numbered assembly, end detail, installation, dimensions and sources. GitHub already provides an outline, so a repeated navigation menu is unnecessary. Use Markdown headings and tables. Use descriptive link text, short part references and relative local paths. Avoid badge rows, emoji metadata, centre-aligned prose and HTML card grids.

Image captions must explain the view and its assumptions. Alternative text should identify the assembly and the fact that the image is generated. Keep images in `presentation/images/` at sufficient resolution for details. Avoid embedding repeated large hero images in every section.

## Writing

Use two writing passes. First, write the complete technical draft and retain it in source notes, including assumptions and validation evidence. Second, edit the public README, captions and manual aggressively: retain only the action, part identification and essential dimension. Remove rationale, repeated qualifications and testing commentary. Keep technical evidence in the agent handoff, not in assembly steps.

Use short headings: "Assembly", "Adjustment", "Dimensions", "Installation". Do not add "and checks". Use imperative sentences: "Seat H2 in the outer hex pocket." Delete sentences that do not change what the builder does. Keep actual actions such as measuring the cell or seating a nut; remove general reminders that instructions can be imperfect.

Use this notice near the start:

> AI-generated images and instructions. Errors possible.

Retain validation results in source notes and QA reports. Do not repeat them in the published instructions.

Published image footer:

> AI-generated CAD illustration. Errors possible.

Use "CAD render" for Blender output from production meshes, "section drawing" for a calculated diagram and "illustrative geometry" for generic rolls or hardware. Do not describe a render as a photograph or as evidence of a completed build.

## Review

Inspect the full-size PDF pages and a compact contact sheet. Large blank margins around a small assembly are not a substitute for legible details: adjust the render camera or aspect ratio. Review the README at desktop and narrow widths. A horizontally scrollable parts table is acceptable; essential instructions should not require horizontal scrolling.
