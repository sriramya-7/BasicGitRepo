from fastapi import FastAPI, HTTPException,Query,Header
from typing import Optional
import os, json
app = FastAPI(title="Student Management API - V2")

DATA_FILE = "data.json"

# 🛠 Utility Functions
def read_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# Basic Welcome Route (V1)
@app.get("/v1/")
def welcome_v1():
    return {"message": "Welcome to FastAPI V1!"}

# Filter Students using Query Parameters
@app.get("/v2/students/filter/")
def filter_students(
    grade: Optional[str] = Query(None, description="Filter students by grade"),
    min_age: int = Query(6, ge=6, le=19, description="Minimum age filter (default: 6)")
):
    data = read_data()
    
    # Apply filters
    if grade:
        data = [s for s in data if s["grade"].lower() == grade.lower()]
    
    data = [s for s in data if s["age"] >= min_age]

    return {"filtered_students": data}

# 📌 Protected Route Using Request Header
@app.get("/v2/students/auth/")
def get_students_with_auth(
    x_auth_token: Optional[str] = Header(None, description="Authentication token required")
):
    # Simulate an authentication check
    if not x_auth_token or x_auth_token != "secret123":
        raise HTTPException(status_code=401, detail="Invalid or missing authentication token")
    
    data = read_data()
    return {"message": "Authenticated successfully", "students": data}
