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

Each part needs `ref`, `name`, `quantity`, `spec` and `verification`. Printed parts also need a repository-relative `stl` path. Hardware should include its verified `url` and `oomp_id`; use an empty URL and null ID when no exact record has been found, with an explanation. A catalogue ID is an identity reference, not proof of a supplier's dimensions.

`readme` contains all variables in `templates/README.template.md` except `title` and `parts_table`, which are supplied by the generator. `assembly_steps` and `installation_steps` are arrays of short actions and become numbered lists. Other fields are Markdown strings. No template field may be silently omitted; Python's strict substitution reports a missing key.

Use `md5_6_alpha` only when verified in a catalogue record. The combined table uses the code as a compact clickable label for `url`. If a real short URL has also been verified, store it in `short_url`; otherwise keep the canonical catalogue URL. Use null for missing codes. Preserve the full draft in `presentation/source-notes.json`; keep the manifest's published text terse.

`hero_image`, `configuration_image`, `assembly_image` and `detail_image` are filenames relative to `presentation/images/`. Their corresponding `_alt` fields describe the view. `quantity_basis` states what the first quantity represents. Include measured dimensions, unknowns, and explicit physical-test status in `dimensions` and `verification`.

The validator checks local paths, duplicate references, positive quantities, images, AI notices and PDF text bounds. It does not infer mechanical correctness or perform a new remote hardware check. The project must add a geometry audit for recesses, seating, repeated pieces and thread engagement.

When the renderer uses fixed transforms, assert the expected manifest dimensions before creating scenes so changes cannot silently leave old geometry behind. A new geometry revision requires updating the renderer and section drawing, re-running the audit, and inspecting the resulting pages.
