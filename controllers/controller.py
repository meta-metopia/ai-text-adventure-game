from pymongo import MongoClient


class Controller:
    client: MongoClient

    def __init__(self, client: MongoClient):
        self.client = client
        self.db = self.client["gamebot"]
