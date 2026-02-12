from app.api.v1.router import router as v1_router
from fastapi import FastAPI

app = FastAPI(title="Credit Card Fraud API")
app.include_router(v1_router, prefix="/api/v1")
