import logging
from typing import Dict

import pymongo

from backend.models import Card, CardDoc


# Should probably make the class name less generic, or make the class more
# generic and inherit it to a more accurately named class.
class MongoClient:
    """MongoDB client specifically for interfacing with cards collection.
    Actions include inserting/updating cards and retrieving cards from the
    cards collection.

    Example:

        with MongoClient() as client:
            client.upsert_card(card)

    This class can be used as a context manager as shown in the example
    above.
    """

    def __init__(self, host: str = "localhost", port: int = 27017):
        """Initialise MongoClient"""
        self.logger = logging.getLogger(self.__class__.__name__)
        self._client = pymongo.MongoClient(f"mongodb://{host}:{port}/")
        self.logger.info("Connection to mongodb established")

        self._db = self._client["runeterra-roulette-db"]
        self.card_collection = self._db["cards"]

    def __enter__(self):
        """Allows class to be used with context manager"""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Close connect to mongodb on manager exit"""
        self.logger.info("Connection to mongodb closed")
        self._client.close()

    def upsert_card(self, card: Card):
        """Update/insert a card into the 'cards' collection in the database.

        Cards are unique by card code. If one exists already in the collection
        with the same _id then the document will be updated. This is to make
        updating the card collection easy when Riot releases patches.
        """
        _id = {"_id": card["cardCode"]}
        # Have to make mypy look the other way due to an issue with dict.update
        # that I think the ** is using internally.
        # https://github.com/python/mypy/issues/6462
        # https://github.com/python/mypy/issues/9408
        doc: CardDoc = {**card, **_id}  # type: ignore
        self.card_collection.replace_one(filter=_id, replacement=doc, upsert=True)
        self.logger.info("Inserted '%s' to the database", card["name"])
