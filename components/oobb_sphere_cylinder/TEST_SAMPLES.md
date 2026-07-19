# Test Samples

## Exact `samples` block to paste into `working.py`

```python
samples = [{'filename': 'test_1',
  'preview_rot': [45, 0, 25],
  'kwargs': {'pos': [0, 0, 0], 'depth': 18, 'radius': 7, 'radius_rounded': 2, 'zz': 'center', 'mode': 'true'}},
 {'filename': 'test_2',
  'preview_rot': [45, 0, 25],
  'kwargs': {'pos': [0, 0, 0], 'depth': 18, 'radius': 7, 'radius_rounded': 2, 'style': 'cylinder', 'zz': 'center', 'mode': 'true'}},
 {'filename': 'test_3',
  'preview_rot': [45, 0, 25],
  'kwargs': {'pos': [0, 0, 0], 'depth': 12, 'radius_name': 'hole_radius_m6', 'radius_rounded': 1, 'zz': 'bottom', 'mode': 'true'}}]
```

## Sample-by-sample meaning

### Sample 1: `test_1.png`
- Intent: rounded OOBB sphere cylinder.
- preview_rot: `[45, 0, 25]`
- kwargs: `{"pos":[0,0,0],"depth":18,"radius":7,"radius_rounded":2,"zz":"center","mode":"true"}`
- Implementation rule: keep the sample values exactly as written.

### Sample 2: `test_2.png`
- Intent: same inputs switched back to normal cylinder output.
- preview_rot: `[45, 0, 25]`
- kwargs: `{"pos":[0,0,0],"depth":18,"radius":7,"radius_rounded":2,"style":"cylinder","zz":"center","mode":"true"}`
- Implementation rule: keep the sample values exactly as written.

### Sample 3: `test_3.png`
- Intent: mode-aware named radius with bottom anchoring.
- preview_rot: `[45, 0, 25]`
- kwargs: `{"pos":[0,0,0],"depth":12,"radius_name":"hole_radius_m6","radius_rounded":1,"zz":"bottom","mode":"true"}`
- Implementation rule: keep the sample values exactly as written.

## Folder-specific notes

- Notes: this component exists as a drop-in OOBB-level version of `sphere_cylinder`, with `style="cylinder"` available when a plain cylinder is needed.
