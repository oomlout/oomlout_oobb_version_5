# Test Samples

## Exact `samples` block to paste into `working.py`

```python
samples = [{'filename': 'test_1',
  'preview_rot': [45, 0, 25],
  'kwargs': {'type': 'positive', 'r': 8, 'h': 20, 'radius_rounded': 2, 'pos': [0, 0, 0]}},
 {'filename': 'test_2',
  'preview_rot': [45, 0, 25],
  'kwargs': {'type': 'positive', 'diameter': 18, 'depth': 12, 'radius_rounded': 3, 'pos': [0, 0, 0]}},
 {'filename': 'test_3',
  'preview_rot': [45, 0, 25],
  'kwargs': {'type': 'positive', 'r': 8, 'h': 20, 'radius_rounded': 2, 'center': True, 'pos': [0, 0, 0]}}]
```

## Sample-by-sample meaning

### Sample 1: `test_1.png`
- Intent: rounded cylinder using the normal `r` and `h` cylinder keys.
- preview_rot: `[45, 0, 25]`
- kwargs: `{"type":"positive","r":8,"h":20,"radius_rounded":2,"pos":[0,0,0]}`
- Implementation rule: keep the sample values exactly as written.

### Sample 2: `test_2.png`
- Intent: rounded cylinder using `diameter` and `depth` aliases.
- preview_rot: `[45, 0, 25]`
- kwargs: `{"type":"positive","diameter":18,"depth":12,"radius_rounded":3,"pos":[0,0,0]}`
- Implementation rule: keep the sample values exactly as written.

### Sample 3: `test_3.png`
- Intent: centered rounded cylinder matching OpenSCAD cylinder `center=True` behaviour.
- preview_rot: `[45, 0, 25]`
- kwargs: `{"type":"positive","r":8,"h":20,"radius_rounded":2,"center":true,"pos":[0,0,0]}`
- Implementation rule: keep the sample values exactly as written.

## Folder-specific notes

- Notes: show the rounded top and bottom outside edges clearly.
