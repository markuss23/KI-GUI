import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from api.database import SqlSessionDependency, init_db
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


# CORS middleware
# Slouží pro povolení CORS (Cross-Origin Resource Sharing)
# CORS je bezpečnostní opatření, které omezuje přístup k API z jiných domén
# allow_origins - seznam povolených domén
# allow_credentials - povolení cookies a HTTP autentizace
# allow_methods - povolené HTTP metody
# allow_headers - povolené HTTP hlavičky
# origins - seznam povolených domén
# V tomto případě je povoleno všechno
# (což není bezpečné pro produkční prostředí)
# V produkčním prostředí by měly být povoleny pouze konkrétní domény
origins: list[str] = [
    "*",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
