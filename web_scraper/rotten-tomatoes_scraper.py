import os
import requests
from bs4 import BeautifulSoup
import mysql.connector
import time
import random
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_DATABASE")
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
    
    # Find all movie containers
    movie_containers = soup.find_all('div', class_='row countdown-item')
    
    movie_count = 0  # Counter for movies processed
    expected_movie_count = len(movie_containers)  # Expected number of movies
    
    # Load SQL insert query from environment variable
    insert_query = os.getenv("INSERT_QUERY")
    
    for movie in movie_containers:
        try:
            # Extract the movie title and URL
            title_container = movie.find('div', class_='article_movie_title')
            movie_title_tag = title_container.find('h2').find('a')
            movie_title = movie_title_tag.text.strip()
            movie_page_url = movie_title_tag['href']
            
            # Extract the Tomatometer score
            tomatometer_score = movie.find('span', class_='tMeterScore').text.strip().replace('%', '')
            
            # Send a GET request to the movie's page URL
            movie_page_response = requests.get(movie_page_url)
            
            if movie_page_response.status_code == 200:
                # Parse the HTML content of the movie's page
                movie_page_soup = BeautifulSoup(movie_page_response.text, 'html.parser')
                
                # Extract the full synopsis from the meta description
                meta_tags = movie_page_soup.find('head').find_all('meta')
                synopsis = ""
                for tag in meta_tags:
                    if tag.get('name') == 'description':
                        synopsis = tag.get('content')
                        break
                
                # Insert into MySQL database using prepared statement
                cursor.execute(insert_query, (movie_title, tomatometer_score, synopsis))
                db.commit()

                print("Inserted movie into table")
                
                movie_count += 1
                
                # Delay between each movie
                delay_between_movies = random.uniform(5, 10)
                time.sleep(delay_between_movies)
                
                # Check if 10 movies have been processed, then apply longer delay
                if movie_count % 10 == 0:
                    print(f"Processed {movie_count} movies. Taking a 60-second break.")
                    time.sleep(60)
            
            else:
                print(f"Failed to retrieve the movie page. Status code: {movie_page_response.status_code}")
        
        except Exception as e:
            print(f"Error occurred: {str(e)}")
    
    print(f"Total movies added to database: {movie_count}")
    
    # Check if the number of movies added matches the expected count
    if movie_count == expected_movie_count:
        print(f"All {expected_movie_count} movies added successfully.")
    else:
        print(f"Expected {expected_movie_count} movies, but added {movie_count}. Discrepancy found.")
            
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

print("Done with all movies listed in this URL")

# Close the database connection
cursor.close()
db.close()