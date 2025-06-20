from fastapi import FastAPI

app = FastAPI(title="Simple API - V1")

# Basic Welcome Route (V1)
@app.get("/v1/")
def welcome_v1():
    return {"message": "Welcome to FastAPI V1!"}
