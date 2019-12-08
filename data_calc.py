import json
import os
import sqlite3

def popularity_by_year(f):
    # Opening cache
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cache_file = dir_path + '/' + "popular_movies.json"
    with open (cache_file, 'r') as infile:
        st = infile.read()
        dic = json.loads(st)
        results = dic.get("results")
    
    # Getting average popularity
    total_popularity = {}
    for movie in results:
        movie_pop = movie["popularity"]
        year = int(movie["release_date"][0:4])
        total_popularity[year] = total_popularity.get(year, [])
        total_popularity[year].append(movie_pop)

    average_popularity = {}

    for year in total_popularity.keys():
        pop_list = total_popularity[year]
        num_movies = len(pop_list)
        sum_pop = sum(pop_list)
        average_popularity[year] = (num_movies, sum_pop/num_movies)

    sorted_average_popularity = sorted(average_popularity.items(), key = lambda x: x[1], reverse = True)

    # Add to text file
    f.write("Average popularity of movies per year\n")
    f.write("Year, number of movies in year, average popularity\n")
    for year_data in sorted_average_popularity:
        year = year_data[0]
        num, avg = year_data[1]
        entry = "{}, {}, {}\n".format(year, num, avg)
        f.write(entry)
    f.write('\n')

def main():
    with open("calculations.txt", 'w') as f:
        popularity_by_year(f)

if __name__ == "__main__":
    main()