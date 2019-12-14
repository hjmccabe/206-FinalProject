import json
import requests
import os
import sqlite3

def get_popular_movie_titles():
    titles = []
    full_path = os.path.join(os.path.dirname(__file__), "popular_movies.json")
    f = open(full_path)
    file_data = f.read()
    f.close()
    popular_movies = json.loads(file_data)

    for page in range(1,9):
        key = "Page " + str(page)
        for movie in popular_movies[key]:
            title = movie["title"]
            titles.append(title)

    titles_no_repeat = []
    
    for movie in titles:
        if movie not in titles_no_repeat:
            titles_no_repeat.append(movie)

    # print(titles_no_repeat)
    return titles_no_repeat


def get_api_data(film):
    # Get 20 most popular movies from TMDB
    api_key = '975f8068'
    baseurl= "http://www.omdbapi.com/?t={}&apikey={}"
    movie_info = []

    ratings_url = baseurl.format(film, api_key)
    r = requests.get(ratings_url)
    data = json.loads(r.text)
    box_office = data.get("BoxOffice")
    try:
        box_office = int(box_office[1:].replace(',', ''))
    except:
        box_office = 0
    movie_name = data.get("Title")
    director = data.get("Director")
    ratings = data.get("Ratings")
    try:
        rotten_tomato = ratings[1].get("Value")
        rotten_tomato = int(rotten_tomato[:-1])
    except:
        rotten_tomato = 0

    movie_info = (movie_name, box_office, director, rotten_tomato)

    return movie_info

def make_cache(movie_info):
    # Cache was created on 12/7/19 at 9:45 PM

    dir_path = os.path.dirname(os.path.realpath(__file__))
    cache_file = dir_path + '/' + "omdb.json"

    movie_results = {}
    movie_results['results'] = movie_info

    with open (cache_file, 'w') as outfile:
        json.dump(movie_results, outfile, indent = 2)

def open_cache():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cache_file = dir_path + '/' + "omdb.json"
    with open (cache_file, 'r') as infile:
        st = infile.read()
        dic = json.loads(st)
        results = dic.get("results")
    
    return results

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS Directors")
    cur.execute("CREATE TABLE Directors (title TEXT PRIMARY KEY, director TEXT)")

    cur.execute("DROP TABLE IF EXISTS Ratings_and_Box")
    cur.execute("CREATE TABLE Ratings_and_Box (title TEXT PRIMARY KEY, box_office INT, rotten_tomatoes INT)")

    conn.commit()

    return cur, conn

def directors_table(movie, cur, conn):
    # Movie info: (Title, box office, director, rotten tomatoes)
    cur.execute("INSERT INTO Directors (title, director) VALUES (?,?)", (movie[0], movie[2]))
    conn.commit()

def bort_table(movie, cur, conn):
    # Excuse me, my son is also named 'Bort'
    # We need more Bort license plates in the Gift Shop. Repeat, we are sold out of Bort license plates.

    # Movie info: (Title, box office, director, rotten tomatoes)
    cur.execute("INSERT INTO Ratings_and_Box  (title, box_office, rotten_tomatoes) VALUES (?,?,?)",(movie[0], movie[1], movie[3]))
    conn.commit()

def main():
    cur, conn = setUpDatabase("movies_data.db")
    titles = get_popular_movie_titles()
    movie_info_list = []

    source = input("Do you want to get data from the cache or the API? (type 'cache', 'api', or 'quit')").lower()
    api_source = source == "api"
    cache_source = source == "cache"
    quit_source = source == 'quit'

    while((api_source == False) and (cache_source == False) and (quit_source == False)):
        source = input("Please type either type 'cache', 'api', or 'quit')").lower()
        api_source = source == "api"
        cache_source = source == "cache"
        quit_source = source == 'quit'

    try:
        if cache_source == True:
            movie_info_list = open_cache()
            for film in movie_info_list:
                directors_table(film, cur, conn)
                bort_table(film, cur, conn)

            conn.close()
    except:
        print("Please run from API since there is error with caching")
        api_source = True

    if api_source == True:
        for film in titles:
            movie = get_api_data(film)
            movie_info_list.append(movie)
            directors_table(movie, cur, conn)
            bort_table(movie, cur, conn)

        make_cache(movie_info_list)
        conn.close()

if __name__ == "__main__":
    main()