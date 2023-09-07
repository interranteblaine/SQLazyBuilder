QUERY_CLASSES = {}


def register_query_class(cls):
    QUERY_CLASSES[cls.__name__] = cls
    return cls


def is_registered_query_class(value):
    return type(value) in QUERY_CLASSES.values()
