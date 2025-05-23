from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    # List of movie objects for user, one-to-many-relationship
    # <backref> creates reverse reference/relationship in the other class
    movies = db.relationship('Movie', backref='user')

    def __repr__(self):
        """
        Returns a string that represents the object for debugging.

        Example:
            User(id = 1, name = 'Peyman')
        """
        return f"User(id = {self.id}, name = {self.name})"


class Movie(db.Model):
    
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False)
    director = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float)
    poster = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        """
        Returns a string that represents the object for debugging.

        Example:
            Movie(id = 1, title = 'Inception')
        """
        return f"Movie(id = {self.id}, name = {self.name})"
