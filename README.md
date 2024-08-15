# Chatbot Application

## Overview

This chatbot application allows users to interact with a chatbot that provides responses and saves chat history. It is designed to be easy to set up and run locally.

## Backend Setup

The backend of the application is built using Django. Follow these steps to set up and run the backend:

### 1. Clone this repository  
  
```bash
git clone https://github.com/T7-JonathanAdriel/backend.git
```

### 2. Navigate to the repository's directory and create a virtual environment  
```bash
python -m venv env
```

### 3. Activate the virtual environment 
```bash 
- On Windows:
  .\env\Scripts\activate
- On macOS/Linux:
  source env/bin/activate
```

### 4. Install dependencies  
```bash
pip install -r requirements.txt
```

### 5. Prepare for migration  
```bash
python manage.py makemigrations
```

### 6. Apply migrations  
```bash
python manage.py migrate
```

### 7. Seed predefined responses  
```bash
python manage.py seed_data
```

### 8. Run the server  
```bash
python manage.py runserver
```

The backend server will be running at `http://127.0.0.1:8000/`.