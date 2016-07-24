# view2d-django

## What it does

Plots the current position of the International Space Station, similar to websites like http://www.isstracker.com or http://iss.astroviewer.net. 

![-screenshot of view2d-](https://raw.githubusercontent.com/artur-scholz/view2d-django/master/docs/screenshot.png "screenshot")


## Purpose

The purpose of this tool is to demonstrate the capabilities of the [bokeh](http://bokeh.pydata.org) plotting library combined with the power of the Python web framework [Django](https://www.djangoproject.com). It is using Ajax requests every 1 second to update the ISS position on the world map.

## How to run it

The following install instructions are for Linux. Windows and Mac OS installations are carried out in similar fashion. I let you figure out the details.

The script uses Python 3. To install, visit https://www.python.org/downloads.

Get the repository:
```
git clone https://github.com/artur-scholz/view2d-django.git
```

Within the root folder of the project, create a virtual environment for the Python libraries to be downloaded:
```
virtualenv venv --python=python3
```
Activate the virtual environment:
```
source venv/bin/activate
```
Install the libraries:
```
pip install -r requirements.txt
```
Note: If this step fails because of the Pillow library, then run "sudo apt-get install libjpeg-dev zlib1g-dev" and the above pip command again.
Run the local django server:
```
cd view2d
python manage.py runserver
```
Navigate to the following URL with your browser:
```html
http://localhost:8000/view2d/
```

