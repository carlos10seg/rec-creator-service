from os import path, listdir
from datetime import datetime
from lenskit_proxy import LenskitProxy
from data_manager import DataManager
from db_manager import DbManager
from model_manager import ModelManager

class Controller:
    models = {}

    def create_db_structure_with_data(self):
        dataManager = DataManager()
        dbManager = DbManager()
        movies = dataManager.get_movies()
        ratings = dataManager.get_ratings()
        dbManager.create_db_structure_with_data(movies, ratings)

    def save_models(self, algos):
        lkProxy = LenskitProxy()
        #dataManager = DataManager()
        #ratings = dataManager.get_ratings()
        dbManager = DbManager()
        ratings = dbManager.get_ratings()
        #print(len(ratings))
        modelManager = ModelManager()
        for algo in algos.split(','):
            model = lkProxy.create_model(algo, ratings)
            modelManager.store(model, algo)