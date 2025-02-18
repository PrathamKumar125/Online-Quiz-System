# Online Quiz System

A modern web application for creating and managing online quizzes, built with FastAPI backend and React frontend.
![Screenshot 2025-02-19 011940](https://github.com/user-attachments/assets/51bb4ac7-15a0-4d95-a64a-7e1a1f7238c1)

<br>

![Screenshot 2025-02-19 012010](https://github.com/user-attachments/assets/6ad9fa59-c260-4781-8ff2-04be018036e3)



<br>

## Project Structure

```
sparkl_/
├── backend/       # FastAPI backend application
│   ├── routers/   # API route handlers
│   ├── services/  # Business logic
│   └── models/    # Database models
├── frontend/      # React frontend application
│   ├── src/       # Source code
│   └── public/    # Static assets
```

## Features

- User authentication and authorization
- Quiz creation and management
- Multiple choice questions support
- Real-time quiz taking
- Score tracking and results
- Rate limiting for API endpoints

## Tech Stack

### Backend
- FastAPI (Python web framework)
- SQLAlchemy (ORM)
- MySQL database
- JWT authentication
- SlowAPI for rate limiting

### Frontend
- React 18
- Material-UI components
- Axios for API calls
- React Router for navigation
- Formik for form handling

## Getting Started

### Prerequisites

- Python 3.13+
- Node.js 14+
- MySQL database

### Installation

1. Clone the repository:
```bash
git clone https://github.com/PrathamKumar125/Online-Quiz-System.git
cd Online-Quiz-System
```

2. Set up the backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure environment variables:
Create a `.env` file in the backend directory with:
```
DATABASE_URL=mysql://user:password@localhost/quiz_db
SECRET_KEY=your_secret_key
```

4. Set up the frontend:
```bash
cd frontend
npm install
```

### Running the Application

1. Start the backend:
```bash
cd backend
uvicorn main:app --reload
```

2. Start the frontend:
```bash
cd frontend
npm start
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## API Documentation

- Authentication endpoints:
  - POST /api/token - Get access token
- Quiz endpoints:
  - GET /api/quizzes - List all quizzes
  - POST /api/quizzes - Create new quiz
  - GET /api/quizzes/{id} - Get quiz details
  - PUT /api/quizzes/{id} - Update quiz
  - DELETE /api/quizzes/{id} - Delete quiz
- users
    - /users/ - Get Users
    - /users/ - Post Users
