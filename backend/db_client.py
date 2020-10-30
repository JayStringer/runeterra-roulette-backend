"""MongoDB client for interfacing with cards collection"""

import logging
from typing import Dict, List, Optional, Union

import pymongo

from backend.models import Card, CardDoc, RarityRef, RegionRef


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
        """Initialise MongoClient."""
        self.logger = logging.getLogger(self.__class__.__name__)
        self._client = pymongo.MongoClient(f"mongodb://{host}:{port}/")
        self.logger.info("Connection to mongodb established")

        self._db = self._client["runeterra-roulette-db"]
        self.card_collection = self._db["cards"]
        self.collection_config = self._db["config"]

    def __enter__(self):
        """Allows class to be used with context manager."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Close connection to mongodb on manager exit."""
        self.close()

    def close(self):
        """Close connection to client."""
        self._client.close()
        self.logger.info("Connection to mongodb closed")

    def update_db_indexes(self) -> None:
        """Add indexes to card collection to make queries faster"""
        self.card_collection.create_index(
            [
                ("regionRef", pymongo.ASCENDING),
                ("rarityRef", pymongo.ASCENDING),
                ("collectible", pymongo.ASCENDING),
            ]
        )
        self.logger.info("Cards collection indexes updated")

    def upsert_card(self, card: Card) -> None:
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

    def find_cards(
        self,
        regions: List[RegionRef],
        rarities: List[RarityRef],
        limit: int = 0,
        projection: Optional[Union[Dict, List]] = None,
    ):
        """Search for N (limit) number of cards in cards that falls under any
        of the given regions and matches rarity to one of the given rarities.
        A limit of 0 (default) is the same as having no limit.

        Specify what is returned with the projection argument.
        """
        query = {
            "collectible": True,
            "regionRef": {"$in": regions},
            "rarityRef": {"$in": rarities},
        }

        self.logger.info("Card search query: %s", query)

        return self.card_collection.find(filter=query, limit=limit, projection=projection)

    def get_first_image_url(self) -> str:
        """Return absoluteGamePath url string for first card in the collection.
        To be used exclusively to determine what the version of the card
        collection is in the 'update_cards_database' script.

        This is unfortunately the only way i've discovered of
        getting the version of the 'latest' cards after downloading them. It
        would be good if they included the version of the cards collection as
        part of the meta.json file (just incase any riot devs are reading).

        This method is super brittle, use at your own risk or at the very least
        wrap this in a try.
        """
        self.logger.warning("Getting image url of first card, I hope you know what you're doing.")
        first_card = self.card_collection.find_one(projection={"assets.gameAbsolutePath"})
        return first_card["assets"][0]["gameAbsolutePath"]  # Wonky data structure

    def upsert_collection_version(self, version: str) -> None:
        """Update the version of the card collection"""
        _id = {"_id": "version"}
        doc = {**_id, "version": version}
        self.collection_config.replace_one(filter=_id, replacement=doc, upsert=True)
        self.logger.info("Updated collection version to %s", version)

    def get_collection_version(self) -> str:
        """Retrieve the collection version from the collection config"""
        self.logger.info("Requesting collection version")
        return self.collection_config.find_one({"_id": "version"})["version"]
