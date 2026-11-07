"""GT2 and HTD5M clamshell pulleys, built from discoverable OOBB components.

Local origin is the belt centre. Print layouts put both mating faces
on Z=0. Dimensions are millimetres; diameter is only an OOBB catalogue size.
"""

import copy
import csv
from pathlib import Path
import math


def describe():
    variables = []
    variables.append({"name": "belt_profile", "type": "string", "default": "gt2", "description": "gt2 (2 mm pitch) or htd5m (5 mm pitch)."})
    variables.append({"name": "number_of_teeth", "type": "number", "default": 60, "description": "Integer tooth count, at least 16."})
    variables.append({"name": "depth", "type": "number", "default": 6, "description": "Nominal belt width, not assembled thickness."})
    variables.append({"name": "style", "type": "string", "default": "basic", "description": "basic, idler_bearing_606, mechanical_coupling_underneath, mechanical_coupling_recessed."})
    variables.append({"name": "layout", "type": "string", "default": "print", "description": "print, assembled, exploded, lower, upper, section."})
    variables.append({"name": "coupler", "type": "dict", "default": {}, "description": "Flange dimensions copied from the OOMP mechanical coupler CSV."})
    variables.append({"name": "coupler_mount_rotation", "type": "number", "default": 45, "description": "Diagonal flange bolt pattern, leaving the orthogonal grub-screw access paths clear."})
    variables.append({"name": "coupler_grub_screw_from_flange", "type": "number", "default": 5, "description": "Grub-screw centre measured along the barrel from the flange top face; accessed from +X."})
    variables.append({"name": "bearing_radial_clearance", "type": "number", "default": 0.15, "description": "Radial allowance on the 17 mm 606 outer race."})
    variables.append({"name": "oobb_holes", "type": "bool", "default": True, "description": "Available M6 holes on the 15 mm grid and intervening M3 holes on the 7.5 mm grid."})
    variables.append({"name": "oobb_hole_minimum_web", "type": "number", "default": 0.3, "description": "Minimum material between grid holes and the tooth roots or hardware envelopes, in mm."})
    variables.append({"name": "joining_rotation", "type": "number", "default": 45, "description": "Joining pattern offset: recessed couplers default to 0 degrees on the axes, other styles to 45 degrees."})
    variables.append({"name": "pos", "type": "list", "default": [0, 0, 0], "description": "Position after layout and rotation."})
    variables.append({"name": "rot", "type": "list", "default": [0, 0, 0], "description": "Whole-component rotation in degrees."})
    return {
        "name": "oobb_timing_pulley",
        "name_long": "OOBB Motion: GT2 and HTD5M Timing Pulley",
        "description": "Two screw-together halves, retained 606 bearing or measured flange coupler; small basic pulleys are one piece.",
        "category": "OOBB Motion",
        "shape_aliases": ["timing_pulley"],
        "returns": "List of geometry component dictionaries.",
        "variables": variables,
    }


def define():
    return describe()


