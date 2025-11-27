from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.analyze import router as analyze_router
from app.api.v1.stream import router as stream_router
from app.logic.ingestion import ingest_data

app = FastAPI(
    title="Sentinel-Ke API",
    description="Sovereign National Threat Graph Engine",
    version="1.0.0"
)

# CORS middleware for React integration (e.g., allowing frontend on port 3000 to access backend on 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",   # Vite default
        "http://127.0.0.1:5173",   # Vite fallback
        "http://localhost:3000",   # If you ever use Create React App
        "*"                        # Remove this line when you deploy
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include routers with /api/v1 prefix
app.include_router(analyze_router, prefix="/api/v1")
app.include_router(stream_router, prefix="/api/v1")

# Startup event to ingest synthetic data (as per MVP requirements)
@app.on_event("startup")
async def startup_event():
    ingest_data("data/synthetic_kenya.csv")

# Health check endpoint
@app.get("/")
def health_check():
    return {"status": "Sentinel-Ke Online", "security_level": "DEFCON 4"}