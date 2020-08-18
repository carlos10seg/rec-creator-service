import sys
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import urllib
from config_reader import ConfigReader
from pandas.io import sql
from datetime import datetime

class DbManager:
    def __init__(self):
        reader = ConfigReader()
        db_connection = reader.get_value("db_connection")
        # "+mysqlconnector",
        self.conn_string = '{db_engine}{connector}://{user}:{password}@{server}'.format(
            db_engine=db_connection['db_engine'],
            connector=db_connection['connector'],
            user=db_connection['user'],
            password=db_connection['password'],
            server=db_connection['server'])
        self.db_name = db_connection['database']
    
    def create_db_structure_with_data(self, movies, ratings):
        try:
            engine = create_engine(self.conn_string)
            engine.execute("CREATE DATABASE IF NOT EXISTS " + self.db_name)
            engine = create_engine(self.conn_string + "/" + self.db_name)

            movies.to_sql('movies', con=engine, if_exists='replace', index=False)
            ratings.to_sql('ratings', con=engine, if_exists='replace', index=False, chunksize=10000)

            # Create index
            sql.execute('''CREATE INDEX idx1 ON ratings (userId, itemId)''', engine)
            sql.execute('''CREATE INDEX idx1 ON movies (itemId);''', engine)
        except: # catch *all* exceptions
            e = sys.exc_info()[0]
            print(e)
 
    def get_ratings(self):
        return sql.read_sql("SELECT userId as user, itemId as item, rating, timestamp FROM ratings;", create_engine(self.conn_string + "/" + self.db_name))

    def get_movies(self):
        return sql.read_sql("SELECT itemId, title, genres FROM movies;", create_engine(self.conn_string + "/" + self.db_name))

    def get_links(self):
        return sql.read_sql("SELECT itemId, imdbId, tmdbId FROM links;", create_engine(self.conn_string + "/" + self.db_name))

    def get_ratings_for_user(self, user_id):
        return sql.read_sql("SELECT itemId as item, rating FROM ratings WHERE userId = {userId}".format(
                    userId=user_id), create_engine(self.conn_string + "/" + self.db_name))

    def build_movies(self, movies):
        try:
            #engine = create_engine(self.conn_string)
            #engine.execute("CREATE DATABASE IF NOT EXISTS " + self.db_name)
            engine = create_engine(self.conn_string + "/" + self.db_name)
            movies.to_sql('movies', con=engine, if_exists='replace', index=False)
        except: # catch *all* exceptions
            e = sys.exc_info()[0]
            print(e)