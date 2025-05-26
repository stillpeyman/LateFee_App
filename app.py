from flask import Flask, render_template, request, redirect, url_for, flash
from datamanager.models import db, User, Movie
from datamanager.sqlite_data_manager import SQLiteDataManager
from api.omdb_api import get_movie_data as omdb
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler
import os
import openai


# App and Config

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
openai.api_key = os.getenv('OPENAI_API_KEY')

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'data', 'latefee_movies.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path

# Connect Flask app to SQLAlchemy (db)
db.init_app(app)
# Create instance of SQLiteDataManager
data_manager = SQLiteDataManager()


# Logging Setup

if not os.path.exists('logs'):
    os.makedirs('logs')

file_handler = RotatingFileHandler(
    'logs/latefee_movies.log', 
    maxBytes=10240, 
    backupCount=3
    )
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
file_handler.setFormatter(formatter)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)


# Routes

@app.route('/')
def index():
    """
    Render the home page of the LateFee App.
    """
    return render_template('index.html')


@app.route('/users')
def list_users():
    """
    Display a list of all users.
    """
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<int:user_id>')
def user_movies(user_id):
    """
    Display all movies for a specific user.
    """
    user = User.query.get(user_id)
    if not user:
        flash('User not found')
        return redirect(url_for('list_users'))
    
    movies = data_manager.get_user_movies(user_id)
    return render_template('user_movies.html', user=user, movies=movies)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """
    Add a new user to the database.
    """
    if request.method == 'POST':
        name = request.form.get('name')
        if not name:
            flash('User name is required.')
            return redirect(url_for('add_user'))

        user = User(name=name)
        db.session.add(user)
        db.session.commit()
        app.logger.info(f"User '{name}' added.")
        flash(f"User '{name}' added successfully!")

        return redirect(url_for('list_users'))
    
    # GET: show the form
    return render_template('add_user.html') 


@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    """
    Add a new movie to a user's collection using OMDb API data.
    """
    if request.method == 'POST':
        title = request.form.get('name')
        year = request.form.get('year')

        if not title:
            flash('Movie title is required.')
            return redirect(url_for('add_movie', user_id=user_id))
        
        try:
            movie_data = omdb(title, year=year)

        except ValueError as e:
            app.logger.warning(f"OMDb API error for '{title}': {e}")
            flash(f'Error: {str(e)}')
            return redirect(url_for('add_movie', user_id=user_id))
        
        # Check for duplicate, <.first()> returns first result
        existing_movie = Movie.query.filter_by(
            name=movie_data.get('Title', 'Unknown Title'),
            user_id=user_id
        ).first()

        if existing_movie:
            app.logger.info(
                f"Dublicate movie '{existing_movie.name}' "
                f"for user {user_id}."
                )
            flash(f"Movie '{existing_movie.name}' is already in your collection!")
            return redirect(url_for('user_movies', user_id=user_id))
        
        # Extract data from OMDb response
        movie = Movie(
            name=movie_data.get('Title', 'Unknown Title'),
            director=movie_data.get('Director', 'Unknown Director'),
            year=int(movie_data.get('Year', 0)),
            rating=float(movie_data.get('imdbRating', 0)),
            poster=movie_data.get('Poster', ''),
            user_id=user_id
        )
        data_manager.add_movie(movie)
        app.logger.info(f"Movie '{movie.name}' added for user {user_id}.")
        flash(f"Movie '{movie.name}' added successfully!")

        return redirect(url_for('user_movies', user_id=user_id))
    
    # GET: show the form
    return render_template('add_movie.html', user_id=user_id)


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    """
    Update the details of a specific movie in a user's collection.
    """
    movie = Movie.query.get(movie_id)
    if not movie:
        flash('Movie not found.')
        return redirect(url_for('user_movies', user_id=user_id))

    if request.method == 'POST':
        name = request.form.get('name')
        director = request.form.get('director')
        year = request.form.get('year')
        rating = request.form.get('rating')

        # Only update fields that are not empty 
        if name:
            movie.name = name

        if director:
            movie.director = director

        if year:
            try:
                movie.year = int(year)
            except ValueError:
                flash('Year must be a number.')
                return redirect(url_for('user_movies', user_id=user_id))
            
        if rating:
            try:
                movie.rating = float(rating)
            except ValueError:
                flash('Rating must be a number.')
                return redirect(url_for('user_movies', user_id=user_id))

        db.session.commit()
        app.logger.info(
            f"Movie '{movie.name}' (ID {movie_id}) "
            f"updated for user {user_id}."
            )
        flash(f"Movie '{movie.name}' updated successfully!")

    # GET: show pre-filled form
    return render_template('update_movie.html', user_id=user_id, movie=movie)


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['POST'])
def delete_movie(user_id, movie_id):
    """
    Delete a specific movie from a user's collection.
    """
    if data_manager.delete_movie(movie_id):
        app.logger.info(
            f"Movie ID {movie_id} deleted "
            f"for user {user_id}."
            )
        flash(f"MovieID '{movie_id}' deleted successfully!")
    else:
        app.logger.warning(
            f"Tried to delete non-existent movie ID {movie_id} "
            f"for user {user_id}."
            )
        flash('Movie not found.')

    return redirect(url_for('user_movies', user_id=user_id))


@app.route('/users/<int:user_id>/<int:movie_id>/eye_of_the_duck')
def eye_of_the_duck(movie_id, user_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        flash('Movie not found.')
        return redirect(url_for('user_movies', user_id=user_id))
    
    prompt = (
        f"In film theory, the 'Eye of the Duck' " 
        f"is the most essential scene " 
        f"that reveals the heart or core of a movie. "
        f"For the movie '{movie.name}' "
        f"(directed by {movie.director}, {movie.year}), "
        f"describe what the 'Eye of the Duck' scene might be and explain why."
    )

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                    {
                        "role": "system",
                        "content": "You are a film critic who explains the 'Eye of the Duck' scene for movies."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
        print(response)
        explanation = response.choices[0].message.content
    
    except Exception as e:
        explanation = (
            f"Sorry, there was an error generating "
            f"the 'Eye of the Duck' explanation: {e}"
        )
    
    return render_template(
        'eye_of_the_duck.html', 
        movie=movie, 
        explanation=explanation
        )

    



# Error Handlers

@app.errorhandler(404)
def not_found_error(error):
    """
    Show a user-friendly 404 page if a route or resource is missing.
    """
    # <request.path> gives path portion of URL for current request
    app.logger.warning(f"404 Not found: {request.path}")
    return render_template(
        'error.html', 
        message="404 Not Found: The requested resource does not exist."
        ), 404


@app.errorhandler(405)
def method_not_allowed_error(error):
    """
    Show a clear message if the request method is not allowed for the route.
    """
    app.logger.warning(
        f"405 Method Not Allowed: {request.method} at {request.path}"
        )
    return render_template(
        'error.html', 
        message="405 Method Not Allowed: That method is not allowed for this URL."
        ), 405


@app.errorhandler(Exception)
def server_error(error):
    """
    Catch-all for unexpected errors, showing a generic error page.
    """
    # <exc_info=True> includes full exception traceback in log output
    app.logger.error(f"Unhandled Exception: {error}", exc_info=True)
    return render_template(
        'error.html', 
        message="An unexpected error occurred. Please try again later."
        ), 500


if __name__ == '__main__':
    app.run(debug=True)




