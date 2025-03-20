from fastapi import FastAPI

# Vytvoření instance FastAPI
# docs_url="/" - nastavení URL pro dokumentaci
# (výchozí je "/docs")
app = FastAPI(
    docs_url="/",
)
