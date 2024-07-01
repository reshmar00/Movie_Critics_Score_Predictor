import requests
from bs4 import BeautifulSoup
import re
import mysql.connector

# Function to fetch and parse HTML
def fetch_html(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')

# Base URL for the movie details
base_url = 'https://www.rottentomatoes.com'

# Function to scrape movies in theaters page
def scrape_movies_in_theaters(page_url):
    soup = fetch_html(page_url)
    
    # Find all movie containers
    movie_containers = soup.find_all('div', class_='flex-container')
    
    for container in movie_containers:
        # Check if critics score is available
        critics_score = container.find('rt-text', {'slot': 'criticsScore'})
        if critics_score:
            critics_rating = critics_score.text.strip()
            if critics_rating:
                # Extract movie title
                # TODO: CHECK HERE
                movie_title_elem = container.find('span', class_='p--small') #{'data-qa': 'discovery-media-list-item-title'})
                if movie_title_elem:
                    movie_title = movie_title_elem.text.strip()
                    
                    # Construct movie details page URL
                    movie_relative_url = container.find('a', class_='js-tile-link')['href']
                    movie_url = base_url + movie_relative_url
                    
                    # Fetch and parse movie details page
                    movie_soup = fetch_html(movie_url)
                    
                    # Extract synopsis
                    synopsis = ''
                    title_tag = movie_soup.find('title')
                    if title_tag:
                        movie_name = title_tag.text.split('|')[0].strip()
                        if movie_name == movie_title:
                            meta_description = movie_soup.find('meta', {'name': 'description'})
                            if meta_description:
                                synopsis = meta_description['content']
                    
                    # Print for verification (replace with database insertion)
                    print(f"Movie Title: {movie_title}")
                    print(f"Critics Score: {critics_rating}")
                    print(f"Synopsis: {synopsis}")
                    print("\n")
                    
                    # Insert into MySQL database
                    insert_into_database(movie_title, critics_rating, synopsis)

# Function to insert data into MySQL database
def insert_into_database(movie_title, critics_rating, synopsis):
    connection = mysql.connector.connect(
        host='localhost',
        user='your_username',
        password='your_password',
        database='movie_info_collections'
    )
    
    cursor = connection.cursor()
    insert_query = "INSERT INTO rotten_tomatoes_info (movie_title, tomatometer_score, description) VALUES (%s, %s, %s)"
    data = (movie_title, critics_rating, synopsis)
    
    cursor.execute(insert_query, data)
    connection.commit()
    
    cursor.close()
    connection.close()

# Main function to start scraping
def main():

    url = "https://www.rottentomatoes.com/browse/movies_in_theaters/?page=4"
    scrape_movies_in_theaters(url)

if __name__ == "__main__":
    main()