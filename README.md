# Simple FastAPI CRUD Application

This project provides a FastAPI-based CRUD (Create, Read, Update, Delete) application with authentication and filtering capabilities.

## Installation & Setup

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run FastAPI server
```bash
uvicorn main:app --reload
```

### Build Docker Image
<!-- ```bash
docker build -t fastapi-crud .
``` -->

### Run Container
```bash
docker run -d -p 8000:8000 fastapi-crud
```

### To run the FastAPI server for the main_crud and main_advanced modules, you can use the following commands:

### For main_crud:

```bash
uvicorn main_crud:app --reload
```
### For main_advanced:

```bash
uvicorn main_advanced:app --reload
```

### If we want to run main_crud and main_advanced with Dockerfile we need to change main in CMD



### API Access
The API will be accessible at: [http://localhost:8000](http://localhost:8000)

## API Endpoints

### Simple API Version
- **`GET /v1/`** - Simple welcome message

### Advanced API Version (CRUD & Filtering)
Base URL: [http://localhost:8000/v2/students/](http://localhost:8000/v2/students/)

#### CRUD Operations
- **`POST /v2/students/`** - Create a new student
- **`GET /v2/students/`** - Retrieve all students
- **`GET /v2/students/{student_id}`** - Retrieve a student by ID
- **`PUT /v2/students/{student_id}`** - Update student details
- **`DELETE /v2/students/{student_id}`** - Delete a student

#### Filtering
- **Get students with a generic filter parameter:**
  ```
  http://localhost:8000/v2/students/filter/?param=value
  ```

#### Search
- **Search for students by name:**
  ```
  GET /v2/search/?q=name
  ```

## Using Postman
1. Open Postman and create a new request.
2. Set the request type (GET, POST, PUT, DELETE).
3. Enter the API URL (e.g., `http://localhost:8000/v2/students/`).
4. For POST and PUT, go to the **Body** tab, select **raw**, choose **JSON**, and input the required payload.
5. Click **Send** to execute the request.

### Import Postman Collection
A pre-configured Postman collection is available in the project.

## cURL Examples

### Create a Student
```bash
curl -X 'POST' 'http://localhost:8000/v2/students/' \
-H 'Content-Type: application/json' \
-d '{
    "id": 4,
    "name": "David Parker",
    "age": 16,
    "grade": "11th",
    "email": "david@example.com"
}'
```

### Fetch Student with Authentication Token
```bash
curl -X 'GET' 'http://localhost:8000/v2/students/auth/' \
-H 'X-Auth-Token: secret123' \
-H 'accept: application/json'
```

### Fetch a Student by ID
```bash
curl -X 'GET' 'http://localhost:8000/v2/students/1' -H 'accept: application/json'
```

### Fetch a Non-Existent Student
```bash
curl -X 'GET' 'http://localhost:8000/v2/students/99' -H 'accept: application/json'
```

---

## License
This project is licensed under the MIT License.

## Contributors
- Whitebox Learning
