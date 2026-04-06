from fastapi import FastAPI
from routers.auth import router as auth_router


import models

app= FastAPI()

@app.get("/")
def read_root():
    return {"message": "App is running!"}

app.include_router(auth_router)
#app.include_router(tasks_router)