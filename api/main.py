from fastapi import FastAPI
from api.database import SqlSessionDependency, init_db
from sqlalchemy import text

from api.src.routers import router

# Vytvoření instance FastAPI
# docs_url="/" - nastavení URL pro dokumentaci
# (výchozí je "/docs")
app = FastAPI(
    docs_url="/",
    responses={
        404: {"description": "Not found"},
        409: {"description": "Conflict"},
    },
)

init_db()


@app.get("/health")
def health_check(
    sql: SqlSessionDependency,
) -> dict:
    sql.execute(text("SELECT 1")).first()

    return {"status": "ok", "db": "ok"}


# Připojení routeru k aplikaci
# router - router, který obsahuje definice endpointů
# include_router - metoda pro připojení routeru k aplikaci
app.include_router(router=router)
