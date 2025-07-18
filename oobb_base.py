"""Utilities for creating and manipulating OOBB parts.

This module provides a collection of helper functions that are used by
other scripts in this repository to generate models and helper files.
The original code grew very organically and ended up rather messy.
This file attempts to organise the most commonly used helpers in a
single place with a little more structure and inline documentation so
that debugging and future development is easier.
"""

from oobb_get_items_base import *  # noqa: F401,F403  (imported for side effects)

import copy
import json
import os

import oobb
import oobb_get_items_base
import oobb_get_items_oobb
import oobb_get_items_other
import oobb_get_items_test


def get_thing_from_dict(thing_dict):
    """Return a thing instance based on the dictionary description.

    The helper modules contain many ``get_<type>`` functions.  This
    function looks up the appropriate constructor based on ``thing_dict``
    and returns the created object.

    Parameters
    ----------
    thing_dict : dict
        Dictionary describing the object.  At minimum it requires a
        ``"type"`` key.
    """

    full_object = thing_dict.get("full_object", False)

    try:
        func = getattr(oobb_get_items_oobb, f"get_{thing_dict['type']}")
    except AttributeError:
        try:
            func = getattr(oobb_get_items_other, f"get_{thing_dict['type']}")
        except AttributeError:
            func = getattr(oobb_get_items_test, f"get_{thing_dict['type']}")

    return func(**thing_dict)

    pass


# Location where generated parts are stored.  Adjust if your checkout uses a
# different path.
THINGS_FOLDER = "C:\\gh\\oomlout_oobb_version_4_generated_parts\\parts"


