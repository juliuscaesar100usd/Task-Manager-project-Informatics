from fastapi import FastAPI
from routers.auth import auth_router
from routers.tasks import tasks_router


import models

app= FastAPI()

@app.get("/")
def read_root():
    return {"message": "App is running!"}

app.include_router(auth_router)
app.include_router(tasks_router)