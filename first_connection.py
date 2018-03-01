# Day 1 of March Madness

import requests
import sys

# the website you want to make a request to
URL = 'https://www.google.com'
def MakeConnection(URL):
    # Your header should include your info
    myHeader = {'User-Agent': 'python-requests/2.18.4 (Compatible; Grooco; mailto:grorco.linux@gmail.com)'}

    # Submit a get request to the URL, along with your header
    response = requests.get(URL, headers=myHeader)

    # If the status code is not 200 something went wrong, print Rejected and exit the program
    if response.status_code != 200:
        print('Rejected')
        sys.exit()

    # return the response object
    return response

# Get the response object for your URL/robots.txt
response = MakeConnection(URL + '/robots.txt')

# Print out the text of the response object
print(response.text)