# base functions
def get_default_thing(**kwargs):
    """Construct the base data dictionary for a new part.

    Parameters are passed in via ``kwargs``.  The resulting dictionary
    contains standard keys used throughout the project such as ``id``,
    ``description``, dimensions and calculated helper values.  Only a
    subset of the monster original implementation is documented here but
    hopefully the comments make the intent clearer.
    """

    thing: dict = {}
    extra = kwargs.get("extra", "")
    typ = kwargs["type"]
    type_string = typ.replace("_", " ")
    width = kwargs.get("width", "0")
    height = kwargs.get("height", "0")
    thickness = kwargs.get("thickness", "0")
    try:
        thing.update({"description": f"{type_string} {width}x{height}x{thickness}"})
    except:
        thing.update({"description": f"{type_string}"})

    var_names = [
        "type",
        "width",
        "height",
        "diameter",
        "thickness",
        "radius_name",
        "depth",
        "radius_hole",
        "width_mounting",
        "name",
        "bearing_name",
        "bearing",
        "oring_type",
        "extra",
        "shaft",
    ]
    zfill_values = ["width", "height", "thickness", "depth", "diameter"]
    acronyms = {
        "width": "",
        "height": "",
        "diameter": "",
        "thickness": "",
        "depth": "",
        "size": "",
        "type": "",
        "radius_hole": "rh",
        "radius_name": "",
        "width_mounting": "mo",
        "height_mounting": "hm",
        "name": "nm",
        "bearing_name": "",
        "bearing": "",
        "oring_type": "or",
        "extra": "ex",
        "shaft": "sh",
    }

    if type == "test":
        var_names.append("radius_name")
        acronyms.update({"radius_name": "rn"})
        var_names.append("shape")
        acronyms.update({"shape": "sh"})
        var_names.append("style")
        acronyms.update({"style": "st"})

    deets = {}
    for var in var_names:
        deets[var] = {}

        # if zfill
        if var in zfill_values:
            val = kwargs.get(var, "")
            if isinstance(val, list):
                for i in range(0, len(val)):
                    val[i] = str(val[i]).zfill(2)
                val = "_".join(val)
                deets[var].update({"value": val})
            else:
                if val != "":
                    deets[var].update({"value": str(val).zfill(2)})
                else:
                    deets[var].update({"value": kwargs.get(val, "")})
        else:
            deets[var].update({"value": kwargs.get(var, "")})
        deets[var].update({"acronym": acronyms[var]})
        value_string = deets[var]["value"]
        # print(value_string)
        # if it's a list
        if type(value_string) == list:
            value_string = "_".join(value_string)

        if deets[var]["acronym"] != "":
            deets[var]["str"] = f"_{deets[var]['acronym']}_{value_string}"
        else:
            deets[var]["str"] = f"_{value_string}"

    id = kwargs.get("size", "")
    for var in deets:
        if deets[var]["value"] != "":
            if deets[var]["value"] != "":
                id += deets[var]["str"]
    id = id.replace(".", "d")
    # print(id)
    extra_test = str(kwargs.get("extra", ""))
    if "servo_standard" in extra_test:
        pass

    thing.update({"id": id})
    thing.update({"type": f"{typ}"})
    try:
        thing.update({"type_oobb": f"{type_dict[typ]}"})
    except:
        pass

    for var in var_names:
        try:
            thing.update({var: kwargs[var]})
        except:
            pass
    try:
        thing.update({"width_mm": kwargs["width"] * ob.gv("osp") - ob.gv("osp_minus")})
    except:
        pass
    try:
        if thickness != "":
            thing.update({"thickness_mm": kwargs["thickness"]})
    except:
        pass
    try:
        thing.update({"height_mm": kwargs["height"] * ob.gv("osp") - ob.gv("osp_minus")})
    except:
        pass
    thing.update({"components": []})
    thing.update({"components_string": []})
    thing.update({"components_objects": []})

    ##make folder
    # if not os.path.exists(folder):
    #    os.makedirs(folder)

    # adding oomp id
    if True:
        part = thing
        size = part["type"]  # different in oomp

        attributes = ["width", "height", "diameter", "thickness"]
        description_main = ""
        for attribute in attributes:
            test_value = part.get(attribute, "")
            # if it's a list
            if isinstance(test_value, list):
                attribute_new = ""
                for value in test_value:
                    attribute_new += f"{value}_"
                test_value = attribute_new[:-1]
            if test_value != "":
                if description_main != "":
                    description_main += "_"
                attribute_name = attribute
                if attribute == "thickness":
                    attribute_name = "mm_depth"
                description_main += f"{test_value}_{attribute_name}"
                description_main = description_main.replace(".", "_")

        # remove anything after "ex_" in the description
        string_extra = ""
        tests = ["bearing", "shaft", "extra", "bearing_name", "radius_name", "depth", "oring_type"]
        for test in tests:
            if test in part:
                deet = part.get(test, "")
                # if it's a list
                if isinstance(deet, list):
                    attribute_new = ""
                    for value in deet:
                        attribute_new += f"{value}_"
                    deet = attribute_new[:-1]

                if deet != "":
                    if string_extra != "":
                        string_extra += "_"
                    string_extra += f"{deet}_{test}"
        description_extra = string_extra

        part_details = {}
        part_details["classification"] = "oobb"
        part_details["type"] = "part"
        part_details["size"] = size
        part_details["color"] = ""

        part_details["description_main"] = description_main
        part_details["description_extra"] = description_extra
        part_details["manufacturer"] = ""
        part_details["part_number"] = ""
        part_details["short_name"] = ""

        part_details["link_redirect"] = (
            f"https://github.com/oomlout/oomlout_oobb_version_4_generated_parts/tree/main/parts/{part['id']}"
        )
        navigate_link = (
            f"{part_details['classification']}/"
            f"{part_details['type']}/"
            f"{part_details['size']}/"
            f"{part_details['description_main']}"
        )
        if part_details["description_extra"] != "":
            navigate_link += f"/{part_details['description_extra']}"
        part_details["link_main"] = (
            "https://github.com/oomlout/oomlout_oobb_version_4_generated_parts/"
            f"tree/main/navigation_oomp/{navigate_link}/part"
        )

        thing.update(part_details)

        id_parts = [
            "classification",
            "type",
            "size",
            "color",
            "description_main",
            "description_extra",
            "manufacturer",
            "part_number",
        ]
        id = ""
        for id_part in id_parts:
            value = part_details.get(id_part, "")
            if value != "":
                id += f"{part[id_part]}_"
        id = id[:-1]
        id = id.replace(".0_", "_")
        id = id.replace(".", "d")
        part_details["id"] = id
        thing.update(part_details)

        name = id.replace("_", " ").title()
        name = name.replace("Mm", "mm")
        thing.update({"name": name})

        short_name = name
        short_name = short_name.replace("Oobb Part ", "")
        short_name = short_name.replace(" Width ", "x")
        short_name = short_name.replace(" Height ", "x")
        short_name = short_name.replace(" Diameter ", "x")
        short_name = short_name.replace(" Thickness ", "x")
        short_name = short_name.replace("mm Depth ", " ")
        short_name = short_name.replace("mm Depth", "")
        short_name = short_name.replace("  ", " ")
        short_name = short_name.replace("  ", " ")
        # max length 20 characters
        length_max = 40
        if len(short_name) > length_max:
            # split at space
            short_name = short_name.split(" ")
            short_name_working = ""
            for word in short_name:
                if len(short_name_working) + len(word) < length_max:
                    short_name_working += word + " "
                else:
                    break
            short_name_working = short_name_working.strip()
            short_name = short_name_working

        thing.update({"name_short": short_name})

    # deciding folder
    if True:
        folder = f"{THINGS_FOLDER}\\{id}"
        thing.update({"folder": folder})
        if not os.path.exists(folder):
            os.makedirs(folder)

    # dump thing to working.yaml
    import yaml

    with open(f"{folder}/working.yaml", "w") as outfile:
        yaml.dump(thing, outfile, indent=4)

    if "caliper_digital" in str(extra):
        pass

    return thing


