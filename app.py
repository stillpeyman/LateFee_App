from flask import Flask, render_template, request, redirect, url_for, flash
from datamanager.models import db, User, Movie
from datamanager.sqlite_data_manager import SQLiteDataManager
from api.omdb_api import get_movie_data as omdb
from dotenv import load_dotenv
import os


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'data', 'moviwebapp.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path

# Connect Flask app to SQLAlchemy (db)
db.init_app(app)
# Create instance of SQLiteDataManager
data_manager = SQLiteDataManager()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<int:user_id>')
def user_movies(user_id):
    user = User.query.get(user_id)
    movies = data_manager.get_user_movies(user_id)
    return render_template('user_movies.html', user=user, movies=movies)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form.get('name')
        user = User(name=name)
        db.session.add(user)
        db.session.commit()

        flash(f"User '{name}' added successfully!")

        return redirect(url_for('list_users'))
    
    # GET: show the form
    return render_template('add_user.html') 


@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    if request.method == 'POST':
        title = request.form.get('name')

        try:
            movie_data = omdb(title)

        except ValueError as e:
            flash(f'Error: {str(e)}')
            return redirect(url_for('add_movie', user_id=user_id))
        
        # Extract data from OMDb response
        movie = Movie(
            name=movie_data['Title'],
            director=movie_data['Director'],
            year=int(movie_data['Year']),
            rating=float(movie_data['imdbRating']),
            poster=movie_data['Poster'],
            user_id=user_id
        )

        data_manager.add_movie(movie)
        flash(f"Movie '{movie.name}' added successfully!")
        return redirect(url_for('user_movies', user_id=user_id))
    
    # GET: shwo the form
    return render_template('add_movie.html', user_id=user_id)


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    movie = Movie.query.get(movie_id)

    if request.method == 'POST':
        # Update movie data from form
        movie.name = request.form.get('name', movie.name)
        movie.director = request.form.get('director', movie.director)
        movie.year = request.form.get('year', movie.year)
        movie.rating = request.form.get('rating', movie.rating)

        db.session.commit()
        flash(f"Movie '{movie.name}' updated successfully!")

    # GET: show pre-filled form
    return render_template('update_movie.html', user_id=user_id, movie=movie)


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['POST'])
def delete_movie(user_id, movie_id):

    if data_manager.delete_movie(movie_id):
        flash(f"MovieID '{movie_id}' deleted successfully!")
    else:
        flash('Movie not found.')

    return redirect(url_for('user_movies', user_id=user_id))


if __name__ == '__main__':
    app.run(debug=True)




