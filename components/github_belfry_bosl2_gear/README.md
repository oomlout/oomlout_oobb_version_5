# github_belfry_bosl2_gear

**GitHub BelfrySCAD BOSL2: Spur Gear**

BOSL2 `spur_gear()` wrapper — metric involute spur gears with optional helical or herringbone teeth and a centre shaft bore.

Source library: [BelfrySCAD/BOSL2 gears.scad](https://github.com/BelfrySCAD/BOSL2/wiki/gears.scad)

## Library

BOSL2 is included as a git submodule at `BOSL2/`. After cloning this repository, initialise it with:

```bash
git submodule update --init components/github_belfry_bosl2_gear/BOSL2
```

## Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| pos | 3-element [x,y,z] position. | list | [0,0,0] |
| rot | Rotation [rx,ry,rz] in degrees. | list | [0,0,0] |
| type | Geometry type: positive or negative. | string | "positive" |
| teeth | Number of gear teeth (integer >= 4). | number | 16 |
| mod | Gear module (metric pitch). Pitch diameter = mod*teeth. | number | 2 |
| thickness | Gear face thickness in mm (alias: depth). | number | 8 |
| shaft_diam | Centre shaft bore diameter in mm (0 = no bore). | number | 0 |
| pressure_angle | Tooth pressure angle in degrees. | number | 20 |
| backlash | Backlash in mm. | number | 0 |
| helical | Helical angle in degrees (0 = spur gear). | number | 0 |
| herringbone | If true, produce a herringbone (double-helical) gear. | bool | false |
| gear_spin | Rotate the gear teeth pattern by this many degrees. | number | 0 |
| mode | Render modes: "laser", "3dpr", "true". | list | ["laser","3dpr","true"] |

## Category

External Library Wrappers

## Gear Sizing Reference

Pitch diameter (mm) = `mod × teeth`

| mod | teeth | pitch diameter |
|-----|-------|----------------|
| 1   | 16    | 16 mm          |
| 2   | 16    | 32 mm          |
| 2   | 24    | 48 mm          |
| 3   | 20    | 60 mm          |

Two gears mesh when they share the same `mod` and `pressure_angle`.
Centre-to-centre distance = `mod × (teeth_a + teeth_b) / 2`.

## Sample Notes

Requires the BOSL2 submodule to be initialised.
