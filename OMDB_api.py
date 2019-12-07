import unittest
import json
import requests
import os

def get_popular_movie_titles():
    titles = []
    full_path = os.path.join(os.path.dirname(__file__), "popular_movies.json")
    f = open(full_path)
    file_data = f.read()
    f.close()
    popular_movies = json.loads(file_data)

    for movie in popular_movies["results"]:
        print(movie)
        title = movie["title"]
        titles.append(title)

    return titles

    

def get_api_data_all():
    # Get 20 most popular movies from TMDB
    api_key = '975f8068'
    baseurl= "http://www.omdbapi.com/?t={}&apikey={}"
    title_list = []
    bor_list = []

    # Each fetch returns 1 movie per page
    #want 20 movies

    popular_movie_titles = get_popular_movie_titles()
    print(popular_movie_titles)

    for title in popular_movie_titles: 
        ratings_url = baseurl.format(title, api_key)
        r = requests.get(ratings_url)
        data = json.loads(r.text)
        ratings = data.get("Ratings")
        boxoffice = data.get("BoxOffice")
        moviename = data.get("Title")
        title_list.append(moviename)
        bor_list.append((ratings, boxoffice))
    print(bor_list)
    print(title_list)
    return title_list, bor_list #want the title information so it is easier for us to identify

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

# class TestAllMethods(unittest.TestCase):
#     def test_get_api_data_all(self):
#         results_dict = get_api_data()
#         self.assertEqual(len(results_dict), 100) # Testing if 100 movies are added
#         self.assertFalse(results_dict[0] == results_dict[20]) # Testing if unique pages were returned

def main():
    get_api_data_all()
    # create_cache()

if __name__ == "__main__":
    main()
    unittest.main(verbosity = 2)