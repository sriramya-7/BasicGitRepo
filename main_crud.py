from fastapi import FastAPI, Path, Query, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
import json
import os

app = FastAPI(title="Advanced FastAPI - V2")

DATA_FILE = "data.json"


# 🛠 Utility Functions
def read_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def write_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


# 📌 Student Model
class Student(BaseModel):
    id: int
    name: str = Field(..., min_length=2, max_length=50)
    age: int = Field(..., gt=5, lt=20, description="Age must be between 6 and 19")
    grade: str
    email: EmailStr


# 🛠 V1 Welcome Route
@app.get("/v1/")
def welcome_v1():
    return {"message": "Welcome to FastAPI V1"}


# 🛠 V2 Student Routes

# Create a Student
@app.post("/v2/students/", status_code=status.HTTP_201_CREATED)
def create_student(student: Student):
    data = read_data()
    
    if any(s["id"] == student.id for s in data):
        raise HTTPException(status_code=400, detail="Student with this ID already exists.")
    
    data.append(student.dict())
    write_data(data)
    
    return {"message": "Student created successfully", "student": student}


# Read All Students
@app.get("/v2/students/", response_model=List[Student])
def get_students():
    return read_data()


# Read a Single Student
@app.get("/v2/students/{student_id}")
def get_student(student_id: int = Path(..., title="Student ID", gt=0)):
    data = read_data()
    student = next((s for s in data if s["id"] == student_id), None)
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return student


# Update a Student
@app.put("/v2/students/{student_id}")
def update_student(student_id: int, student: Student):
    data = read_data()
    
    for i, existing_student in enumerate(data):
        if existing_student["id"] == student_id:
            data[i] = student.dict()
            write_data(data)
            return {"message": "Student updated successfully", "student": student}
    
    raise HTTPException(status_code=404, detail="Student not found")


# Delete a Student
@app.delete("/v2/students/{student_id}")
def delete_student(student_id: int):
    data = read_data()
    
    if not any(s["id"] == student_id for s in data):
        raise HTTPException(status_code=404, detail="Student not found")
    
    data = [s for s in data if s["id"] != student_id]
    write_data(data)
    
    return {"message": "Student deleted successfully"}


# Search Students by Name
@app.get("/v2/search/")
def search_students(q: str = Query(..., min_length=2)):
    data = read_data()
    results = [s for s in data if q.lower() in s["name"].lower()]
    return {"results": results}
