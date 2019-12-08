#limit --> default is 50;
#attribute = movie
import unittest
import json
import requests
import os
import sqlite3
import re

# def movie_titles_fileload(filename):
#     # Get same movies from OMDB
#     source_dir = os.path.dirname(__file__) #<-- directory name
#     full_path = os.path.join(source_dir, filename)
#     with open(full_path, "r") as f:
#         z= f.read()
#     return z


def get_movies_dict(db_filename):
    path = os.path.dirname(os.path.abspath(__file__))
    drdictionary = {}
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()
    cur.execute('''SELECT Popularity.release_date, OMDB.director, OMDB.title
    FROM Popularity
    LEFT JOIN OMDB
    ON Popularity.title = OMDB.title;''')
    count = 0
    for var in list(cur):
        count+=1
        newsdir = ''
        if var[1] != None and var[1] != '' and var[1] != 'N/A': #MODIFY IF WE FIX THE DATABASE ISSUE!!!!!!!
            title = var[2]
            director = var[1] #got director
            director = director.strip(' ').split(',')[0].strip(' ')
            newsdir = newsdir + director
            released = var[0] #got release date
            drdictionary[title] = (newsdir, released)
    print(count)
    conn.close()
    return drdictionary

def modified_movietitles(db_filename):
    dbdictionary = get_movies_dict(db_filename)
    titlelst1 = []
    titlelst = []
    #loadedfile = json.loads(file2)
    for title in dbdictionary.items():
        titlelst1.append(title[0])
    for titleconvert in titlelst1:
        title= titleconvert.replace(" ", "+")
        titlelst.append(title)
    return titlelst

def movie_get(db_filename):
    count = 0
    titlelst = modified_movietitles(db_filename)
    moviesdict = get_movies_dict(db_filename)
    baseurl= "https://itunes.apple.com/search?term={}&country=US&entity=movie&limit=20"
    movie_list = []
    for ntitle in titlelst: #TESTING WITH 2 ITEMS
        url = baseurl.format(ntitle)
        itunesr = requests.get(url)
        data = json.loads(itunesr.text)
        mtitle = ntitle.replace('+', ' ')
        for tup in moviesdict[mtitle]:
            for i in range(len(data['results'])):
                if re.findall("director ([A-Z]{1}[a-z]* [A-Z]{1}[a-z]*)",data['results'][i]["longDescription"])and tup[1] == data['results'][i]['releaseDate'].split('T'):
#(tup[0] in data['results'][i]['artistName'].split(' &') or tup[0] in data['results'][i]['artistName']) 
                    nresults = data['results']
                    movie_list = movie_list + nresults
            else:
                count +=1
        print("{} titles cannot be matched in itunes".format(count))
        
    return movie_list


# def corrected_movies_from_db(db_filename):
#     drdictionary = get_movies_dict(db_filename)
#     for info in drdictionary.items():


        



def create_cache(db_filename):
    index = 0
    ituneslst = []
    while index in range(20): #TESTING IT WITH 2 ITERATIONS!
        mvget_lst = movie_get(db_filename)
        ituneslst = mvget_lst + ituneslst
        index = index+1
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cache_file = dir_path + '/' + "itunes_b.json"
    movie_results = {}
    for i in range(len(ituneslst)-1):
        movie_results['results'] =  ituneslst[i]
    with open (cache_file, 'w') as outfile:
        json.dump(movie_results, outfile, indent = 2)

# class TestAllMethods(unittest.TestCase):
#     def test_get_api_data_popular(self):
#         results_dict = get_api_data_popular()
#         self.assertEqual(len(results_dict), 100) # Testing if 100 movies are added
#         self.assertFalse(results_dict[0] == results_dict[20]) # Testing if unique pages were returned

def main():
    #filename = "popular_movies.json"
    db_file = "movies.db"
    create_cache(db_file)

if __name__ == "__main__":
    main()
    unittest.main(verbosity = 2)