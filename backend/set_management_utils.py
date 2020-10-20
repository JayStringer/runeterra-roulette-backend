"""Utility Functions responsible for making set management easier."""

import json
import logging
import os
import shutil
from typing import List
from zipfile import ZipFile

import requests

from backend.models import Card

LOGGER = logging.getLogger("SetManager")


_HERE = os.path.dirname(__file__)  # 'private' const

# Temp directory for intermediate data store
TEMP_DIR = os.path.join(_HERE, "temp")
NUMBER_OF_SETS = 3  # Total sets released for LoR


def set_zip(set_num: int) -> str:
    """Helper to build set zip name for given set number"""
    return f"set{set_num}-lite-en_us.zip"


def set_json(set_num: int) -> str:
    """Helper to build set JSON file name for given set number"""
    return f"set{set_num}-en_us.json"


def in_temp(filename: str) -> str:
    """Helper to build paths to files found in temp folder"""
    return os.path.join(TEMP_DIR, filename)


def guarantee_temp_dir() -> None:
    """Create a temp directory. Catch error in the event it already exists."""
    try:
        os.mkdir(TEMP_DIR)
        LOGGER.info("Temp directory created")
    except FileExistsError:  # Better to ask for forgiveness than permission
        LOGGER.info("Temp directory already exists")


def delete_temp_dir() -> None:
    """Delete temp directory and its contents."""
    try:
        shutil.rmtree(TEMP_DIR)
        LOGGER.info("Temp directory deleted")
    except OSError as err:
        LOGGER.error(err.strerror)


def download_set_data(set_num: int) -> str:
    """Download the set data from data dragon for given set number.
    Return file destination path.
    """
    file_name = set_zip(set_num)
    file_destination = os.path.join(TEMP_DIR, file_name)

    base_url = "https://dd.b.pvp.net/latest/"
    download_url = base_url + file_name

    LOGGER.info("Requesting %s", download_url)
    resp = requests.get(download_url, stream=True)

    with open(file_destination, "wb") as file_data:
        for chunk in resp.iter_content(chunk_size=128):
            file_data.write(chunk)

    LOGGER.info("Completed download of %s", file_name)
    return file_destination


def extract_set_json(set_num: int) -> str:
    """Extract set JSON file to temp folder.
    Extraction copies zip directory structure which is why path is
    temp/en_us/data/*.json. Path to extract json file is returned
    """
    set_json_filename = set_json(set_num)
    extract_target = f"en_us/data/{set_json_filename}"
    zip_location = in_temp(set_zip(set_num))
    extracted_to = os.path.join(TEMP_DIR, extract_target)

    with ZipFile(zip_location, "r") as zip_file:
        LOGGER.info(
            "Extracting %s from %s to %s",
            extract_target,
            zip_location,
            extracted_to,
        )
        zip_file.extract(member=extract_target, path=TEMP_DIR)

    return extracted_to


def read_set_json(set_json_path: str) -> List[Card]:
    """Read set JSON file at given path and return cards as Python List"""
    with open(set_json_path, "r") as set_json_content:
        cards = json.load(set_json_content)
    return cards
