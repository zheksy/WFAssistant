#!/usr/bin/python3
import time
import random
import datetime
import WayfarerDataManager as wfdm
import ReviewManager as rm
import json
import requests
import os
from datetime import date
import SiteStateResolver as ssr
import subprocess

def read_accs_and_offsets(file):
    accs_and_offsets = []
    with open(file) as f:
        for i in f.read().splitlines():
            tmp = i.split(',')
            accs_and_offsets.append(tmp)
    return accs_and_offsets

def do_reviews(downloadsDir,database):
    review_log = []
    negativeMatches = 5
    lastKnownSequence = []
    fileFound = False
    while negativeMatches:
        print("beginning review...")
        time.sleep(15)
        files = os.listdir(downloadsDir)
        for file in files:
            fileFound = False
            if "Wayfarer" in file:
                fileFound = True
                print("loading HTML file for parsing...")
                wayfarerHtmlPath = downloadsDir + file

                review_state = ssr.define_site_state(wayfarerHtmlPath)
                if review_state == "photo":
                    rm.photo_key_sequence()
                    remove_saved_sites(downloadsDir)                      
                    break
                if review_state == "edit":
                    rm.edit_key_sequence()
                    remove_saved_sites(downloadsDir)                       
                    break                
                if review_state == "captcha":
                    ssr.resolve_captcha()
                    remove_saved_sites(downloadsDir)  
                    break
                
                with open(wayfarerHtmlPath, encoding="utf8") as f:
                    currentSubmission = f.readlines()

                noMatch = True
                for submission in database:
                    imageUrl = str(submission["imageUrl"])
                    if imageUrl in str(currentSubmission):
                        #this part of the code manages reviews in case of a match in the wayfarer site, and the review database.
                        sequence = rm.build_sequence_from_json(submission)
                        print("match found!\n")
                        print(sequence)
                        noMatch = False                        
                        break

                remove_saved_sites(downloadsDir)   
                        
                if noMatch:
                    print("no match, generating random sequence...\n")
                    sequence = rm.generate_random_sequence()
                    negativeMatches = negativeMatches - 1
                    if negativeMatches == 0:
                        sequence = ['3','3']
                    print(sequence)

                lastKnownSequence = sequence
                rm.review_key_sequence(sequence)
                break
        if not fileFound:                             
            print("file not found, possibly needed to select the type of submission. resolving and trying again...")
            rm.possible_submission_type_needed_resolve(lastKnownSequence)
    if negativeMatches == 0:
        print("5 negative matches detected, stopping review on this account to prevent rating decrease")

    return review_log

def remove_saved_sites(downloadsDir):
    """removes all wayfarer .html files in the directory.
    """
    files = os.listdir(downloadsDir)
    for file in files:
        fileFound = False
        if "Wayfarer" in file:
            fileFound = True
            wayfarerHtmlPath = downloadsDir + file
            try:
                os.remove(wayfarerHtmlPath) 
            except:
                print("wayfarer site HTML file doesn't seem to exist")

        if "Sign in - Google Accounts" in file:
            fileFound = True
            wayfarerHtmlPath = downloadsDir + file
            try:
                os.remove(wayfarerHtmlPath) 
            except:
                print("wayfarer site HTML file doesn't seem to exist")

def main():
   # print("pulling database...")
   # try:
   #     wfdm.pull_database_json(wfdm.DB_URL, "./database.json")
   # except:
   #     print("pulling db failed, using latest local version instead...")
    database = wfdm.parse_json("./database.json")

    print("backuping old data..")
    wfdm.backup("./db_backups/",database)
    with open("./downloads_dir.txt") as f:
        downloadsDir = f.readlines()
    downloadsDir = downloadsDir[0]

    accs_and_offsets = read_accs_and_offsets("./accs_and_offsets.txt")
    print("accounts to be used in this session:\n")
    print(accs_and_offsets)

    os.startfile("wf_front.url")
    ssr.logout()
    ssr.exitbrowser()

    for acc in accs_and_offsets:
        time.sleep(15)
        review_log = []
        os.startfile("review.url")
        ssr.login_with_google()
        ssr.select_an_account(int(acc[1]))
        print("cleaning up saved sites before starting reviews on a new account")
        remove_saved_sites(downloadsDir)       
        review_log = do_reviews(downloadsDir,database)
        time.sleep(5)
        ssr.logout()
        ssr.exitbrowser()

             
   
    


if __name__ == "__main__":
    #database = wfdm.parse_json("./database.json")
    #with open("./downloads_dir.txt") as f:
    #    downloadsDir = f.readlines()
    #downloadsDir = downloadsDir[0]
    #do_reviews(downloadsDir,database)
    main()