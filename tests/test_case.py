import pytest

from graphene_sqlalchemy import case


# some of the test cases are expected to fail
# it's not worth it to implement one-size-fits-all function
# in most cases the case of the source string is known
# an can be handled in a more specific manner
def omit(*args):
    xfail = pytest.mark.xfail(reason="won't fix", run=False)
    return pytest.param(*args, marks=xfail)


@pytest.mark.parametrize('name, expected', [
    ("make_pascal_case", "MakePascalCase"),
    ("AlreadyPascalCase", "AlreadyPascalCase"),
    ("camelCase", "CamelCase"),
    ("A_Snake_and_a_Camel", "ASnakeAndACamel"),
    omit("ENUM_VALUE_NAME", "EnumValueName"),
    ("ENUM_VALUE_NAME".lower(), "EnumValueName"),
])
def test_to_pascal(name, expected):
    actual = case.to_pascal(name)

    assert actual == expected


@pytest.mark.parametrize('name, expected', [
    ("make_enum_value_name", "MAKE_ENUM_VALUE_NAME"),
    ("makeEnumValueName", "MAKE_ENUM_VALUE_NAME"),
    ("PascalCase", "PASCAL_CASE"),
    ("HTTPStatus400Message", "HTTP_STATUS400_MESSAGE"),
    ("ALREADY_ENUM_VALUE_NAME", "ALREADY_ENUM_VALUE_NAME"),
])
def test_to_upper_snake(name, expected):
    actual = case.to_upper_snake(name)

    assert actual == expected


@pytest.mark.parametrize('name, expected', [
    ("makeSnakeCase", "make_snake_case"),
    ("MakeSnakeCase", "make_snake_case"),
    ("already_snake_case", "already_snake_case"),
    ("ENUM_VALUE_NAME", "enum_value_name"),
    omit("A_Snake_and_a_Camel", "a_snake_and_a_camel"),
    (case.to_camel("A_Snake_and_a_Camel"), "a_snake_and_a_camel"),
])
def test_to_snake(name, expected):
    actual = case.to_snake(name)

    assert actual == expected


@pytest.mark.parametrize('name, expected', [
    ("make_camel_case", "makeCamelCase"),
    ("alreadyCamelCase", "alreadyCamelCase"),
    ("PascalCase", "pascalCase"),
    ("A_Snake_and_a_Camel", "aSnakeAndACamel"),
    omit("ENUM_VALUE_NAME", "enumValueName"),
    ("ENUM_VALUE_NAME".lower(), "enumValueName"),
])
def test_to_camel(name, expected):
    actual = case.to_camel(name)

    assert actual == expected
