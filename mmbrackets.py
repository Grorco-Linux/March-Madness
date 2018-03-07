import requests
from bs4 import BeautifulSoup as bs
import copy
import pprint
import json

# request the pag
request = requests.get('https://www.cbssports.com/collegebasketball/ncaa-tournament/brackets/viewable_men#')

# parse it
bsed = bs(request.content, 'html.parser')
fullbracket = {}
round_0 = []


for li in bsed.find_all("li"):
    # if li doesn't have a class you get a type error
    try:
        # I searched for li first to narrow down my results to the first round
        if 'round0' in li.get('class'):
            # Each set of teams is in one div
            for div in li.find_all('div'):
                # The names have a link associated with them so I grab the text from that
                teams = div.find_all('a')
                # There should be 2 non blank teams in a bracket
                if len(teams) == 2 and teams[0].text != "":
                    # Take the names with there seeds from teams and div respectively
                    round_0.append([{'name': teams[0].text, 'seed':div.find_all('span')[0].text},
                                    {'name': teams[1].text, 'seed':div.find_all('span')[-3].text}])

    # ignore these li's we don't need them
    except TypeError:
        pass

fullbracket.update({'round_0': round_0})
pprint.pprint(fullbracket)
