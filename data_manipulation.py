import where_can_i_go_bot as souper
import sys

# The URL is only in a list for compatibility
URLlist = ['http://www.statisticstimes.com']
# Where I want to get my data from
path = '/economy/countries-by-projected-gdp-capita.php'

# Grab robots.txt from the site
robottxt = souper.MakeConnection(URLlist[0], URLlist, '/robots.txt')


# Check if I'm allowed to scrape there
def oktoscrape(robottxt):
    # Get the allowed and disallowed paths
    allowed, disallowed = souper.GetAllowed(robottxt)
    
    # Check both list
    for paths in allowed:
        # if the path is in the allow list no need to keep looking
        if path.find(paths) == 0:
            return
    for paths in disallowed:
        # if the path is in disallow tell the user where it's not allowed and exit
        if path.find(disallowed) == 0:
            print('Bots not allowed {}'.format(paths))
            sys.exit()


def processing(bsdata):
    # Create a dictionary to hold the data I want
    datadict = {}
    # Using my browsers inspection tool, I found that the information I wanted was all grouped under either
    # <tr class="odd"> or <tr class="even">, for some reason when I make a request this information is lost.
    # So I had to take a slightly different approach, if anyone knows why this happens please let me know!

    # Every country is listed under <td 'class'='name'> so I search for that
    for td in bsdata.find_all('td', attrs={'class': 'name'}):
            # Add the countries name to my dictionaries keys
            datadict.update({td.text:[]})
            # All the data for the country is held within it's parents children, so get the parent
            temp = td.parent
            # For each of it's childrens data
            for data in temp:
                # If there is an empty text field just pass it
                try:
                    # If the data isn't the name of the country
                    if data.text != td.text:
                        # Append the data to the list associated with the countries name
                        datadict[td.text].append(data.text)
                except AttributeError:
                    pass

    # Create a list to hold all 10 values
    average = [0,0,0,0,0,0,0,0,0,0]
    # Not every value is reported by every country, so count them
    nodata = [0,0,0,0,0,0,0,0,0,0]
    # I don't want this in my data
    world = datadict.pop('World\n      ')

    # Look through all the data list in the dictionary
    for countrystats in datadict.values():
        #if datadict['World'] != countrystats:
            # For each entry in the list
        for i in range(len(countrystats)):
            # Some values were left out using an - so don't use them
                if countrystats[i] != '-':
                    # Add their values to the appropriate column
                    average[i] += float(countrystats[i].replace(',', ''))
                else:
                    # If the country didn't have data available, don't count it for the average
                    nodata[i] += 1
    # Grab the average for all ten items
    for i in range(len(average)):
        average[i] = round(average[i]/len(datadict)-nodata[i],2)

    # print the results
    print("""Average Nominal GDP 2017: {}
Average Nominal GDP 2022: {}
Average PPP GDP 2017:     {}
Average PPP GDP 2022:     {}""".format(average[0],average[3],average[5],average[8]))


# Check if you are allowed to scrape at the path
oktoscrape(robottxt)
# Grab the page
datasource = souper.MakeConnection(URLlist[0], URLlist, path)
# Parse the data
bsdata = souper.bs(datasource.content, 'html.parser')
# Do something with the data
processing(bsdata)
