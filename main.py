"""
this is the main script to run the program
the program chooses a random anime for you to watch
"""

import random
import pandas as pd
import requests as rq
import json
import os
import sys
from termcolor import colored, cprint

os.system("cls")
message = colored("Do You Want To Choose Another One? ('y','n'):\n", 'red', attrs=['reverse', 'blink'])



def choose_anime() -> json:
    """Returns anime
        args:
            None
        returns:
            anime - json
    """
    anime = rq.get("https://api.jikan.moe/v4/random/anime/")
    anime = json.loads(anime.text)
    anime = anime["data"]
    return anime

def get_genres(x) -> list :
    """Returns the genres of the anime
        args:
            anime - json
        returns:
            genres - list
    """
    x = pd.DataFrame(x["genres"])
    if 'name' not in x:
        return ["None"]
    else:
        return pd.Series(x.name).to_string(index=False)

def get_rating(x) -> str:
    """Returns anime rating
        args:
            anime - json
        returns:
            rating - string
    """
    return x["rating"]

def isvalid(x) -> bool:
    """checks if anime is valid for audience under 18
        args:
            anime - json
        returns:
            if anime is valid or not - bool
    """
    if str(get_rating(x)) == 'Rx - Hentai' or str(get_rating(x)) == 'R+ - Mild Nudity':
        return False
    else:
        return True
        

while True:
    anime = choose_anime()
    if isvalid(anime) == True:
        os.system("cls") #clears the terminal every random anime choice
        print("---------------------------------------------------------")
        print ("Name : ", anime["title"]) #print anime title
        print ("Genres : \n", get_genres(anime)) #print anime genres
        print ("Rating : ", get_rating(anime)) #print anime rating
        choice = input(message) #takes the response from the user
        if choice == "y": #checks if choice is "y"
            continue #runs the while loop again
        else:
            break #exit the loop and terminate the program
    else:
        continue #runs the while loop again


