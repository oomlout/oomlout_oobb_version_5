# Optional top and bottom edge radii

Existing calls retain their exact previous behavior. `radius_rounded` still
controls both edges when neither new option is set.

To control the edges independently, pass `radius_top` and/or `radius_bottom`.
An omitted side uses `radius_rounded`; zero leaves that edge square. The plan
corner radius remains `radius`. Each edge radius must fit inside the plan
radius, and their sum must not exceed the thickness.

```python
oobb.append_full(thing, shape="oobb_rounded_rectangle_rounded",
    type="positive", size=[44, 44, 3], radius=5,
    radius_top=1.5, radius_bottom=0, pos=[0, 0, 0])
```

This gives a flat-bottomed 3 mm plate with R5 plan corners and a 1.5 mm top
rim round. Holes/cutouts are applied afterward by the caller. Position,
rotation and positive/negative polarity are supported. The opt-in profile
uses a raw SCAD module; native CAD adapters must explicitly support that module.

Regression tests in `tests/test_rounded_rectangle_edge_radii.py` preserve the
pre-change component hashes for legacy calls, including transformed cutters.
