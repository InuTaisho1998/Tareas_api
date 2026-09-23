from fastapi import FastAPI

from app.routers import auth, tasks

app = FastAPI()

# Include routers
app.include_router(auth.router)

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(tasks.router)