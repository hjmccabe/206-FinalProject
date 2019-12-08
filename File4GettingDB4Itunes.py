#will use movies.db, leftjoin Popularity and OMDB tables by title
#will then get title, release date, and director information
#must modify director info to .split() by ','
#must then say if the length is >1 and <3, then if director 1 and director 2 match
#if length >=3 then find the first 3 directors
#if the director is N/A then search without the director in itunes
import unittest
import json
import requests
import os
import sqlite3

def get_movies_dict(db_filename):
    path = os.path.dirname(os.path.abspath(__file__))
    drdictionary = {}
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()
    cur.execute('''SELECT Popularity.release_date, OMDB.director
    FROM Popularity
    LEFT JOIN OMDB
    ON Popularity.title = OMDB.title;''')
    count = 0
    for var in list(cur):
        newsdir = ''
        
        if var[1] != None and var[1] != '' and var[1] != 'N/A': #MODIFY IF WE FIX THE DATABASE ISSUE!!!!!!!
            count += 1
            director = var[1] #got director
            adir = director.replace("(co-director)", '')
            adir2 = adir.strip(' ')
            newsdir = newsdir + adir2
            released = var[0] #got release date
            drdictionary[newsdir] = released
    print(count)
    print(len(drdictionary.items()))
    
    conn.close()
    return drdictionary
  #PROBLEM: return 77 items in dictionary, seems we should get 88

def main():
    filename = "movies.db"
    get_movies_dict(filename)

if __name__ == "__main__":
    main()
    unittest.main(verbosity = 2)
#EDGE CASES:
    #('2017-12-13', 'N/A')
    #('2019-05-24', 'Chris Renaud, Jonathan del Val(co-director)')
#OTHER TEST CASES:
    #len(movies in dictionary from get_movies_dict) == 88
