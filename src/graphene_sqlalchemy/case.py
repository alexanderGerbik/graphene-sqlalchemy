import re


def to_pascal(name):
    return "".join(_capitalize(word) for word in name.split("_"))


def to_camel(name):
    words = iter(name.split("_"))
    return _decapitalize(next(words)) + "".join(w.title() for w in words)


def to_snake(name):
    return _underscorize(name).lower()


def to_upper_snake(name):
    return _underscorize(name).upper()


def _capitalize(word):
    return word[:1].upper() + word[1:]


def _decapitalize(word):
    return word[:1].lower() + word[1:]


def _underscorize(name):
    s1 = _first_cap_re.sub(r"\1_\2", name)
    return _all_cap_re.sub(r"\1_\2", s1)


_first_cap_re = re.compile("(.)([A-Z][a-z]+)")
_all_cap_re = re.compile("([a-z0-9])([A-Z])")
