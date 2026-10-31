"""Gridfinity trays with mixed whole/half/quarter feet on one axis."""

import copy
import math
from pathlib import Path

from components.gridfinity_tray_raw import working as tray_raw


MODULE_DEFAULTS = copy.deepcopy(tray_raw.MODULE_DEFAULTS)
MODULE_DEFAULTS["efficient_floor"] = "on"
_WRAPPER_FILE = str(Path(__file__).with_name("gridfinity_tray_quarter_increment.scad"))


def define():
    description = copy.deepcopy(tray_raw.define())
    description.update(
        name="gridfinity_tray_quarter_increment",
        name_long="Gridfinity: Tray Quarter Increment",
        shape_aliases=["gridfinity_tray_quarter_increment"],
        description="Tray with whole, half and quarter bottom feet; quarter steps on one axis only.",
        notes=[
            "A 0.75 x 1 tray has 0.5 x 1 and 0.25 x 1 feet.",
            "The other axis supports whole and half units, including 0.25 x 0.5 feet.",
            "Feet use whole units first, then a half and/or quarter remainder.",
            "The efficient floor follows each foot by default; use efficient_floor='off' for a flat floor.",
            "Near/far grid alignment is supported. Sub-pitch and flat-base overrides are not used.",
            "The original gridfinity_tray_raw component is unchanged.",
        ],
    )
    for variable in description["variables"]:
        if variable["name"] == "efficient_floor":
            variable["default"] = '"on"'
    return description


def describe():
    return define()


def _units(value, pitch):
    # Match Gridfinity Extended: a nonzero mm entry overrides the unit entry.
    if isinstance(value, (list, tuple)) and len(value) == 2:
        return float(value[1]) / pitch if value[1] else float(value[0])
    return float(value)


def action(**kwargs):
    kwargs.setdefault("efficient_floor", MODULE_DEFAULTS["efficient_floor"])
    result = tray_raw.action(**kwargs)
    params = result["module_kwargs"]
    dimensions = [
        _units(params[key], params["pitch"][axis])
        for axis, key in enumerate(("gridfinity_width", "gridfinity_height"))
    ]
    quarter_axes = 0
    for value in dimensions:
        if not math.isfinite(value) or value <= 0 or not math.isclose(
            value * 4, round(value * 4), abs_tol=1e-7, rel_tol=0
        ):
            raise ValueError("Quarter-increment tray dimensions must be positive multiples of 0.25.")
        quarter_axes += round(value * 4) % 2
    if quarter_axes > 1:
        raise ValueError("Quarter increments are supported on only one axis per tray.")
    if any(params[key] not in ("near", "far") for key in ("align_grid_x", "align_grid_y")):
        raise ValueError("Quarter-increment feet require near or far grid alignment.")
    result.update(file=_WRAPPER_FILE, module="gridfinity_tray_quarter_increment")
    return result
