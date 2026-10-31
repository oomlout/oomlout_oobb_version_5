# OOBB v5 full-depth bevel gear

`shape="oobb_gear_bevel"` is automatically discovered and reuses the existing
`components/github_belfry_bosl2_gear/BOSL2` submodule.

```python
p3 = copy.deepcopy(kwargs)
p3["type"] = "positive"
p3["shape"] = "oobb_gear_bevel"
p3["teeth"] = 40
p3["mate_teeth"] = 40
p3["mod"] = 1.5
p3["depth"] = 6
p3["pressure_angle"] = 20
p3["backlash"] = 0.2
p3["shaft_diam"] = 0
p3["base_chamfer"] = 0.8
p3["underside_angle"] = 45
p3["pos"] = [0, 0, 0]
oobb.append_full(thing, **p3)
```

The bevel spans the full specified axial thickness. There is no cylindrical
backing or straight lower tooth extension. The bottom is cut flat at the outer
heel, and the top is cut flat exactly `depth` mm above it, removing raised tooth
tips. The outer pitch diameter stays `mod * teeth`; the gear is not enlarged.
The underside rises outward from a circular bed-contact area to the teeth at
`underside_angle=45` degrees. It is formed by removing material: the center
stays directly on the bed, without a pedestal, and the outer tooth tips begin
above it. `base_chamfer` now sets the bed-circle inset below the tooth-root
circle (0.8 mm at module 1.5, 0.4 mm at module 0.75). Setting it to zero starts
the ramp at the root circle; it does not remove the ramp. The angle is measured
from the bed and can be set from 45 to less than 90 degrees. The
active gear-project catalog has 6 mm and 9 mm depths; 12 mm versions are retired.

`dimensions(**kwargs)` chooses a cone face width long enough for the top cut
to pass through the center plate as well as the teeth. A supplied `face_width`
must be at least that long and strictly less than the cone distance. It returns
a conservative `inner_root_radius` for protecting bores and mounting holes.
Some diameter/depth combinations cannot fit a shaft bore and must be omitted
or made thinner. Full-depth faces can exceed the conventional one-third-cone
face-width recommendation; physical mesh and load testing remain necessary.

Teeth are straight (`spiral=0`, `cutter_radius=0`), with a 90 degree shaft angle.
Match teeth/mate_teeth, module, pressure angle and clearance across a pair.
The catalog uses identical gears for equal-ratio drives. Anchors: `center`,
`bottom`, `pitchbase` and `apex`. Named OOBB holes should be subtracted by the
caller for mode-specific allowances; `shaft_diam` provides a fixed-size bore.

For assembly, align both apex anchors and rotate one gear by `[-90,0,0]`.
Phase an equal pair by half a tooth (`180/teeth`). For a centered exported STL,
the local apex Z coordinate is `mod*teeth/2 - oobb_gear_bevel_base_z(...) - depth/2`
for a 1:1 pair. The gear-project examples and validator use this reference.

Source: [BOSL2 bevel gear documentation](https://github.com/BelfrySCAD/BOSL2/wiki/gears.scad#functionmodule-bevel_gear).
