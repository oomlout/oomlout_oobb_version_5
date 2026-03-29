d = {}


def define():
    global d
    if not d:
        d = {
            "name": "others",
            "name_short": ["ots"],
            "description": "Other utility part-set definitions.",
            "category": "Part Sets",
            "variables": ["size"],
        }
    return dict(d)


def items(size="oobb", **kwargs):
    ots = []

    ots.append({"type": "other", "extra": "timing_belt_clamp_gt2", "width": 2.5, "height": 1.5, "thickness": 14, "size": size})
    ots.append({"type": "other", "extra": "timing_belt_clamp_gt2", "width": 2.5, "height": 1.5, "thickness": 6, "size": size})

    ots.append({"type": "other", "extra": "corner_cube", "width": 2, "height": 2, "thickness": 29, "size": size})

    ots.append({"type": "other", "extra": "bolt_stacker", "diameter": 1.5, "thickness": 24, "size": size})
    ots.append({"type": "other", "extra": "bolt_stacker", "width": 1, "height": 6, "thickness": 3, "size": size})

    heights = [7, 5, 3]
    shafts = ["m6", "quarter_inch_pipe_thread"]
    for h in heights:
        for s in shafts:
            ots.append({"type": "other", "extra": "ptfe_tube_holder", "width": 1, "height": h, "thickness": 14, "size": size, "shaft": s})
            ots.append({"type": "other", "extra": "ptfe_tube_holder_ninety_degree", "width": 1, "height": h, "thickness": 14, "size": size, "shaft": s})

    return ots


def test(**kwargs):
    result = items(**kwargs)
    return isinstance(result, list) and len(result) >= 1 and all(isinstance(item, dict) for item in result)
