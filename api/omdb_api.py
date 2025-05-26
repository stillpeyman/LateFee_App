import json
import os
import logging
from dotenv import load_dotenv
import requests
import time


# Set up module-level logger, <__name__> holds name of this module
logger = logging.getLogger(__name__)


load_dotenv()
API_KEY = os.getenv("OMDB_API_KEY")
HOST = "www.omdbapi.com"


def get_movie_data(title, year=None, max_retries=3, timeout=5):
    """
    Fetch movie data from OMDb by title (optionally using year too) and save it to 'response.json'. Retry if the request fails due to network issues. Return the movie data as a dictionary.

    Raises:
        ValueError: If movie not found or API returns an error.
    """
    params = {
        'apikey': API_KEY,
        't': title
    }

    if year:
        # Only add year if provided
        params['y'] = year

    api_url = f"http://{HOST}/"

    # Retry logic
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(api_url, params=params, timeout=timeout)

            if response.status_code == 200:
                movie_data = response.json()

                if movie_data.get("Response") == "False":
                    logger.warning(
                        f"OMDb API error for {title}': "
                        f"{movie_data.get('Error', 'Unknown Error')}"
                        )
                    raise ValueError(movie_data.get("Error", "Unknown Error"))

                try:
                    with open("data/response.json", "w", encoding="utf-8") as handle:
                        json.dump(movie_data, handle, indent=4)

                except Exception as file_error:
                    logger.warning(
                        f"Could not write response.json: {file_error}"
                        )
                
                logger.info(f"Successfully fetched data for '{title}' from OMDb.")
                return movie_data

            else:
                logger.error(
                    f"HTTP error from OMDb ({response.status_code}) "
                    f"for '{title}'."
                    )
                # Retrying won't fix HTTP request errors (400s: e.g. Unauthorized, Forbidden, Not found)
                break

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            logger.warning(f"Attempt {attempt} failed: {e}")

            if attempt < max_retries:
                logger.info("Retrying ...")
                # wait 1 sec before retry
                time.sleep(1)

            else:
                logger.error(
                    f"Failed to fetch data from OMDb for "
                    f"'{title}' after {max_retries} attempts."
                    )
                raise ValueError(
                    f"Failed to fetch data from OMDb "
                    f"after {max_retries} attempts."
                    )

        except requests.exceptions.RequestException as e:
            logger.error(
                f"An unexpected requests error occurred "
                f"for '{title}': {e}")
            
            # Unlikely to succeed on retry
            break
    
    # Ensure the function never returns <None>, prevent AttributeError
    logger.error(
        f"Failed to fetch data from OMDb "
        f"for '{title}': Unknown error."
        )
    raise ValueError("Failed to fetch data from OMDb: Unknown error.")