def number(name, value, minimum=0, positive=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number")
    if value < minimum or (positive and value == minimum):
        raise ValueError(f"{name} must be {'greater than' if positive else 'at least'} {minimum}")
    return float(value)


def get_oobb_hole_layout(values):
    """Keep a centred OOBB/OOBE lattice; never rotate the mounting grid.

    The mode-aware OOBB hole primitive performs the cuts. This helper only
    filters positions against the actual pulley and hardware, because a plain
    circular oobb_holes array cannot reserve these non-circular features.
    """
    import oobb

    positions = []
    excluded = []
    if not values["oobb_holes"]:
        return positions, excluded
    half_spacing = oobb.gv("osp") / 2
    extent = math.floor(values["root_radius"] / half_spacing)
    web = values["oobb_hole_minimum_web"]
    centre_radius = values["centre_keepout"]
    if values["style"].startswith("mechanical_coupling"):
        # A through screw must also clear the real metal flange projection.
        centre_radius = max(centre_radius, values["coupler"]["diameter_baseplate"] / 2)

    for grid_x in range(-extent, extent + 1):
        for grid_y in range(-extent, extent + 1):
            if grid_x == 0 and grid_y == 0:
                # The existing shaft/bearing/coupler geometry owns the centre.
                continue
            position = [grid_x * half_spacing, grid_y * half_spacing]
            distance = math.hypot(*position)
            if distance > values["root_radius"]:
                continue
            radius_name = "m3"
            if grid_x % 2 == 0 and grid_y % 2 == 0:
                radius_name = "m6"
            radius = max(oobb.gv("hole_radius_" + radius_name, mode) for mode in ["3dpr", "true", "laser"])
            hole = {"position": position, "radius_name": radius_name, "radius": radius}
            reason = ""
            if distance + radius + web > values["root_radius"]:
                reason = "tooth_root"
            elif distance - radius - web < centre_radius:
                reason = "centre_feature"
            elif any(math.dist(position, joining) < radius + values["joining_head_radius"] + web for joining in values["joining_positions"]):
                reason = "joining_fastener"
            elif any(math.dist(position, mount) < radius + values["mounting_head_radius"] + web for mount in values["mounting_positions"]):
                reason = "coupler_fastener"
            elif values["allen_key_access_diameter"] and radius_name != "m6":
                port_clearance = values["allen_key_access_diameter"] / 2 + radius + web
                if position[0] >= 0 and abs(position[1]) < port_clearance:
                    reason = "allen_key_window"
            if reason:
                hole["reason"] = reason
                excluded.append(hole)
            else:
                positions.append(hole)
    return positions, excluded


def dimensions(**kwargs):
    import oobb

    belt_profile = kwargs.get("belt_profile", "gt2")
    if belt_profile not in ["gt2", "htd5m"]:
        raise ValueError(f"Unknown timing pulley belt profile: {belt_profile}")
    teeth = number("number_of_teeth", kwargs.get("number_of_teeth", 60), 16)
    if int(teeth) != teeth:
        raise ValueError("number_of_teeth must be an integer")
    depth = number("depth", kwargs.get("depth", 6), 6)
    style = kwargs.get("style", "basic")
    styles = ["basic", "idler_bearing_606", "mechanical_coupling_underneath", "mechanical_coupling_recessed"]
    if style not in styles:
        raise ValueError(f"Unknown timing pulley style: {style}")
    layout = kwargs.get("layout", "print")
    if layout not in ["print", "assembled", "exploded", "lower", "upper", "section"]:
        raise ValueError(f"Unknown timing pulley layout: {layout}")

    belt_clearance = number("belt_clearance", kwargs.get("belt_clearance", 0.5))
    flange_depth = number("flange_depth", kwargs.get("flange_depth", 1), positive=True)
    flange_extension = number("flange_extension", kwargs.get("flange_extension", 1), positive=True)
    minimum_web = number("minimum_web", kwargs.get("minimum_web", 1), positive=True)
    radial_clearance = number("bearing_radial_clearance", kwargs.get("bearing_radial_clearance", 0.15))
    axial_clearance = number("bearing_axial_clearance", kwargs.get("bearing_axial_clearance", 0.2))
    coupler_clearance = number("coupler_radial_clearance", kwargs.get("coupler_radial_clearance", 0.2))
    coupler_axial_clearance = number("coupler_axial_clearance", kwargs.get("coupler_axial_clearance", 0.2))
    print_gap = number("print_gap", kwargs.get("print_gap", 10), 1)
    oobb_holes = kwargs.get("oobb_holes", True)
    if not isinstance(oobb_holes, bool):
        raise ValueError("oobb_holes must be a boolean")
    oobb_hole_minimum_web = number("oobb_hole_minimum_web", kwargs.get("oobb_hole_minimum_web", 0.3), positive=True)
    joining_rotation = number("joining_rotation", kwargs.get("joining_rotation", 0 if style == "mechanical_coupling_recessed" else 45))
    allowed_rotations = [0, 45] if style == "mechanical_coupling_recessed" else [45]
    if joining_rotation % 90 not in allowed_rotations:
        raise ValueError("joining_rotation must be 45 degrees modulo 90, or 0 for a recessed coupler")
    width_extra = number("additional_tooth_width", kwargs.get("additional_tooth_width", 0.2))
    depth_extra = number("additional_tooth_depth", kwargs.get("additional_tooth_depth", 0))
    if width_extra > 0.5 or depth_extra > 0.3:
        raise ValueError("Tooth allowances exceed the supported profile range")

    pitch = 5 if belt_profile == "htd5m" else 2
    pitch_diameter = teeth * pitch / math.pi
    outside_radius = pitch_diameter / 2 - (0.5715 if belt_profile == "htd5m" else 0.254)
    # Conservative circle inside every groove of the inherited GT2 polygon.
    root_radius = outside_radius - 0.9 - depth_extra
    if belt_profile == "htd5m":
        # Match the inherited HTD polygon placement and allowance scaling.
        # The deepest polygon point is 2.198511 mm, rounded up to 2.199.
        groove_origin = math.sqrt(outside_radius ** 2 - ((3.781 + width_extra) / 2) ** 2)
        root_radius = groove_origin - 2.199 - depth_extra
    flange_radius = outside_radius + flange_extension
    belt_depth = depth + belt_clearance
    belt_center = 0
    total_depth = belt_depth + flange_depth * 2
    bottom = -total_depth / 2
    top = total_depth / 2
    shaft_diameter = number("shaft_diameter", kwargs.get("shaft_diameter", 6.5), positive=True)
    centre_keepout = shaft_diameter / 2
    split = teeth >= 40
    coupler = copy.deepcopy(kwargs.get("coupler", {}))
    mounting_positions = []
    mounting_radius_name = "m3"
    mounting_head_radius = oobb.gv("screw_countersunk_radius_m3", "3dpr")
    access_diameter = 0
    access_z = 0
    access_open_top = False
    split_z = 0
    coupler_mount_rotation = 0
    shared_joining_fasteners = style == "mechanical_coupling_recessed"

    if style == "idler_bearing_606":
        split = True
        # Read the actual 606 row rather than borrowing a different bearing's
        # width. The OOBB 600-series table specifies 6 x 17 x 6 mm.
        bearing_path = Path(oobb.__file__).parent / "data" / "bearing" / "bearing_600.csv"
        with bearing_path.open(encoding="utf-8-sig", newline="") as handle:
            bearing_row = next(row for row in csv.DictReader(handle) if row["Size"] == "606")
        bearing_inner = float(bearing_row["Inner Dimension"])
        bearing_outer = float(bearing_row["Outer Dimension"])
        bearing_depth = float(bearing_row["Width OPEN"])
        centre_keepout = bearing_outer / 2 + radial_clearance
        shaft_diameter = bearing_inner + 6  # Outer-race lips clear both inner races.
        if bearing_depth + axial_clearance + 2 * minimum_web > total_depth:
            total_depth = bearing_depth + axial_clearance + 2 * minimum_web
            flange_depth = (total_depth - belt_depth) / 2
            bottom = -total_depth / 2
            top = total_depth / 2
        if centre_keepout - shaft_diameter / 2 < minimum_web:
            raise ValueError("Bearing radial relief leaves no retaining lip")

    if style.startswith("mechanical_coupling"):
        split = True
        required = ["bore", "diameter_baseplate", "diameter_cylindrical", "diameter_screw_grub", "diameter_screw_hole", "height_total", "height_cylindrical", "distance_diagonal_screw_hole", "flange_thickness", "count_screw_hole", "dimension_d"]
        for key in required:
            if key not in coupler:
                raise ValueError(f"coupler is missing {key}")
            number(f"coupler.{key}", coupler[key], positive=True)
        if coupler["count_screw_hole"] != 4:
            raise ValueError("Only four-hole flange couplers are supported")
        if abs(coupler["height_total"] - coupler["height_cylindrical"] - coupler["flange_thickness"]) > 0.01:
            raise ValueError("Coupler flange and barrel heights must sum to height_total")
        if coupler["diameter_cylindrical"] <= coupler["bore"]:
            raise ValueError("Coupler barrel must enclose the shaft bore")
        shaft_diameter = coupler["bore"] + 0.5
        centre_keepout = shaft_diameter / 2
        if coupler["diameter_screw_hole"] == 4:
            mounting_radius_name = "m4"
            mounting_head_radius = oobb.gv("screw_countersunk_radius_m4", "3dpr")
        bolt_radius = coupler["distance_diagonal_screw_hole"] / 2
        if style == "mechanical_coupling_recessed":
            coupler_mount_rotation = number("coupler_mount_rotation", kwargs.get("coupler_mount_rotation", 45))
            if coupler_mount_rotation % 90 != 45:
                raise ValueError("Recessed coupler mounting bolts must be diagonal to keep the Allen-key paths clear")
        for angle in [coupler_mount_rotation, coupler_mount_rotation + 90, coupler_mount_rotation + 180, coupler_mount_rotation + 270]:
            radians = math.radians(angle)
            mounting_positions.append([bolt_radius * math.cos(radians), bolt_radius * math.sin(radians)])
        if bolt_radius + mounting_head_radius + minimum_web > root_radius:
            raise ValueError("Pulley is too small for the coupler mounting screws")
        if style == "mechanical_coupling_underneath":
            if coupler["diameter_baseplate"] / 2 + minimum_web > root_radius:
                raise ValueError("Pulley is too small to support the underside flange")
        else:
            # The normal belt channel and flanges determine pulley thickness.
            # Locate the barrel axially, not by thickening the pulley around it.
            grub_from_flange = number("coupler_grub_screw_from_flange", kwargs.get("coupler_grub_screw_from_flange", coupler["height_cylindrical"] / 2), positive=True)
            if grub_from_flange >= coupler["height_cylindrical"]:
                raise ValueError("Grub-screw centre must lie within the coupler barrel")
            # Recess the complete flange and the nuts beneath it. The barrel
            # may project above the pulley.
            coupler_flange_top = bottom + coupler["flange_thickness"] + oobb.gv("nut_depth_" + mounting_radius_name, "3dpr")
            coupler_flange_bottom = coupler_flange_top - coupler["flange_thickness"]
            coupler_top = coupler_flange_top + coupler["height_cylindrical"]
            shaft_diameter = coupler["diameter_cylindrical"] + 2 * coupler_clearance
            centre_keepout = shaft_diameter / 2
            access_z = coupler_flange_top + grub_from_flange
            access_diameter = number("allen_key_access_diameter", kwargs.get("allen_key_access_diameter", 4 if mounting_radius_name == "m3" else 5), 3)
            access_open_top = access_z - access_diameter / 2 < top <= access_z + access_diameter / 2
            if coupler_flange_top + oobb.gv("screw_countersunk_height_" + mounting_radius_name, "3dpr") > top:
                raise ValueError("Recessed flange leaves insufficient depth for countersunk screws")
            # Shared screws can clamp the lower half only if a sound plastic
            # roof remains between the flange and the central mating plane.
            shared_joining_fasteners = coupler_flange_top + minimum_web <= split_z
            if not shared_joining_fasteners:
                # Put the flange seating shoulder on the mating face instead
                # of leaving a thin ledge across the split. Both halves still
                # print mating-face-down, with the shoulder on the bed.
                split_z = coupler_flange_top

    head_radius = max(oobb.gv("screw_countersunk_radius_m3", "3dpr"), oobb.gv("nut_radius_m3", "3dpr"))
    if belt_profile == "htd5m" and style == "basic":
        # HTD teeth are larger: select a clamshell by available material,
        # rather than applying the legacy GT2 tooth-count threshold.
        required_radius = max(7.5, centre_keepout + head_radius + minimum_web)
        split = required_radius + head_radius + minimum_web <= root_radius
    joining_positions = []
    if shared_joining_fasteners:
        # The four coupler screws are also the four clamshell screws.
        joining_positions = copy.deepcopy(mounting_positions)
        joining_rotation = coupler_mount_rotation
    else:
        joining_radius = max(7.5, centre_keepout + head_radius + minimum_web)
        if style.startswith("mechanical_coupling"):
            joining_radius = max(joining_radius,
                                 coupler["diameter_baseplate"] / 2 + coupler_clearance + head_radius + minimum_web,
                                 coupler["distance_diagonal_screw_hole"] / 2 + mounting_head_radius + head_radius + minimum_web + 0.01)
        if split:
            if joining_radius + head_radius + minimum_web > root_radius:
                raise ValueError("Pulley is too small for the centre feature and M3 clamshell screws")
            for angle in [joining_rotation, joining_rotation + 90, joining_rotation + 180, joining_rotation + 270]:
                radians = math.radians(angle)
                position = [joining_radius * math.cos(radians), joining_radius * math.sin(radians)]
                for mount in mounting_positions:
                    if math.dist(position, mount) < head_radius + mounting_head_radius + minimum_web:
                        raise ValueError("Clamshell and coupler fasteners overlap; use a larger pulley")
                joining_positions.append(position)
        elif centre_keepout + minimum_web > root_radius:
            raise ValueError("Shaft bore leaves insufficient material at the tooth roots")

    result = {}
    result["belt_profile"] = belt_profile
    result["pitch"] = pitch
    result["number_of_teeth"] = int(teeth)
    result["depth"] = depth
    result["style"] = style
    result["layout"] = layout
    result["pitch_diameter"] = pitch_diameter
    result["outside_radius"] = outside_radius
    result["root_radius"] = root_radius
    result["flange_radius"] = flange_radius
    result["flange_depth"] = flange_depth
    result["belt_depth"] = belt_depth
    result["belt_center"] = belt_center
    result["belt_bottom"] = belt_center - belt_depth / 2
    result["belt_top"] = belt_center + belt_depth / 2
    result["assembled_depth"] = top - bottom
    result["bottom"] = bottom
    result["top"] = top
    result["split"] = split
    result["split_z"] = split_z
    result["lower_half_depth"] = split_z - bottom
    result["upper_half_depth"] = top - split_z
    result["joining_positions"] = joining_positions
    result["joining_rotation"] = joining_rotation
    result["joining_head_radius"] = head_radius
    result["mounting_positions"] = mounting_positions
    result["mounting_radius_name"] = mounting_radius_name
    result["mounting_head_radius"] = mounting_head_radius
    result["shaft_diameter"] = shaft_diameter
    result["centre_hole_diameter"] = shaft_diameter
    result["shared_joining_fasteners"] = shared_joining_fasteners
    result["centre_keepout"] = centre_keepout
    result["minimum_web"] = minimum_web
    result["coupler"] = coupler
    result["coupler_radial_clearance"] = coupler_clearance
    result["coupler_axial_clearance"] = coupler_axial_clearance
    result["coupler_mount_rotation"] = coupler_mount_rotation
    if style == "mechanical_coupling_recessed":
        result["coupler_bottom"] = coupler_flange_bottom
        result["coupler_top"] = coupler_top
        result["coupler_flange_top"] = coupler_flange_top
        result["coupler_flange_center"] = (coupler_flange_bottom + coupler_flange_top) / 2
        result["coupler_grub_screw_from_flange"] = grub_from_flange
        result["coupler_shaft_bore_diameter"] = coupler["bore"]
        result["coupler_flange_recess_depth"] = max(0, coupler_flange_top - bottom)
        result["coupler_fastener_nut_bottom"] = coupler_flange_bottom - oobb.gv("nut_depth_" + mounting_radius_name, "3dpr")
        result["coupler_fastener_depth"] = top - result["coupler_fastener_nut_bottom"]
        result["allen_key_access_open_top"] = access_open_top
    result["bearing_radial_clearance"] = radial_clearance
    result["bearing_axial_clearance"] = axial_clearance
    if style == "idler_bearing_606":
        result["bearing_inner_diameter"] = bearing_inner
        result["bearing_outer_diameter"] = bearing_outer
        result["bearing_depth"] = bearing_depth
    result["allen_key_access_diameter"] = access_diameter
    result["allen_key_access_z"] = access_z
    result["print_spacing"] = flange_radius * 2 + print_gap
    result["additional_tooth_width"] = width_extra
    result["additional_tooth_depth"] = depth_extra
    result["oobb_holes"] = oobb_holes
    result["oobb_hole_minimum_web"] = oobb_hole_minimum_web
    result["oobb_hole_positions"], result["oobb_holes_excluded"] = get_oobb_hole_layout(result)
    return result


def group(objects, pos=None, rot=None, typ="positive"):
    return {"type": "rotation", "typetype": typ, "pos": pos or [0, 0, 0], "rot": rot or [0, 0, 0], "objects": copy.deepcopy(objects)}


def coupler_reference(**kwargs):
    """Non-printing metal reference for assembly and cutaway review layouts.

    Flange/barrel/bore/mounts use the measured CSV. The user-specified grub
    position is halfway along the 10 mm barrel, above the central seam.
    Production action() never includes this hardware geometry.
    """
    import oobb

    values = dimensions(**kwargs)
    if values["style"] != "mechanical_coupling_recessed":
        raise ValueError("Metal reference is for the recessed coupling style")
    coupler = values["coupler"]
    metal = []

    def append(shape, typ, **details):
        details["shape"] = shape
        details["type"] = typ
        details.setdefault("pos", [0, 0, 0])
        metal.extend(oobb.oobb_easy(**details))

    append("oobb_cylinder", "positive", radius=coupler["diameter_baseplate"] / 2, depth=coupler["flange_thickness"], pos=[0, 0, values["coupler_flange_center"]], color="Silver")
    append("oobb_cylinder", "positive", radius=coupler["diameter_cylindrical"] / 2, depth=coupler["height_cylindrical"], zz="bottom", pos=[0, 0, values["coupler_flange_top"]], color="Silver")
    append("oobb_hole", "negative", radius=coupler["bore"] / 2, depth=coupler["height_total"] + 2, pos=[0, 0, values["coupler_bottom"] - 1])
    for position in values["mounting_positions"]:
        append("oobb_hole", "negative", radius=coupler["diameter_screw_hole"] / 2, depth=coupler["flange_thickness"] + 2, pos=[position[0], position[1], values["coupler_bottom"] - 1])
    for rotation in [[0, 90, 0], [-90, 0, 0]]:
        append("oobb_hole", "negative", radius=coupler["diameter_screw_grub"] / 2, depth=coupler["diameter_cylindrical"], pos=[0, 0, values["allen_key_access_z"]], rot=rotation)
    assembled_metal = group(metal)
    screws = []
    screw_radius = coupler["diameter_screw_grub"] / 2 - 0.05
    # Inset the flat screw end so its edges fit inside the curved barrel.
    screw_end = math.sqrt((coupler["diameter_cylindrical"] / 2) ** 2 - screw_radius ** 2)
    for position, rotation in [([screw_end - 2.5, 0, values["allen_key_access_z"]], [0, 90, 0]), ([0, screw_end - 2.5, values["allen_key_access_z"]], [-90, 0, 0])]:
        screw = oobb.oobb_easy(shape="oobb_cylinder", type="positive", radius=screw_radius, depth=2.5, zz="bottom", pos=[0, 0, 0], color="DimGray")
        screws.append(group(screw, pos=position, rot=rotation))
    return [group([assembled_metal] + screws, pos=kwargs.get("pos", [0, 0, 0]), rot=kwargs.get("rot", [0, 0, 0]))]


def _assembled(parameters):
    import oobb

    values = parameters
    objects = []

    def append(shape, typ, **details):
        details["shape"] = shape
        details["type"] = typ
        details.setdefault("pos", [0, 0, 0])
        objects.extend(oobb.oobb_easy(**details))

    append("pulley_" + values["belt_profile"], "positive", number_of_teeth=values["number_of_teeth"], depth=values["belt_depth"], pos=[0, 0, values["belt_bottom"]], additional_tooth_width=values["additional_tooth_width"], additional_tooth_depth=values["additional_tooth_depth"])
    for z in [values["bottom"], values["belt_top"]]:
        append("oobb_cylinder", "positive", radius=values["flange_radius"], depth=values["flange_depth"], zz="bottom", pos=[0, 0, z])

    if values["style"] == "mechanical_coupling_recessed":
        coupler = values["coupler"]
        if values["coupler_flange_recess_depth"] > 0:
            # A shallow seat is needed only when the flange overlaps the normal
            # lower face. Never change the belt channel or outer body thickness.
            append("oobb_cylinder", "negative", radius=coupler["diameter_baseplate"] / 2 + values["coupler_radial_clearance"], depth=values["coupler_flange_recess_depth"] + 1, zz="bottom", pos=[0, 0, values["bottom"] - 1])
        # One cylindrical +X clearance, including where it breaks through
        # the top face. Never replace its circular section with a box.
        access_radius = values["allen_key_access_diameter"] / 2
        append("oobb_cylinder", "negative", radius=access_radius, depth=values["flange_radius"] + 2, zz="bottom", pos=[0, 0, values["allen_key_access_z"]], rot=[0, 90, 0])

    append("oobb_hole", "negative", radius=values["shaft_diameter"] / 2, depth=values["top"] - values["bottom"] + 2, pos=[0, 0, values["bottom"] - 1])

    for hole in values["oobb_hole_positions"]:
        append("oobb_hole", "negative", radius_name=hole["radius_name"], depth=values["top"] - values["bottom"] + 2, pos=[hole["position"][0], hole["position"][1], values["bottom"] - 1])

    if values["style"] == "idler_bearing_606":
        append("oobb_cylinder", "negative", radius=values["bearing_outer_diameter"] / 2 + values["bearing_radial_clearance"], depth=values["bearing_depth"] + values["bearing_axial_clearance"])

    # Screws span the complete outer faces of the pulley body.
    flange_top = values["top"]
    screw_depth = flange_top - values["bottom"]
    for index, position in enumerate([] if values["shared_joining_fasteners"] else values["joining_positions"]):
        z = flange_top
        depth = screw_depth
        rotation = [0, 0, 0]
        if index % 2:
            z = values["bottom"]
            rotation = [180, 0, 0]
        if values["style"] == "mechanical_coupling_recessed" and position[0] > 0 and abs(position[1]) < 1e-6:
            # The +X joining screw crosses the keyway: seat its head below
            # the tool envelope and open a straight well down to that seat.
            z = min(flange_top, values["allen_key_access_z"] - values["allen_key_access_diameter"] / 2)
            depth = z - values["bottom"]
            rotation = [0, 0, 0]
            append("oobb_cylinder", "negative", radius=oobb.gv("screw_countersunk_radius_m3", "3dpr"), depth=flange_top - z + 1, zz="bottom", pos=[position[0], position[1], z])
        append("screw_countersunk", "negative", radius_name="m3", depth=depth, nut=True, overhang=True, pos=[position[0], position[1], z], rot=rotation)

    if values["style"].startswith("mechanical_coupling"):
        for position in values["mounting_positions"]:
            if values["style"] == "mechanical_coupling_underneath":
                # Screw heads stay outside, below the commercial flange. Nuts
                # are captured at the opposite plastic face; no assumed threads.
                head_z = values["bottom"] - values["coupler"]["flange_thickness"]
                append("screw_countersunk", "negative", radius_name=values["mounting_radius_name"], depth=flange_top - head_z, nut=True, overhang=True, pos=[position[0], position[1], head_z], rot=[180, 0, 0])
            else:
                # Four screws mount the commercial flange. Separate outer
                # screws join the halves when the lower roof is too thin.
                append("screw_countersunk", "negative", radius_name=values["mounting_radius_name"], depth=values["coupler_fastener_depth"], nut=True, overhang=True, pos=[position[0], position[1], flange_top])
    return objects


def action(**kwargs):
    import oobb

    values = dimensions(**kwargs)
    objects = _assembled(values)
    layout = values["layout"]
    span = values["flange_radius"] * 2 + 20

    def half(upper):
        clipped = copy.deepcopy(objects)
        z = values["split_z"] - span if upper else values["split_z"]
        clipped.extend(oobb.oobb_easy(shape="cube", type="negative", size=[span * 2, span * 2, span], pos=[-span, -span, z]))
        return clipped

    if layout == "assembled":
        result = objects
    elif layout == "section":
        result = objects
        result.extend(oobb.oobb_easy(shape="cube", type="negative", size=[span, span * 2, span * 2], pos=[0, -span, -span]))
    elif not values["split"]:
        result = [group(objects, pos=[0, 0, -values["bottom"]])]
    elif layout == "lower":
        result = half(False)
    elif layout == "upper":
        result = half(True)
    elif layout == "exploded":
        result = [group(half(False), pos=[0, 0, -5]), group(half(True), pos=[0, 0, 5])]
    else:
        result = []
        result.append(group(half(False), pos=[0, 0, values["split_z"]], rot=[180, 0, 0]))
        result.append(group(half(True), pos=[values["print_spacing"], 0, -values["split_z"]]))

    return [group(result, pos=kwargs.get("pos", [0, 0, 0]), rot=kwargs.get("rot", [0, 0, 0]), typ=kwargs.get("type", "positive"))]


def test():
    """Generate a representative print layout through the standard component API."""
    import os
    import opsc

    folder = os.path.join(os.path.dirname(__file__), "test", "clamshell_60_teeth")
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, "working.scad")
    opsc.opsc_make_object(path, action(number_of_teeth=60), mode="3dpr", save_type="none")
    return [path]
