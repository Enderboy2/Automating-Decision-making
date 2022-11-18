import random
import pandas as pd
import requests as rq
import json
import os
import sys
from termcolor import colored, cprint
from subprocess import run as r
from random_anime_chooser import myFuncs as f
import pick as p

settings_list = []

with open(r'data\Settings.txt', 'r') as fp:
    for line in fp:
        x = line[:-1]
        # add current item to the list
        settings_list.append(bool(x))
fp.close()
def settings():
    explict = settings_list[0]
    while True:
        options = ["Show explict content : " + str(explict),"Save & Exit"]
        option, index = p.pick(options, "Automating Decision-Making", indicator='=>', default_index=0)
        if index == 0:
            if explict == True:
                explict = False
                settings_list[0] = explict
            else:
                explict = True
                settings_list[0] = explict
        elif index == 1:
            fp =open(r'data\Settings.txt', 'w')
            for setting in settings_list:
                fp.write("%s\n" % str(setting))# write each item on a new line)
            fp.close()
            break
    select_app()

def select_app():
    options = ["Random anime","Settings","Exit"]
    option, index = p.pick(options, "Automating Decision-Making", indicator='=>', default_index=0)
    if option == "Random anime":
        run()
    elif index == 1:
        settings()
    elif index == 2:
        print("Program Exited")
        quit()
        

def clear():
    """
    clears the terminal
    """
    os.system("cls") #clears the terminal every random anime choice

def display(x):
    """
    Displays the anime information
    """
    print("---------------------------------------------------------")
    print ("Name : ", x["title"]) #print anime title
    print ("Genres : \n", get_genres(x)) #print anime genres
    print ("Rating : ", get_rating(x)) #print anime rating

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

#app

def choose_anime() -> json:
    """Returns anime
        args:
            None
        returns:
            anime - json
    """
    url = "https://api.jikan.moe/v4/random/anime/"

    try:
        anime = rq.get(url)
        anime = json.loads(anime.text)
        anime = anime["data"]
    except rq.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
        return choose_anime()
    except rq.exceptions.TooManyRedirects:
        # Tell the user their URL was bad and try a different one
        print("there was a problem with the url provided")
    except rq.exceptions.RequestException as e:
        # catastrophic error - exit.
        raise SystemExit(e)

    return anime

message = colored("Do You Want To Choose Another One? ('y','n'):\n", 'red', attrs=['reverse', 'blink'])

def run():
    #This is the driver code for the random anime chooser
    while True:
        anime = choose_anime()
        if settings_list[0] == True:
                f.clear()
                f.display(anime)
                choice = input(message) #takes the response from the user
                if choice == "y": #checks if choice is "y"
                    continue #runs the while loop again
                else:
                    select_app()
        else:
            if f.isvalid(anime) == True:
                os.system("cls") #clears the terminal every random anime choice
                print("---------------------------------------------------------")
                print ("Name : ", anime["title"]) #print anime title
                print ("Genres : \n", f.get_genres(anime)) #print anime genres
                print ("Rating : ", f.get_rating(anime)) #print anime rating
                choice = input(message) #takes the response from the user
                if choice == "y": #checks if choice is "y"
                    continue #runs the while loop again
                else:
                    select_app()
            else:
                continue #runs the while loop again