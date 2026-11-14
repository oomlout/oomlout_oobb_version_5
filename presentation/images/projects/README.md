# Project index images

These are downsampled copies of existing project CAD previews for the root
[README](../../../README.md). The main image is the 5 by 5 OOBB plate, 3 mm thick.
The user explicitly requested local thumbnails for every listed project.

The 15 thumbnails are 280 by 210 pixels, with the complete source frame fitted
above a readable AI-generated notice. The plate hero is 960 by 600 pixels.
No CAD geometry, camera view or source image is changed. The plate-cutout image
uses its existing yellow OpenSCAD preview; other projects retain their existing
render colours. These images do not establish physical fit or assembly validation.

Rebuild with Pillow installed:

```powershell
python presentation/scripts/build_project_thumbnails.py
```

The script normally reads sibling project checkouts. Use `--projects-root` to
select another parent directory. Missing public sources can be downloaded from
GitHub; the four local projects require their checkouts. Rebuilding may pick up
new upstream images, so review the results before publishing.

[sources.json](sources.json) records each source path, public URL where available,
source and thumbnail hashes, dimensions and the hero hash. Full-resolution source
images remain in their original projects.

Reviewed on 14 November 2026: all 15 thumbnails inspected together; root README
rendered at 1100 px and 390 px widths with all 16 images loading and no page
overflow. Local image links, Markdown anchors and manifest hashes passed.
Published project navigation is retained; local previews link to the generator
guide's checkout locations. Review screenshots are local working files under
`temporary/readme-review/`.
