from storage_api import movie_storage_sql as storage
from movies_omdb_api import movie_omdb_api as movie_api
import random
import difflib
import matplotlib.pyplot as plt


def list_movies():
    """Retrieve and display all movies from the database."""
    movies = storage.list_movies()
    print(f'\n{len(movies)} movies in total')
    for movie in movies:
        print(f"{movie} ({movies[movie]['year']}) : {movies[movie]['rating']}")
    print()


def list_movies_spl(movies):
    """Retrieve and display all movies from the database."""
    print(f'\n{len(movies)} movies in total')
    for movie in movies:
        print(f"{movie} ({movies[movie]['year']}) : {movies[movie]['rating']}")
    print()


def add_movie(movie_name):
    """
    Add a new movie to the database if it doesn't already exist.
    """
    movies = storage.list_movies()
    for movie in movies:
        if movie_name.lower() == movie.lower():
            print('Movie already in the database.\n')
            return

    movie_info = movie_api.get_movie_info(movie_name)
    if movie_info is not None:
        storage.add_movie(movie_info['title'], year=movie_info['year'], rating=movie_info['rating'], image_link=movie_info['image_link'])


def delete_movie(movie_name):
    """
    Delete a movie from the database by its name.
    """
    movies = storage.list_movies()
    for movie in movies:
        if movie_name.lower() == movie.lower():
            storage.delete_movie(movie)
            return
    print(f"Movie {movie_name} doesn't exist.\n")
    return


def update_movie(movies, movie_name, movie_rating):
    """
    Update the rating of an existing movie.

    Args:
        movies (dict of dicts): Existing movie dictionaries.
        movie_name (str): Name of the movie to update.
        movie_rating (float): New rating value.

    Returns:
        dict of dicts: Updated dict of movies.
    """
    for movie in movies:
        if movie_name.lower() == movie.lower():
            movies[movie]['rating'] = movie_rating
            storage.update_movie(movie, movie_rating)
            print(f'Movie {movie} successfully updated.\n')
            return movies
    print(f"Movie {movie_name} doesn't exist.\n")
    return movies


