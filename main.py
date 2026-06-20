from fastapi import FastAPI

from app.database import Base, engine
from app.routes import router as api_router
from app.frontend import router as frontend_router
from app import models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Auction System REST API",
    description="System aukcji internetowych wykonany w FastAPI",
    version="1.0.0"
)

app.include_router(frontend_router)
app.include_router(api_router)