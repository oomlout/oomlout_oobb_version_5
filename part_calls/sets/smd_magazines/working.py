d = {}


def define():
    global d
    if not d:
        d = {
            "name": "smd_magazines",
            "name_short": [],
            "name_long": "OOBB Part Set: Smd Magazines",
            "description": "smd_magazines part-set definitions.",
            "category": "Part Sets",
            "variables": ["size"],
        }
    return dict(d)


def items(size="oobb", **kwargs):
    import oobb_make_sets

    getter = getattr(oobb_make_sets, "get_smd_magazines")
    try:
        return getter(size=size, **kwargs)
    except TypeError:
        return getter(**kwargs)


def test(**kwargs):
    return isinstance(items(**kwargs), list)
