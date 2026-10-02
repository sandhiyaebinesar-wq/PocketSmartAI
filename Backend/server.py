from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Backend.database.db import initialize_database
from Backend.api.account import router as account_router
from Backend.api.planner import router as planner_router
from Backend.api.history import router as history_router


app = FastAPI(
    title="PocketSmart AI",
    description="Smart Budget & Recommendation Assistant",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    initialize_database()


@app.get("/")
def home():
    return {
        "message": "PocketSmart AI backend is running!"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


app.include_router(account_router)
app.include_router(planner_router)
app.include_router(history_router)
