from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv
from app.database.database import init_db
from app.routes.chat import router as chat_router

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Customer Internet Support Agent",
    description="AI-powered troubleshooting assistant",
    version="0.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()
    print("✅ Database initialized")

# Include routes
app.include_router(chat_router)

# Serve frontend
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

# Health check endpoint
@app.get("/health")
async def health():
    return {"status": "ok"}

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Customer Internet Support Agent API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)