def get_comment(comment, type="p", **kwargs):
    """Create a text comment as a list of OOBB components."""
    kwargs["comment"] = comment
    kwargs["type"] = type
    m = kwargs.get("m", "*")
    pos = kwargs.get("pos", [0, 0, 0])
    pos = copy.deepcopy(pos)
    line_length = kwargs.get("line_length", 30)
    comment_shift_line = kwargs.get("comment_shift_line", 0)
    shift_line = 7
    pos[1] = pos[1] + shift_line + comment_shift_line
    return_value = []

    # add \n to comment every line_length characters if no \n
    if "\n" not in comment:
        comment = "\n".join(
            [comment[i : i + line_length] for i in range(0, len(comment), line_length)]
        )

    # split comment by \n
    comment_list = comment.split("\n")

    pos_line = copy.deepcopy(pos)
    # move y up line count shift_line
    pos_line[1] = pos_line[1] + ((len(comment_list) - 1) * shift_line)
    # add COMMENT to element 0
    comment_list[0] = f"COMMENT {comment_list[0]}"
    for comment in comment_list:
        p3 = copy.deepcopy(kwargs)
        p3["s"] = "text"
        p3["text"] = comment
        p3["depth"] = 1
        p3["pos"] = copy.deepcopy(pos_line)
        p3["size"] = 4.5
        p3["center"] = True
        p3["m"] = m
        p3["color"] = "gray"
        p3["font"] = "Arial:style=Bold"
        p3.pop("objects", "")

        if comment != "":
            return_value.extend(oobb_base.oobb_easy(**p3))
            pos_line[1] = pos_line[1] - shift_line

    return return_value

def set_variable(name, value, mode=""):
    """Store a variable in the global variable store."""
    if mode:
        name = f"{name}_{mode}"
    oobb.variables.update({name: value})


def gv(name, mode=""):
    """Convenience wrapper for :func:`get_variable`."""
    return get_variable(name, mode)


def get_variable(name, mode=""):
    """Retrieve a value from :mod:`oobb`'s variable store."""
    if mode:
        name = f"{name}_{mode}"
    rv = oobb.variables[name]
    return rv


