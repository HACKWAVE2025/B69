"""FastAPI main application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import alerts, flows, stats
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="NetSage ML API",
    description="Network Anomaly Detection Platform API",
    version="1.0.0"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(alerts.router)
app.include_router(flows.router)
app.include_router(stats.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "NetSage ML API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    from api.models.database import get_database
    try:
        db = get_database()
        # Try to ping the database
        db.client.admin.command('ping')
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run(app, host=host, port=port)

