try:
    import rapidjson as json
except ImportError:
    try:
        import ujson as json
    except ImportError:
        import json
