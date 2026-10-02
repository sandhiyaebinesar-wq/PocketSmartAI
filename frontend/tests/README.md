# PocketSmart AI

PocketSmart AI is a Smart Budget and Recommendation Assistant.

It provides recommendations for:

1. Home Planning
2. Party Planning
3. Jewelry Planning


## Technologies Used

Frontend:
- HTML
- CSS
- JavaScript

Backend:
- Python
- FastAPI
- SQLite

AI:
- Google Gemini API


## Project Structure

PocketSmartAI
|
|-- backend
|-- frontend
|-- tests
|-- requirements.txt
|-- .env.example
|-- .gitignore
|-- start.bat
|-- README.md


## How to Run

Step 1:
Create a virtual environment.

python -m venv venv


Step 2:
Activate the virtual environment.

venv\Scripts\activate


Step 3:
Install required packages.

pip install -r requirements.txt


Step 4:
Start the backend.

uvicorn backend.server:app --reload


Step 5:
Open the frontend.

frontend/html/index.html


## Features

- User Registration
- User Login
- Budget-based Recommendations
- Home Planner
- Party Planner
- Jewelry Planner
- AI Recommendations using Gemini
- Fallback Recommendations
- Recommendation History
- Product Search Links


## Backend API

http://127.0.0.1:8000


## API Documentation

http://127.0.0.1:8000/docs