import ssl
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import time
import certifi

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

url = "https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=250&start=1"
# url2 = "https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=250&start=251"
# url3 = "https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=250&start=501"
# url4 = "https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=250&start=751"


imdb_movie_names = []
imdb_movie_scores = []
imdb_movie_synopses = []
index_to_grab = 0  # Index of the 'span' element to grab

meta_movie_title = ""
metascore = ""
meta_synopsis = ""
link_synopsis = ""
span_class = ""

# User-Agent header
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

request = Request(url, headers=headers)

print("Request sent")

# Main scraping loop
# while request_count < max_requests and time.time() - start_time < timeframe_seconds:
try:
    context = ssl.create_default_context(cafile=certifi.where())
    print("Attempting to open the URL")
    list_response = urlopen(request, context=context)
    # Fetch the HTML content from the URL
    #print("Attempting to open the URL")
    #list_response = urlopen(url)

    print("Fetching the HTML content from the URL")
    list_html_content = list_response.read()

    # Parse the HTML content with BeautifulSoup
    print("Parsing the HTML content with BeautifulSoup")
    list_soup = BeautifulSoup(list_html_content, 'html.parser')

    print("Finding all 'h3' tags with class 'lister-item-header'")
    # Find all 'h3' tags with class 'lister-item-header'
    h3_tags = list_soup.find_all('h3', class_='lister-item-header')

    # ***************************** IMDB ************************** #

    print("Finding all 'metascore' tags")
    # Find all 'metascore' tags
    metascore_tags = list_soup.find_all('div', class_='inline-block ratings-metascore')
    
    print("Looping through each 'h3' tag and extracting details")
    # Loop through each 'h3' tag and extract the movie details
    for h3, metascore_obj in zip(h3_tags, metascore_tags):
        a_tag = h3.find('a')  # Get the first 'a' tag within the 'h3'
        if a_tag:  # Check if an 'a' tag was found
            meta_movie_title = a_tag.text.strip()
            # imdb_movie_names.append(meta_movie_title)  # Append the title to the list of movie names
            print("Movie title:", meta_movie_title)

            # span_class = a_tag.find('span', class_='lister-item-index unbold text-primary')
            # meta_movie_id = span_class.text.strip()
            # print(meta_movie_id)

            meta_tag = metascore_obj.find('span')
            if meta_tag:
                # Get the movie's metascore (critic's score)
                metascore = meta_tag.text.strip()
                # imdb_movie_scores.append(metascore)
                print("Metascore:", metascore)

            synopsis_tag = h3.find_next_sibling('p', class_='text-muted', string=True)
            if synopsis_tag:
                meta_synopsis = synopsis_tag.get_text(separator=' ')
                # synopses = synopsis_tag.find_all('a')
                # for a_tag in synopses:
                #    print(a_tag.get_text)
                # imdb_movie_synopses.append(meta_synopsis)
                print("Synopsis:", meta_synopsis)
            else:
                continue

            # Increment the request count
            request_count += 1

            # Introduce a delay between requests
            time.sleep(30)
        #     break
        # break
except Exception as e:
    print(f"Error: {e}")
    # break
print("IMDb scraping part done")