from fastapi import FastAPI
from app.api.user.router import user_main
from app.api.ledger.router import ledger_main
from app.api.models.db import database

app = FastAPI(openapi_url="/openapi.json")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.router.prefix = "/api/v1"
app.include_router(user_main.users, prefix="/users")
app.include_router(ledger_main.ledger, prefix="/accounts")
