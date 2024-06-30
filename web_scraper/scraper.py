from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
import mysql.connector
from mysql.connector import errorcode
import time

# Setting the maximum no. of requests and the timeframe
max_requests = 10
timeframe_seconds = 60

# Initializing counters
request_count = 0
start_time = time.time()

config = {
  'user': 'rotten_scraper01',
  'password': 'n00b@THIS',
  'host': 'localhost',
  'database': 'movie_info_rt',
  'raise_on_warnings': True
}

# list_url = "https://www.imdb.com/search/title/?count=100&groups=top_1000&sort=user_rating"
url1 = "https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=250&start=1"
url2 = "https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=250&start=251"
url3 = "https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=250&start=501"
url4 = "https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=250&start=751"

list_urls = [url1, url2, url3, url4]
movie_names = []

# Main scraping loop
while request_count < max_requests and time.time() - start_time < timeframe_seconds:
    for list_url in list_urls:
        # Fetch the HTML content from the URL
        list_response = urlopen(list_url)
        list_html_content = list_response.read()

        # Parse the HTML content with BeautifulSoup
        list_soup = BeautifulSoup(list_html_content, 'html.parser')

        # Find all `h3` tags with class `lister-item-header`
        h3_tags = list_soup.find_all('h3', class_='lister-item-header')

        # Loop through each `h3` tag and extract the movie title
        for h3 in h3_tags:
            a_tag = h3.find('a')  # Get the first `a` tag within the `h3`
            if a_tag:  # Check if an `a` tag was found
                # Extract the text within the `a` tag
                # and remove any leading/trailing whitespace
                movie_title = a_tag.text.strip()
                movie_names.append(movie_title)  # Append the title to the list of movie names

        # Increment the request count
        request_count += 1

        # Introduce a delay between requests
        time.sleep(30)

print('Completed scraping the urls for movie titles')

special_characters = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=', '{', '}', '[', ']', '|', ';', ':', "'", '"', '<', '>', ',', '.', '?', '/', '`', '~']
formatted_title = ""

# Setting the maximum no. of requests and the timeframe again
max_requests = 10
timeframe_seconds = 60

# Re-initializing counters
request_count = 0
start_time = time.time()

for movie in movie_names:
    formatted_title = movie.replace(" ", "_")

    # Create the URL for the movie page
    movie_url = f"https://www.rottentomatoes.com/m/{formatted_title}"

    while request_count < max_requests and time.time() - start_time < timeframe_seconds:
        try:
            # Fetch the HTML content from the URL
            movie_response = urlopen(movie_url)
            movie_html_content = movie_response.read()

            # Parse the HTML content with BeautifulSoup
            movie_soup = BeautifulSoup(movie_html_content, 'html.parser')

            # Find the title tag and get its text content
            title_tag = movie_soup.find('title')
            movie_title = title_tag.get_text()

            # Remove the " - Rotten Tomatoes" suffix from the movie title
            movie_title = movie_title.replace(" - Rotten Tomatoes", "")
            # print(movie_title)

            # Find the <p> tag with the specified attributes and get its text content
            synopsis = movie_soup.find('p', {'data-qa': 'movie-info-synopsis', 'slot': 'content'}).text

            # Remove all newlines and other whitespace characters from the description
            synopsis_short = synopsis.strip()
            # print(synopsis_short)

            # Find the score-details-manager section
            score_element = movie_soup.find('score-details-manager')

            try:
                # Use json to grab the specific details you want from that section
                score_json = json.loads(score_element.find('script', {'id': 'score-details-json'}).text)

                # Store the critics score (tomatometer score) in the variable
                tomatometer_score = score_json['modal']['tomatometerScoreAll']['value']
                # print(tomatometer_score)
                print(f"Got movie info for {movie}")

                # Increment the request count
                request_count += 1

                # Introduce a delay between requests
                time.sleep(30)

            except:
                tomatometer_score = "N/A"

            # try:
            #     cnx = mysql.connector.connect(**config)
            #     cursor = cnx.cursor()
            #
            #     add_movie = ("INSERT INTO movie "
            #                  "(title, score, description) "
            #                  "VALUES (%s, %s, %s)")
            #     movie_data = (movie_title, tomatometer_score, synopsis_short)
            #
            #     # Insert new movie
            #     cursor.execute(add_movie, movie_data)
            #
            #     # Make sure data is committed to the database
            #     cnx.commit()
            #
            # except mysql.connector.Error as err:
            #     if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            #         print("Something is wrong with your username or password")
            #     elif err.errno == errorcode.ER_BAD_DB_ERROR:
            #         print("Database does not exist")
            #     else:
            #         print(err)
            #
            # else:
            #     cursor.close()
            #     cnx.close()

        except:
            print(f"Failed to fetch data for movie {movie}")

# print(movies)
print("No. of movies stored: " + str(len(movies)))