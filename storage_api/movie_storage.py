import json

"""
def write_json():
  movies = {
      "The Shawshank Redemption": {"year": 1994, "rating": 9.5},
      "Pulp Fiction": {"year": 1994, "rating": 8.8},
      "The Room": {"year": 2003, "rating": 3.6},
      "The Godfather": {"year": 1972, "rating": 9.2},
      "The Dark Knight": {"year": 2008, "rating": 9.0},
      "Forrest Gump": {"year": 1994, "rating": 8.8},
      "Interstellar": {"year": 2014, "rating": 8.6},
      "Inception": {"year": 2010, "rating": 8.8},
      "Gladiator": {"year": 2000, "rating": 8.5},
      "The Matrix": {"year": 1999, "rating": 8.7},
}
  with open("data.json", "w", encoding="utf-8") as f:
    json.dump(movies, f, indent=2)


write_json()
"""

def get_movies(json_path='data.json'):
    """
    Returns a dictionary of dictionaries that
    contains the movies information in the database.

    The function loads the information from the JSON
    file and returns the data. 

    For example, the function may return:
    {
      "Titanic": {
        "rating": 9,
        "year": 1999
      },
      "..." {
        ...
      },
    }
    Args:
        json_path (str): Path to the JSON file. Defaults to 'data.json'.

    Returns:
        dict of dict: The loaded movie database.
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        movies = json.load(f)
    return movies

def save_movies(movies):
    """
    Gets all your movies as an argument and saves them to the JSON file.
    """
    with open('../database/data.json', 'w', encoding='utf-8') as f:
        json.dump(movies, f, indent=2)
    return movies


def add_movie(title, year, rating):
    """
    Adds a movie to the movies database.
    Loads the information from the JSON file, add the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies('../database/data.json')
    movies[title] = {'year': year, 'rating': rating}
    save_movies(movies)
    return movies


def delete_movie(title):
    """
    Deletes a movie from the movies database.
    Loads the information from the JSON file, deletes the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies('../database/data.json')
    del movies[title]
    save_movies(movies)
    return movies


def update_movie(title, rating):
    """
    Updates a movie from the movies database.
    Loads the information from the JSON file, updates the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies('../database/data.json')
    movies[title]['rating'] = rating
    save_movies(movies)
    return movies
  