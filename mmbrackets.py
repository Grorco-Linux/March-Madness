import requests
from bs4 import BeautifulSoup as bs
import copy
import pprint
import json
from mmobjects import Team
import pickle
# request the pag
request = requests.get('https://www.cbssports.com/collegebasketball/ncaa-tournament/brackets/viewable_men#')

# parse it
bsed = bs(request.content, 'html.parser')
fullbracket = {}
round_0 = []


for li in bsed.find_all("li"):
    # if li doesn't have a class you get a type error
    try:

        if 'region0' in li.get('class'):
            division = 'First Four'
        if 'region1' in li.get('class'):
            division = 'South'
        if 'region2' in li.get('class'):
            division = 'East'
        if 'region3' in li.get('class'):
            division = 'West'
        if 'region4' in li.get('class'):
            division = 'Midwest'
        # I searched for li first to narrow down my results to the first round
        if 'round0' in li.get('class'):
            # Each set of teams is in one div
            for div in li.find_all('div'):
                # The names have a link associated with them so I grab the text from that
                teams = div.find_all('a')
                # There should be 2 non blank teams in a bracket
                if len(teams) == 2 and teams[0].text != "":
                    # Take the names with there seeds from teams and div respectively
                    round_0.append([Team(name= teams[0].text, seed=div.find_all('span')[0].text, region=division),
                                    Team(name= teams[1].text, seed=div.find_all('span')[-3].text, region=division)])

    # ignore these li's we don't need them
    except TypeError:
        pass

fullbracket.update({'round_0': round_0})
pprint.pprint(fullbracket, width=120)
