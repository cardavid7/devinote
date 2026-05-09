from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv

from app.core.config import settings
from app.core.db import init_db
from app.api.routers.auth_router import router as auth_router
from app.api.routers.notes_router import router as notes_router
from app.api.routers.labels_router import router as labels_router
from app.api.routers.shares_router import router as shares_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    #Startup event
    print("Starting up...")
    load_dotenv()

    #Database connection
    init_db()
    print("Connecting to database...")
    
    #Run background tasks
    print("Running background tasks...")
    
    yield

    #Shutdown event
    print("Shutting down...")
    
    #Close database connection
    #Stop background tasks

app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan,
    swagger_ui_parameters={
        "persistAuthorization": True,
    },
    description="Devinote API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(notes_router, prefix="/api/v1")
app.include_router(labels_router, prefix="/api/v1")
app.include_router(shares_router, prefix="/api/v1")