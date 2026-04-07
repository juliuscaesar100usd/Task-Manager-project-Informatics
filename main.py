from fastapi import FastAPI
from routers.auth import auth_router
from routers.tasks import tasks_router
from fastapi.middleware.cors import CORSMiddleware

import models

app= FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "App is running!"}

app.include_router(auth_router)
app.include_router(tasks_router)