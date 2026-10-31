# oobb_funnel_rounded_rectangle

Open, rounded rectangular funnel made from OOBB `rounded_rectangle` sections and hulls. The straight spout starts at `z=0`, and the mouth ends at `z=size[2]`. Its inner and outer profiles use the same taper and corner centres, leaving a settable horizontal wall thickness (default 1.5 mm).

| Parameter | Default | Meaning |
| --- | --- | --- |
| `size` | `[36, 36, 14]` | Spout outside width, height, and total funnel depth in mm |
| `mouth_size` | `[63, 63]` | Mouth outside width and height in mm |
| `spout_depth` | `8` | Straight section that inserts into a pot in mm |
| `radius` | `4` | Spout outside corner radius in mm |
| `mouth_radius` | `8` | Mouth outside corner radius in mm |
| `wall_thickness` | `1.5` | Horizontal wall thickness in mm |
| `pos`, `rot`, `type` | `[0,0,0]`, `[0,0,0]`, `p` | OOBB placement and polarity |

For printing, place the wide mouth on the build plate. With the default 36 mm spout, 63 mm mouth, 8 mm insertion depth and 14 mm total depth, the taper rises 6 mm while narrowing 13.5 mm per side, a slope of about 24 degrees above the bed. This shallow wall is likely to need support on a typical FDM printer. A support-free 45-degree taper with the same mouth and spout would need at least 21.5 mm total depth.
