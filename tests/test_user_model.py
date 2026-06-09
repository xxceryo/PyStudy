from sqlalchemy import inspect

from app.models import User


def test_user_model_defines_profile_and_inherited_fields() -> None:
    table = inspect(User).local_table

    assert User.__tablename__ == "users"
    assert set(table.columns.keys()) == {
        "username",
        "password_hash",
        "nickname",
        "avatar_url",
        "signature",
        "phone_number",
        "id",
        "deleted",
        "lock_version",
        "gmt_create",
        "gmt_modified",
    }


def test_user_model_configures_field_types_and_nullability() -> None:
    table = inspect(User).local_table

    assert table.c.username.type.length == 50
    assert table.c.username.nullable is False
    assert table.c.password_hash.type.length == 255
    assert table.c.password_hash.nullable is False
    assert table.c.nickname.type.length == 50
    assert table.c.nickname.nullable is True
    assert table.c.avatar_url.type.length == 500
    assert table.c.avatar_url.nullable is True
    assert table.c.signature.type.length == 255
    assert table.c.signature.nullable is True
    assert table.c.phone_number.type.length == 32
    assert table.c.phone_number.nullable is True


def test_user_model_defines_unique_identity_indexes() -> None:
    table = inspect(User).local_table
    unique_index_columns = {
        tuple(column.name for column in index.columns)
        for index in table.indexes
        if index.unique
    }

    assert unique_index_columns == {("username",), ("phone_number",)}
