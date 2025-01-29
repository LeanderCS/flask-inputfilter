import timeit

field_info = {"fallback": "default_value"}


def variant1():
    fallback = field_info.get("fallback")
    if fallback is None:
        raise ValueError
    return fallback


def variant2():
    if field_info.get("fallback") is None:
        raise ValueError
    return field_info.get("fallback")


def variant3():
    field = field_info["fallback"]
    if field is None:
        raise ValueError
    return field


def variant4():
    if field_info["fallback"] is None:
        raise ValueError
    return field_info["fallback"]


def variant5():
    if field_info["fallback"] is None:
        raise ValueError
    variant55(field_info["fallback"])
    return field_info["fallback"]


def variant55(f):
    if f is None:
        raise ValueError
    return f


def variant6():
    if field_info["fallback"] is None:
        raise ValueError
    variant66(field_info)
    return field_info["fallback"]


def variant66(f):
    if f["fallback"] is None:
        raise ValueError
    return f["fallback"]


def variant7():
    f = field_info["fallback"]
    if f is None:
        raise ValueError
    variant77(f)
    return f


def variant77(f):
    if f is None:
        raise ValueError
    return f


print(timeit.timeit(variant1, number=10000000))
print(timeit.timeit(variant2, number=10000000))
print(timeit.timeit(variant3, number=10000000))
print(timeit.timeit(variant4, number=10000000))
print(timeit.timeit(variant5, number=10000000))
print(timeit.timeit(variant6, number=10000000))
print(timeit.timeit(variant7, number=10000000))