def get_hole_pos(x, y, wid, hei, size="oobb"):
    """Return the physical (x, y) position for a grid hole."""
    sp = gv("osp")
    if size == "oobe":
        sp = gv("osp") / 2

    x_mm = -(wid - 1) * sp / 2 + (x - 1) * sp
    y_mm = -(hei - 1) * sp / 2 + (y - 1) * sp
    return x_mm, y_mm


def add_thing(thing):
    """Add an object to the global ``oobb.things`` dictionary."""
    oobb.things.update({thing["id"]: thing})


def dump(mode="json"):
    """Persist all known things and variables to disk."""
    print(f"dumping {mode}")
    if mode == "json":
        with open("things.json", "w") as outfile:
            json.dump(oobb.things, outfile)
        with open("variables.json", "w") as outfile:
            json.dump(oobb.variables, outfile)
    elif mode == "pickle":
        import pickle

        # create temporary directory
        if not os.path.exists("temporary"):
            os.makedirs("temporary")
        with open("temporary/things.pickle", "wb") as outfile:
            pickle.dump(oobb.things, outfile)
        with open("temporary/variables.pickle", "wb") as outfile:
            pickle.dump(oobb.variables, outfile)
    elif mode == "folder":
        for thing in oobb.things:
            # print a single dot with no new line
            print(".", end="")
            filename = f"{THINGS_FOLDER}/{thing}/details.json"
            if not os.path.exists(os.path.dirname(filename)):
                os.makedirs(os.path.dirname(filename))
            with open(filename, "w") as outfile:
                json.dump(oobb.things[thing], outfile, indent=4)
            # dump to json.yaml
            import yaml

            filename = f"{THINGS_FOLDER}/{thing}/details.yaml"
            with open(filename, "w") as outfile:
                yaml.dump(oobb.things[thing], outfile, indent=4)


def load(mode="json"):
    """Load previously stored things/variables from disk."""
    if mode == "json":
        with open("things.json") as json_file:
            oobb.things = json.load(json_file)
        with open("variables.json") as json_file:
            variables = json.load(json_file)
    elif mode == "folder":
        # load all the details.json files from the fodlers in things directory
        for thing in os.listdir(f"{THINGS_FOLDER}"):
            try:
                with open(f"{THINGS_FOLDER}/{thing}/details.json") as json_file:
                    oobb.things.update({thing: json.load(json_file)})
            except FileNotFoundError:
                pass


def build_things(save_type="none", overwrite=True, filter="", modes=["3dpr", "laser", "true"]):
    """Build all things that match the given filter."""
    # turn filter into an array if its a string
    if type(filter) == str:
        filter = [filter]
    for f in filter:
        for thing in oobb.things:
            if f in thing:
                print(f"building {thing}")
                build_thing(thing, save_type, overwrite, modes=modes)


def build_thing(thing, save_type="all", overwrite=True, modes=["3dpr", "laser", "true"]):
    """Render a single thing in the given modes."""

    if type(modes) != list:
        modes = [modes]
    if "all" in modes:
        modes = ["3dpr", "laser", "true"]
    for mode in modes:
        depth = oobb.things[thing].get("depth_mm", oobb.things[thing].get("thickness_mm", 3))
        height = oobb.things[thing].get("height_mm", 100)
        layers = depth / 3
        tilediff = height + 10
        start = 1.5
        if layers != 1:
            start = 1.5 - (layers / 2) * 3
        if "bunting" in thing:
            start = 0.5
        # opsc.opsc_make_object(f'things/{thing}/{mode}.scad', oobb.things[thing]["components"], mode=mode, save_type=save_type, overwrite=overwrite, layers=layers, tilediff=tilediff, start=start)
        filename = f"{THINGS_FOLDER}/{thing}/{mode}.scad"
        opsc.opsc_make_object(
            filename,
            oobb.things[thing]["components"],
            mode=mode,
            save_type=save_type,
            overwrite=overwrite,
            layers=layers,
            tilediff=tilediff,
            start=start,
        )
        # make the description file
        with open(f"{THINGS_FOLDER}/{thing}/{mode}.txt", "w") as outfile:
            component_strings = oobb.things[thing]["components_string"]
            for component in component_strings:
                outfile.write(f"{component}\n")
        # make the json file
        with open(f"{THINGS_FOLDER}/{thing}/{mode}.json", "w") as outfile:
            json.dump(oobb.things[thing]["components_objects"], outfile, indent=4)

        # make the yaml file
        import yaml

        with open(f"{THINGS_FOLDER}/{thing}/{mode}.yaml", "w") as outfile:
            yaml.dump(oobb.things[thing]["components_objects"], outfile, indent=4)


