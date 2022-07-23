# Human-Skintone-Detection

#About the Project: 
=================== 
The project is to find out the skin tone of a person and then classify them into different categories like ‘fair’, ‘mild’, or ‘dark.
The user can upload the images which are to be processed either by uploading a file from the local machine, or an online URL of the image.
The image as input must cover most part of the image with face for improved accuracy. Also, the image URL should be freely accessible online for the program to get the image from it.

#Features: 
========== 
Detects SkinTone of various types, like fair, mild and dark. User can input either by Uploading a file locally or upload the image link.

#What’s in the Project: 
======================= 
Web Development:
Frontend: HTML CSS Bootstrap JavaScript
Backend: Python Django
Machine Learning:
Algorithms Used:
kmeans clustering algorithm

#Requied Installations: 
======================= 
Python 3 https://www.python.org/
Django 3 https://www.djangoproject.com/
Following packages are required to be installed before running the project: 
Package Version Used In Project 
---------- -----------------------
Django 3.2.2
Flask 2.0.0
imutils 0.5.4
matplotlib 3.4.2
numpy 1.20.3
opencv-python 4.5.2.52
pandas 1.2.4
Pillow 8.2.0
requests 2.25.1
sklearn 0.0
xlrd 2.0.1

For installing these packages, open Command Prompt as Administrator and then type the following command: pip install <name_of_package>

#Running the Project: 
===================== 
Copy the path of your project directory 
Open Command Prompt Type the following and hit Enter: cd <path of the project you copied> 
Then run the project by: python manage.py runserver 
Copy the URL which is displayed and paste in your web browser.

#Common Issues: 
===============
ModuleNotFoundError: No module named 'xyz'.
Solution: Install that missing package using pip install <name_of_package>
You have x unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): ‘abc’, ‘def’, ‘ghi’.
Solution: Go inside the project directory using cd <path of the project> command and then write the following commands: python manage.py makemigrations python manage.py migrate
