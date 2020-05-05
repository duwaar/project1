from flask import Flask, session, request, render_template, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os
import time

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/", methods=["GET"])
def home_page():
    search_by = request.args.get("search_by")
    query = request.args.get("query")

    if query:
        if search_by == "title"\
                or search_by == "author"\
                or search_by == "isbn":
            results = db.execute(f"SELECT * FROM books WHERE {search_by} ILIKE '%{query}%';").fetchall()
        elif search_by == "year":
            results = db.execute(f"SELECT * FROM books WHERE {search_by} = {query};").fetchall()
    else:
        results = []
    
    return render_template("home.html", query=query, results=results)

def valid_login(username, password):
    account = db.execute(f"SELECT username, pw_hash FROM users WHERE username = '{username}'").fetchone()
    if password == account[1]:
        return True
    else:
        return False

@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        if valid_login(request.form.get("username"), request.form.get("password")):
            session["username"] = request.form.get("username")
            message = f"Welcome back to BookReader, {session.get('username')}!"
        else:
            message = "Invalid login."
    else:
        message = "Enter your login information."

    return render_template("login.html", message=message)

@app.route("/logout", methods=["GET", "POST"])
def logout_page():
    if request.method == "POST":
        session["username"] = None
        message = "You have been logged out."
    else:
        message = "Click the button to log out."

    return render_template("logout.html", message=message)

def check_reg_form(form_data):
    success = False
    if form_data.get("email") == "":
        message = "You must enter an email address."
    elif len(form_data.get("username")) < 5\
            or len(form_data.get("username")) > 20:
        message = "Username must be between 5 and 20 characters long."
    elif db.execute(f"SELECT id FROM users WHERE username = '{form_data.get('username')}';").fetchall():
        message = f"An account with the username \"{form_data.get('username')}\" already exists."
    elif len(form_data.get("password")) < 6\
            or len(form_data.get("password")) > 50:
        message = "Password must be between 6 and 50 characters long."
    elif form_data.get("password") == form_data.get("username"):
        message = "Please do not make your password the same as your username."
    elif form_data.get("password") != form_data.get("re_pword"):
        message = "You re-typed your password incorrectly."
    else:
        success = True
        message = "Form filled correctly."
    
    return success, message

@app.route("/register", methods=["GET", "POST"])
def register_page():
    if request.method == "POST":
        reg_valid, err_message = check_reg_form(request.form)
        if reg_valid:
            db.execute(f"INSERT INTO users (username, pw_hash, email) VALUES (:username, :pw_hash, :email);",\
                    {"username":request.form.get("username"), "pw_hash":request.form.get("password"), "email":request.form.get("email")})
            db.commit()
            #user_id = db.execute(f"SELECT id FROM users WHERE username = '{request.form.get('username')}';").fetchall()[0][0]
            message = f"Yay! You have registered as {request.form.get('username')}. Welcome to Bookreader!"
        else:
            message = err_message
    else:
        message = "Please fill out the form."

    return render_template("register.html", message=message)

@app.route("/book/<string:book_isbn>", methods=["GET", "POST"])
def book_page(book_isbn):
    db_result = db.execute(f"SELECT id, title, author, year, isbn FROM books WHERE isbn = '{book_isbn}';").fetchone()
    book_data = {'id':'', 'title':'', 'author':'', 'year':'', 'isbn':''}
    if db_result:
        book_data['id']     = db_result[0]
        book_data['title']  = db_result[1]
        book_data['author'] = db_result[2]
        book_data['year']   = db_result[3]
        book_data['isbn']   = db_result[4]

    return render_template("book.html", book_data=book_data)

@app.route("/submit_read/<string:book_isbn>", methods=["GET", "POST"])
def submit_read_page(book_isbn):
    if request.method == "POST" and session['username']:
        user_id = db.execute(f"SELECT id FROM users WHERE username = '{session['username']}';").fetchone()[0]
        book_id = db.execute(f"SELECT id FROM books WHERE isbn = '{book_isbn}';").fetchone()[0]

        db.execute("INSERT INTO reads (user_id, book_id, rating, review, date) VALUES (:user_id, :book_id, :rating, :review, :date);",\
                {"user_id":user_id, "book_id":book_id, "rating":request.form.get("stars"), "review":request.form.get("review"), "date":time.asctime()})
        db.commit()

        return redirect(url_for('book_page', book_isbn=book_isbn))

    return render_template("submit_read.html", book_isbn=book_isbn)