from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Vytvoření instance FastAPI
# docs_url="/" - nastavení URL pro dokumentaci
# (výchozí je "/docs")
app = FastAPI(
    docs_url="/",
)


# Pydantic model pro validaci dat
# BaseModel je základní třída pro vytvoření modelu
# Field() - validace dat
# max_length=255 - maximální délka řetězce
class Item(BaseModel):
    name: str = Field(max_length=255, min_length=3)
    description: str = Field(max_length=255)
    price: float

    @field_validator("price")
    @classmethod
    def validate_price(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("Price must be greater than 0")
        return value


class AppSettings(BaseModel):
    name: str = Field(max_length=64)
    version: str = Field(max_length=16)
    description: str = Field(max_length=255)


class SqlSettings(BaseModel):
    name: str

    def get_url(self):
        return f"sqlite://{self.name}.db"


class Settings(BaseSettings):
    app: AppSettings
    sql: SqlSettings

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
    )


settings = Settings()


# Decorátor pro vytvoření endpointu
# Decorátor app.get() vytvoří endpoint pro GET request
# GET /asd
# Funkce read_root() vrací slovník
# {"Hello": "World"}
# Tento slovník se automaticky převede na JSON
# a odešle klientovi
@app.get("/asd")
def read_root() -> dict[str, str]:
    return {"Hello": "World"}


@app.get("/asd/{asd_id}")
def read_item(asd_id) -> dict:
    return {
        "asd_id": asd_id,
    }


@app.post("/items")
def read_items(data: Item) -> Item:
    return data


@app.get("/settings")
def read_settings() -> Settings:
    return settings.model_dump()
