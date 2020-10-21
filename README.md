# 206-FinalProject
SI 206 Final Project for team H&amp;M

Who are you working with?
Harrison McCabe, Madeline Rosenberg
What APIs will you be gathering data from?<br>
OMDB, TMDB, iTunes<br>
What data will you collect from each API and store in a database?  Be specific.<br>
By category: top 20 by genre for drama, action, comedy, indie<br>
OMDB: Ratings, box office<br>
TMDB: Similar Movies (pick one and see results) https://developers.themoviedb.org/3/movies/get-similar-movies<br>
Itunes price for same movies as OMDB<br>
What data will you be calculating from the data in the database?<br>
Frequency of average ratings in time categories for 100 movies (20 from each genre category: action, drama, comedy, indie)<br>
Average ratings for top 20 movies in each genre (specified in 5.a.)<br>
Ratings vs box office scatterplot comparing relationships between variables<br>
Relationship between ratings, price, and prices of similar movies<br>
What visualization package will you be using (matplotlib, plotly, seaborn, etc)?  See https://www.fusioncharts.com/blog/best-python-data-visualization-libraries/ (Links to an external site.)
 Matplotlib<br>
What graphs/charts will you be creating?<br>
Box and Whisker plots Average top 20 rating in drama vs. average top 20 rating in action vs. top 20 in comedy vs top 20 in indie vs top 20 rating in documentary from OMDB<br>
Histogram: x-axis of iTunes price, y-axis of frequency among selected 100 movies from OMDB (20 from each top 5 genres specified in 7.a.)<br>
Scatterplot: Box office from OMDB (y-axis) versus average rating from OMDB (x-axis) for each top movie in the drama, action, comedy, indie, documentary categories where each genre is a different color;  is there a relationship? <br>
Scatterplot: Compare ratings of the top movie from OMDB to similar movies from TMDB<br>
