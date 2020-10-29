"""Script to update card database with latest data from Legends or Runeterra
data dragon.
"""

from backend.db_client import MongoClient
from backend.scripts.script_utils import (
    delete_temp_dir,
    download_set_data,
    extract_set_json,
    get_game_version_from_image_url,
    guarantee_temp_dir,
    read_set_json,
)

NUMBER_OF_SETS = 3  # Total sets released for LoR
SET_NUMBERS = range(1, NUMBER_OF_SETS + 1)


def main():
    guarantee_temp_dir()
    # Download all of the sets to a temporary folder
    for set_num in SET_NUMBERS:
        download_set_data(set_num)

    # Extract the JSON file that we're interested in from the set zips
    set_json_paths = [extract_set_json(set_num) for set_num in SET_NUMBERS]

    mongo_client = MongoClient()

    for set_json_path in set_json_paths:
        # Read card data from json files
        set_json = read_set_json(set_json_path)
        # Upsert each card to the database, mypy and pylint really hate this
        for card in set_json:
            mongo_client.upsert_card(card)

    # Not proud of this, to determine what the version of the card
    # collection is, get the image path url for the first card in the collection
    # and extract the version url from it.
    image_path = mongo_client.get_first_image_url()
    version = get_game_version_from_image_url(image_path)
    mongo_client.upsert_collection_version(version)

    # Update indexes to make sure queries are more efficient
    mongo_client.update_db_indexes()
    mongo_client.close()

    # Clean up by deleting the temporary folder
    delete_temp_dir()


if __name__ == "__main__":
    main()
