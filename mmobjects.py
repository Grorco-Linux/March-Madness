
class Team:
    def __init__(self, name='', region='', seed='', points=0):
        super().__init__()
        self.name = name
        self.region = region
        self.seed = seed
        self.points = points
        self.nextgame = 0

        # append True or False as they progress
        self.roundwins = []

        # The following are per season
        self.totalpoints = 0
        self.totalpointsgiven = 0
        self.totalgameswon = 0
        self.totalgameslost = 0

