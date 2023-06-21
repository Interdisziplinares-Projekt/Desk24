# Desk24
## Deployment

Bei der ersten Ausführung auf einer leeren Datenbank wird WARP das Datenbankschema erstellen und einen Administratorbenutzer erstellen.

Die Standardadministratorzugangsdaten sind: admin:noneshallpass

## Schnellstart der Demo

Die bevorzugte Methode zur Bereitstellung besteht darin, sie über Docker auszuführen. Sie benötigen ein funktionierendes Docker, und ich werde hier nicht darauf eingehen.

### docker compose

Terminal: 
``` bash

git clone https://github.com/sebo-b/warp.git
cd warp
docker compose -f demo_compose.yaml up
```

Danach öffnen Sie http://127.0.0.1:8080 in Ihrem Browser und melden sich als admin mit dem Passwort noneshallpass an.

### Entwicklung

Sie benötigen eine funktionierende Python3-Umgebung, Node.js und PostgreSQL.

Von der Befehlszeile aus:

Einrichten von PostgreSQL unter Ubuntu
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

```bash 
# clone repo
git clone https://github.com/sebo-b/warp.git
cd warp

# create virtual envirnoment and activate it
python3 -m venv --prompt warp .venv
source .venv/bin/activate

# install python requirements
pip install -r requirements.txt

# compile JavaScript files
pushd js
npm ci
npm run build
popd

# setup Flask and database URL
export FLASK_APP=desk24
export FLASK_ENV=development
export WARP_DATABASE=postgresql://warp:warp@localhost:5432/warp

$ flask run
```

Danach öffnen Sie http://127.0.0.1:5000 in Ihrem Browser und melden sich als admin mit dem Passwort noneshallpass an.



### Bekannte Probleme
Falls die .env-Variable im Code keinen Wert findet, kann dies daran liegen, dass Flask in einer zu neuen Version vorliegt und Node nicht aktuell genug ist.
```bash
node --version
flask --version
```
Wenn diese Befehle zeigen, dass Node unter 14.0 und Flask 2.3 ist, müssen einige Anpassungen vorgenommen werden:

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm list-remote
nvm install {latest-lts-version}

(sudo) pip uninstall flask
pip install flask==2.2
```






