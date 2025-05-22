from flask import Flask, render_template, request, redirect, url_for, flash
from datamanager.models import db, User, Movie
from datamanager.sqlite_data_manager import SQLiteDataManager
import os


app = Flask(__name__)


basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'data', 'moviwebapp.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path

# Connect Flask app to SQLAlchemy (db)
db.init_app(app)
# Create instance of SQLiteDataManager
data_manager = SQLiteDataManager()


@app.route('/')
def home():
    return "Welcome to MovieWeb App!"


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return str(users)


if __name__ == '__main__':
    app.run(debug=True)




