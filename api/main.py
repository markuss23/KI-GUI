from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Header, Path, Query
from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Vytvoření instance FastAPI
# docs_url="/" - nastavení URL pro dokumentaci
# (výchozí je "/docs")
app = FastAPI(
    docs_url="/",
)


# Funkce pro zpracování závislosti
def ahoj(item_id) -> str:
    return ("mam svoje id a mohu s ním dělat co chci ", item_id)


# Závislost pro ověření API klíče
def verify_api_key(api_key: Annotated[str | None, Header()] = None) -> str:
    if api_key != "key":
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return api_key


# Anotace pro ID
# Slouží pro validaci ID v URL
# Rozšiřuje základní datový typ int
# Path() - popis parametru
# Závislosti se používají pro validaci dat
# Depends() - závislost vyvolá funkci a předá jí hodnotu
# (v tomto případě ID)
ID_PATH_ANNOTATION = Annotated[
    int, Path(description="ID of the item", ge=0), Depends(ahoj)
]

# Anotace pro limit a offset
# Slouží pro validaci limit a offset v URL
# Rozšiřuje základní datový typ int
# Query() - popis parametru
LIMIT_QUERY_ANNOTATION = Annotated[
    int, Query(description="Limit of items", ge=0, le=100)
]
OFFSET_QUERY_ANNOTATION = Annotated[int, Query(description="Offset of items", ge=0)]


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
def read_sitem(asd_id) -> dict:
    return {
        "asd_id": asd_id,
    }


class ItemNotDict:
    def __init__(self, name, description, price):
        self.name = name
        self.description = description
        self.price = price


@app.post("/items")
def read_items(data: Item) -> Item:
    # Testování validace modelu pokud není přímo dict
    item_not_dict = ItemNotDict(name="asd", description="asd", price=1)
    print(type(item_not_dict))
    print(item_not_dict.__dict__)
    print(Item.model_validate(item_not_dict, from_attributes=True))
    #
    return Item.model_validate(data)


@app.get("/items/{item_id}")
def read_item(
    item_id: ID_PATH_ANNOTATION,
    limit: LIMIT_QUERY_ANNOTATION = 10,
    offset: OFFSET_QUERY_ANNOTATION = 0,
) -> dict:
    return {
        "item_id": item_id,
        "limit": limit,
        "offset": offset,
    }


@app.get("/settings")
def read_settings() -> Settings:
    return settings.model_dump()


@app.get("/secure-data")
def get_secure_data(api_key: str = Depends(verify_api_key)) -> dict:
    return {"message": "Access granted!", "api_key": api_key}
