"""Reusable OOEB wire-holder clearances for 2.54 mm header hardware."""

import copy
import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)


# Absolute millimetres from the electronic project's wire plates. Hardware
# dimensions do not scale with the OOBB grid.
# (centre X, entry width, entry top Y, step Y, run width)
WIRE_CHANNELS = {
    "basic": (1.27, 5.62, 11.43, -2.54, 7.62),
    "power": (0.00, 3.08, 11.43, -2.54, 5.08),
    "motor": (0.00, 3.08, 10.16, 3.81, 5.08),
    "motor_stepper": (0.00, 8.16, 10.16, 3.81, 10.16),
    "i2c": (1.27, 8.16, 10.16, 3.81, 10.16),
}
WIRE_POCKET_LENGTH = 2.54 + 0.54
WIRE_POCKET_EXTRA_WIDTH = 2 * 2.54
WIRE_POCKET_FRONT_CLEARANCE = 6.18
WIRE_HOUSING_LENGTH = 14.0
# Extra clearance on each XY side of the header bar and inner housing.
WIRE_FIT_CLEARANCE = 0.2
WIRE_EXIT_NOTCH_TYPES = ("basic", "power", "i2c")
WIRE_EXIT_NOTCH_RADIUS = 1.5
WIRE_EXIT_NOTCH_GAP = 3


def describe():
    variables = [
        ("wire_type", "Connector: basic, power, motor, motor_stepper, or i2c.", "string", '"basic"'),
        ("polarizing_pin", "Include the polarizing pin clearance notch on basic, power and i2c exits.", "bool", True),
        ("plate", "Include a plain OOBB plate with the wire void; mounting holes belong to the calling project.", "bool", False),
        ("width", "Optional plate width in OOBB units.", "number", 3),
        ("height", "Height in OOBB units used to locate the front edge.", "number", 3),
        ("depth", "Host plate thickness in mm.", "number", 4),
        ("cutout_depth", "Depth of the housing run, header pocket and exit below the top surface, in mm.", "number", 2.8),
        ("front_y", "Override the front edge Y in local mm; defaults to the negative edge of height.", "number", ""),
        ("pos", "Origin at the centre of the host's bottom face, in mm.", "list", "[0,0,0]"),
        ("rot", "Rotate the whole wire feature about its local origin before placement.", "list", "[0,0,0]"),
        ("type", "Boolean polarity: defaults to negative for cutouts, positive with plate=True.", "string", ""),
        ("inclusion", "Render mode: all, 3dpr, laser, or true.", "string", '"all"'),
        ("m", "OpenSCAD modifier, e.g. #, %, *.", "string", '""'),
    ]
    return {
        "name": "oobb_wire",
        "name_long": "OOBB Electronic: Wire Holder",
        "description": "Wire-holder clearances for five 2.54 mm connector styles, with an optional plain plate.",
        "category": "OOBB Electronic Components",
        "shape_aliases": [],
        "returns": "List of geometry component dicts.",
        "variables": [dict(zip(("name", "description", "type", "default"), item)) for item in variables],
    }


def define():
    return describe()


