"""Script to update card database with latest data from Legends or Runeterra
data dragon.
"""

import logging

from backend.db_client import MongoClient
from backend.set_management_utils import (delete_temp_dir, download_set_data,
                                          extract_set_json, guarantee_temp_dir,
                                          read_set_json)

NUMBER_OF_SETS = 3  # Total sets released for LoR
SET_NUMBERS = range(1, NUMBER_OF_SETS + 1)


def main():
    guarantee_temp_dir()
    # Download all of the sets to a temporary folder
    [download_set_data(set_num) for set_num in SET_NUMBERS]
    
    # Extract the JSON file that we're interested in from the set zips
    set_json_paths = [extract_set_json(set_num) for set_num in SET_NUMBERS]

    for set_json_path in set_json_paths:
        # Read card data from json files
        set_json = read_set_json(set_json_path)
        
        with MongoClient() as client:
            # Upsert each card to the database
            [client.upsert_card(card) for card in set_json]

    # Clean up by deleting the temporary folder
    delete_temp_dir()


if __name__ == "__main__":
    main()
