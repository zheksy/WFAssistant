import time
import random
import datetime
import json
from datetime import date
import keyboard
import WayfarerDataManager as wfdm
from lxml import html
import random

def resolve_captcha():
    """sends an email to the user to manually resolve the captcha.
    """
def exitbrowser():
    keyboard.press_and_release("alt+f4")

def logout():
    """
    """
    time.sleep(15)
    keyboard.press_and_release("f5")
    for i in range(0,11):
        time.sleep(1)
        keyboard.press_and_release("tab")
    keyboard.press_and_release("enter")

def login_with_google():
    """
    """
    time.sleep(15)
    sequence = ["f5","tab","enter"]
    for key in sequence:
        time.sleep(1)
        keyboard.press_and_release(key)


def select_an_account(offset):
    """
    """
    time.sleep(15)
    keyboard.press_and_release("f5")
    offset = offset + 1 #skips the first line
    for i in range(0,offset):
        time.sleep(1)
        keyboard.press_and_release("tab")
    keyboard.press_and_release("enter")

def define_site_state(path):
    """determines whether it's a submission, edit or photo review in wayfarer.
       @param path: path to the saved HTML of review site, done using SingleFile browser extension.
       @return state: returns the current state of the review site. used to determine the course of action, depending if it's a submission, edit or a photo review in wayfarer
    """
    #this ABSOLUTELY needs to be done better, using some sort of div selection. but i don't want to currently.
    with open(path, encoding ="utf8") as f:
        htmlstring = f.read()
    if "<span ng-show=\"reviewCtrl.reviewType==='NEW'\">Review</span>" in htmlstring:
        state = "review"
    else:
        if "<span ng-show=\"reviewCtrl.reviewType==='EDIT'\">Edit</span>" in htmlstring:
            state = "edit"
        if "<span ng-show=\"reviewCtrl.reviewType==='PHOTO'\">Select the photos that don't meet the criteria</span>" in htmlstring:
            state = "photo"
        if "captcha" in htmlstring:
            state = "captcha"
        if "Choose an account" in htmlstring:
            state = "select_account"
        if "Continue with Google" in htmlstring:
            state = "login_screen"
        if "Featured Wayspots" in htmlstring:
            state = "wf_home"

    print(state)
    return state

def main():
    time.sleep(10)
    login_with_google()
    time.sleep(10)
    select_an_account(1)
    time.sleep(10)
    logout()

if __name__ == "__main__":
    main()