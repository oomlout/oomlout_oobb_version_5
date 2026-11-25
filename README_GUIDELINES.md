# OOBB project README guidelines

Start with the project name and a plain description of the object: what it does, what it fits and what files the repository provides. Credit the inspiration immediately afterwards, linking both the specific source and its creator. Verify the creator's name rather than inferring it from a URL.

Include this standard message near the description:

> This is an entirely AI-generated coding project. The source code is largely unreadable by humans, but usable generated files are included. It is published so others can use their own AI tools to understand, modify and regenerate the design.

Describe any untested physical properties accurately for that project. Retain the separate notice: “AI-generated CAD images and instructions. Errors possible.” Do not claim generated files or hardware have been validated beyond the checks actually completed.

For projects with assembly instructions and multiple design versions, use a compact landing README with a versions table. Start with one row and add rows as versions become available:

| Image | Version and description | Main README | HTML assembly instructions | PDF download |
| --- | --- | --- | --- | --- |
| Linked CAD thumbnail | Version name and essential differences | Version-specific design and build notes | Hosted browser viewer | Direct PDF download |

Link each project, version or part name and its thumbnail to its main README. Use the README's `#assembly` anchor when linking directly to the written instructions. Use the deployed GitHub Pages URL for the primary HTML viewer link in the landing README, part README and documentation indexes. A repository-relative HTML link opens GitHub’s file view. Reserve download links for separately labelled offline copies. Verify the Pages URL anonymously in a browser and confirm that the initial instruction page and navigation work. Keep PDF and standalone HTML downloads separately labelled. Check that the viewer serves HTML and the PDF link serves a PDF.

Put preparation, numbered assembly actions, illustrations and fit notes in the main README under Assembly. For a catalogue with several guided parts, include their sequences in the project README and generate each part's sequence in its own README from the same source. For versioned builds, put the full sequence in the version README reached from the landing table. An existing `ASSEMBLY.md` can remain available for older bookmarks. Each future version must have its own appropriate README, viewer and PDF targets.

The primary HTML assembly link opens the four-step landscape A4 page viewer, initially showing steps 1-4. Its pages must match the PDF. Keep individual panel images available from the detailed written instructions; do not make a one-step slideshow the primary assembly link.

Define descriptions, credits and version rows in the project's populate code and generate the landing README through the usual populate → working_oomp → working_scad progression. Changes must survive regeneration. This version-index layout takes precedence over the older four-section landing layout for multipart assembly projects; individual part catalogues retain their catalogue conventions. Store graphics and instructions inside each version's parts directory.
