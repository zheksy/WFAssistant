#!/usr/bin/python3
import time
import random
import datetime
import WayfarerDataManager as wfdm
import json
import requests
from datetime import date

WAYFARER_JSON_PATH = './reviews.json'
DATABASE_PATH = './database.json'
REMOTE_DB_URL = 'https://api.jsonbin.io/v3/b/604faf7e7ea6546cf3dee383'

def main():
    dbUrl = REMOTE_DB_URL + "/latest"
    wfdm.pull_database_json(dbUrl,DATABASE_PATH)
    unprocessedData = wfdm.parse_json(WAYFARER_JSON_PATH)
    print(unprocessedData)
    print("\n===============================\n")
    processedData = wfdm.update_local_database(unprocessedData,DATABASE_PATH)
    #processedData = wfdm.remove_outdated_reviews(processedData,30)
    print(processedData)
    print("\n===============================\n")
    wfdm.sync_remote_database(REMOTE_DB_URL,processedData)
    


if __name__ == "__main__":
    main()