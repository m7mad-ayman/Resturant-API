# Resturant-API
#### A Django API for Resturant is a backend service built using the Django framework to handle the core functionalities of an Resturant System.

## Tools :
- Django
- RestFramework

## Featues :
- RESTful API Endpoints
- Register [admin - staff - customer]
- Ingredients Management ( admin )
- Table Management ( admin - staff )
- Menu Items ( updates by admin only )
- Orders ( updates by admin - staff )
- Reservation ( updates by admin - staff )
  
## Installation :
  ### Requirements
  - Python (3.x.x)
  ### SetUp
  - Create virtual environment in Unix , Windows
    ```
    python -m venv venv
    ```
  - Copy project folder to /venv/
    
  - Activate Virtual Environment
    
    Windows
    ```
    /venv/Scripts/activate
    ```
    Unix
    ```
    source /venv/Scripts/activate
    ```
  - Install Requirements
    ```
    cd Resturant-API-master
    pip install -r requirements.txt
    ```
  - Create database
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```
  - Create Admin User (username,password) required
    ```
    python manage.py createsuperuser
    ```
  - Runserver
    ```
    python manage.py runserver
    ```
