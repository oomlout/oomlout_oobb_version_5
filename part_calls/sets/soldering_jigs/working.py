d = {}


def define():
    global d
    if not d:
        d = {
            "name": "soldering_jigs",
            "name_short": [],
            "name_long": "OOBB Part Set: Soldering Jigs",
            "description": "soldering_jigs part-set definitions.",
            "category": "Part Sets",
            "variables": ["size"],
        }
    return dict(d)


def items(size="oobb", **kwargs):
    import oobb_make_sets

    getter = getattr(oobb_make_sets, "get_soldering_jigs")
    try:
        return getter(size=size, **kwargs)
    except TypeError:
        return getter(**kwargs)


def test(**kwargs):
    return isinstance(items(**kwargs), list)
