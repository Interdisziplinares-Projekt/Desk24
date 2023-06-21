from setuptools import setup, find_packages
import subprocess

version = "2.0"

def getRequirements():
    with open('requirements.txt', 'r') as file:
        return file.readlines()

    return []

setup(
    name='warp',
    packages=find_packages(),
    version='2.0.dev1',
    include_package_data=True,
    install_requires=getRequirements(),
)
