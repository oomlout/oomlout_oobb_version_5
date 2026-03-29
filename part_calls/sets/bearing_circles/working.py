d = {}


def define():
    global d
    if not d:
        d = {
            "name": "bearing_circles",
            "name_short": ["bcs"],
            "description": "Bearing circle part-set definitions.",
            "category": "Part Sets",
            "variables": ["size"],
        }
    return dict(d)


def items(size="oobb", **kwargs):
    bcs = []
    bcs.append({"type": "bearing_circle", "diameter": 3, "thickness": 12, "bearing": "606", "size": size})
    return bcs


def test(**kwargs):
    result = items(**kwargs)
    return isinstance(result, list) and len(result) >= 1 and isinstance(result[0], dict)
