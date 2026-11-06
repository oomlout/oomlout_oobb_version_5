# Reference research and decisions

Reviewed 6 November 2026. These notes were written with AI assistance. The observations below are design decisions, not claims that these sources validate the KALLAX holder.

## Documentation references

| Primary source | Observation | Decision for this template |
| --- | --- | --- |
| [Voron Trident README](https://github.com/VoronDesign/Voron-Trident/blob/main/README.md) | Leads with the project, a download link and an assembly image; directs readers to the bill of materials. | Put the assembled object and usable downloads near the start. Keep repository navigation out of the visual design. |
| [Prusa MINI+ X-axis and extruder guide](https://help.prusa3d.com/guide/3-x-axis-extruder-assembly_199519) | Separates tools, parts preparation, assembly and checks into explicit numbered actions. | Use action-based steps and identify parts before they become hidden. Keep the guide structure, not the website's navigation elements. |
| [IKEA KALLAX assembly instructions](https://www.ikea.com/gb/en/assembly_instructions/kallax-shelving-unit-white__AA-2703514-1-100.pdf) | Uses numbered visual assembly sequences and hardware quantities. | Give each diagram a narrow purpose and use short part references. Keep explanatory text where this project's hidden fasteners need it. |
| [GitHub README documentation](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes) | Documents automatic outlines and branch-aware relative links. | Use plain Markdown sections and relative local image/STL paths. Avoid a repeated breadcrumb or navigation row. |

The previous KALLAX guide used a repeated slash-separated header/footer, tinted panels and promotional headings. The revision removes those features, enlarges the mechanical views, retains a restrained dimension-line colour and uses factual headings. Its style decisions are ours, informed by the references above; no reference artwork was copied into the deliverables.

## Hardware research for the worked example

| Requirement | Verified record | Finding |
| --- | --- | --- |
| M6 ordinary hex nut | [OOMP hardware_nut_m6](https://github.com/oomlout/oomlout_oomp_version_1_messy/tree/main/parts/hardware_nut_m6) | Correct catalogue identity. Eight per cell: four fixed and four retaining. Model uses 5 mm nominal thickness; measure the hardware. |
| M6 coupling nut | [OOMP hardware_nut_m6_coupling](https://github.com/oomlout/oomlout_oomp_version_1_messy/tree/main/parts/hardware_nut_m6_coupling) | Correct coupling identity; one per rod. OOMP alone does not establish the assumed length. |
| Coupling dimensions | [Accu M6 DIN 6334](https://www.accu.co.uk/hexagonal-stud-connector-nuts/62290-HTBN-M6-A2) | 18 mm length and 10 mm across flats support the nominal model. |
| Fully threaded hex-head M6 x 25 | [OOMP hardware_set_screw_m6_25_mm_length](https://github.com/oomlout/oomp_hardware_bolt_version_5/tree/main/parts/hardware_set_screw_m6_25_mm_length) | The working YAML explicitly identifies full thread and hex head. The similar `hardware_bolt_m6_25_mm_length` identifies partial thread and is not the chosen record. |
| M6 rod cut to 300 mm | No exact OOMP entry verified | The checked local OOMP catalogue and web search did not produce an exact entry. The BOM specifies cut stock and records the missing catalogue link instead of inventing one. |

OOMP records were checked through the connected GitHub tool, including the nut and coupling README files and the fully threaded fastener's `working.yaml`. The local bolt catalogue supplied the initial distinction between bolt and set screw. The lookup is an identity check; no price or availability claim is made.

## Furniture and geometry

[IKEA's current UK product page](https://www.ikea.com/gb/en/p/kallax-shelving-unit-white-30275861/) identifies the 4 x 4 unit and lists 147 cm width, 39 cm depth and 146.5 cm height. The illustrative shell retained from the CAD study is 1470 x 1470 x 390 mm, with nominal 335 mm cells; it is a simplified setting, not an accurate furniture manufacturing model. Do not present the 335 mm opening or model height as an IKEA-verified internal dimension.

The final end arrangement follows the user's correction: a retaining nut against the final frame, covered by a hex spacer, with a shorter slotted cover. The chosen 7 mm full-hex and 7 mm slotted parts already exist in the project. Together they replace the earlier 14 mm clip while preserving the nominal 335.01 mm span. The 25 mm bolt calculation remains unchanged. Assembly access and physical clearance remain to be tested.
