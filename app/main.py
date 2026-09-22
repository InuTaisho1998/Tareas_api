from dotenv import load_dotenv
from fastapi import FastAPI

from app.routers import auth, tasks

load_dotenv()

app = FastAPI()

# Include routers
app.include_router(auth.router)

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(tasks.router)