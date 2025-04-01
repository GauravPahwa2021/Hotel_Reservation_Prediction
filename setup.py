from setuptools import setup, find_packages
from pathlib import Path

with open("requirements.txt",'r') as f:
    requirements = f.read().splitlines()


setup(
    name="Hotel_Reservation_Prediction_Project",
    version="0.0.1",
    author="Gaurav_Pahwa",
    packages=find_packages(),
    install_requires=requirements,
    python_requires=">=3.8",
)   