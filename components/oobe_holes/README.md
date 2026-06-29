# oobe_holes

**OOBB Geometry Helpers: OOBE Hole Array (M3, 7.5 mm)**

M3 screw holes on the OOBE 7.5 mm half-grid. Identical patterns to `oobb_holes` but spacing is fixed at 7.5 mm and hole size is fixed at M3. No `both_holes` option — there is no smaller grid.

## Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| holes | Hole pattern(s): `all`, `perimeter`, `perimeter_miss_middle`, `u`, `top`, `bottom`, `left`, `right`, `corners`, `single`, `missing_middle`, `just_middle`, `circle`. | list | ["all"] |
| width | Width of the hole grid in OOBE units (each unit = 7.5 mm). | number | 0 |
| height | Height of the hole grid in OOBE units (each unit = 7.5 mm). | number | 0 |
| pos | Base position [x, y, z] in mm. | list | [0,0,0] |
| depth | Hole depth in mm. | number | 100 |
| middle | Include the centre hole for patterns that have one. | bool | true |
| circle | Filter an `all` grid to only holes inside a circular boundary. | bool | false |
| diameter | Circular pattern diameter in OOBE units. | number | 0 |
| diameter_clearance | Edge clearance in mm for circular filtering. | number | 7.5 |
| diameter_center_clearance | Min distance from centre in mm before a hole is allowed. | number | 0 |
| loc | Grid location(s) for the `single` pattern. 1-based [x,y], e.g. `loc=[1,1]`. | list | [0,0] |
| donut | When true, use the circle approach — holes fill a ring. Requires `diameter` for the outer size. | bool | false |
| diameter_center | Diameter of the hole-free zone in the centre, in OOBE units (each unit = 7.5 mm). Only used when `donut=true`. | number | 0 |

## Category

OOBB Geometry Helpers

## Notes

- Spacing fixed at 7.5 mm (OOBE half-grid).
- Hole size fixed at M3.
- Delegates to `oobb_holes` with `size="oobe"` and `radius_name="m3"`.
