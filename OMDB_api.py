import unittest
import json
import requests
import os
import sqlite3
import matplotlib.pyplot as plt

def get_popular_movie_titles():
    titles = []
    full_path = os.path.join(os.path.dirname(__file__), "popular_movies.json")
    f = open(full_path)
    file_data = f.read()
    f.close()
    popular_movies = json.loads(file_data)

    for movie in popular_movies["results"]:
        title = movie["title"]
        titles.append(title)

    return titles


def get_api_data_all():
    # Get 20 most popular movies from TMDB
    api_key = '975f8068'
    baseurl= "http://www.omdbapi.com/?t={}&apikey={}"
    movie_info = []

    # Each fetch returns 1 movie per page
    # want 20 movies

    popular_movie_titles = get_popular_movie_titles()
    # print(popular_movie_titles)

    for title in popular_movie_titles: 
        ratings_url = baseurl.format(title, api_key)
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

        movie_info.append((movie_name, box_office, director, rotten_tomato))

    return movie_info

def make_cache(movie_info):
    # Cache was created on 12/7/19 at 9:45 PM

    dir_path = os.path.dirname(os.path.realpath(__file__))
    cache_file = dir_path + '/' + "omdb.json"

    movie_results = {}
    movie_results['results'] = movie_info

    with open (cache_file, 'w') as outfile:
        json.dump(movie_results, outfile, indent = 2)
    pass

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
    return cur, conn

def add_to_database(movie_info, cur, conn):
    titles = [] # We don't want any repeat titles


    cur.execute("DROP TABLE IF EXISTS OMDB")
    cur.execute("CREATE TABLE OMDB (title TEXT PRIMARY KEY, box_office INT, director TEXT, rotten_tomatoes INT)")
    for movie in movie_info:
        title = movie[0]
        if title not in titles:
            titles.append(title)
            if None in movie:
                continue
            cur.execute("INSERT INTO OMDB (title, box_office, director, rotten_tomatoes) VALUES (?,?,?,?)",(movie[0], movie[1], movie[2], movie[3]))
            conn.commit()
def boxoffice_by_rating(f):
    # Opening cache
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cache_file = dir_path + '/' + "omdb.json"
    with open (cache_file, 'r') as infile:
        st = infile.read()
        dic = json.loads(st)
        results = dic.get("results") #a list of lists
    
    # Getting average box office per rating
    total_dict = {}
    count80 = 0
    bo80 = 0
    avg80 = 0
    count60 = 0
    bo60 = 0
    avg60 = 0
    count40 = 0
    bo40 = 0
    avg40 = 0
    count20 = 0
    bo20 = 0
    avg20 = 0
    mvsucks = 0
    bomvsucks = 0 
    sucksavg = 0 
    for movie in results:
        boxoffice = movie[1]
        rating = movie[-1]
        if boxoffice != 0 and rating !=0:
            if rating >80:
                count80+= 1
                bo80+=boxoffice
            if rating >60:
                count60+= 1
                bo60+=boxoffice
            if rating>40:
                count40+= 1
                bo40+=boxoffice
            if rating>20:
                count20+= 1
                bo20+=boxoffice
            else:
                mvsucks+=1
                bomvsucks+=1
    avg80 = bo80/count80
    avg60 = bo60/count60
    avg40 = bo40/count40
    avg20 = bo20/count20
    if mvsucks !=0:
        sucksavg = bomvsucks/mvsucks

    # Add to text file
    f.write("------\n")
    f.write("Average Boxoffice Price per Rating Category\n")
    f.write("rating category, number of movies category, average boxoffice\n")
    entry1 = "80-100, {}, {}\n".format(str(count80), str(avg80))
    f.write(entry1)
    entry2 = "60-80, {}, {}\n".format(str(count60),str(avg60)) 
    f.write(entry2)
    entry3 = "40-60, {}, {}\n".format(str(count40), str(avg40))
    f.write(entry3)
    entry4 = "20-40, {}, {}\n".format(str(count20), str(avg20))
    f.write(entry4)
    if sucksavg !=0:
        entry5 = "<=20, {}, {}\n".format(str(mvsucks), str(sucksavg))
        f.write(entry5)
    else:
        entry5 = "<=20, 0, 0\n".format(str(mvsucks), str(sucksavg))
        f.write(entry5)
    f.write('\n')


def make_visualizations(file):
    rtrating = []
    bins = []
    count = -20
    num = 3
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_ = dir_path + '/' + "omdb-calculations.txt"
    with open (file_, 'r') as infile:
        something = infile.readlines()#[31:]
    for line in something: 
        if num in range(len(something) - 1) and line == something[num]:
            num+=1
            line = line.strip('\n')
            count+=20
            bins.append(count)
            l = line.split(',')
            rtrating.append(int(l[1]))
    bins.append(100)
    plt.hist(rtrating, bins, histtype='bar', rwidth=0.8)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.title("Average Boxoffice Price per Rating Category")
    plt.xlabel("rating category")
    plt.ylabel("number of movies category")
    fig, ax = plt.subplots()
    fig.savefig("omdbhist.png")
    plt.show()
    plt.legend()
    plt.show()

    
'''
def create_cache():
    # Cache was created on 12/4/19 at 11:58 PM
    index = 0
    while index in range(5):
        title_list, bor_list = get_api_data_all()
        index = index+1
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cache_file = dir_path + '/' + "boratings.json"
    movie_results = {}
    n_dict = {}
    for i in range(len(title_list)):
        n_dict[title_list[i]] = title_list[1]
        movie_results['title'] =  n_dict[title_list[i]]
        n_dict[bor_list[i]] = bor_list[i]
        movie_results['boxoffice'] = bor_list[i] #it made a file before but now added box office as a separate category, now not working
#REDO THE PART ABOVE!!!!!
    with open (cache_file, 'w') as outfile:
        json.dump(movie_results, outfile, indent = 2)
'''

# class TestAllMethods(unittest.TestCase):
#     def test_get_api_data_all(self):
#         results_dict = get_api_data()
#         self.assertEqual(len(results_dict), 100) # Testing if 100 movies are added
#         self.assertFalse(results_dict[0] == results_dict[20]) # Testing if unique pages were returned

def main():
    # movie_info = get_api_data_all()
    # make_cache(movie_info)

    movie_info_cache = open_cache()
    cur, conn = setUpDatabase("movies.db")
    add_to_database(movie_info_cache, cur, conn)
    with open("omdb-calculations.txt", 'w') as f:
        boxoffice_by_rating(f)
        make_visualizations(f)

    # create_cache()

if __name__ == "__main__":
    main()
    unittest.main(verbosity = 2)