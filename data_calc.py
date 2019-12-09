import json
import os
import sqlite3
import matplotlib.pyplot as mpl

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
    total_movies = len(results)

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
    f.write("Year, number of movies in year, average popularity, percent of total movies\n")
    for year_data in sorted_average_popularity:
        year = year_data[0]
        num, avg = year_data[1]
        entry = "{}, {}, {}\n".format(year, num, avg)
        f.write(entry)
    f.write('\n')

    return sorted_average_popularity

def popularity_bar_graph(data):
    years = []
    nums = []
    score = []

    for entry in data:
        years.append(entry[0])
        nums.append(entry[1][0])
        score.append(entry[1][1])


    # Create the bar graph
    fig, ax1 = mpl.subplots()
    width = 0.69

    ax1.bar(years, nums, width, align='edge', color = "#00274C")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Number of Popular Movies")
    ax1.set_title("Number of Popular Movies per Release Year")

    # Use these to make sure that your x axis labels fit on the page
    mpl.xticks(rotation=90)
    mpl.tight_layout()


    fig.savefig("pop_movies.png")
    mpl.show()

def popularity_by_decade(data, f):
    decade_totals = {}
    total_number = 0

    for year_info in data:
        total_number += year_info[1][0]


    for year_info in data:
        year = year_info[0]
        num_in_year = int(year_info[1][0])

        if year >= 2020:
            number = decade_totals.get("2020s", [0])[0] + num_in_year
            percentage = float('%.2f' % ((number / total_number) * 100))
            decade_totals["2020s"] = (number, percentage)
        elif year == 2019:
            number = decade_totals.get("2019", [0])[0] + num_in_year
            percentage = float('%.2f' % ((number / total_number) * 100))
            decade_totals["2019"] = (number, percentage)
        elif year >= 2010 and year <= 2018:
            number = decade_totals.get("2010-2018", [0])[0] + num_in_year
            percentage = float('%.2f' % ((number / total_number) * 100))
            decade_totals["2010-2018"] = (number, percentage)
        elif year >= 2000 and year <= 2009:
            number = decade_totals.get("2000s", [0])[0] + num_in_year
            percentage = float('%.2f' % ((number / total_number) * 100))
            decade_totals["2000s"] = (number, percentage)
        elif year >= 1990 and year <= 1999:
            number = decade_totals.get("1990s", [0])[0] + num_in_year
            percentage = float('%.2f' % ((number / total_number) * 100))
            decade_totals["1990s"] = (number, percentage)
        elif year >= 1980 and year <= 1989:
            number = decade_totals.get("1980s", [0])[0] + num_in_year
            percentage = float('%.2f' % ((number / total_number) * 100))
            decade_totals["1980s"] = (number, percentage)
        elif year >= 1970 and year <= 1979:
            number = decade_totals.get("1970s", [0])[0] + num_in_year
            percentage = float('%.2f' % ((number / total_number) * 100))
            decade_totals["1970s"] = (number, percentage)
        elif year >= 1960 and year <= 1969:
            number = decade_totals.get("1960s", [0])[0] + num_in_year
            percentage = float('%.2f' % ((number / total_number) * 100))
            decade_totals["1960s"] = (number, percentage)

    # Add to text file
    f.write("Number and percentage of movies by decade\n")
    f.write("Decade, number of movies in decade, percent of total popular movies\n")

    for decade in decade_totals.keys():
        number, percentage = decade_totals[decade]
        entry = "{}, {}, {}\n".format(decade, number, percentage)
        f.write(entry)

    f.write("\n")

    print(decade_totals)
    return decade_totals

def popularity_pie_chart(decade_dict):
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    # decades = ["2019", "2010-2018", "2000s", "1990s", "1980s", "1970s", "1960s", "2020s"]
    decades = []
    percs = []
    
    for entry in decade_dict.keys():
        decades.append(entry)
        percs.append(decade_dict[entry][1])

    labels = decades
    sizes = percs

    fig1, ax1 = mpl.subplots()
    wedges, texts, autotexts = ax1.pie(sizes, labels=None, autopct='%1.2f%%', pctdistance=1, 
            shadow=False, startangle=90)
    # patches, texts = mpl.pie(sizes, shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.



    legend_info = []

    for i in range(len(decades)):
        legend_info.append((decades[i], percs[i]))

    ax1.legend(wedges, legend_info,
          title="Legend",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))
    
    mpl.title("Percentage of popular movies by decade")

    mpl.tight_layout()
    fig1.savefig("pop_movies_pie.png")
    mpl.show()

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
    bolst = []
    count = -20
    num = 3
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_ = dir_path + '/' + "calculations.txt"
    with open (file_, 'r') as infile:
        something = infile.readlines()[46:]
    for line in something: 
        if num in range(len(something) - 1) and line == something[num]:
            num+=1
            line = line.strip('\n')
            count+=20
            bins.append(count)
            l = line.split(',')
            rtrating.append(int(l[1]))
            bolst.append(int(l[-1]))
    count+=20
    bins.append(count)

    # get the figure
    fig = mpl.figure()

    ax1 = fig.add_subplot(111)
    width = 0.69
    ax1.bar(bins, rtrating, width, align = 'edge', color = 'g-')
    ax1.set_xlabel("rating category")
    ax1.set_title("Number of Movies per Rotten Tomato Category")
    ax1.grid()
    ax1.set_ylim(0, 40)
    ax1.set_yaxis("Number of movies")
    mpl.xticks(rotation=90)
    mpl.tight_layout()
    # save the figure
    fig.savefig("omdbhist.png")
    mpl.show()

    # plot the box office data (add line)
    ax2 = fig.add_subplot(111)
    ax2.bar(bins, bolst, align = 'edge', color ='y-')
    ax2.set_title("Average Boxoffice Price per Rotten Tomatoe Rating Category")
    ax2.set_xlabel("rating category")
    ax2.grid()
    ax2.set_ylim(100000, 453865219)
    ax1.set_yaxis("box office movie average")
    mpl.xticks(rotation=90)
    mpl.tight_layout()
    # save the figure
    fig.savefig("omdbhist2.png")
    mpl.show()

    # Use these to make sure that your x axis labels fit on the page
    mpl.xticks(rotation=90)
    mpl.tight_layout()


    # mpl.hist(rtrating, bins, histtype='bar', rwidth=0.8)
    # mpl.xticks(rotation=90)
    # mpl.tight_layout()
    # mpl.title("Average Boxoffice Price per Rating Category")
    # mpl.xlabel("rating category")
    # mpl.ylabel("number of movies category")
    # fig, ax = mpl.subplots()
    # fig.savefig("omdbhist.png")
    # mpl.show()
    # mpl.legend()


def main():
    with open("calculations.txt", 'w') as f:
        sorted_average_popularity = popularity_by_year(f)
        # popularity_bar_graph(sorted_average_popularity)

        pop_decade = popularity_by_decade(sorted_average_popularity, f)
        popularity_pie_chart(pop_decade)

        boxoffice_by_rating(f)
        make_visualizations(f)


if __name__ == "__main__":
    main()