def stats(movies):
    """
    Display statistics about the movie ratings:
    average, median, best-rated, and worst-rated movies.

    Args:
        movies (dict of dicts): Dict of movie dictionaries.
    """
    ratings = sorted(movies[movie]['rating'] for movie in movies)
    avg_rating = sum(ratings) / len(ratings)
    print(f'Average rating: {avg_rating:.2f}')

    ratings_len = len(ratings)
    if ratings_len % 2 == 1:
        median_rating = ratings[ratings_len // 2]
    else:
        median_rating = (ratings[ratings_len // 2 - 1] + \
                         ratings[ratings_len // 2]) / 2
    print(f'Median rating: {median_rating:.2f}')

    best = max(movies, key=lambda title: movies[title]['rating'])
    worst = min(movies, key=lambda title: movies[title]['rating'])
    print(f'Best movie: {best}, {movies[best]["rating"]}')
    print(f'Worst movie: {worst}, {movies[worst]["rating"]}\n')


def random_movie(movies):
    """
    Select and display a random movie from the list.

    Args:
        movies (dict of dicts): Dict of movie dictionaries.
    """
    movies_list = [movie for movie in movies]
    choice = random.choice(movies_list)
    print(f"Your movie for tonight: {choice}, rated {movies[choice]['rating']}\
            \n")


def search_movie(movies, search_term):
    """
    Search for movies whose names contain the search term (case-insensitive).
    If none found, suggest the closest match.

    Args:
        movies (dict of dicts): List of movie dictionaries.
        search_term (str): Substring to search for in movie names.
    """
    name_to_rating = {m: movies[m]['rating'] for m in movies}
    lookup = {m.lower(): m for m in movies}
    found = False

    for lower_name, original_name in lookup.items():
        if search_term.lower() in lower_name:
            print(f'{original_name}, Rating: {name_to_rating[original_name]}')
            found = True

    if not found:
        print(f'The movie "{search_term}" does not exist. Did you mean:')
        suggestions = difflib.get_close_matches(
            search_term, name_to_rating.keys(), n=1, cutoff=0.6
        )
        for suggestion in suggestions:
            print(f"{suggestion}, Rating: {name_to_rating[suggestion]}")
    print()


def movies_sorted_by_rating():
    """
    Print movies sorted in descending order by rating.

    Args:
        movies (dict of dicts): List of movie dictionaries.
    """
    movies = storage.list_movies()
    sorted_dict = {
      title: movies[title]
      for title in sorted(movies, key=lambda t: movies[t]['rating'], reverse=True)
    }
    list_movies_spl(sorted_dict)


def movies_sorted_chronological_order(choice):
    """
    Print movies sorted in chronological order by rating.

    Args:
        movies (dict of dicts): List of movie dictionaries.
    """
    reverse = True if choice == 'Y' else False
    movies = storage.list_movies()
    sorted_dict = {
      title: movies[title]
      for title in sorted(movies, key=lambda t: movies[t]['year'], reverse=reverse)
    }
    list_movies_spl(sorted_dict)


def filter_movies(movies, min_rating=0.0, start_year=0, end_year=9999):
    """
    Filter the movies based on rating, start year and end year.

    Args:
        movies (dict of dicts): List of movie dictionaries
        min_rating: Minimum rating of the listed movies
        start_year: Start year of the listed movies
        end_year:   End year of the listed movies
    """
    if not min_rating:
        min_rating = 0.0
    if not start_year:
        start_year = 0
    if not end_year:
        end_year = 9999
    print('Filtered Movies:')
    filtered_movies = dict()
    for movie in movies:
        if min_rating <= movies[movie]['rating'] and \
        start_year <= movies[movie]['year'] and \
        end_year >= movies[movie]['year']:
            filtered_movies[movie] = movies[movie]
    list_movies_spl(filtered_movies)


def create_rating_histogram(movies):
    """
    Generate and save a histogram of movie ratings to a file.

    Args:
        movies (dict of dicts): List of movie dictionaries.
    """
    ratings = [movies[title]['rating'] for title in movies]
    filename = input("Enter the filename to save the histogram\
    (e.g., ratings.png): ")
    plt.figure()
    plt.hist(ratings, bins=5, edgecolor='black')
    plt.title("Movie Ratings Histogram")
    plt.xlabel("Rating")
    plt.ylabel("Number of Movies")
    plt.savefig(filename)
    print(f"Histogram saved to {filename}\n")
    plt.close()

def serialize_movie(movies):
    """ Serializes the movies object data and produces a HTML string as output """
    output = ''
    for movie in movies:
        output += '<li>\n'
        output += '<div class ="movie" >\n'
        output += f'<img class ="movie-poster" src="{movies[movie]["image_link"]}"/>\n'
        output += f'<div class ="movie-title"> {movie}</div>\n'
        output += f'<div class ="movie-year"> {movies[movie]["year"]} </div>\n'
        output += '</div>\n'
        output += '</li>\n'
    return output


def generate_website():
    """ Generates the HTML code necessary for the website """
    movies = storage.list_movies()

    template_str = ''
    with open('static/index_template.html', 'r+') as f:
        template_str = f.read()

    final_output = template_str.replace('__TEMPLATE_MOVIE_GRID__', serialize_movie(movies))
    with open('static/index.html', 'w+') as f:
        f.write(final_output)
    print('Website was generated successfully.')


def get_input_from_user(input_str, error_str, data_type, q_type='y', allow_blank=False):
    """
    Gets the Input from the User with the right data type and then outputs the value.

    Args:
        input_str (string): The input question to be asked to user
        error_str (string): The error message displayed to user in case of an invalid input
        data_type (type object): The data type of the input given by the user
        q_type (str, optional): 'yes_no' in case it is a yes or a no type. Defaults to 'y'.
        allow_blank (bool, optional): whether input is allowed to be blank. Defaults to False.

    Returns:
        type depends on the data_type: Value as entered by the user
    """
    while True:
        try:
            if data_type == type("abc"):
                choice = input(input_str).strip()
                if not choice and not allow_blank:
                    print("Input String cannot be empty. Please try again!")
                    continue
                if q_type == 'yes_no' and (choice.upper() != 'Y' and choice.upper() != 'N'):
                    continue
                return choice
            elif data_type == type(1):
                choice = input(input_str).strip()
                if not choice and not allow_blank:
                    print("Input Integer value cannot be empty. Please try again!")
                    continue
                if allow_blank and not choice:
                    return choice
                return int(choice)
            elif data_type == type(1.0):
                choice = input(input_str).strip()
                if not choice and not allow_blank:
                    print("Input Float value cannot be empty. Please try again!")
                    continue
                if allow_blank and not choice:
                    return choice
                return float(choice)
        except ValueError:
            print(error_str)


def main():
    """
    Run the interactive Movies Database CLI.
    Offers a menu for listing, adding, deleting, updating, and analyzing
    movies.
    """
    movies = storage.list_movies()

    while True:
        print('****** My Movies Database ******')
        print('0. Exit')
        print('1. List movies')
        print('2. Add movie')
        print('3. Delete movie')
        print('4. Update movie rating')
        print('5. Stats')
        print('6. Random movie')
        print('7. Search movie')
        print('8. Movies sorted by rating')
        print('9. Generate website')
        print('10. Movies sorted chronologically')
        print('11. Filter Movies\n')

        try:
            choice = int(input('Enter choice (0-11): ').strip())
        except ValueError:
            print("Invalid input. Please enter a number between 0 and 11.\n")
            continue

        if choice == 1:
            movies = storage.list_movies()
            list_movies()
        elif choice == 2:
            movie_name = get_input_from_user('Enter new movie name: ', \
              'Invalid Input, Please enter a valid Movie name.', type("abc")
              )
            add_movie(movie_name)
        elif choice == 3:
            movie_name = get_input_from_user('Enter movie name to delete: ', \
              'Invalid Input, Please enter a valid Movie name.', type("abc")
              )
            delete_movie(movie_name)
        elif choice == 4:
            name = get_input_from_user('Enter movie name to update: ', \
              'Invalid Input, Please enter a valid Movie name.', type("abc")
              )
            rating = get_input_from_user('Enter new rating (0-10): ', \
              'Invalid Input, Please enter a valid Movie rating.', type(1.1)
              )
            update_movie(movies, name, rating)
        elif choice == 5:
            stats(movies)
        elif choice == 6:
            random_movie(movies)
        elif choice == 7:
            term = get_input_from_user(
              'Enter part of the movie name to search: ', 
              'Invalid Input, Please enter a valid Movie name.', type("abc")
              )
            search_movie(movies, term)
        elif choice == 8:
            movies_sorted_by_rating()
        elif choice == 9:
            generate_website()
        elif choice == 10:
            choice = get_input_from_user(
              'Do you want to see the latest movies first? Y/N: ',
              'Invalid Input, Please enter either Y or N', type("abc"),
              'yes_no'
            )
            movies_sorted_chronological_order(choice)
        elif choice == 11:
            min_rating = get_input_from_user(
                'Enter minimum rating (leave blank for no minimum rating):',
                'Invalid Input, Please enter a valid Movie rating', type(1.1),
                '', True
            )
            start_year = get_input_from_user(
                'Enter start year (leave blank for no start year): ',
                'Invalid Input, Please enter a valid Movie start year', type(1)
                , '', True
            )
            end_year = get_input_from_user(
                'Enter end year (leave blank for no end year):',
                'Invalid Input, Please enter a valid Movie end year', type(1),
                '', True
            )
            filter_movies(movies, min_rating, start_year, end_year)
        elif choice == 0:
            print('Bye!')
            break
        else:
            print('Invalid choice! Please enter a number between 0 and 11')


if __name__ == "__main__":
    main()
