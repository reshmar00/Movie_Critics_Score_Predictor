import mysql.connector
from mysql.connector import errorcode

config = {
  'user': 'rotten_scraper01',
  'password': 'n00b@THIS',
  'host': 'localhost',
  'database': 'movie_info_collections',
  'raise_on_warnings': True
}

try:
    cnx = mysql.connector.connect(**config)
    print("Connection successful!")
    cnx.close()
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your username or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)