def build_thing_filename(
    thing, save_type="all", overwrite=True, filename="", depth=3, height=200, render=True
):
    """Build ``thing`` directly to ``filename``."""
    modes = ["3dpr", "laser", "true"]
    for mode in modes:
        depth = depth
        height = height
        layers = depth / 3
        tilediff = height + 10
        start = 1.5
        if layers != 1:
            start = 1.5 - (layers / 2) * 3
        opsc.opsc_make_object(
            f"{filename}{mode}.scad",
            thing,
            mode=mode,
            save_type=save_type,
            overwrite=overwrite,
            layers=layers,
            tilediff=tilediff,
            start=start,
            render=render,
        )


def oobb_easy_get_string(**kwargs):
    """Serialise the provided parameters into a short string."""
    return_value = ""
    p3 = copy.deepcopy(kwargs)

    if p3["pos"] == [0, 0, 0]:
        p3.pop("pos", "")
    p3.pop("m", "")
    p3.pop("inclusion", "")

    order = ["shape", "type", "radius_name", "depth", "pos"]
    value_pairs = []
    for key in order:
        if key in p3:
            value_pairs.append([key, p3[key]])
    for key in p3:
        if key not in order:
            value_pairs.append([key, p3[key]])

    for pair in value_pairs:
        key = pair[0]
        value = pair[1]
        value = str(p3[key])
        # remove [ , and ]
        value = value.replace("[", "")
        value = value.replace("]", "")
        value = value.replace(",", "_")
        value = value.replace(" ", "")
        if value != "":
            return_value += f"{value}_{key}_"

    return return_value[:-1].lower()


def oobb_easy_string(**kwargs):
    """Wrapper calling :func:`oobb_easy` after parsing a string."""
    return oobb_easy(**oobb_easy_string_params(**kwargs))


