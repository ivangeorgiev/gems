Movielens with Django Rest Framework Kata
==========================================================

The goal of this kata is to create a browasble API, using MovieLens database.

#. Download the small MovieLens database from https://grouplens.org/datasets/movielens/latest/ into `ml-latest-small` workspaceFolder
#. Examine the content of the files. You are going to import `movies.csv` and `links.csv`
#. Create Django project and application
#. Create `Movie` model
#. Create `MovieLink` model
#. Update your model to support movie genres stored into a single column in `movies.csv`
#. Use Django management command to create cli for importing `movies.csv`
#. Add cli for importing `links.csv`
#. Create `api/movies/` api which returns list of movies, e.g.
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

#. Paginate the response from the `movies` API
#. Implement filter on the `movies` API which looks for movies which title includes given string.


.. collapse:: Solution 1

   https://github.com/ivangeorgiev/movielens-drf

