# Test Samples

## Implementation Contract

Apply these instructions exactly in `working.py` for this folder. Do not shorten or reinterpret the steps.

1. Open `working.py` in this folder.
2. If `def test():` already exists, replace the whole function. If it does not exist, add a new `test()` at the end of the file after the existing public functions.
3. Add the imports shown in the code skeleton below inside `test()`.
4. Set `folder = os.path.dirname(os.path.abspath(__file__))`.
5. Set `test_dir = os.path.join(folder, "test")`.
6. Call `os.makedirs(test_dir, exist_ok=True)`.
7. Copy the exact `samples = ...` block from this file into `test()`.
8. For each sample, deep-copy the sample data before modifying it.
9. Normalize the return from `action(...)` into a list before rendering:
   - if the result is already a list, keep it unchanged
   - if the result is a single dict, wrap it as `[result]`
10. Do not adjust the camera. The only allowed view control is the `preview_rot` geometry rotation listed in this file.
11. Write matching `.scad` and `.png` files into the local `test` folder using each sample filename.
12. Return a `generated_files` list containing the PNG paths in render order.

### Exact code skeleton

```python
def test():
    import copy
    import os
    import opsc

    folder = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(folder, "test")
    os.makedirs(test_dir, exist_ok=True)

    samples = [
        # Paste the exact samples block from this TEST_SAMPLES.md here.
    ]

    generated_files = []

    for sample in samples:
        kwargs = copy.deepcopy(sample["kwargs"])
        result = action(**kwargs)
        if isinstance(result, dict) and "components" in result:
            components = copy.deepcopy(result["components"])
        elif isinstance(result, list):
            components = result
        else:
            components = [result]

        preview_rot = sample["preview_rot"]
        wrapped = components
        if preview_rot != [0, 0, 0]:
            wrapped = [{
                "type": "rotation",
                "typetype": "positive",
                "pos": [0, 0, 0],
                "rot": preview_rot,
                "objects": components,
            }]

        sample_dir = os.path.join(test_dir, sample["filename"])
        os.makedirs(sample_dir, exist_ok=True)
        scad_path = os.path.join(sample_dir, "working.scad")
        png_path = os.path.join(sample_dir, "image.png")

        opsc.opsc_make_object(
            scad_path,
            wrapped,
            mode="true",
            save_type="none",
            overwrite=True,
            render=True,
        )
        opsc.save_preview_images(scad_path, sample_dir)
        generated_files.append(png_path)

    return generated_files
```

### Exact samples block

```python
samples = [
    {
        "filename": "test_1",
        "preview_rot": [45, 0, 25],
        "kwargs": {"type": "positive", "bearing_size": "606", "clearance": 0, "pos": [0, 0, 0]},
    },
    {
        "filename": "test_2",
        "preview_rot": [45, 0, 25],
        "kwargs": {"type": "positive", "bearing_size": "6701", "clearance": 0, "pos": [0, 0, 0]},
    },
    {
        "filename": "test_3",
        "preview_rot": [45, 0, 25],
        "kwargs": {"type": "positive", "bearing_size": "MR104", "clearance": 0.5, "pos": [0, 0, 0]},
    },
]
```