def oobb_easy_string_params(**kwargs):
    """Parse a convenience item string into parameter dictionary."""
    item = kwargs.get("item", "")
    # example
    # oobb_screw_socket_cap_m3_12_mm_depth
    input_string = item

    variable_names = [
        "_radius_name",
        "_depth",
        "_pos",
        "_width",
        "_height",
        "_extra",
        "_nut",
        "_clearance",
        "_bearing",
        "_type",
        "_holes",
        "_slots",
        "_inserts",
        "_insertion_cone",
        "_overhang",
        "_inclusion",
        "_rot",
        "_thickness",
    ]

    result_dict = {}

    # shape is first make it the string in front of "_shape"
    # to deal with bearing being in shape name
    shape = input_string.split("_shape")[0]
    result_dict["_shape"] = {}
    result_dict["_shape"]["value"] = shape
    input_string = input_string.replace(shape + "_shape", "")

    i = 0
    while i < len(input_string):
        for variable in variable_names:
            if input_string.startswith(variable, i):
                start = i
                end = i + len(variable)
                before = input_string[:start]
                after = input_string[end:]
                result_dict[variable] = {"before": before, "after": after}
                i = end

        i += 1
    variable_indexes = {"": 0}
    for variable in variable_names:
        # get variable index
        variable_index = input_string.find(variable)
        # if it's in the string store it
        if variable_index != -1:
            variable_indexes[variable] = input_string.find(variable)

    # Remove sections that pertain to other variables in the "before" section
    for current_variable in variable_names:
        # get the index the variable occurs at in input_string
        index = input_string.find(current_variable)
        # find the variable whose index is closest to the current variable but also less
        closest_variable = ""
        for variable in variable_names:
            try:
                if (
                    variable_indexes[variable] < index
                    and variable_indexes[variable] > variable_indexes[closest_variable]
                ):
                    closest_variable = variable
            except KeyError:
                pass  # variable not in string

        # value is the string between the two variables
        try:
            value = input_string[variable_indexes[closest_variable] : index]
            # remove the variable name
            value = value.replace(closest_variable, "")
            # remove leading and trailing _
            value = value.strip("_")
            result_dict[current_variable]["value"] = value
        except KeyError:
            pass
            # print (f"KeyError: {closest_variable} not found in {variable_indexes}")

    # load into kwargs
    p3 = copy.deepcopy(kwargs)
    p3["shape"] = result_dict["_shape"]["value"]
    for variable in variable_names:
        if variable in result_dict:
            value = result_dict[variable]["value"]
            # remove _mm
            value = value.replace("_mm", "")
            p3[variable] = value

    p3["_type"] = p3.get("_type", "p")

    # float convert
    convert_to_floats = ["_depth", "_width", "_height"]
    for key in convert_to_floats:
        if key in p3:
            p3[key] = float(p3[key])
    if "_pos" in p3:
        pos_split = p3["_pos"].split("_")
        p3["_pos"] = [float(pos_split[0]), float(pos_split[1]), float(pos_split[2])]
    if "_rot" in p3:
        pos_split = p3["_rot"].split("_")
        p3["_rot"] = [float(pos_split[0]), float(pos_split[1]), float(pos_split[2])]

    # go through p3 nd remove the leading _ from each key
    for key in list(p3.keys()):
        if key.startswith("_"):
            p3[key[1:]] = p3[key]
            del p3[key]

    return p3


def append_full(thing, **kwargs):
    """Append items to ``thing`` handling the many convenience options."""
    # test for objects if so iterate
    objects_raw = kwargs.get("objects", [])
    # objects might be a list of list of lists unpop it to be a single list of dicts do it recursively

    objects = []
    for object in objects_raw:
        if type(object) == list:
            for object_2 in object:
                if type(object_2) == list:
                    for object_3 in object_2:
                        if type(object_3) == list:
                            for object_4 in object_3:
                                if type(object_4) == list:
                                    for object_5 in object_4:
                                        if type(object_5) == list:
                                            for object_6 in object_5:
                                                objects.append(object_6)
                                        else:
                                            objects.append(object_5)
                                else:
                                    objects.append(object_4)
                        else:
                            objects.append(object_3)
                else:
                    objects.append(object_2)
        else:
            objects.append(object)

    m = kwargs.get("m", "")
    if objects != []:
        for object in objects:
            object["m"] = m
            append_full(thing, **object)
        return
    # add loop for multiple pos
    kwargs_original = copy.deepcopy(kwargs)
    poss = kwargs.get("pos", [0, 0, 0])
    if poss == []:
        poss = [0, 0, 0]
    if type(poss[0]) != list:
        poss = [poss]

    # add loop for multipe shapes
    shapes = kwargs.get("shape", "")
    if type(shapes) != list:
        shapes = [shapes]

    rot_shifts = kwargs.get("rot_shift", None)
    # test if rot_shifts is a list of lists
    if type(rot_shifts) == list:
        if type(rot_shifts[0]) == list:
            rot_shifts = rot_shifts
        else:
            rot_shifts = [rot_shifts]
    else:
        rot_shifts = [rot_shifts]

    for shape in shapes:
        for pos in poss:
            for rot_shift in rot_shifts:
                kwargs = copy.deepcopy(kwargs_original)
                kwargs["pos"] = pos
                kwargs["shape"] = shape
                if rot_shift is not None:
                    kwargs["rot_shift"] = rot_shift
                else:
                    kwargs.pop("rot_shift", None)

                # thing = kwargs.get("thing", "")
                comment = kwargs.get("comment", "")
                comment_display = kwargs.get("comment_display", False)
                m = kwargs.get("m", "")
                item = kwargs.get("item", "")

                p3 = copy.deepcopy(kwargs)
                if item != "":  # item means we are defining by string
                    string_params = oobb_easy_string_params(item=item)
                    p3.update(string_params)

                # add yaml to components
                ths = thing["components_objects"]
                p4 = copy.deepcopy(p3)
                p4.pop("comment", None)
                p4.pop("thing", None)
                p4.pop("item", None)
                ths.append(p4)

                # descriptino to txt
                ths = thing["components_string"]
                p4 = copy.deepcopy(p3)
                p4.pop("comment", None)
                p4.pop("thing", None)
                p4.pop("item", None)
                p4.pop("objects", "")
                string_to_add = oobb_easy_get_string(**p4)
                ths.append(string_to_add)

                # add item to components
                th = thing["components"]

                # comment
                if comment != "":
                    p4 = copy.deepcopy(p3)
                    p4.pop("rot", "")
                    p4.pop("type", None)
                    p4["m"] = "*"
                    if comment_display:
                        p4["m"] = m
                    pass
                    # th.extend(get_comment(**p4))

                # description
                p4 = copy.deepcopy(p3)
                p4["comment"] = f"description {string_to_add}\n"
                p4["m"] = "*"
                # th.extend(get_comment(**p4))

                p4 = copy.deepcopy(p3)
                th.extend(oobb_easy(**p4))

                pass


