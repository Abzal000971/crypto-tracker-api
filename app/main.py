from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models
from .routes import auth, user, crypto, watchlist
from .core.config import settings

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["auth"])
app.include_router(user.router, prefix=settings.API_V1_STR, tags=["user"])
app.include_router(crypto.router, prefix=settings.API_V1_STR, tags=["crypto"])
app.include_router(watchlist.router, prefix=settings.API_V1_STR, tags=["watchlist"])

@app.get("/")
async def root():
    return {"message": "Welcome to CryptoTracker API"} 