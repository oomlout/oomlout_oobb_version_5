d = {}


def define():
    global d
    if not d:
        d = {
            "name": "bearings",
            "name_short": [],
            "name_long": "OOBB Part Set: Bearings",
            "description": "bearings part-set definitions.",
            "category": "Part Sets",
            "variables": ["size"],
        }
    return dict(d)


def items(size="oobb", **kwargs):
    import oobb_make_sets

    getter = getattr(oobb_make_sets, "get_bearings")
    try:
        return getter(size=size, **kwargs)
    except TypeError:
        return getter(**kwargs)


def test(**kwargs):
    return isinstance(items(**kwargs), list)
