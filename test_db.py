from app import app, data_manager
from datamanager.models import User, Movie, db


def run_tests():
    with app.app_context():
    #     # Clean up any existing data for repeatability
    #     Movie.query.delete()
    #     User.query.delete()
    #     db.session.commit()

        # Define users and their movies
        users_data = [
            {
                "name": "Alice",
                "movies": [
                    {"name": "Inception", "director": "Christopher Nolan", "year": 2010, "rating": 9.0},
                    {"name": "The Matrix", "director": "Wachowski Sisters", "year": 1999, "rating": 8.7}
                ]
            },
            {
                "name": "Bob",
                "movies": [
                    {"name": "Interstellar", "director": "Christopher Nolan", "year": 2014, "rating": 8.6},
                    {"name": "The Godfather", "director": "Francis Ford Coppola", "year": 1972, "rating": 9.2}
                ]
            }
        ]

        users = []
        movies = []

        # Create users and their movies
        for user_data in users_data:
            user = User(name=user_data["name"])
            db.session.add(user)
            db.session.commit()  # Commit to assign user.id
            users.append(user)
            print(f"Added user: {user}")

            for m in user_data["movies"]:
                movie = Movie(
                    name=m["name"],
                    director=m["director"],
                    year=m["year"],
                    rating=m["rating"],
                    user_id=user.id
                )
                data_manager.add_movie(movie)
                movies.append(movie)
                print(f"    Added movie: {movie}")

        # Query all users
        all_users = data_manager.get_all_users()
        print("\nAll users in DB:")
        for user in all_users:
            print(user)

        # Query movies for each user
        print("\nMovies for each user:")
        for user in users:
            user_movies = data_manager.get_user_movies(user.id)
            print(f"User {user.name} (id={user.id}):")
            for movie in user_movies:
                print(f"  {movie}")

        # # Update a movie for Alice
        # alice = users[0]
        # alice_movies = data_manager.get_user_movies(alice.id)
        # if alice_movies:
        #     movie_to_update = alice_movies[0]
        #     movie_to_update.name = "Inception [Edited]"
        #     data_manager.update_movie(movie_to_update)
        #     print(f"\nUpdated Alice's movie: {movie_to_update}")

        # # Delete a movie for Bob
        # bob = users[1]
        # bob_movies = data_manager.get_user_movies(bob.id)
        # if bob_movies:
        #     movie_to_delete = bob_movies[1]
        #     data_manager.delete_movie(movie_to_delete.id)
        #     print(f"\nDeleted Bob's movie: {movie_to_delete}")

        # Final state
        print("\nFinal users and their movies:")
        for user in data_manager.get_all_users():
            print(user)
            for movie in data_manager.get_user_movies(user.id):
                print(f"  {movie}")


if __name__ == "__main__":
    run_tests()
