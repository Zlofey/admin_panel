from urllib.parse import quote_plus

from pydantic import PostgresDsn, Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """Database specific configuration."""

    host: str = Field(description="Хост базы данных")
    port: int = Field(description="Порт базы данных")
    user: str = Field(description="Пользователь БД")
    password: str = Field(description="Пароль БД")
    name: str = Field(description="Имя базы данных")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="DB_",
        case_sensitive=False,
        extra="ignore",
    )

    @computed_field
    def url(self) -> PostgresDsn:
        """Собирает бд url."""
        safe_password = quote_plus(self.password)
        dsn_string = f"postgresql://{self.user}:{safe_password}@{self.host}:{self.port}/{self.name}"
        return PostgresDsn(dsn_string)


class Settings(BaseSettings):
    db: DatabaseSettings = DatabaseSettings()

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
