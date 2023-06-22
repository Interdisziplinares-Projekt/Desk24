# Einführung
Desk24 ist eine intuitive Webanwendung, die es Ihren Mitarbeitern ermöglicht, Tische und Sitzplätze ohne umfangreiches Vorwissen zu buchen. Mit Desk24 können Benutzer einfach einen Tisch für einen bestimmten Tag und Zeitraum reservieren, alle Buchungen einsehen, bei Bedarf stornieren und Feedback zu den Sitzplätzen geben. Als Administrator haben Sie die Möglichkeit, alle Buchungen einzusehen, eine umfassende Statistik zu generieren und neue Zonen anzulegen, die beispielsweise als Stockwerke betrachtet werden können.

Desk24 bietet eine benutzerfreundliche Oberfläche, die es Ihren Mitarbeitern ermöglicht, bequem auf die verfügbaren Sitzplätze zuzugreifen und diese zu reservieren. Es erfordert kein umfangreiches technisches Know-how, sodass Ihre Mitarbeiter schnell und einfach mit der Buchung von Tischen und Sitzplätzen beginnen können.

Als Administrator haben Sie die Kontrolle über das gesamte System. Sie können alle Buchungen einsehen und verwalten, um sicherzustellen, dass alles reibungslos abläuft. Desk24 ermöglicht es Ihnen auch, benutzerdefinierte Zonen einzurichten, die den verschiedenen Bereichen Ihres Unternehmens entsprechen. Dies kann nützlich sein, um beispielsweise verschiedene Stockwerke, Abteilungen oder Teams zu repräsentieren.

Desk24 bietet außerdem umfassende Analysemöglichkeiten. Als Administrator können Sie Statistiken generieren, um Einblicke in die Auslastung der Sitzplätze, beliebte Buchungszeiten oder andere relevante Metriken zu erhalten. Diese Informationen können dabei helfen, Ressourcen effizienter zu nutzen und die Arbeitsumgebung für Ihre Mitarbeiter zu optimieren.

Mit Desk24 können Sie den Buchungsprozess vereinfachen, die Transparenz verbessern und die Nutzung der verfügbaren Sitzplätze maximieren. Ganz gleich, ob es sich um ein Büro, ein Coworking-Space oder eine öffentliche Einrichtung handelt, Desk24 ist die ideale Lösung, um Ihre Arbeitsplatzbuchungen effizient zu verwalten und das Nutzererlebnis zu verbessern.

# Installation

### Ubuntu
```bash
#Docker installation
sudo apt-get update

sudo apt-get install ca-certificates curl gnupg

sudo install -m 0755 -d /etc/apt/keyrings

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

``` bash

git clone https://github.com/Interdisziplinares-Projekt/Desk24.git
cd desk24
(sudo) docker compose -f demo_compose.yaml up
```


### Windows
Um unter Windows Docker Desktop zum laufen zu bekommen folgen sie bitte der Anleitung unter diesem link [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)

```powershell
git clone https://github.com/Interdisziplinares-Projekt/Desk24.git
cd desk24
docker compose -f demo_compose.yaml up
```

### Mac
Für die Installation von Docker Desktop folgenden sie bitte dieser Anleitung [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/)

```terminal
git clone https://github.com/Interdisziplinares-Projekt/Desk24.git
cd desk24
docker compose -f demo_compose.yaml up
```


### Login 
Auf die Webanwendung kommen sie mit http://127.0.0.1:80 und die Login Daten für den Admin sind **Admin** und als Passwort **noneshallpass** 


# Entwicklerinstallation
### Ubuntu
```bash
#python3
sudo apt update && sudo apt upgrade
sudo apt install python3 python3-pip


#nodejs, npm und nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
source ~/.nvm/nvm.sh
nvm --version
nvm install node

node --version
npm --version


#postgresql
sudo apt update && sudo apt upgrade
sudo apt install postgresql

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
git clone https://github.com/Interdisziplinares-Projekt/Desk24.git
cd desk24

pip3 install -r requirements.txt


pushd js
npm ci
npm run build
popd

export FLASK_APP=desk24
export FLASK_ENV=development

flask run
```


### Zugriff ohne Installation
Da wir niemanden zwingen möchten, Docker zu installieren, und die Installation für Entwickler ebenfalls etwas komplexer ist, haben wir in Absprache mit dem Fachschaftsrat einen Raspberry Pi an der Jade HS installiert. Auf diesem Raspberry Pi läuft die Serverseite der Anwendung. Das bedeutet, dass Sie über folgenden Link [Desk24]() auf die Webseite zugreifen können, solange Sie sich in der Jade HS befinden oder über VPN mit der Jade HS verbunden sind.


# Fehlerbehebung
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



# Entwicklung
Um am Projekt Desk24 mitzuwirken, bitten wir Sie, wie folgt vorzugehen:

Erstellen Sie einen Fork des Repositories, indem Sie auf den "Fork" Button oben rechts auf der GitHub-Seite klicken. Dadurch wird eine Kopie des Repositories in Ihrem eigenen GitHub-Account erstellt.

Klonen Sie nun das geforkte Repository auf Ihren lokalen Computer, indem Sie den folgenden Befehl in Ihrem Terminal oder Ihrer Eingabeaufforderung ausführen:

```bash
Copy code
git clone <URL Ihres geforkten Repositories>
```
Ersetzen Sie <URL Ihres geforkten Repositories> durch den URL-Link zu Ihrem geforkten Repository.

Fügen Sie Ihre Änderungen zu Ihrem lokalen Repository hinzu und führen Sie die entsprechenden Git-Befehle aus, um Ihre Änderungen zu commiten und zu pushen. Dies kann beispielsweise die Aktualisierung von Code, das Hinzufügen neuer Funktionen oder das Beheben von Fehlern beinhalten.

Öffnen Sie einen neuen Pull Request (PR), um Ihre Änderungen in das ursprüngliche Projekt einzubringen. Gehen Sie dazu auf die GitHub-Seite Ihres geforkten Repositories, klicken Sie auf den "Pull Request" Button und folgen Sie den Anweisungen, um den PR zu erstellen.

Wir werden Ihre Änderungen überprüfen und in das Hauptprojekt integrieren, sofern sie den Anforderungen und Richtlinien entsprechen.

Vielen Dank für Ihre Mitwirkung am Desk24-Projekt!


# Feature Driven Development (FDD)
Um eine einheitliche Softwareentwicklungsmethode aus dem agilen Bereich zu verwenden, haben wir uns für das Feature Driven Development (FDD) entschieden. Das Feature Driven Development ist eine agile Softwareentwicklungsmethode, die sich auf die iterative und inkrementelle Entwicklung von Software konzentriert. Sie legt einen starken Fokus auf die Definition und Umsetzung von Features, die einen messbaren Mehrwert für den Benutzer bieten.

![Git Graph](./res/assets/git_graph.png)