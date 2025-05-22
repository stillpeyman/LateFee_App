from .models import db, User, Movie
from .data_manager_interface import DataManagerInterface


class SQLiteDataManager(DataManagerInterface):
    
    def get_all_users(self):
        return User.query.all()

    def get_user_movies(self, user_id):
        return Movie.query.filter_by(user_id=user_id).all()

    def add_movie(self, movie):
        db.session.add(movie)
        db.session.commit()

    def update_movie(self, movie):
        existing = Movie.query.get(movie.id)
        if not existing:
            return False
        existing.name = movie.name
        existing.director = movie.director
        existing.year = movie.year
        existing.rating = movie.rating
        return True

    def delete_movie(self, movie_id):
        movie = Movie.query.get(movie_id)
        if not movie:
            return False
        db.session.delete(movie)
        db.session.commit()
        return True

