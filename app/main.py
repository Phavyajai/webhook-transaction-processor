from fastapi import FastAPI
from datetime import datetime
from app.api.routes import router

app = FastAPI(title="Webhook Transaction Processor")

# include all API routes
app.include_router(router)

# health check endpoint
@app.get("/")
def health_check():
    return {
        "status": "HEALTHY",
        "current_time": datetime.utcnow()
    }
