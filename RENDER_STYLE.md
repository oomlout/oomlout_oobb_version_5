# OOBB render style

Use this house style for presentation renders of OOBB parts, assemblies and habitat builds. Carry each part's material through the assembled, exploded and detail views.

## Filament colours

| Role | Bambu Lab PLA Basic | Studio swatch | Typical use |
| --- | --- | --- | --- |
| Primary | Turquoise 10605, called **teal** in OOBB | `#00B1B7` | The habitat body, enclosure, main plate and other large printed surfaces. Teal should read first in the assembled view. |
| Secondary | Black 10101 | `#000000` | A support, bridge, saddle or secondary mechanical group. Use soft reflections to reveal edges and recessed features. |
| Highlight | Sunflower Yellow 10402 | `#FEC601` | An index mark, adjustment point, fit sample or complete family of functional parts. Use yellow on every copy when it helps the reader follow the group through assembly. |

Use the swatches as sRGB. Convert them to linear RGB for Blender shader inputs. Give PLA a satin finish with metallic at zero and roughness near 0.4. A near-black shader such as `#121212` keeps details readable under studio lighting. Purchased motors, bearings, fasteners and contacts keep their physical materials. These filament swatches were sampled from the manufacturer's PLA Basic colour selector. [Bambu Lab PLA Basic](https://uk.store.bambulab.com/products/pla-basic-filament)

Use all three filament colours within one multipart mechanism when they distinguish pieces the builder handles separately. For example, both the inner guide sleeves and the complete outer ring of printed lobe contacts can be sunflower. Apply the same yellow to a connected printed contact ring when it replaces the individual sleeves. A stacked shaft can use sunflower end journals, teal nut carriers and black eccentric halves. Keep each role consistent across views and name it in the palette key.

## Presentation

- Render the current production CAD or exported meshes. Restore print-oriented parts to their assembly positions before rendering. Use an orthographic three-quarter camera, large soft lights and a quiet warm-white background. Check the silhouette, holes, black recesses and metal edges at the final viewing size.
- Lead with the assembled object. Use an open-shell or underside inset when it reveals how a part seats or where a nut loads.
- Explode parts along their assembly axes. Keep fasteners aligned with their holes. Label the functional parts, screw lengths, captive nut locations and any assembly sequence that matters. Separate a dense assembly into two views if the hardware paths overlap.
- For a fit trial, show both the combined print and the part in use. Match the labels on the print, give clearances with units and say whether they are per side. Highlight the starting sample in sunflower.
- Use short captions, dark text, fine leaders and a small palette key. Keep callouts legible at chat-preview size. Save full-resolution PNGs beside the corresponding STLs in their actual `parts/<catalogue-id>/` folders.

## Example

For complete project README and assembly-manual packages, use the [presentation workflow](presentation/README.md). It adds a direct technical writing style, a plain page layout, visible AI-generated notices, verified OOMP hardware references and reusable build/validation scripts. Keep the render materials and lighting rules above; apply project-specific colour overrides from the user.

The sibling motor-holder repo contains a reproducible Blender renderer in `render_tt_holder.py`. Its TT sheets show a teal clamshell and face plate, a black bearing bridge and a sunflower index at the short rear screw. The index is a render finish. See the [renderer](../oomlout_oobb_part_holder_motor_version_5/render_tt_holder.py) and the [assembled and exploded sheets](../oomlout_oobb_part_holder_motor_version_5/parts/oobb_part_holder_motor_gear_tt_5_width_3_height_23d5_depth_bearing_6704_version2).
