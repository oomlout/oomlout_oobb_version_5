import copy
import os

from components.withering_bvu_logo import working as _square_badge

_COMPONENT_ROOT = os.path.dirname(os.path.abspath(__file__))
_SCAD_LOGO = os.path.join(_COMPONENT_ROOT, "image_scad.svg")
_NAME = "withering_root_logo"
_CACHE_NAME = "withering_root_logo.svg"

d = {}


def describe():
    global d
    d = copy.deepcopy(_square_badge.describe())
    d["name"] = _NAME
    d["name_long"] = "Withering ROOT Elder Care Logo"
    d["description"] = (
        "Rounded-square ROOT elder-care badge with the SVG regions subtracted "
        "from the top face for engraving or colour inlay."
    )
    d["shape_aliases"] = [_NAME, "withuering_root_logo"]
    return d


def define():
    if not d:
        describe()
    return copy.deepcopy(d)


def action(**kwargs):
    result = _square_badge.action(**copy.deepcopy(kwargs))
    badge = result[0]["objects"][0]
    badge["shape"] = _NAME
    badge["file"] = kwargs.get("file", kwargs.get("image", _SCAD_LOGO))
    return result


def render(params):
    return _square_badge.render(
        params,
        _logo_file=_SCAD_LOGO,
        _cache_name=_CACHE_NAME,
        _error_name=_NAME,
    )
