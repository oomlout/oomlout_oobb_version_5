d = {}


def define():
    global d
    if not d:
        d = {
            "name": "wires",
            "name_short": [],
            "name_long": "OOBB Part Set: Wires",
            "description": "wires part-set definitions.",
            "category": "Part Sets",
            "variables": ["size"],
        }
    return dict(d)


def items(size="oobb", **kwargs):
    import oobb_make_sets

    getter = getattr(oobb_make_sets, "get_wires")
    try:
        return getter(size=size, **kwargs)
    except TypeError:
        return getter(**kwargs)


def test(**kwargs):
    return isinstance(items(**kwargs), list)
