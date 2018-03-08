import  where_can_i_go_bot as souper
import data_manipulation


class Titanic:
    """A class representing the Titanic"""
    def __init__(self):
        # Create a empty list for each passengers ticket type
        self.firstclass = []
        self.secondclass = []
        self.thirdclass = []

    def fill_boat(self, URL, paths):
        """This class scrapes passenger information, creates passenger objects,
         and assigns them to where they stayed on the titanic"""
        # Grab the data and parse it
        self.data = souper.MakeConnection(URL[0], URL, paths[0])
        self.soup = souper.bs(self.data.content, 'html.parser')

        # This array needs an extra entry because of a table without data we need
        templist = [[],[],[],[]]
        # Track which ticket class we are on
        listpos = 0

        # The information we want is split up into tables
        for table in self.soup.find_all('table'):
            # specify the list we are working on in the temp array
            workinglist = templist[listpos]
            # Next time around we will work on the next list in the array
            listpos += 1

            # Find the table rows
            for tr in table.find_all('tr'):
                # Then the table data in each row
                for td in tr.find_all('td'):
                    # Not every td contains a class keyword, but we need to check it to sort out the rows we don't need
                    try:
                        if 'tdheading' not in td['class'] and 'tdwhite' not in td['class']:
                            # If it's not a heading or white space append the data to our list
                            workinglist.append(td.text)
                    # If it throws a key error it's still valid data we need
                    except KeyError:
                        # Append it to our list
                        workinglist.append(td.text)
        # The data is clean and in order, now to group it
        for i in range(0, len(templist[0]), 5):
            self.firstclass.append(passenger(templist[0][i], templist[0][i + 1],
                                             templist[0][i+2], templist[0][i+3], templist[0][i+4]))
        for i in range(0, len(templist[1]), 5):
            self.secondclass.append(passenger(templist[1][i], templist[1][i + 1],
                                              templist[1][i+2], templist[1][i+3], templist[1][i+4]))
        for i in range(0, len(templist[2]), 5):
            self.thirdclass.append(passenger(templist[2][i], templist[2][i + 1],
                                             templist[2][i+2], templist[2][i+3], templist[2][i+4]))

    def find_survivors(self, group):
        """Takes a list of passangers and returns a list of the survivors from it"""
        survivors = []
        for person in group:
            if person.survived:
                survivors.append(person)
        return survivors

    def find_sex(self, group):
        """Takes a list of passangers and returns a dictionary containing list of the survivors by sex"""
        sex = {'Males': [], 'Females': [], 'Unknown': []}

        for person in group:
            if person.sex == 'Male':
                sex['Males'].append(person)
            elif person.sex == 'Female':
                sex['Females'].append(person)
            else:
                sex['Unknown'].append(person)

        return sex


class passenger:
    """A class representing the passengers of the Titanic"""
    def __init__(self, lastname, firstname, age, boarded, survived):
        # These are used to try to determine sex
        self.maleprefixs = ['Mr', 'Dr', 'Master', 'Sir', 'Colonel', 'Reverend', 'Father', 'Major', 'Captain', 'Don.']
        self.femaleprefixs = ['Ms', 'Mrs', 'Miss', 'Mme.', 'Mlle']

        self.firstname, self.sex = self._getsex(firstname)

        self.lastname = lastname
        self.age = age
        self.boarded = boarded
        if survived == 'S':
            self.survived = True
        else:
            self.survived = False

    def _getsex(self, firstname):
        """An attempt at determining sex using prefixs, done automatically at creation"""

        for prefix in self.femaleprefixs:
            if firstname.startswith(prefix):
                firstname = firstname.lstrip(prefix + ' ').lstrip()
                return firstname, 'Female'
        for prefix in self.maleprefixs:
            if firstname.startswith(prefix):
                firstname = firstname.lstrip(prefix + ' ').lstrip()
                return firstname, 'Male'
        return firstname, 'Unknown'


# create an instance of titance
bigboat = Titanic()

URL = ['http://www.titanicfacts.net']
paths = ['/titanic-passenger-list.html']
# Grab robots.txt from the site
robottxt = souper.MakeConnection(URL[0], URL, '/robots.txt')
# Check that it's okay to scrape there
for path in paths:
    scrape = data_manipulation.oktoscrape(robottxt, path)
    # If it is make a request, and parse the returned data
    if scrape:
        bigboat.fill_boat(URL, paths)


# Here's an example of some of the things you could do, I might add more later
# Get the survivors from 1st and 3rd class
survivors = bigboat.find_survivors(bigboat.firstclass + bigboat.thirdclass)

# From them find who is male, female, or unknown
sexofsurvivors = bigboat.find_sex(survivors)

# print off their names
for female in sexofsurvivors['Females']:
    print(female.firstname, female.lastname)

