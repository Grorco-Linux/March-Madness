import requests
from bs4 import BeautifulSoup as bs
import pprint

# A list of URLs you want to get the robots.txt from
URLlist = ['http://www.google.com', 'https://www.reddit.com']

def MakeConnection(URL, URLlist):
    myHeader = {'User-Agent': 'python-requests/2.18.4 (Compatible; Grorco; mailto:Grorco.linux@gmail.com)'}
    response = requests.get(URL, headers=myHeader)
    if response.status_code != 200:
        if URLlist.index(URL) == len(URLlist):
            print('{} has rejected your request, trying {} next'.format(URL, URLlist[URLlist.index(URL)+1]))
        else:
            print('{} has rejected your request, there are no more URLs to try'.format(URL))
        response = None
    return response

def GetAllowed(response):
    # Create a blank list for the allowed and disallowed paths
    allowedlist = []
    disallowedlist = []

    # wait is a variable to ignore other bots allows and disallows
    wait = False

    # Check each line in the text
    for line in response.text.split('\n'):
        # First see if it is talking about you, for us that would be *
        if line.startswith('User-Agent:'):
            if line.split()[1] == '*':
                # If its us no need to wait
                wait = False
            else:
                wait = True
        # There isn't an enforced capitalization standard, so check using lower
        # If the line starts with allow/disalow split it and add the path to the associated list
        if line.lower().startswith('allow:') and wait == False:
            allowedlist.append(line.split()[1])
        elif line.lower().startswith('disallow:') and wait == False:
            disallowedlist.append(line.split()[1])

    return allowedlist, disallowedlist


def SiteDictMaker(URLlist):
    # Create a dictionary to store your info in
    sitedict = {}
    # For each site in your URL list
    for site in URLlist:
        # Request the robots.txt file
        response = MakeConnection(URLlist[0] + '/robots.txt', URLlist)
        # Check for None type
        if response:
            # sort the file into an allowed and disallowed list
            allowedlist, disallowedlist = GetAllowed(response)
            # store it all in a dictionary
            sitedict.update({site: {'allowed': allowedlist, 'disallowed': disallowedlist}})
    return sitedict


def GetLinks():
    URLlist = ['http://www.ncaa.com', 'https://www.pbs.com', 'http://www.google.com/1234']
    for URL in URLlist:
        response = MakeConnection(URL, URLlist)
        if response:
            soup = bs(response.content, "html.parser")
            for a in soup.find_all('a'):
                try:
                    if a.get('href').startswith('https://') or a.get('href').startswith('http://'):
                        print(a.text)
                        print(a.get('href'))
                except AttributeError:
                    pass
# Runs everything
sitedict = SiteDictMaker(URLlist)
# pretty print out the results
pprint.pprint(sitedict)
# Grabs some links from sites
GetLinks()




