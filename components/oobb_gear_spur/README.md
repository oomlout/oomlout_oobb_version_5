# oobb_gear_spur

**OOBB Motion: Spur Gear**

Metric involute spur gear via BOSL2. Pressure angle fixed at 20°.

Delegates to `github_belfry_bosl2_gear`. Helical angle, herringbone, and gear_spin are fixed at their spur-gear defaults.

## Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| pos | 3-element [x,y,z] position. | list | [0,0,0] |
| rot | Rotation [rx,ry,rz] in degrees. | list | [0,0,0] |
| type | Geometry type: positive or negative. | string | "positive" |
| teeth | Number of gear teeth (integer >= 4). | number | 16 |
| mod | Gear module (metric pitch). Pitch diameter = mod*teeth. | number | 2 |
| depth | Gear face thickness in mm. | number | 8 |
| shaft_diam | Centre shaft bore diameter in mm (0 = no bore). | number | 0 |
| backlash | Backlash in mm. | number | 0 |
| gear_bevel | Chamfer depth (mm) on top and bottom outer edges. 0 = flat faces. | number | 0 |

## Category

OOBB Motion

## Gear Sizing Reference

Pitch diameter (mm) = `mod × teeth`  
Centre-to-centre distance = `mod × (teeth_a + teeth_b) / 2`

Two gears mesh when they share the same `mod`.

## Dependencies

Requires BOSL2 submodule initialised in `github_belfry_bosl2_gear`:
```bash
git submodule update --init components/github_belfry_bosl2_gear/BOSL2
```
