Movielens with Django Rest Framework Kata
==========================================================

The goal of this kata is to create a browasble API as an interface to the MovieLens database.

Download the *small* MovieLens database from https://grouplens.org/datasets/movielens/latest/ and examine the content of the files. We are interested in
`movies.csv` and `links.csv` files.

Following are the requirements for this kata:

#. Django application with `Movie` and `MovieLink` models exists
#. The application model support movie genres from the `genres` column of `movies.csv` file
#. User can import `movies.csv` into the Movie model using cli
#. User can import `links.csv` into the MovieLink model using cli
#. The `api/movies/` REST API returns a list of all movies, e.g.

   .. code-block:: json

      [
        {
            "movie_id": 1,
            "genres": [
                "Adventure",
                "Animation",
                "Children",
                "Comedy",
                "Fantasy"
            ],
            "links": [
                "https://www.imdb.com/title/tt0114709",
                "https://www.themoviedb.org/movie/862"
            ],
            "title": "Toy Story (1995)"
        },
        {
            "movie_id": 2,
            "genres": [
                "Adventure",
                "Children",
                "Fantasy"
            ],
            "links": [
                "https://www.imdb.com/title/tt0113497",
                "https://www.themoviedb.org/movie/8844"
            ],
            "title": "Jumanji (1995)"
        }
      ]

#. The `movies` API response is paginated
#. The `movies` API can filter the result and return only movies which title includes given string


.. collapse:: Solution 1

   https://github.com/ivangeorgiev/movielens-drf

