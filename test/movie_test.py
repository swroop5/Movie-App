from storage_api.movie_storage_sql import add_movie, list_movies, delete_movie, update_movie

# Test adding a movie
add_movie("Inception", 2010, 8.8)
add_movie("Avengers Endgame", 2015, 8.4)
add_movie("The Matrix", 1997, 7.8)
add_movie("My Girl", 1994, 8.6)
add_movie("Deep Impact", 1999, 9.0)
add_movie("There is no Tomorrow", 2027, 9.5)

# Test listing movies
movies = list_movies()
print(movies)

# Test updating a movie's rating
update_movie("Inception", 9.0)
print(list_movies())

# Test deleting a movie
delete_movie("Inception")
print(list_movies())