from bs4 import BeautifulSoup as bs
from mmobjects import Team
import pickle
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def main():


    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(firefox_options=options)

    #driver = webdriver.PhantomJS()
    driver.get('https://www.cbssports.com/collegebasketball/ncaa-tournament/brackets/viewable_men#')

    html = driver.page_source
    # request the page
    #request = requests.get('https://www.cbssports.com/collegebasketball/ncaa-tournament/brackets/viewable_men#')

    # parse it
    bsed = bs(html, 'html.parser')
    driver.close()
    fullbracket = {}
    round_0 = []
    round_1 = []
    round_2 = []
    round_3 = []

    for li in bsed.find_all("li"):
            # if li doesn't have a class you get a type error
        try:

            if 'region0' in li.get('class'):
                region = 'First Four'
            if 'region1' in li.get('class'):
                region = 'South'
            if 'region2' in li.get('class'):
                region = 'East'
            if 'region3' in li.get('class'):
                region = 'West'
            if 'region4' in li.get('class'):
                region = 'Midwest'
            # I searched for li first to narrow down my results to the first round
            if 'round0' in li.get('class'):
                # Each set of teams is in one div
                round_0 = populate(round_0, region, li)
            if 'round1' in li.get('class'):
                # Each set of teams is in one div
                round_1 = populate(round_1, region, li)
            if 'round2' in li.get('class'):
                # Each set of teams is in one div
                round_2 = populate(round_2, region, li)
            if 'round3' in li.get('class'):
                # Each set of teams is in one div
                round_3 = populate(round_3, region, li)


        # ignore these li's we don't need them
        except TypeError:
            pass

    fullbracket.update({'Round 1': round_0, 'Round 2': round_1, 'Round 3': round_2, 'Round 4': round_3})
    print(fullbracket)
    if round_0 != []:
        with open('test', 'wb') as f:
            pickle.dump(fullbracket, f, -1)
        return fullbracket

def populate(roundnum, region, li):
    for div in li.find_all('div'):
        # The names have a link associated with them so I grab the text from that
        teams = div.find_all('a')
        # There should be 2 non blank teams in a bracket
        if len(teams) == 2 and teams[0].text != "":
            # Take the names with there seeds from teams and div respectively
            roundnum.append([Team(name= teams[0].text, seed=div.find_all('span')[0].text,
                                 points= div.find_all('span')[2].text, region=region),
                            Team(name= teams[1].text, seed=div.find_all('span')[-3].text,
                                 points= div.find_all('span')[-1].text,region=region)])

    return roundnum

if __name__ == '__main__':
    main()
