#limit --> default is 50;
#attribute = movie
import unittest
import json
import requests
import os

def movie_titles(filename):
    # Get same movies from OMDB
    titlelst1 = []
    titlelst = []
    
    with open(filename, "r") as f:
        z = f.loads()
    for info in z['results']:
        titlelst1.append(info['title'])
    for titleconvert in titlelst1:
        title= titleconvert.replace(" ", "+")
        titlelst.append(title)
    return titlelst

def movie_get(titlelst):
    baseurl= "https://itunes.apple.com/search?term={}&country=US&entity=movie&limit=20"
    movie_list = []
    for ntitle in titlelst[:1]: #TESTING WITH 2 ITEMS
        url = baseurl.format(ntitle)
        itunesr = requests.get(url)
        data = json.loads(itunesr.text)
        movie_list = movie_list + data
    print(movie_list)
    return movie_list







    

    
#
#get the title first and turn it into name+name format
#write these parameters into the cache file one at a time


#     # Each fetch returns 20 movies on a page
#     # This iterates 5 times to return 100 movies
#     for num in range(1,6):
#         popular_url = baseurl.format(api_key, num)
#         r = requests.get(popular_url)
#         data = json.loads(r.text)
#         results = data["results"]
#         popular_list = popular_list + results
#     return popular_list


#     # Cache was created on 12/4/19 at 9:15 PM

#     dir_path = os.path.dirname(os.path.realpath(__file__))
#     cache_file = dir_path + '/' + "popular_movies.json"

#     movie_results = {}
#     movie_results['results'] = pop_results

#     with open (cache_file, 'w') as outfile:
#         json.dump(movie_results, outfile, indent = 2)

# class TestAllMethods(unittest.TestCase):
#     def test_get_api_data_popular(self):
#         results_dict = get_api_data_popular()
#         self.assertEqual(len(results_dict), 100) # Testing if 100 movies are added
#         self.assertFalse(results_dict[0] == results_dict[20]) # Testing if unique pages were returned

def main():
    filename = "popular_movies.json"
    results = movie_titles(filename) 
    mlst = movie_get(results)
    #create_cache(mlst)

# if __name__ == "__main__":
#     main()
#     unittest.main(verbosity = 2)