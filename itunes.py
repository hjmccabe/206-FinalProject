#limit --> default is 50;
#attribute = movie
import unittest
import json
import requests
import os

def movie_titles_fileload(filename):
    # Get same movies from OMDB
    source_dir = os.path.dirname(__file__) #<-- directory name
    full_path = os.path.join(source_dir, filename)
    with open(full_path, "r") as f:
        z= f.read()
    return z
def modified_movietitles(filename):
    file2 = movie_titles_fileload(filename)
    titlelst1 = []
    titlelst = []
    loadedfile = json.loads(file2)
    for info in loadedfile['results']:
        titlelst1.append(info['title'])
    for titleconvert in titlelst1:
        title= titleconvert.replace(" ", "+")
        titlelst.append(title)
    return titlelst

def movie_get(filename):
    titlelst = modified_movietitles(filename)
    baseurl= "https://itunes.apple.com/search?term={}&country=US&entity=movie&limit=20"
    movie_list = []
    for ntitle in titlelst[1:3]: #TESTING WITH 2 ITEMS
        url = baseurl.format(ntitle)
        itunesr = requests.get(url)
        data = json.loads(itunesr.text)
        nresults = data['results']
        movie_list = movie_list + nresults
    return movie_list
def create_cache(filename):
    index = 0
    ituneslst = []
    while index in range(2): #TESTING IT WITH 2 ITERATIONS!
        mvget_lst = movie_get(filename)
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
    filename = "popular_movies.json"
    create_cache(filename)

if __name__ == "__main__":
    main()
    unittest.main(verbosity = 2)