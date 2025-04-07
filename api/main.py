import time
from fastapi import FastAPI
from api.database import SqlSessionDependency, init_db
from sqlalchemy import text

from api.src.routers import router
from api.logger import logger

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


# Middlewares
# Slouží pro zpracování požadavků a odpovědí
# Middleware - funkce, která se vykonává před a po zpracování požadavku
# Lze použít pro logování, autentizaci, atd.
@app.middleware("http")
async def add_rpcess_time_header(request, call_next):
    """
    Middleware pro přidání hlavičky s časem zpracování
    """
    start_time: float = time.time()
    response = await call_next(request)
    process_time: float = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.middleware("http")
async def logging_middleware(request, call_next):
    """
    Middleware pro logování požadavků
    """
    response = await call_next(request)
    logger.info(
        f"Request: {request.method} {request.url} - "
        f"Response status: {response.status_code}"
    )
    return response
