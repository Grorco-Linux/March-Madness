import requests
from bs4 import BeautifulSoup as bs
import pprint

# A list of URLs you want to get the robots.txt from
URLlist = ['http://www.google.com', 'https://www.reddit.com']

def MakeConnection(URL, URLlist):
    # The user-agent basically lets the website know who you are
    myHeader = {'User-Agent': 'python-requests/2.18.4 (Compatible; Grorco; mailto:Grorco.linux@gmail.com)'}
    # Tell the website who you are, and request the content of the page you have sent them
    response = requests.get(URL, headers=myHeader)
    # If you are allowed and there are no problems, you should get a response code of 200
    # An example of a fail would be a 404 error
    if response.status_code != 200:
        # Check how far you hav iterated through the list, and give an appropriate error
        if URLlist.index(URL) == len(URLlist):
            print('{} has rejected your request with a {} error,'
                  ' trying {} next'.format(URL, response.status_code, URLlist[URLlist.index(URL)+1]))
        else:
            print('{} has rejected your request with a {} error,'
                  ' there are no more URLs to try'.format(URL, response.status_code))
        # If you got a bad response change it to a None type so we can check it for Truth
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
    # For every URL in your list
    for URL in URLlist:
        # Try to make a connection and get a response
        response = MakeConnection(URL, URLlist)
        # If the response holds information, is not None/False
        if response:
            # Use Beautiful Soup to organise the information in a more useful manner
            soup = bs(response.content, "html.parser")
            # In html <a href=somelink.com>My Link</a> signifies a link, find all looks for the word inside the trailing
            # </> so for a link we want to itterate over the list returned from find_all('a')
            for a in soup.find_all('a'):
                # Not every link is to a url, so you need to catch an error if it doesn't contain a 'href'
                try:
                    # if a has a 'href'(Hypertext REFerence) that points to http, or https
                    if a.get('href').startswith('https://') or a.get('href').startswith('http://'):
                        # Print the text that holds the link
                        print(a.text)
                        # Print the URL it points too
                        print(a.get('href'))
                # This could happen if it was <a download=somefilelocation>My file</a> or something along those lines
                except AttributeError:
                    pass
# Runs everything
sitedict = SiteDictMaker(URLlist)
# pretty print out the results
pprint.pprint(sitedict)
# Grabs some links from sites
GetLinks()




