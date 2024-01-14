<h1 align="center">Note-app <i style="font-size: 1.8rem">RESTAPI</i></h1>

This project provides backend api's for a note app. It provides all basic functionality of a note application. It uses the <i> Django RESTful API's </i> for crud operation, authentication, rate limiting etc.

## Getting Started

### Prerequisites
* Should have Python >=3.8 in your system. For installation python refer <a src = 'https://www.python.org/downloads/'>Python Download</a>
* Install Django in your system. For installation refer <a src='https://www.djangoproject.com/download/'>Django Download</a>

### Set up project

1. Clone this repo in your local environment
```sh
git clone https://github.com/mayankr5/django-noteapp.git
```

2. Open project in vscode code or any editor and start virtual environment. For virtual environment refer <a src='https://docs.python.org/3/library/venv.html'>venv</a>

3. Now install <i>Django RESTful Framework<i> using following command.
```sh
pip install djangorestframework
```

4. Now run following command for creating admin.
```sh
python manage.py createsuperuser
```

5. Now run following command on terminal to run server.
```sh
python manage.py runserver
```
Now your server is running on port 8000 and you can access api on this port.

---
**_NOTE:_**
  1. By Default SUPERUSER is: 
  ```
  username: admin
  password: admin@123
  ```
  2. By Default unautherised user limit is 100/day and autherised user limit is 1000/day. You can change this limit in setting.py.
  ```
    REST_FRAMEWORK = {
        ... ,
        'DEFAULT_THROTTLE_RATES': {
            'anon': '100/day',
            'user': '1000/day'
        }
    }
  ```
---