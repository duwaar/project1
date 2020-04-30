import os

from flask import Flask, session, render_template
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv('DATABASE_URL'):
    raise RuntimeError('DATABASE_URL is not set')

# Configure session to use filesystem
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Set up database
engine = create_engine(os.getenv('DATABASE_URL'))
db = scoped_session(sessionmaker(bind=engine))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return 'The login page.'

@app.route('/register')
def register():
    return 'The registration page.'

@app.route('/search')
def search():
    return 'The search page.'

@app.route('/book/<int:book_id>')
def book_info(book_id):
    return 'The info page for book ' + str(book_id)

@app.route('/read/<int:book_id>')
def submit_read(book_id):
    return 'The reading/review submission page for book ' + str(book_id)