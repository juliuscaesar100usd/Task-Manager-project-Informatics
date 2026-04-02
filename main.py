from fastapi import FastAPI
import models

app= FastAPI()

@app.get("/")
def read_root():
    return {"message": "Server is running"}