import requests

OMDB_MAIN_URL_LINK = ' http://www.omdbapi.com/?i=tt3896198&apikey='

api_key = '1dc44a68'

movie_name = 'The Matrix'
def get_json_response_using_api(movie_name):
    movie_link = OMDB_MAIN_URL_LINK + api_key + '&t=' + movie_name

    try:
        res = requests.get(movie_link, timeout=10)
        res.raise_for_status()  # Raises HTTPError for 4xx/5xx status codes
        json_response = res.json()

        # Check if movie was not found in the response
        if json_response.get("Response") == "False":
            print(f"Movie not found: {json_response.get('Error')}")
            return None

        return json_response

    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return None

def get_movie_info(movie_name):
    title = ''
    year = ''
    rating = ''
    image_link = ''
    json_response = get_json_response_using_api(movie_name)
    if json_response is not None:
        title = json_response['Title']
        year = json_response['Year']
        rating = json_response['imdbRating']
        img_link = json_response['Poster']
        return {'title': title, 'year': year, 'rating': rating, 'image_link': img_link}
    return None
