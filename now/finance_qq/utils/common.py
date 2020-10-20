def get_in(coll, path=None, default=None):
    if path is None:
        return coll

    for key in path.split('.'):
        try:
            if isinstance(coll, dict):
                coll = coll[key]
            elif isinstance(coll, list):
                coll = coll[int(key)]
            else:
                raise KeyError
        except (KeyError, IndexError, TypeError, ValueError):
            return default
    return coll
