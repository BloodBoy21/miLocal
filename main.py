from fastapi import FastAPI, HTTPException
from database.db import engine, db
from database.mongo import database
from api.init import api_router

app = FastAPI(title="miLocal")
app.include_router(api_router, prefix="/api")


@app.on_event("startup")
async def startup():
    print("Starting up")
    db.metadata.create_all(bind=engine, checkfirst=True)
    await database.client.start_session()


@app.get("/")
def root():
    return {"status": "ok"}
