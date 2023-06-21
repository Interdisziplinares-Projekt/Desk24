from setuptools import setup, find_packages
import subprocess

version = "2.0"

def getRequirements():
    # Öffnet die Datei 'requirements.txt' im Lesemodus
    with open('requirements.txt', 'r') as file:
        # Liest den Inhalt der Datei und gibt ihn als Liste von Zeilen zurück
        return file.readlines()

    # Falls die Datei nicht gefunden oder nicht lesbar ist, wird eine leere Liste zurückgegeben
    return []

setup(
    name='desk24',
    packages=find_packages(),
    version='2.0.dev1',  # Setzt die Versionsnummer des Pakets auf '2.0.dev1'
    include_package_data=True,
    install_requires=getRequirements(),  # Verwendet die Funktion, um die erforderlichen Pakete aus 'requirements.txt' zu laden
)