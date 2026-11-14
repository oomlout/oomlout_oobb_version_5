"""Resize existing project renders for the root README; never regenerate CAD.

Run: python presentation/scripts/build_project_thumbnails.py
Sibling checkouts supply local images. Public sources can be downloaded when a
checkout is absent; the four local projects require their source checkout.
"""

from pathlib import Path
import argparse
import base64
import hashlib
import io
import json
import urllib.request

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
SOURCES = [
    ("flat-plates", "oomlout_oobb_part_plate_version_5", "parts/oobb_part_plate_basic_5_width_5_height_3_depth/3dpr_presentation.png"),
    ("circle-plates", "oomlout_oobb_part_plate_circle_version_5", "parts/oobb_part_plate_circle_5_width_5_height_3_depth/3dpr_presentation.png"),
    ("l-plates", "oomlout_oobb_part_plate_l_version_5", "parts/oobb_part_plate_bracket_l_12_width_12_height_15_mm_depth/3dpr_presentation.png"),
    ("u-plates", "oomlout_oobb_part_plate_u_version_5", "parts/oobb_part_plate_u_10_width_10_height_15_mm_depth/3dpr_presentation.png"),
    ("90-degree-plates", "oomlout_oobb_part_plate_90_degree_version_5", "parts/oobb_part_plate_90_degree_1_width_10_height_14_mm_depth/3dpr_presentation.png"),
    ("plate-cutouts", "oomlout_oobb_part_plate_cutout_version_5", "parts/oobb_part_plate_cutout_30_diameter_cutout_1_multiple_buffer_middle_5_width_5_height_3_depth/3dpr.png"),
    ("bearing-holders", "oomlout_oobb_part_holder_bearing_version_5", "parts/oobb_part_holder_90_degree_bearing_606_bearing_size_3_width_3_height_12_depth/3dpr_presentation.png"),
    ("electronic-parts", "oomlout_oobb_electronic_version_5", "parts/oobb_part_electronic_spacer_big_plate_3_width_3_height_4_depth/3dpr_presentation.png"),
    ("gears", "oomlout_oobb_gear_version_5", "parts/oobb_part_gear_big_scale_1_diameter_10_teeth_standard_style_6_mm_depth/3dpr_presentation.png"),
    ("timing-pulleys", "oomlout_oobb_part_timing_pulley_version_5", "parts/oobb_part_timing_pulley_3_diameter_72_number_of_teeth_basic_9_depth_gt2/3dpr_presentation.png"),
    ("cycloidal-gearbox", "oomlout_oobb_part_motor_gearbox_cycloidal_version_5", "presentation/images/in-use.png"),
    ("motor-holders", "oomlout_oobb_part_holder_motor_version_5", "parts/oobb_part_holder_motor_gear_tt_5_width_3_height_23d5_depth_bearing_6704_version2/assembled_printed.png"),
    ("timing-belt-storage", "oomlout_oobb_part_timing_belt_storage_version_5", "parts/oobb_part_timing_belt_storage_reel_gt2_belt_size_11_diameter_6_depth/3dpr_presentation.png"),
    ("precision-screwdriver", "oomlout_oobb_tool_precision_screwdriver_version_5", "parts/tool_precision_screwdriver_version_1_bit_lock/3dpr_presentation.png"),
    ("captive-nut-plates", "oomlout_oobb_part_plate_captive_nut_version_5", "parts/oobb_part_plate_captive_nut_m6_basic_3_width_3_height_12_assembly_depth_base_9_depth/3dpr_presentation.png"),
]
LOCAL = {"motor-holders", "timing-belt-storage", "precision-screwdriver", "captive-nut-plates"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--projects-root", type=Path, default=ROOT.parent)
    args = parser.parse_args()
    out = ROOT / "presentation/images/projects"
    out.mkdir(parents=True, exist_ok=True)
    font = ImageFont.load_default(size=10)
    records = []
    for slug, repo, path in SOURCES:
        local = args.projects_root / repo / path
        url = f"https://raw.githubusercontent.com/oomlout/{repo}/main/{path}"
        if local.is_file():
            data = local.read_bytes()
        elif slug in LOCAL:
            raise FileNotFoundError(f"Local project image required: {local}")
        else:
            with urllib.request.urlopen(url, timeout=30) as response:
                data = response.read()
            # Some GitHub gateways return a contents-API envelope for raw URLs.
            if data.lstrip().startswith(b"{"):
                payload = json.loads(data)
                if payload.get("encoding") != "base64":
                    raise ValueError(f"Expected an image or base64 content: {url}")
                data = base64.b64decode(payload["content"])
        with Image.open(io.BytesIO(data)) as source:
            source.load()
            original = source.convert("RGB")
        small = original.copy()
        small.thumbnail((280, 180), Image.Resampling.LANCZOS)
        thumb = Image.new("RGB", (280, 210), "#f7f5f0")
        thumb.paste(small, ((280 - small.width) // 2, (180 - small.height) // 2))
        draw = ImageDraw.Draw(thumb)
        draw.text((8, 185), "AI-generated CAD illustration. Errors possible.", font=font, fill="#354547")
        target = out / f"{slug}.png"
        thumb.save(target, optimize=True)
        record = {
            "project": repo, "source_path": path,
            "source_url": None if slug in LOCAL else url,
            "source_sha256": hashlib.sha256(data).hexdigest(),
            "source_dimensions": list(original.size),
            "thumbnail": target.name,
            "thumbnail_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
            "thumbnail_dimensions": list(thumb.size),
        }
        if slug == "flat-plates":
            hero = original.copy()
            hero.thumbnail((960, 600), Image.Resampling.LANCZOS)
            hero_path = out / "plate-5x5x3.png"
            hero.save(hero_path, optimize=True)
            record["hero"] = hero_path.name
            record["hero_sha256"] = hashlib.sha256(hero_path.read_bytes()).hexdigest()
        records.append(record)
    (out / "sources.json").write_text(json.dumps({
        "description": "Existing CAD renders, downsampled for the project index. Full source frames retained; thumbnails add an AI notice. No geometry changes.",
        "command": "python presentation/scripts/build_project_thumbnails.py",
        "images": records,
    }, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(records)} thumbnails and one plate hero to {out}")


if __name__ == "__main__":
    main()
