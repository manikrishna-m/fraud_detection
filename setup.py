from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='MyDataScienceProject',
    version='0.1',
    packages=find_packages(),
    install_requires=requirements,  # Use the list from requirements.txt here
    author='Your Name',
    author_email='your.email@example.com',
    description='A small example package for data analysis',
    url='URL to project repository or project home page',
)