def oe(**kwargs):
    """Alias for :func:`oobb_easy`."""
    return oobb_easy(**kwargs)


def oobb_easy(**kwargs):
    """Main helper used by many item generators."""
    # add loop for multiple pos
    kwargs_original = copy.deepcopy(kwargs)
    poss = kwargs.get("pos", [0, 0, 0])
    shapes = kwargs.get("shape", "")
    # if poss isn't a list of lists make it one
    if type(poss[0]) != list:
        poss = [poss]
    if type(shapes) != list:
        shapes = [shapes]

    return_value_2 = []
    for shape in shapes:
        for pos in poss:
            kwargs = copy.deepcopy(kwargs_original)
            kwargs["pos"] = pos
            kwargs["shape"] = shape
            # sort out shortcut names
            key_mappings = {"type": "t", "shape": "s", "radius_name": "rn"}

            for new_key, old_key in key_mappings.items():
                value = kwargs.get(old_key)
                if value is not None:
                    kwargs[new_key] = value
                    del kwargs[old_key]

            shape = kwargs.get("shape", "")

            if "oobb" in shape or "oobe" in shape:
                # if its an oobb_plat then call get_oobb_plate
                shape = kwargs["shape"]
                if shape == "oobb_pl":
                    return_value = []
                    holes = kwargs.get("holes", True)
                    return_value.append(get_oobb_plate(**kwargs))
                    if holes:
                        return_value.extend(get_oobb_holes(**kwargs))
                    return_value_2.append(return_value)
                if shape == "oobe_pl":
                    return_value = []
                    return_value.append(get_oobe_plate(**kwargs))
                    return_value.extend(get_oobe_holes(**kwargs))
                    return_value_2.append(return_value)
                else:
                    # Call the function dynamically using its string name
                    shape = shape.replace("_extra_mm", "")
                    shape = shape.replace("_spacer_10_mm", "")
                    func = globals()[f"get_{shape}"]
                    return_value_2.append(func(**kwargs))
            else:
                return_value = opsc.opsc_easy(**kwargs)
                # if return value is a dict
                if type(return_value) == dict:
                    return_value = [return_value]
                return_value_2.append(return_value)
    return return_value_2


