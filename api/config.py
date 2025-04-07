from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

"""
Tento soubor definuje nastavení aplikace pomocí Pydantic a Pydantic Settings.
Používá se zde Pydantic pro definici modelů a validaci dat.
Nastavení aplikace jsou rozdělena do dvou částí:
1. `AppSettings` - obsahuje základní informace o aplikaci, jako je název, verze a popis.
2. `SqlSettings` - obsahuje nastavení pro SQL databázi, včetně názvu databáze a metody pro získání URL pro připojení k databázi.
"""


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
