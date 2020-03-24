import pytest
import sqlalchemy as sa

from graphene import Enum, List, ObjectType, Schema, String

from graphene_sqlalchemy.utils import get_session
from .models import Base, Editor, Pet


def test_get_session():
    session = "My SQLAlchemy session"

    class Query(ObjectType):
        x = String()

        def resolve_x(self, info):
            return get_session(info.context)

    query = """
        query ReporterQuery {
            x
        }
    """

    schema = Schema(query=Query)
    result = schema.execute(query, context_value={"session": session})
    assert not result.errors
    assert result.data["x"] == session
