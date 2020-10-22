"""API for Runterra Roulette Web Application"""

import random

from flask import Flask, jsonify, request
from flask_cors import CORS

import backend.api_utils as api_utils
from backend.db_client import MongoClient


class RunterraRouletteAPI:
    def __init__(self):
        self.app = Flask(self.__class__.__name__)
        CORS(app=self.app)
        self.mongo_client = MongoClient()

        self.app.add_url_rule(rule="/cards", methods=["GET"], view_func=self.get_cards)

    def run(self, host: str = "localhost", port: int = 8080, debug: bool = True):
        self.app.run(host=host, port=port, debug=debug)

    def get_cards(self):
        """waffles"""
        request_data = api_utils.digest_request(req=request)
        cards = self.mongo_client.find_cards(
            regions=request_data["region_refs"],
            rarities=request_data["rarity_refs"],
            projection=["name", "assets.gameAbsolutePath", "cardCode", "set"],
        )

        cards = list(cards)
        if count := request_data["count"]:
            random.shuffle(cards)
            cards = cards[:count]

        return jsonify(cards)


if __name__ == "__main__":
    api = RunterraRouletteAPI()
    api.run()
