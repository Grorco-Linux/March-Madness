import where_can_i_go_bot as souper
import data_manipulation
import time
import threading
import json
import pprint

URLlist = {'nbc':'https://www.nbcnews.com', 'cbs':'http://www.cbs.news'}
newsdict = {'cbs': {}, 'nbc': {}}




def nbc(bsdata, newsdict, name):
    print(name, 'Thread')

    while True:
        time.sleep(60)
        for a in bsdata.find_all('a'):
            try:
                if a.get('href').startswith('/'):
                    cleantext = a.text.replace('\n','').replace('\t', '').replace('  ', '')
                    if cleantext not in newsdict[name].keys():
                        newsdict[name].update({cleantext: URLlist[name] + a.get('href')})
                        print(cleantext, '\n', URLlist[name]+a.get('href'))

                elif a.get('href').startswith(URLlist[name]):
                    if cleantext not in newsdict[name].keys():
                        newsdict[name].update({cleantext: a.get('href')})
                        print(cleantext, '\n', URLlist[name] + a.get('href'))
            except AttributeError:
                pass

    #-----------------------------------------JSON to look at-----------------------------------------------------------
        with open('news','w') as f:
            json.dump(newsdict, f)
    #-------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    URLdata = {}
    # if you already have a dictionary try to open it first
    #-------------------------------------------more JSON---------------------------------------------------------------
    try:
        with open('news', 'r') as f:
            newsdict = json.load(f)
    except FileNotFoundError:
        pass
    #-------------------------------------------------------------------------------------------------------------------
    
    for url in URLlist.values():
        # Grab robots.txt from the site
        robottxt = souper.MakeConnection(url, URLlist, '/robots.txt')
        scrape = data_manipulation.oktoscrape(robottxt)

        if scrape:
            bsdata = souper.MakeConnection(url, URLlist, '/')
            URLdata.update({url: souper.bs(bsdata.content, 'html.parser')})
        else:
            print('Unknown Error: Please Consult a REAL Programmer')
    print(URLdata.keys())


    #------------------------------------Threading to look at-----------------------------------------------------------
    threadlist = []
    threadlist.append(threading.Thread(target=nbc, args=[URLdata[URLlist['nbc']], newsdict, 'nbc']))
    threadlist.append(threading.Thread(target=nbc, args=[URLdata[URLlist['cbs']], newsdict, 'cbs']))
    threadlist[0].start()
    threadlist[1].start()
    #-------------------------------------------------------------------------------------------------------------------

    print(newsdict)