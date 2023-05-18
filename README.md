# Desk24

## Deployment

During the first run on an empty database, WARP will populate the database schema and create an admin user.

Default admin credentials are: `admin:noneshallpass`

## Demo quickstart

The preferred way to deploy is to run it via Docker. You need a working docker, and I won't cover it here.

### docker compose

From the command line:
```
# clone the repository
$ git clone https://github.com/sebo-b/warp.git
$ cd warp

$ docker compose -f demo_compose.yaml up
```

After that, open http://127.0.0.1:8080 in your browser and log in as `admin` with password `noneshallpass`.

### Debvelopment

You need a working Python3 environment, Node.js, and PostgreSQL.

From the command line:

Aufsetzen von der PostgreSQL unter Ubuntu
```
# Installation
sudo apt-get update

sudo apt-get install postgresql

sudo systemctl status postgresql

# Datenbank und nutzern anlegen
sudo -u postgres psql

CREATE USER warp WITH PASSWORD 'warp';

CREATE DATABASE warp;

GRANT ALL PRIVILEGES ON DATABASE warp TO warp;

# Testen
psql -U warp -d warp -h localhost -p 5432
```

```
# clone repo
$ git clone https://github.com/sebo-b/warp.git
$ cd warp

# create virtual envirnoment and activate it
$ python3 -m venv --prompt warp .venv
$ source .venv/bin/activate

# install python requirements
$ pip install -r requirements.txt

# compile JavaScript files
$ pushd js
$ npm ci
$ npm run build
$ popd

# setup Flask and database URL
$ export FLASK_APP=warp
$ export FLASK_ENV=development
$ export WARP_DATABASE=postgresql://warp:warp@localhost:5432/warp

# run the app
$ flask run
```

After that, open http://127.0.0.1:5000 in your browser and log in as `admin` with password `noneshallpass`.



### Bekannte Probleme
Sollte die .env variable im code keinenw ert finden kann das daran liegen das flask auf einer zu neuern version ist 
```bash
flask --version
```
es kann also sein das ihr die version manuell auf 2.2 isntalliueren müsst 

```bash
(sudo) pip uninstall flask
pip install flask==2.2
```




### SECRET_KEY

For the production environment, **make sure** that you have generated `SECRET_KEY` used for signing cookies. It is defined in `config.py.`

Flask documentation mentions this method to generate it:
```
$ python -c 'import os; print(os.urandom(16))'
```

Alternatively, you can use OpenSSL and Sed:
```
$ openssl rand -hex 16 | sed 's/\(..\)/\\x\1/g;s/^/b"/;s/$/"/'
```
or wrap it into Python:
```
$ python -c 'from subprocess import run; print(run(["openssl","rand","16"],capture_output=True).stdout)'
```

### Language

Change `LANGUAGE_FILE` variable in `config.py` or set `WARP_LANGUAGE_FILE` environment variable. Currently, language is global for the instance.

### How to import users

You can add them manually one by one via the users' management tab or import them directly to the database. Basically, insert users to `user` table, look at the table definition in `warp/sql/schema.sql.`

The role is one of:
```
10 - admin
20 - regular user
90 - account blocked
```

Password is a hash used by `werkzeug.security.check_password_hash` (more documentation can be [found here](https://werkzeug.palletsprojects.com/en/2.0.x/utils/#werkzeug.security.generate_password_hash)), by default (in my configuration) it is pbkdf2:sha256 with 16 bytes salt and 260,000 iterations.

You can generate it with Python (just make sure you have activated the environment where Flask is installed):
```
python -c 'from getpass import getpass; from werkzeug.security import generate_password_hash; print(generate_password_hash(getpass()))'

