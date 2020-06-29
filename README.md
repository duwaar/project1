# Project 1

CS50W: Web Programming with Python and JavaScript

I have created a web app called BookReader. You can review books and read reviews left by others.

## How to install and run this in Bash
- Clone the repository
- If you don't already have venv, install it
- Set up the python virtual environment and install dependencies
    $ python3 -m venv env
    $ . env/bin/activate
    $ pip install -r requirements.txt
- Start the Flask server
    $ ./start_flask.sh
- Start a browser and navigate to the Flask server URL
    http://127.0.0.1:5000

## File Descriptions
- books.csv is a file of book data provided by the instructors.
- import.py reads the book data out of books.csv and into the database.
- requirements.txt lists all the additional python packages installed.
- start_flask.sh is a shell script that sets some environment variables, activates the python virtual environment, and then starts a flask server.
- gr_api_key.txt is my API key from GoodReads.
- application.py contains all of the python code for the app. I considered making a separate file for the additional functions I created, but decided not to mess with it this time.
- static/styles/
  - styles.scss contains all my style code.
  - styles.css contains all the compiled CSS.
- templates/
  - layout.html is the base layout for all the pages. Mainly, it provides the navbar and the styles.
  - home.html is the homepage where you can search for books.
  - book.html is the template for displaying book data and reviews.
  - error.html is a generic error page, used when you request an ISBN that isn't in the database.
  - login.html contains the login form and also a separate form, which form directs you to the register page.
  - logout.html contains only a button to log the user out.
  - register.html contains a form for creating a new account.
  - submit_read.html contains the form for submitting a review.
