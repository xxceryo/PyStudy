from app.core.config import Settings


def test_settings_use_local_service_connections() -> None:
    settings = Settings(_env_file=None)

    assert settings.database_url == (
        "mysql+asyncmy://root:123456@127.0.0.1:13306/pystudy"
    )
    assert settings.redis_url == "redis://:123456@127.0.0.1:16379/0"
    assert settings.auto_create_tables is False


def test_auto_create_tables_can_be_enabled_from_environment(
    monkeypatch,
) -> None:
    monkeypatch.setenv("PYSTUDY_AUTO_CREATE_TABLES", "true")

    settings = Settings(_env_file=None)

    assert settings.auto_create_tables is True
