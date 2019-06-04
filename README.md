# REST API Store

Rest API made in Python and Flask

## Installation

1. Create a virtual environment that use the project.

```bash
virtualenv venv
```

2. Activate the virtual environment.

* For Windows (PATH is your full "venv" directory)

```bash
C:\path\to\app> PATH\venv\Script\activate.bat
```

* For Mac
```bash
$ source /venv/bin/activate
```

3. Install all the dependencies (one by one) that use the project i.e. Flask, Flask-Restful, Flask-RESTful-Swagger, Flask-SQLAlchemy and Flask-JWT.

```bash
pip install flask
pip install flask-restful
pip install flask-jwt
pip install flask-sqlalchemy
pip install flask-restful-swagger
```

If you have the requirements.txt file must be execute the command

```bash
pip install -r requirements.txt
```

## Run project

You must type this command to execute the project

* For Windows (CMD)
```bash
C:\path\to\app>set FLASK_APP=run.py
C:\path\to\app>flask run
```

* For Windows (Powershell)
```bash
PS C:\path\to\app> $env:FLASK_APP = "run.py"
PS C:\path\to\app> flask run
```

* For Mac
```bash
$ export FLASK_APP=run.py
$ flask run
```

## Debug project

You must type this command to execute the project in debug mode

* For Windows (CMD)
```bash
C:\path\to\app>set FLASK_ENV=development
C:\path\to\app>flask run
```

* For Windows (Powershell)
```bash
PS C:\path\to\app> $env:FLASK_ENV=development
PS C:\path\to\app> flask run
```

* For Mac
```bash
$ export FLASK_ENV=development
$ flask run
```