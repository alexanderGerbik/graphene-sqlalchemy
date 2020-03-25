from functools import singledispatch

from sqlalchemy import types
from sqlalchemy.dialects import postgresql

from graphene import types as graphene_types

from .enums import enum_for_sa_enum, enum_for_sa_utils_enum

try:
    import sqlalchemy_utils as sa_utils

    is_sa_utils_imported = True
except ImportError:
    sa_utils = None
    is_sa_utils_imported = False


@singledispatch
def conversion(type, column, registry):
    raise Exception(
        "Don't know how to convert the SQLAlchemy"
        f" field {column} ({column.__class__})"
    )


@conversion.register(types.Date)
@conversion.register(types.Time)
@conversion.register(types.String)
@conversion.register(types.Text)
@conversion.register(types.Unicode)
@conversion.register(types.UnicodeText)
@conversion.register(postgresql.UUID)
@conversion.register(postgresql.INET)
@conversion.register(postgresql.CIDR)
def convert_column_to_string(type, column, registry):
    return graphene_types.String


@conversion.register(types.DateTime)
def convert_column_to_datetime(type, column, registry):
    return graphene_types.DateTime


@conversion.register(types.SmallInteger)
@conversion.register(types.Integer)
def convert_column_to_int_or_id(type, column, registry):
    # TODO: move primary_key conversion to the right place
    return graphene_types.ID if column.primary_key else graphene_types.Int


@conversion.register(types.Boolean)
def convert_column_to_boolean(type, column, registry):
    return graphene_types.Boolean


@conversion.register(types.Float)
@conversion.register(types.Numeric)
@conversion.register(types.BigInteger)
def convert_column_to_float(type, column, registry):
    return graphene_types.Float


@conversion.register(types.Enum)
def convert_enum_to_enum(type, column, registry):
    return lambda: enum_for_sa_enum(type, registry)


@conversion.register(types.ARRAY)
@conversion.register(postgresql.ARRAY)
def convert_array_to_list(_type, column, registry):
    inner_type = conversion(column.type.item_type, column, registry)
    return graphene_types.List(inner_type)


@conversion.register(postgresql.HSTORE)
@conversion.register(postgresql.JSON)
@conversion.register(postgresql.JSONB)
def convert_json_to_string(type, column, registry):
    return graphene_types.JSONString


if is_sa_utils_imported:

    @conversion.register(sa_utils.TSVectorType)
    def convert_column_to_string(type, column, registry):
        return graphene_types.String

    @conversion.register(sa_utils.ChoiceType)
    def convert_choice_to_enum(type, column, registry):
        return enum_for_sa_utils_enum(type, column)

    @conversion.register(sa_utils.ScalarListType)
    def convert_scalar_list_to_list(type, column, registry):
        return graphene_types.List(graphene_types.String)

    @conversion.register(sa_utils.JSONType)
    def convert_json_type_to_string(type, column, registry):
        return graphene_types.JSONString
