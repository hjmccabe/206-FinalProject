import unittest
import json
import requests
import os
import sqlite3
import matplotlib.pyplot as plt

def get_api_data_popular(page):
    # Get 160 most popular movies from TMDB
    api_key = 'b45e2b59312812bca0659be8b753a532'
    baseurl= "https://api.themoviedb.org/3/movie/popular?api_key={}&language=en-US&page={}"
    popular_list = []

    # Each fetch returns 20 movies on a page
    # This iterates 8 times to return 160 movies
    popular_url = baseurl.format(api_key, page)
    r = requests.get(popular_url)
    data = json.loads(r.text)
    results = data["results"]

    # print(results)
    # for movie in results:
    #     popular_list = popular_list.append(movie)
    return results

def create_cache(pop_results):
    # Cache was created on 12/9/19 at 2:45 PM

    dir_path = os.path.dirname(os.path.realpath(__file__))
    cache_file = dir_path + '/' + "popular_movies.json"

    movie_results = {}
    key = "Page 1"
    movie_results[key] = pop_results

    with open (cache_file, 'w') as outfile:
        json.dump(movie_results, outfile, indent = 2)

def add_to_cache(pop_results, page):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cache_file = dir_path + '/' + "popular_movies.json"
    key = "Page " + str(page)
    with open (cache_file, 'r') as infile:
        st = infile.read()
        dic = json.loads(st)

    with open (cache_file, 'w') as outfile:
        dic[key] = pop_results
        json.dump(dic, outfile, indent = 2)

def load_from_cache(page):

    dir_path = os.path.dirname(os.path.realpath(__file__))
    cache_file = dir_path + '/' + "popular_movies.json"
    with open (cache_file, 'r') as infile:
        st = infile.read()
        dic = json.loads(st)
        key = "Page " + str(page)
        results = dic.get(key)
    
    return results

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def setUpPopularityTable(results, cur, conn):
    titles = [] # We don't want any repeat titles

    cur.execute("DROP TABLE IF EXISTS Popularity")
    cur.execute("CREATE TABLE Popularity (title TEXT PRIMARY KEY, popularity REAL)")
    for movie in results:
        title = movie.get("title")

        if title not in titles:
            titles.append(title)
            pop = movie.get("popularity")
            cur.execute("INSERT INTO Popularity (title, popularity) VALUES (?,?)",(title, pop))
            
    conn.commit()

    return titles

def setUpReleaseTable(results, cur, conn):
    titles = [] # We don't want any repeat titles
    cur.execute("DROP TABLE IF EXISTS ReleaseDates")
    cur.execute("CREATE TABLE ReleaseDates (title TEXT PRIMARY KEY, year INTEGER, full_date DATE)")

    for movie in results:
        title = movie.get("title")

        if title not in titles:
            titles.append(title)
            release_date = movie.get('release_date')
            release_year = int(release_date[0:4])
            cur.execute("INSERT INTO ReleaseDates (title, year, full_date) VALUES (?,?,?)",(title, release_year, release_date))

    conn.commit()





def updatePopularityTable(results, titles, cur, conn):
    for movie in results:
        title = movie.get("title")

        if title not in titles:
            titles.append(title)
            release_date = movie.get('release_date')
            pop = movie.get("popularity")
            cur.execute("INSERT INTO Popularity (title, release_date, popularity) VALUES (?,?,?)",(title, release_date, pop))
            
    conn.commit()

    return titles

def load_all_from_cache():
    all_results = []

    dir_path = os.path.dirname(os.path.realpath(__file__))
    cache_file = dir_path + '/' + "popular_movies.json"
    with open (cache_file, 'r') as infile:
        st = infile.read()
        dic = json.loads(st)

    for page in dic.keys():
        all_results = all_results + dic[page]

    return all_results


def visualization(all_results):


    years = []
    nums = []

    year_num_dic = {}

    for movie in all_results:
        release_year = int(movie.get("release_date")[0:4])
        if release_year in year_num_dic.keys():
            year_num_dic[release_year] += 1
        else:
            year_num_dic[release_year] = 1

    year_num_sorted = sorted(year_num_dic.items(), key = lambda x: x[0])

    for year in year_num_sorted:
        years.append(year[0])
        nums.append(year[1])
        
    # Create the bar graph
    fig, ax = plt.subplots()
    ax.bar(years, nums, color = '#762579')
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Popular Movies")
    ax.set_title("Number Popular Movies per Year")


    # Use these to make sure that your x axis labels fit on the page
    plt.xticks(rotation=90)
    plt.tight_layout()

    fig.savefig("pop_movies.png")
    plt.show()

def main():
    ### Only ran these to get popular movies once
    ### Popular movies are dynamic and change with time
    ### Made one cache so data is consistent

    # results_1 = get_api_data_popular(1)
    # create_cache(results_1)

    # db_name = "movies.db"
    # cur, conn = setUpDatabase(db_name)
    # titles = setUpPopularityTable(results_1, cur, conn)
    
    # for page in range(2,9):
    #     results = get_api_data_popular(page)
    #     add_to_cache(results, page)
    #     cache = load_from_cache(page)
    #     titles = updatePopularityTable(cache, titles, cur, conn)
       

    all_results = load_all_from_cache()
    db_name = "movies_data.db"
    cur, conn = setUpDatabase(db_name)
    titles = setUpPopularityTable(all_results, cur, conn)
    setUpReleaseTable(all_results, cur, conn)



    # visualization(all_results)
    conn.close()
    

if __name__ == "__main__":
    main()
    unittest.main(verbosity = 2)