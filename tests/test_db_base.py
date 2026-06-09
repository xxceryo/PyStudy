from sqlalchemy import inspect

from app.db.base import Base


class ExampleModel(Base):
    __tablename__ = "example"


def test_base_model_defines_common_persistence_fields() -> None:
    mapper = inspect(ExampleModel)
    table = ExampleModel.__table__

    assert set(table.columns.keys()) == {
        "id",
        "deleted",
        "lock_version",
        "gmt_create",
        "gmt_modified",
    }
    assert table.c.id.primary_key
    assert table.c.id.autoincrement is True
    assert table.c.deleted.default.arg is False
    assert table.c.lock_version.default.arg == 1
    assert table.c.gmt_create.server_default is not None
    assert table.c.gmt_modified.server_default is not None
    assert table.c.gmt_modified.onupdate is not None
    assert mapper.version_id_col is table.c.lock_version
