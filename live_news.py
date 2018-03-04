import where_can_i_go_bot as souper
import data_manipulation
import time
import threading
import json


URLdict = {'nbc':'https://www.nbcnews.com', 'cbs':'http://www.cbs.news'}
newsdict = {'cbs': {}, 'nbc': {}}


def nbc(URLdict, newsdict, name):

    while True:
        # This just let's you visually see both threads are running
        print(name, 'Thread')
        # Grab robots.txt from the site
        robottxt = souper.MakeConnection(URLdict[name], URLdict.values(), '/robots.txt')
        # Check that it's okay to scrape there
        scrape = data_manipulation.oktoscrape(robottxt)
        # If it is make a request, and parse the returned data
        if scrape:
            bsdata = souper.MakeConnection(URLdict[name], URLdict.values(), '/')
            bsdata = souper.bs(bsdata.content, 'html.parser')
        # This should never happen, but if it does..
        else:
            print('Unknown Error: Please Consult a REAL Programmer')

        # I originally had seperate functions to do this, but NBC's lack of information in their code left me with no good way
        # to sort their links. So I decided to just allow the links I didn't want to populate the dictionaries first for both,
        # leaving me with(hopefully) just headlines after going live.
        # TODO I think a way extract what I actually want would be to,
        # TODO compare a new dictionary with the original removing all the links they share.
        for a in bsdata.find_all('a'):
            try:
                # if you do this you will understand how crazy the news site format their strings
                # this is just removing excess white space inside and out on the strings
                cleantext = a.text.replace('\n', '').replace('\t', '').replace('  ', '')
                # some links are stored as just /foo/bar.html or whatever, this ties them into a full URL
                if a.get('href').startswith('/'):
                    # if the text(headline) isn't in the dictionary add it and print
                    if cleantext not in newsdict[name].keys():
                                                            # added a time stamp
                        newsdict[name].update({cleantext: [time.time(), URLlist[name] + a.get('href')]})
                        print(cleantext, '\n', URLlist[name]+a.get('href'))
                # if the link is already a full URL do the same thing
                elif a.get('href').startswith(URLlist[name]):
                    if cleantext not in newsdict[name].keys():
                        newsdict[name].update({cleantext: [time.time(),a.get('href')]})
                        print(cleantext, '\n', URLlist[name] + a.get('href'))
            except AttributeError:
                pass
        # check for updates every x seconds
        time.sleep(10)
    #-----------------------------------------JSON to look at-----------------------------------------------------------
    # json is an easy way to r/w a dictionary to a file json.dump to write out
        with open('news','w') as f:
            json.dump(newsdict, f)
    #-------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # if you already have a dictionary try to open it first
    #-------------------------------------------more JSON---------------------------------------------------------------
    # json.load to read in
    try:
        with open('news', 'r') as f:
            newsdict = json.load(f)
    except FileNotFoundError:
        pass
    #-------------------------------------------------------------------------------------------------------------------




    #------------------------------------Threading to look at-----------------------------------------------------------
    # A container to hold your threads, these could just be variables if you wanted
    threadlist = []
    # The target is the name of the function you want to run, DO NOT USE () it will not work! Pass args using args
    # kwargs using kwargs
    threadlist.append(threading.Thread(target=nbc, args=[URLdict, newsdict, 'nbc']))
    threadlist.append(threading.Thread(target=nbc, args=[URLdict, newsdict, 'cbs']))
    # Once they're set up start them they will run individually until their target function stops
    threadlist[0].start()
    threadlist[1].start()
    #-------------------------------------------------------------------------------------------------------------------
