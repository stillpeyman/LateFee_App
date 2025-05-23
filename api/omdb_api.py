import json
import os
from dotenv import load_dotenv
import requests
import time


load_dotenv()
API_KEY = os.getenv("API_KEY")
HOST = "www.omdbapi.com"


def get_movie_data(title, max_retries=3, timeout=5):
    """
    Fetch movie data from OMDb and save it to 'response.json'.
    Retry if the request fails due to network issues.
    Return the movie data as a dictionary.

    Raises:
        ValueError: If movie not found or API returns an error.
    """
    api_url = f"http://{HOST}/?apikey={API_KEY}&t={title}"

    # Retry logic
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(api_url, timeout=timeout)

            if response.status_code == 200:
                movie_data = response.json()

                if movie_data.get("Response") == "False":
                    # Get value of "Error" key from response.json, else return "Unknown Error!"
                    raise ValueError(movie_data.get("Error", "Unknown Error"))

                with open("data/response.json", "w", encoding="utf-8") as handle:
                    json.dump(movie_data, handle, indent=4)

                return movie_data

            else:
                print(f"Error occurred: {response.status_code}")
                # Retrying won't fix HTTP request errors (400s: e.g. Unauthorized, Forbidden, Not found)
                break

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            print(f"Attempt {attempt} failed: {e}")

            if attempt < max_retries:
                print("Retrying ...")
                # wait 1 sec before retry
                time.sleep(1)

            else:
                raise ValueError(f"Failed to fetch data from OMDb after {max_retries} attempts.")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            # Unlikely to succeed on retry
            break



