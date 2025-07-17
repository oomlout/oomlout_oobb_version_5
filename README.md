# oomlout_oobb_version_4  
This repo is the messy code for generating parts.  
  
Generated parts can be found here  
https://github.com/oomlout/oomlout_oobb_version_4_generated_parts  

## More organized releases are available here:  
* 3D Printing Files -- https://github.com/oomlout/oomlout_oobb_release_3d_print  
* Laser Cutting Files -- https://github.com/oomlout/oomlout_oobb_release_laser_cut  

## Bundles of useful parts  
* Basic Plates -- https://github.com/oomlout/oomlout_oobe_bundle_plates_basic
* Alphabet Bunting -- https://github.com/oomlout/oomlout_oobb_bundle_bunting_alphabet
* Surface Mount Electronic Component Magazines -- https://github.com/oomlout/oomlout_oobb_bundle_smd_magazine
* OOBB Character Decorations -- https://github.com/oomlout/oomlout_oobb_bundle_decorations


## Testing

Install dependencies:
```bash
pip install -r requirements.txt
# clone the opsc helper library
git clone https://github.com/oomlout/oomlout_opsc_version_3 opsc
export PYTHONPATH=$PYTHONPATH:$(pwd)/opsc
```

Generate all test models:
```bash
python tests/generate_tests.py
```

When the outputs look correct, store them as the baseline:
```bash
python tests/save_baseline.py
```

To check for regressions later run:
```bash
python tests/compare_tests.py
```
