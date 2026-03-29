d = {}


def define():
    global d
    if not d:
        d = {
            "name": "jigs",
            "name_short": ["jgs"],
            "description": "Jig part-set definitions.",
            "category": "Part Sets",
            "variables": ["size"],
        }
    return dict(d)


def items(size="oobb", **kwargs):
    jgs = []
    jgs.append({"type": "jig", "extra": "tray_03_03", "width": 5, "height": 5, "thickness": 6, "size": size})
    jgs.append({"type": "jig", "extra": "screw_sorter_m3_03_03", "width": 3, "height": 3, "thickness": 15, "size": size})
    return jgs


def test(**kwargs):
    result = items(**kwargs)
    return isinstance(result, list) and all(isinstance(item, dict) for item in result)