def action(**kwargs):
    import oobb

    params = copy.deepcopy(kwargs)
    wire_type = params.get("wire_type", "basic")
    if wire_type not in WIRE_CHANNELS:
        raise ValueError(f"Unknown wire_type {wire_type!r}; choose from {', '.join(WIRE_CHANNELS)}")
    plate = params.get("plate", False)
    polarizing_pin = params.get("polarizing_pin", True)
    if not isinstance(plate, bool) or not isinstance(polarizing_pin, bool):
        raise ValueError("plate and polarizing_pin must be True or False")

    width = params.get("width", 3)
    height = params.get("height", 3)
    depth = params.get("depth", 4)
    cutout_depth = params.get("cutout_depth", 2.8)
    if width <= 0 or height <= 0 or depth <= 0 or not 0 < cutout_depth <= depth:
        raise ValueError("width, height and depth must be positive; cutout_depth must be > 0 and <= depth")

    front_y = params.get("front_y")
    if front_y is None:
        front_y = -(height * oobb.gv("osp") - oobb.gv("osp_minus")) / 2
    cx, entry_width, entry_top, step_y, run_width = WIRE_CHANNELS[wire_type]
    pocket_bottom = front_y + WIRE_POCKET_FRONT_CLEARANCE
    run_bottom = pocket_bottom + WIRE_POCKET_LENGTH
    if run_bottom >= step_y:
        raise ValueError("The front edge is too close to the entry; increase height or move front_y forward (more negative)")

    # Children are positive for a union of clearances, or negative inside an
    # optional plate. Grouping makes pos/rot apply to the complete feature.
    objects = []
    cut_type = "negative" if plate else "positive"

    def rect(x, y, size_x, size_y, z, size_z):
        objects.append({
            "type": cut_type, "shape": "cube",
            "size": [size_x, size_y, size_z],
            "pos": [x - size_x / 2, y - size_y / 2, z],
        })

    if plate:
        objects.extend(oobb.oe(shape="oobb_plate", type="positive", width=width,
                               height=height, depth=depth, pos=[0, 0, 0]))

    # Only the narrow entry passes through the host, with 1 mm overshoot.
    rect(cx, (entry_top + step_y) / 2, entry_width, entry_top - step_y, -1, depth + 2)
    # The Dupont housing needs 14 mm behind the header pocket regardless of
    # the host grid. Extend toward the entry, keeping the pocket/exit fixed.
    run_length = max(WIRE_HOUSING_LENGTH, step_y - run_bottom)
    pocket_z = depth - cutout_depth
    rect(cx, run_bottom + run_length / 2,
         run_width + 2 * WIRE_FIT_CLEARANCE, run_length + 2 * WIRE_FIT_CLEARANCE,
         pocket_z, cutout_depth + 1)

    if wire_type in ("motor", "motor_stepper"):
        exit_cx, exit_width = cx, run_width
    else:
        exit_cx, exit_width = cx - 1.27, run_width + 2.54
    rect(exit_cx, (run_bottom + pocket_bottom) / 2,
         exit_width + WIRE_POCKET_EXTRA_WIDTH + 2 * WIRE_FIT_CLEARANCE,
         run_bottom - pocket_bottom + 2 * WIRE_FIT_CLEARANCE,
         pocket_z, cutout_depth + 1)
    rect(exit_cx, pocket_bottom - 10, exit_width, 20, pocket_z, cutout_depth + 1)

    if polarizing_pin and wire_type in WIRE_EXIT_NOTCH_TYPES:
        objects.append({
            "type": cut_type, "shape": "cylinder",
            "r": WIRE_EXIT_NOTCH_RADIUS, "h": cutout_depth + 1,
            "pos": [exit_cx - exit_width / 2 - WIRE_EXIT_NOTCH_GAP - WIRE_EXIT_NOTCH_RADIUS,
                    front_y, pocket_z],
        })

    result = {
        "type": "rotation",
        "typetype": params.get("type", "positive" if plate else "negative"),
        "pos": params.get("pos", [0, 0, 0]),
        "rot": params.get("rot", [params.get("rot_x", 0), params.get("rot_y", 0), params.get("rot_z", 0)]),
        "objects": objects,
        "inclusion": params.get("inclusion", "all"),
        "m": params.get("m", ""),
    }
    if "rot_shift" in params:
        result["rot_shift"] = params["rot_shift"]
    return [result]


def test():
    """Generate one plain-plate preview per wire style for the library browser."""
    import opsc

    generated_files = []
    for wire_type in WIRE_CHANNELS:
        folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test", wire_type)
        os.makedirs(folder, exist_ok=True)
        filename = os.path.join(folder, "working.scad")
        opsc.opsc_make_object(filename, action(wire_type=wire_type, plate=True),
                              mode="3dpr", save_type="none", overwrite=True)
        opsc.save_preview_images(filename, folder)
        generated_files.append(os.path.join(folder, "image.png"))
    return generated_files


if __name__ == "__main__":
    test()
