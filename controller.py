from os import path, listdir
from datetime import datetime
from lenskit_proxy import LenskitProxy
from data_manager import DataManager
from db_manager import DbManager
from model_manager import ModelManager

class Controller:
    models = {}

    def build_movies(self):
        dataManager = DataManager()
        dbManager = DbManager()
        movies = dataManager.get_movies()
        dbManager.build_movies(movies)

    def create_db_structure_with_data(self):
        dataManager = DataManager()
        dbManager = DbManager()
        movies = dataManager.get_movies()
        ratings = dataManager.get_ratings()
        dbManager.create_db_structure_with_data(movies, ratings)

    def save_models(self, algos, from_data_files):
        lkProxy = LenskitProxy()        
        if from_data_files:
            dataManager = DataManager()
            dataManager.directory_path = "data/ml-latest-small/"
            ratings = dataManager.get_ratings()
        else:
            dbManager = DbManager()
            ratings = dbManager.get_ratings()
        modelManager = ModelManager()
        for algo in algos.split(','):
            model = lkProxy.create_model(algo, ratings)
            modelManager.store(model, algo, False)

    def load_models(self, algos):
        modelManager = ModelManager()
        for algo in algos.split(','):
            modelManager.load_for_shared_mem(algo)