def oobb_easy_array(**kwargs):
    """Create an array of objects using :func:`oobb_easy`."""
    for i in range(0, 3):
        kwargs["repeats"].append(1)
        kwargs["pos_start"].append(0)
        kwargs["shift_arr"].append(0)
    return_objects = []

    repeats = kwargs["repeats"]
    for x in range(0, int(repeats[0])):
        for y in range(0, int(repeats[1])):
            for z in range(0, int(repeats[2])):
                pos = [0, 0, 0]
                pos[0] = kwargs["pos_start"][0] + x * kwargs["shift_arr"][0]
                pos[1] = kwargs["pos_start"][1] + y * kwargs["shift_arr"][1]
                pos[2] = kwargs["pos_start"][2] + z * kwargs["shift_arr"][2]
                kwargs.update({"pos": pos})
                return_objects.append(oobb_easy(**kwargs))
    return return_objects


# shifting routines
def shift(thing, shift):
    """Shift all component positions by the given offset."""
    # iterate through by index
    mode = "components"

    if "components" in thing:
        return_thing = thing
        thing = thing["components"]
        mode = "thing"
    # pop things out of deeper lists
    # do it 8 times
    for i in range(0, 8):
        thing_2 = []
        for th in thing:
            if type(th) == list:
                thing_2.extend(th)
            else:
                thing_2.append(th)
        thing = thing_2

        # iterate through each component
    for component in thing:
        component["pos"] = copy.deepcopy(component["pos"])
        component["pos"][0] += shift[0]
        component["pos"][1] += shift[1]
        component["pos"][2] += shift[2]
    if mode == "components":
        return thing
    else:
        return return_thing


def highlight(thing):
    """Set display mode to highlight a thing."""
    add_all(thing, "m", "#")
    return thing


def color_set(thing, color):
    """Apply ``color`` to every component in ``thing``."""
    th = thing
    if "components" in thing:
        th = thing["components"]
    add_all(th, "color", color)
    return thing


def remove_if(thing, name, value):
    """Remove components equal to ``value`` for key ``name``."""
    # thing2 = copy.deepcopy(thing)
    # for component in thing2:
    #    things = component
    #    if type(things) != list:
    #        things = [things]
    #    for component in things:
    #        if component.get(name,"") == value:
    #            thing.remove(component)
    return thing


def add_all(thing, name, value):
    """Add ``name=value`` to all components recursively."""
    # component might be a list of list do it recursively
    if type(thing) == list:
        if "type" not in thing:
            for component in thing:
                add_all(component, name, value)
    else:
        thing.update({name: value})
    return thing


def inclusion(thing, include):
    """Filter components based on ``include`` tag."""
    thing2 = []
    for component in thing:
        inclusion = component.get("inclusion", "all")
        if include in inclusion or inclusion == "all":
            component["inclusion"] = include
            thing2.append(component)
            pass
        else:
            pass
    return thing


######### convenience functions #########


def get_oobb_hole_with_text(**kwargs):
    """Convenience wrapper combining a hole and a text label."""

    depth = kwargs.get("depth", 3)
    radius = kwargs.get("radius", 1)
    # offset_text = kwargs.get("offset_text", -10)
    offset_text = -radius - 1
    font_size = kwargs.get("font_size", 14)
    pos = kwargs.get("pos", [0, 0, 0])
    kwargs["pos"] = pos
    return_value = []
    p2 = copy.deepcopy(kwargs)
    return_value.extend(get_oobb_hole(**kwargs))
    p2 = copy.deepcopy(kwargs)
    p2["pos"][0] = p2["pos"][0] + offset_text
    # shift z up by depth
    height_extrusion = 0.3
    p2["pos"][2] = p2["pos"][2] + depth - height_extrusion
    p2["height"] = height_extrusion
    p2["m"] = "#"
    # set halign center and valign center
    p2["halign"] = "right"
    p2["valign"] = "center"
    # deja vu sans mono as font
    p2["font"] = "DejaVu Sans Mono"
    # size equals font size
    p2["size"] = font_size
    return_value.extend(get_oobb_text(**p2))

    return return_value
