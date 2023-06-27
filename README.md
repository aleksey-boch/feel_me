### Introduction
I took the JSON Web Tokens (JWTs) implementation standard as the basis for the design. He fits very well in the conditions of the assignment described.
Partner sites register in the project and get the opportunity to flexibly generate/revoke a token (app.api.token.get_token). 
The new token generation endpoint (app.api.token.get_token) has a limitation: when a new token is issued, the old one is marked as invalid. This restriction was added to reduce the number of tokens issued to one partner on the one hand and flexibility in revoking all old/compromised tokens on the other hand.


The main endpoints for creating (app.api.subscription.add_subscription) and editing (app.api.subscription.update_subscription) subscriptions are available only for requests with a header containing a valid token (app.api.token_required). 
Partner sites cannot edit subscriptions that they did not create.

I have implemented tests that can be used as examples of working with the API:
1. New partner registration: tests.test_register.test_register
2. Token generation: tests.test_token.test_get_token
3. Adding a new subscription: tests.test_subscription.test_add_subscription
4. Subscription updating: tests.test_subscription.test_update_subscription

P.S. Registration of partners (app.main.views.register) is implemented as an example - use in production is prohibited.

## Project Setup

### Virtual Environment Setup

It is preferred to create a virtual environment per project, rather then installing all dependencies of each of your projects system wide. Once you install [virtual env](https://virtualenv.pypa.io/en/stable/installation/), and move to your projects directory through your terminal, you can set up a virtual env with:

```bash
virtualenv venv -p python3
```

This will create a python3.11 based virtual environment (venv) for you within your projects directory.

Note: You need to have [Python 3.11](https://www.python.org/downloads/release/python-311/) installed on your local device.

### Dependency installations

To install the necessary packages:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

This will install the required packages within your venv.

## Project Structure

### Main Modules

Every flask application has a top-level module for creating the app itself, in this case, this module is the `feel_me.py`. This contains the flask application, and is used by other services such as Gunicorn or Flask's CLI while serving the application.

The `feel_me.py` module relies on the `config.py` and the `app/__init__.py` modules. It uses one of the configs specified in the `.env` file to create an application through the `create_app` method, which is placed under the `__init__.py` module.

`app/__init__.py` ties the necessary packages such as your SQLAlchemy or Migrations wrappers to your app, and provides a nice function for generating an application with a pre-specified config.

`config.py` hold multiple configuration files, which can be used in different scenarios such as testing vs production.

### Models

The models, which are your database objects, are handled through SQLAlchemy's ORM. Flask provides a wrapper around the traditional SQLAlchemy package, which is used through out this project.

The models created are similar to your regular Python classes. They are inherited from pre-specified SQLAlchemy classes to make database table creation processes easier. These models can be found under the `app/models` folder.

In some projects, models can be handled within only one module, however in my opinion, it makes things easier when you handle them in multiple modules (one module per model).

If you want to create more models in your application, you can simply create modules under this folder, and later on tie them back to your app.

### API

The project creates a simple API which has 2 endpoints for creating, editing subscriptions. The API is structured by using Flask's `blueprint` functionality.

`api/subscription.py` module creates the endpoints, where the `api/__init__.py` creates the blueprint for API formation.

The blueprint object is later on imported and tied to the app in the `app/__init__.py` module.

### Main APP (Web Page)

The project also creates a very simple web page for creating partners. The flow for this logic is handled under the `app/main` folder.

Like the API, the web page relies on a blueprint, which is initiated in the `__init__.py` module.

The HTML and Static files for CSS required for rendering and styling web pages can be found under the `templates` and `static` folder. (Although there is nothing in the static folder at the moment)

### Logging

Logging is handled through flask's logger. However, custom handlers for logging are created under the `app/utils/log_config.py` module, which are tied to application when initiated with the docker config. (Can be found under the `config.py` module.)

The rotating handler creates rotating logs under the logs folder, while the stream handler logs to the terminal/client. Other logger handlers can be placed here such as an SMTP logger (for emailing errors).

---

## Database Choice & Operations

Usually for smaller projects, databases such as SQLite is preferred for the ease of use. However, in most of the production environments, these databases are never used so learning how to set them up might be useless for larger commercial projects.

Keeping this in mind, even though the project is quite small, I went the extra mile to setup a proper PostgreSQL database. The configurations for this database is specified under the `.env` file, and it is set as the default database.

Python uses `psycopg2` driver to connect to postgres databases. It quite easy to install psycopg2 on Linux based OS, however you may need to get Homebrew on your Mac to make your installation easier for you.

### Setting up a Postgres Database

Assuming that you have installed postgres database (if you haven't [Homebrew](https://gist.github.com/sgnl/609557ebacd3378f3b72) is the way I prefer for installations on Mac, and with [Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04), its even easier), you can easily setup a database through your terminal.

After reaching the postgres terminal through a `PSQL` command such as

```bash
sudo -u postgres psql
```

You can create a new user and make the user a superuser for your project by

```bash
create user tester with password 'password';
alter user tester superuser;
```

(Making the user a superuser makes things easier when creating tables or databases)

And then create a database and grant privileges locally by

```bash
create database stories;
grant all privileges on database stories to tester;
```

Granting privileges allows your user to make changes to your database.

Make sure you save these information, and add them to your `.env` file so your code can make changes to the database

On your `.env` file, you will want to set your `database_host` variable to `localhost`, and probably your database will be operating on port (`database_port`) `5432` unless specified otherwise.

For this case, your `database_name` will be `stories`, `database_user` will be `tester` and `database_password` will be `password`.

This should do it with the database setup!

### Migrations

Database migrations are handled through Flask's Migrate Package, which provides a wrapper around Alembic. Migrations are done for updating and creating necessary tables/entries in your database. Flask provides a neat way of handling these.

After exporting your flask CLI to point towards your application (for example in this case it can be done with):

```bash
export FLASK_APP=feel_me.py
```

You can find the necessary database commands with:

```bash
flask db
```

Initially, if you were to create an app from scratch, you would need to initiate your migrations with:

```bash
flask db init
```

In this case migrations folder is already there. So, you won't have to initiate it. Once you start altering your models, you will need to create a new migrations scripts. For example, if you add or remove fields from the existing models or create new models you would need to generate new migrations and update your database.

For generating new migrations, you can use:

```bash
flask db migrate
```

And for applying your new migrations to your database, you can use:

```bash
flask db upgrade
```

The project also creates a shortcut for upgrading, which is added to Flask's CLI:

```bash
flask deploy
```

---

## Running the Application

Once you have setup your database, you are ready to run the application.
Assuming that you have exported your app's path by:

```bash
export FLASK_APP=feel_me.py
```

You can go ahead and run the application with a simple command:

```bash
flask run
```

You can also run your app using [Gunicorn](http://gunicorn.org/), which a separate WSGI Server that plays very well with Flask:

```bash
gunicorn --reload feel_me:app
```

---

## Docker Setup

The project also has docker functionality, which means if you have docker installed on your computer, you can run it using Docker as well!

Docker creates containers for you, and basically serves your application using these containers. The necessary setting files for the docker setup can be found under `docker-compose.yaml` and `Dockerfile` it self.

In this case, docker uses a prebuilt Python3.11 image that runs on Ubuntu, and creates Nginx reverse proxy and Postgres database containers to serve the application.

To build the docker image, fist, set your `ENV` variable within your `.env` file to `docker`.

And then, run:

```bash
sudo docker-compose up --build
```

Once its built, it will do the necessary migrations for your application, and your app will be running straight away. You do not need to specify the `--build` command a second time to run the docker compose instance:

```bash
sudo docker-compose up
```

Docker becomes especially useful while deploying your applications on servers, and makes the DevOps easier. You can read more about [docker](https://www.docker.com/).

---
