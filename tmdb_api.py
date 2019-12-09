import unittest
import json
import requests
import os
import sqlite3

def get_api_data_popular():
    # Get 120 most popular movies from TMDB
    api_key = 'b45e2b59312812bca0659be8b753a532'
    baseurl= "https://api.themoviedb.org/3/movie/popular?api_key={}&language=en-US&page={}"
    popular_list = []

    # Each fetch returns 20 movies on a page
    # This iterates 6 times to return 120 movies
    for num in range(1,7):
        popular_url = baseurl.format(api_key, num)
        r = requests.get(popular_url)
        data = json.loads(r.text)
        results = data["results"]
        popular_list = popular_list + results
    return popular_list

def create_cache(pop_results):
    # Cache was created on 12/4/19 at 9:15 PM

    dir_path = os.path.dirname(os.path.realpath(__file__))
    cache_file = dir_path + '/' + "popular_movies.json"

    movie_results = {}
    movie_results['results'] = pop_results

    with open (cache_file, 'w') as outfile:
        json.dump(movie_results, outfile, indent = 2)

def load_from_cache():

    dir_path = os.path.dirname(os.path.realpath(__file__))
    cache_file = dir_path + '/' + "popular_movies.json"
    with open (cache_file, 'r') as infile:
        st = infile.read()
        dic = json.loads(st)
        results = dic.get("results")
    
    return results

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def setUpPopularityTable(results, cur, conn):
    titles = [] # We don't want any repeat titles

    cur.execute("DROP TABLE IF EXISTS Popularity")
    cur.execute("CREATE TABLE Popularity (title TEXT PRIMARY KEY, release_date DATE, popularity REAL)")
    for movie in results:
        title = movie.get("title")

        if title not in titles:
            titles.append(title)
            release_date = movie.get('release_date')
            pop = movie.get("popularity")
            cur.execute("INSERT INTO Popularity (title, release_date, popularity) VALUES (?,?,?)",(title, release_date, pop))
            
    conn.commit()


class TestAllMethods(unittest.TestCase):
    # def test_get_api_data_popular(self):
    #     results_dict = get_api_data_popular()
    #     self.assertEqual(len(results_dict), 100) # Testing if 100 movies are added
    #     self.assertFalse(results_dict[0] == results_dict[20]) # Testing if unique pages were returned

    def load_from_cache(self):
        tmdb_cache = load_from_cache()
        self.assertEqual(len(tmdb_cache), 120)
        self.assertEqual(tmdb_cache[0]['title'], "Frozen II")

def main():
    ### Only ran these to get popular movies once
    ### Popular movies are dynamic and change with time
    ### Made one cache so data is consistent

    # results = get_api_data_popular()
    # create_cache(results)

    results = load_from_cache()
    db_name = "movies.db"
    cur, conn = setUpDatabase(db_name)
    setUpPopularityTable(results, cur, conn)
    conn.close()

    

if __name__ == "__main__":
    main()
    unittest.main(verbosity = 2)