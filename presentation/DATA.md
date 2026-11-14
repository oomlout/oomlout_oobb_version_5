# Presentation data contract

`project.json` is the reviewed input for the README and parts CSV. The KALLAX example includes optional `geometry` data for its dimensional checks. A different project's renderer and manual builder must adapt to that project's geometry; the helper is not an automatic assembly solver.

Required top-level fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Currently `1`. |
| `title`, `revision`, `date` | Plain project name, revision and ISO date. |
| `readme_filename` | Existing root filename, preserving case; default `README.md`. |
| `quantity_columns` | Optional two column labels; default one/two assemblies. |
| `printed_parts` | Array of printed-part records. |
| `hardware` | Array of purchased-part records. |
| `readme` | Strings matching the README template variables. |

Each part needs `ref`, `name`, `quantity`, `spec` and `verification`. Printed parts also need a repository-relative `stl` path. Hardware needs its verified OOMP `url`, `oomp_id` and alpha code. A user-accepted draft exception uses `catalogue_status: pending`, null catalogue fields and an explanation. A catalogue ID is an identity reference, not proof of a supplier's dimensions.

For the current template, set `readme.layout` to `four-section`. Supply `summary`, `hero_image`, `hero_alt`, `details`, `details_image`, `details_alt`, `downloads`, `parts_image`, `parts_alt`, `parts_caption`, `parts_scope`, `hardware_notes` and `assembly_steps`. `title` and the hardware-only `parts_table` come from the generator. No template field is silently omitted.

`summary` is a self-contained plain-English introduction, not a caption or shortened title. Identify the kind of project, its purpose and its setting or compatibility before describing its main capability. It must make sense without the title or image. Include a short paragraph stating that this is an entirely AI-generated coding project: its generated outputs are included and usually work, but it is published primarily as a starting point for others to modify with their own AI tools. This explanation is additional to the image/instruction notice. Follow [Summary writing](STYLE.md#summary-writing).

`parts_scope` explicitly states whether the hardware list is complete for one assembly or representative/non-exhaustive for a named sample. A multiple-object repository uses one sample in its images and does not imply that a sample quantity is the repository total. Keep printed downloads in `downloads`; retain printed records for the CSV and scene audit.

Each assembly step is an object: `{"text":"Seat the nut.","image":"step-01.png","alt":"AI-generated CAD render: nut seated in its recess"}`. Images are relative to `presentation/images/`. The builder generates `images/thumbnails/step-01.png` etc., bounded to 480 × 480 px, and links each thumbnail to the original. There is no assembly hero image. Old string steps remain supported only with an older template and without the `four-section` layout flag.

Use `md5_6_alpha` only when verified in a catalogue record. The current hardware table requires `oomp_id`, its canonical OOMP repository `url`, and the verified code. Its code link is `https://oom.lt/a/{code}`. A user-accepted unresolved entry may instead set `catalogue_status: pending` and leave ID/code/URL null. No supplier URL is substituted. Preserve the full draft in `presentation/source-notes.json`; keep published text terse.

`hero_image`, `details_image`, `parts_image` and step `image` fields are relative to `presentation/images/`. Alt text identifies each generated view. Put essential dimensions in Details and keep extended calculations, assumptions and physical-test status in the manifest and handoff notes. Legacy fields such as `configuration_image` and `installation_steps` are not used by the four-section template.

The validator checks local paths, duplicate references, positive quantities, images, AI notices and PDF text bounds. It does not infer mechanical correctness or perform a new remote hardware check. The project must add a geometry audit for recesses, seating, repeated pieces and thread engagement.

When the renderer uses fixed transforms, assert the expected manifest dimensions before creating scenes so changes cannot silently leave old geometry behind. A new geometry revision requires updating the renderer and section drawing, re-running the audit, and inspecting the resulting pages.
