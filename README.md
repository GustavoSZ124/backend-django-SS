# backend-django-SS

## prerequisites
- Python installed
- File .env

## Project setup
First create a python virtual environment and activate
`python -m venv env`
`env\Scripts\activate.bat`

Install the required packages
`pip install -r requeriments.txt`

Add supported addresses to communicate with the server. Example
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080/",
]

Add the file .env to the project folder
**backend-django-SS* folder:
*api*
*backend*
*env*
***.env***
*.gitignore*
*manage.py*
*requeriments.txt*

Create Database
`python manage.py migrate`

## Run Server
`python manage.py runserver`
