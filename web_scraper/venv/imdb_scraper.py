from bs4 import BeautifulSoup
from urllib.request import urlopen
import mysql.connector
from mysql.connector import errorcode
import time
import re

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
  'database': 'movie_info_collections',
  'raise_on_warnings': True
}

# list_url = "https://www.imdb.com/search/title/?count=100&groups=top_1000&sort=user_rating"
url1 = "https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=250&start=1"
url2 = "https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=250&start=251"
url3 = "https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=250&start=501"
url4 = "https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=250&start=751"

list_urls = [url1]  # , url2, url3, url4]
rotten_movie_names = []
imdb_movie_names = []
imdb_movie_scores = []
imdb_movie_synopses = []
index_to_grab = 0  # Index of the 'span' element to grab

meta_movie_title = ""
metascore = ""
meta_synopsis = ""
link_synopsis = ""
span_class = ""

# Main scraping loop
while request_count < max_requests and time.time() - start_time < timeframe_seconds:
    for list_url in list_urls:
        # Fetch the HTML content from the URL
        list_response = urlopen(list_url)
        list_html_content = list_response.read()

        # Parse the HTML content with BeautifulSoup
        list_soup = BeautifulSoup(list_html_content, 'html.parser')

        # Find all 'h3' tags with class 'lister-item-header'
        h3_tags = list_soup.find_all('h3', class_='lister-item-header')

        # ***************************** IMDB ************************** #

        # Find all 'metascore' tags
        metascore_tags = list_soup.find_all('div', class_='inline-block ratings-metascore')

        # Loop through each 'h3' tag and extract the movie title
        for h3, metascore_obj in zip(h3_tags, metascore_tags):
            a_tag = h3.find('a')  # Get the first 'a' tag within the 'h3'
            if a_tag:  # Check if an 'a' tag was found
                meta_movie_title = a_tag.text.strip()
                # imdb_movie_names.append(meta_movie_title)  # Append the title to the list of movie names
                print(meta_movie_title)

                span_class = a_tag.find('span', class_='lister-item-index unbold text-primary')
                meta_movie_id = span_class.text.strip()
                print(meta_movie_id)

                meta_tag = metascore_obj.find('span')
                if meta_tag:
                    # Get the movie's metascore (critic's score)
                    metascore = meta_tag.text.strip()
                    # imdb_movie_scores.append(metascore)
                    print(metascore)

                synopsis_tag = h3.find_next_sibling('p', class_='text-muted', string=True)
                if synopsis_tag:
                    meta_synopsis = synopsis_tag.get_text(separator=' ')
                    # synopses = synopsis_tag.find_all('a')
                    # for a_tag in synopses:
                    #    print(a_tag.get_text)
                    # imdb_movie_synopses.append(meta_synopsis)
                    print(meta_synopsis)
                else:
                    continue

                # Increment the request count
                request_count += 1

                # Introduce a delay between requests
                time.sleep(30)

                # try:
                #     cnx = mysql.connector.connect(**config)
                #     cursor = cnx.cursor()
                #
                #     add_movie = ("INSERT INTO imdb_info "
                #                  "(movie_title, metascore, description) "
                #                  "VALUES (%s, %s, %s)")
                #     movie_data = (meta_movie_title, metascore, meta_synopsis)
                #
                #     # Insert new movie
                #     cursor.execute(add_movie, movie_data)
                #
                #     # Make sure data is committed to the database
                #     cnx.commit()
                #
                #     # print(f"{meta_movie_title} data saved")
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


print("imdb part done")
