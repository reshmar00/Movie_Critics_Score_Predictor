import requests
from bs4 import BeautifulSoup
import mysql.connector

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="rotten_scraper01",
    password="n00b@THIS",
    database="movie_info_collections"
)

cursor = db.cursor()

# Define the URL of the Rotten Tomatoes page
url = "https://editorial.rottentomatoes.com/guide/100-best-classic-movies/"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the first movie container
    first_movie = soup.find('div', class_='row countdown-item')
    
    try:
        # Extract the movie title and URL
        title_container = first_movie.find('div', class_='article_movie_title')
        movie_title_tag = title_container.find('h2').find('a')
        movie_title = movie_title_tag.text.strip()
        movie_page_url = movie_title_tag['href']
        
        # Extract the Tomatometer score
        tomatometer_score = first_movie.find('span', class_='tMeterScore').text.strip().replace('%', '')
        
        # Send a GET request to the movie's page URL
        movie_page_response = requests.get(movie_page_url)
        
        if movie_page_response.status_code == 200:
            # Parse the HTML content of the movie's page
            movie_page_soup = BeautifulSoup(movie_page_response.text, 'html.parser')
            
            # Extract the full synopsis from the meta description
            meta_tags = movie_page_soup.find('head').find_all('meta')
            for tag in meta_tags:
                if tag.get('name') == 'description':
                    synopsis = tag.get('content')
                    break
            
            # Print the information
            print(f"Movie Title: {movie_title}")
            print(f"Tomatometer Score: {tomatometer_score}")
            print(f"Description: {synopsis}")
            
            # Insert into MySQL database
            insert_query = """
            INSERT INTO rotten_tomatoes_info (movie_title, tomatometer_score, description)
            VALUES (%s, %s, %s)
            """
            cursor.execute(insert_query, (movie_title, tomatometer_score, synopsis))
            db.commit()
            
        else:
            print(f"Failed to retrieve the movie page. Status code: {movie_page_response.status_code}")
    
    except Exception as e:
        print(f"Error occurred: {str(e)}")
            
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

# Close the database connection
cursor.close()
db.close()