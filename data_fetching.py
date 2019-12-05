import unittest
import sqlite3
import json
import requests
import os

def omdb_api():
    pass

def itunes_api():
    pass

def tmdb_api():
    tmdb_key = "b45e2b59312812bca0659be8b753a532"

    # Get 20 most popular movies from TMDB
    popular_url = "https://api.themoviedb.org/3/movie/popular?api_key=b45e2b59312812bca0659be8b753a532&language=en-US&page=1"
    r2 = requests.get(popular_url)
    pop_api = json.loads(r2.text)
    print(pop_api)
    pop_results = pop_api["results"] #The actual movies
    print(len(pop_results))


class TestAllMethods(unittest.TestCase):
    def test_omdb_api():
        pass
    def test_itunes_api():
        pass

    def test_tmdb_api():
        pass
def main():
    tmdb_api()

if __name__ == "__main__":
    main()
    unittest.main(verbosity = 2)