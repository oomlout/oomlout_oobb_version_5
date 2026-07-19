# Test Samples

## Exact `samples` block to paste into `working.py`

```python
samples = [
    {
        "filename": "test_1",
        "preview_rot": [65, 0, 25],
        "kwargs": {"type": "positive", "file": "icon.png", "width": 60, "depth": 1, "pos": [0, 0, 0]},
    },
    {
        "filename": "test_2",
        "preview_rot": [65, 0, 25],
        "kwargs": {"type": "positive", "file": "icon.png", "height": 35, "depth": 1.5, "zz": "center", "pos": [0, 0, 0]},
    },
    {
        "filename": "test_3",
        "preview_rot": [65, 0, 25],
        "kwargs": {"type": "positive", "file": "icon.png", "width": 70, "height": 35, "depth": 1, "pos": [0, 0, 0]},
    },
]
```

## Sample-by-sample meaning

### Sample 1: `test_1.png`
- Intent: square icon surface scaled from width only, preserving the image aspect ratio.
- preview_rot: `[65, 0, 25]`
- kwargs: `{"type":"positive","file":"icon.png","width":60,"depth":1,"pos":[0,0,0]}`
- Implementation rule: resize the source image to 1000 pixels wide before calculating millimeter scale, then use the default `slice_bottom=True` to subtract a slicing cube. With `invert=True`, slice from the top.

### Sample 2: `test_2.png`
- Intent: icon surface scaled from height only, preserving the image aspect ratio and centered on Z.
- preview_rot: `[65, 0, 25]`
- kwargs: `{"type":"positive","file":"icon.png","height":35,"depth":1.5,"zz":"center","pos":[0,0,0]}`
- Implementation rule: derive width from the normalized image aspect ratio.

### Sample 3: `test_3.png`
- Intent: forced non-proportional scaling when both width and height are provided.
- preview_rot: `[65, 0, 25]`
- kwargs: `{"type":"positive","file":"icon.png","width":70,"height":35,"depth":1,"pos":[0,0,0]}`
- Implementation rule: use explicit width and height exactly, even when that changes the source aspect ratio.

## Folder-specific notes

- Notes: `oobb_surface` includes `icon.png` as a local documentation sample image and writes a normalized 1000-pixel-wide PNG beside each generated SCAD file. The generated SCAD references that copied PNG by filename only.
