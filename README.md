# Backend - Django!

## Structure
    https://famous-cress-fcf.notion.site/BACK-END-37ad249ad7a9416fae82b7268bf0b38b


## Installation
### Activate virtual environment
    source venv/bin/activate (MacOS/Linux)

    venv\Scripts\activate (Windows)

### Install dependencies
    pip install -r requirements.txt

### Create database
    python manage.py migrate

### Create superuser
    python manage.py createsuperuser

### Run server
    python manage.py runserver

## Usage
### Create new app
    python manage.py startapp <app_name>

### Create migrations
    python manage.py makemigrations

### Migrate
    python manage.py migrate

### Run tests
    python manage.py test

## NOTE
### requirements.txt
    pip freeze > requirements.txt 
After installing new packages, django not automatically add new packages to requirements.txt


    