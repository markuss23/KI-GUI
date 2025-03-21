from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseModel):
    name: str = Field(max_length=64)
    version: str = Field(max_length=16)
    description: str = Field(max_length=255)


class SqlSettings(BaseModel):
    name: str

    def get_url(self) -> str:
        return f"sqlite://{self.name}.db"


# Konfigurace aplikace z .env souboru
# Nastavení pro aplikaci a SQL
# Pomocí SettingsConfigDict() lze nastavit
# prefix pro proměnné prostředí
# (výchozí je "APP_")
# Pomocí env_nested_delimiter lze nastavit
class Settings(BaseSettings):
    app: AppSettings
    sql: SqlSettings

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
    )


settings = Settings()