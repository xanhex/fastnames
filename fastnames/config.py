"""App config."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """App settings class."""

    app_name: str = 'fastnames'
    admin_email: str
    items_per_user: int = 50
    static: str = 'fastnames/static'
    templates: str = 'fastnames/templates'
    database_url: str = 'sqlite+aiosqlite:///fastnames/data.db'

    model_config = SettingsConfigDict(
        env_file='fastnames/.env', extra='ignore',
    )
