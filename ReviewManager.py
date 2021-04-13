import time
import random
import datetime
import json
from datetime import date
import keyboard
import WayfarerDataManager as wfdm
from lxml import html
import random


#def check_for_forks(path, sequence):
#    """checks for fork submissions. adapts the review sequence accordingly.
#    """
#    with open(path) as f:
#        htmlstring = f.read()
#
#    if "Narodne Garde" in htmlstring:
#        sequence = ['1','5','1','f','a','k','e']
#    if "Josipa Jovi" in htmlstring:
#        sequence = ['1','5','1','f','a','k','e']
#    if "Throndheimsk" in htmlstring:
#        sequence = ['1','5','1','f','a','k','e']
#    return sequence
#


def review_key_sequence(sequence):
    """presses the previously defined key sequence for a review.
       @param sequence: a list of keys to press (names of keys, eg. '5', 'enter')
    """
    time.sleep(5)
    for key in sequence:
        keyboard.press_and_release(key)
        time.sleep(1)
    keyboard.press_and_release('enter')


def edit_key_sequence():
    time.sleep(15)
    for i in range (0,12):
        time.sleep(1)
        keyboard.press_and_release("tab")
    keyboard.press_and_release("enter")

def photo_key_sequence():
    time.sleep(15)
    for i in range (0,13):
        time.sleep(1)
        keyboard.press_and_release("tab")
    keyboard.press_and_release("enter")
    
def build_sequence_from_json(review):
    """parses the review for grades and builds a sequence of keys. the sequence is a list of key names as strings.
       @param review: the JSON of the review to parse
       @return sequence: the sequence of keys to press in order to review.
    """
    sequence = []
    grades = review["review"]
    if grades["quality"]:
        if grades["quality"] == 1:
          sequence = ['1','1','2'] #temporary invalid resolver. will be done better in the future
        else:
            quality = str(grades["quality"])
            description = str(grades["description"])
            cultural = str(grades["cultural"])
            uniqueness = str(grades["uniqueness"])
            safety = str(grades["safety"])
            location = str(grades["location"])

            sequence.append(quality)
            sequence.append(description)
            sequence.append(cultural)
            sequence.append(uniqueness)
            sequence.append(safety)
            sequence.append(location)
    else:
        sequence = generate_random_sequence()
    if grades["duplicate"] == "true":
        sequence = ['d','tab','tab']
    
    return sequence

def possible_submission_type_needed_resolve(sequence):
    for i in range(0,72):
        time.sleep(0.1)
        keyboard.press_and_release("tab")
    typeof = random.randint(0,1) #to determine whether it will be marked as playground or as athletic field.
    if typeof:
        keyboard.press_and_release("a")
        time.sleep(0.5)
        keyboard.press_and_release("t")
        time.sleep(0.5)
        keyboard.press_and_release("h")
        for i in range(0,2):
            time.sleep(0.5)
            keyboard.press_and_release("down")
        time.sleep(0.5)
        keyboard.press_and_release("enter")
        for i in range(0,3):
            time.sleep(0.5)
            keyboard.press_and_release("down")
        time.sleep(0.5)
        keyboard.press_and_release("enter")
        review_key_sequence(sequence)
    else:
        keyboard.press_and_release("p")
        time.sleep(0.5)
        keyboard.press_and_release("l")
        time.sleep(0.5)
        keyboard.press_and_release("a")
        time.sleep(0.5)
        keyboard.press_and_release("y")
        time.sleep(0.5)
        keyboard.press_and_release("down")
        time.sleep(0.5)
        keyboard.press_and_release("enter")
        review_key_sequence(sequence)

def generate_random_sequence():
    sequence = []
    grade = str(random.randint(1,5))
    if grade == "1":
        sequence = ['1','1','2']
    else:
        sequence.append(grade)
        sequence.append(str(random.randint(4,5)))
        sequence.append(str(random.randint(2,5)))
        sequence.append(str(random.randint(2,5)))
        sequence.append(str(random.randint(5,5)))
        sequence.append(str(random.randint(3,5)))
        
    return sequence


def main():
    #with open ('./TestReview.json', encoding="utf8") as f:
    #    review = json.load(f)
    #review = review[0]
    #sequence = build_sequence_from_json(review)
    #print(sequence)
    #review_key_sequence(sequence)
    print("starting sequence")
    edit_key_sequence()

if __name__ == "__main__":
    main()