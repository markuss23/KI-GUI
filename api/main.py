from fastapi import FastAPI

# Vytvoření instance FastAPI
# docs_url="/" - nastavení URL pro dokumentaci
# (výchozí je "/docs")
app = FastAPI(
    docs_url="/",
)


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


@app.get("/asd/{asd_id}/items/{item_id}")
def read_item(asd_id, item_id) -> dict:
    return {
        "asd_id": asd_id,
        "item_id": item_id,
    }
