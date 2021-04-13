#!/usr/bin/python3
import time
import random
import datetime
import json
import requests
from datetime import datetime
from datetime import date

DB_URL = "https://api.jsonbin.io/v3/b/604faf7e7ea6546cf3dee383"
DB_PATH = "./database.json"
REVIEWS_JSON_PATH = "./reviews.json"
headers = {
  'X-Master-Key': '$2b$10$2vRroxnJu84XB6w.X78Mqu0tcIL8LjpUJ5lxaY/z.VZnUF.QCm3/m'
    }
headers_post = {
  'Content-Type': 'application/json',
  'X-Master-Key': '$2b$10$2vRroxnJu84XB6w.X78Mqu0tcIL8LjpUJ5lxaY/z.VZnUF.QCm3/m'
}

def pull_database_json(url,path):
    """pulls the json with review scores from the specified URL and saves it to path.

       @param url: url of the database json. most probably a google doc.
    """
    if "latest" not in url:
        url = url + "/latest"
    print(url)
    jsonToWrite = []
    req = requests.get(url, json=None, headers=headers)
    text = req.text
    with open("./tmpdb.json",'w',encoding="utf8") as f:
        f.write(text)
    with open("./tmpdb.json",'r',encoding="utf8") as f:
        data = json.load(f)
    data = data["record"]
    with open("./database.json",'w',encoding="utf8") as f:
        json.dump(data,f)


def backup(backup_dir, data):
    date = str(datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")).replace(":","_")
    
    name = "database_" + date + ".json"
    full_path = backup_dir + name
    with open(full_path, 'x', encoding="utf8") as f:
        f.write(str(data))




def append_data(data,path):
    """removes already existing reviews in database.json from reviews.json, and appends the remaining reviews to database.json.
      also adds a timestamp to new data, for easier json maintenance.
      
      @parameter data: serialized json of raw wayfarer+ review data

      @param path: path to the database.json file

      @return database: database updated with newest data
    """
    with open (path, encoding="utf8") as f: #'./database.json' is path usually
        database = json.load(f)
    for submission in data:
        alreadyExists = False
        for reviewed in database:
            SUrl = submission["imageUrl"]
            RUrl = reviewed["imageUrl"]
            if SUrl == RUrl:
                alreadyExists = True
                break
        if not alreadyExists:
            submission["timestamp"] = str(date.today())
            #print(submission)
            if submission["review"] != False:
                database.append(submission) 
    return database
    
def remove_timeouts(data):
    updatedData = []
    for i in data:
        if i["review"] != False:
            updatedData.append(i)
    
    return updatedData

def sync_remote_database(url,path):
    data = parse_json(path)
    req = requests.put(url, json=data, headers=headers_post)
    print(req.text)

def remove_outdated_reviews(jsonData, age):
    """removes entries that are older than a certain age.
    """
    updatedData = []
    for submission in jsonData:
        timestamp = submission["timestamp"]
        today = date.today()
        difference = today - timestamp
        print(difference.days)
        if difference.days < age:
            submission["timestamp"] = str(timestamp)
            updatedData.append(submission)
    return updatedData
        
    
    
def parse_json(path):

    with open(path,"r", encoding="utf8") as f:
        data = json.load(f)
        return data


def main():
    new_reviews = parse_json(REVIEWS_JSON_PATH)
    database = parse_json(DB_PATH)
    data_to_write = append_data(new_reviews,DB_PATH)
    database = data_to_write
    with open(DB_PATH,"w",encoding="utf8") as f:
        json.dump(database,f)
    sync_remote_database(DB_URL,DB_PATH)
        
if __name__ == "__main__":   
    main()