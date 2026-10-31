# Test Samples

## Implementation Contract

Apply these instructions exactly in `working.py` for this folder. Do not shorten or reinterpret the steps.

1. Open `working.py` in this folder.
2. If `def test():` already exists, replace the whole function. If it does not exist, add a new `test()` at the end of the file after the existing public functions.
3. Add the imports shown in the code skeleton below inside `test()`.
4. Set `folder = os.path.dirname(os.path.abspath(__file__))`.
5. Set `images_dir = os.path.join(folder, "images")`.
6. Call `os.makedirs(images_dir, exist_ok=True)`.
7. Copy the exact `samples = ...` block from this file into `test()`.
8. For each sample, deep-copy the sample data before modifying it.
9. Normalize the return from `action(...)` into a list before rendering:
   - if the result is already a list, keep it unchanged
   - if the result is a single dict, wrap it as `[result]`
10. Do not adjust the camera. The only allowed view control is the `preview_rot` geometry rotation listed in this file.
11. If a sample `kwargs` already contains its own `rot`, keep that value exactly as written and still apply `preview_rot` as the outer wrapper.
12. Write matching `.scad` and `.png` files into the local `images` folder using each sample filename.
13. Return a `generated_files` list containing the PNG paths in render order.

## Exact `samples` block to paste into `working.py`

```python
samples = [
    {
        "filename": "draft_0_degrees",
        "preview_rot": [60, 0, 25],
        "kwargs": {"pos": [0, 0, 0], "type": "positive", "size": [30, 20, 20], "radius": 5, "radius_rounded": 2, "draft_angle": 0},
    },
    {
        "filename": "draft_1_degree",
        "preview_rot": [60, 0, 25],
        "kwargs": {"pos": [0, 0, 0], "type": "positive", "size": [30, 20, 20], "radius": 5, "radius_rounded": 2, "draft_angle": 1},
    },
    {
        "filename": "draft_5_degrees",
        "preview_rot": [60, 0, 25],
        "kwargs": {"pos": [0, 0, 0], "type": "positive", "size": [30, 20, 20], "radius": 5, "radius_rounded": 2, "draft_angle": 5},
    },
]
```

## Sample-by-sample meaning

### Sample 1: `draft_0_degrees.png`
- Intent: undrafted reference geometry.
- preview_rot: `[60, 0, 25]`
- kwargs: `{"pos": [0, 0, 0], "type": "positive", "size": [30, 20, 20], "radius": 5, "radius_rounded": 2, "draft_angle": 0}`

### Sample 2: `draft_1_degree.png`
- Intent: default 1 degree draft, tapering inward toward the bottom.
- preview_rot: `[60, 0, 25]`
- kwargs: `{"pos": [0, 0, 0], "type": "positive", "size": [30, 20, 20], "radius": 5, "radius_rounded": 2, "draft_angle": 1}`

### Sample 3: `draft_5_degrees.png`
- Intent: exaggerated draft tapering inward toward the bottom to make the taper easy to see.
- preview_rot: `[60, 0, 25]`
- kwargs: `{"pos": [0, 0, 0], "type": "positive", "size": [30, 20, 20], "radius": 5, "radius_rounded": 2, "draft_angle": 5}`
