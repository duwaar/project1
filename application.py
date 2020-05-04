import os
from flask import Flask, session, request, render_template
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

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


@app.route("/")
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
            pass
            #redirect(error_page(f"Illegal query: {search_by}")
    else:
        results = []
    
    return render_template("home.html", query=query, results=results)

@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
    else:
        username = ""

    return render_template("login.html", success=False, username=username)

def check_reg_form(form_data):
    success = False
    if form_data["email"] == "":
        message = "You must enter an email address."
    elif len(form_data["username"]) < 5\
            or len(form_data["username"]) > 20:
        message = "Username must be between 5 and 20 characters long."
    elif db.execute(f"SELECT id FROM users WHERE username = '{form_data['username']}';").fetchall():
        message = f"An account with the username \"{form_data['username']}\" already exists."
    elif len(form_data["password"]) < 6\
            or len(form_data["password"]) > 50:
        message = "Password must be between 6 and 50 characters long."
    elif form_data["password"] == form_data["username"]:
        message = "Please do not make your password the same as your username."
    elif form_data["password"] != form_data["re_pword"]:
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
                    {"username":request.form["username"], "pw_hash":request.form["password"], "email":request.form["email"]})
            db.commit()
            #user_id = db.execute(f"SELECT id FROM users WHERE username = '{request.form['username']}';").fetchall()[0][0]
            message = f"Yay! You have registered as {request.form['username']}. Welcome to Bookreader!"
        else:
            message = err_message
    else:
        message = "Please fill out the form."

    return render_template("register.html", message=message)