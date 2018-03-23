from PyQt5 import QtWidgets, QtCore
import sys
import mmbrackets
import pickle
import mmbrackets
import threading

class mmWindow(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('March Madness Brackets')
        self.grid = QtWidgets.QGridLayout()
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.refresh)
        timer.start(1000) # refresh scores once a second

        self.southlbl = QtWidgets.QLabel('South')
        self.westlbl = QtWidgets.QLabel('West')
        self.midwestlbl = QtWidgets.QLabel('Midwest')
        self.eastlbl = QtWidgets.QLabel('East')
        self.southlbl.setAlignment(QtCore.Qt.AlignCenter)
        self.westlbl.setAlignment(QtCore.Qt.AlignCenter)
        self.midwestlbl.setAlignment(QtCore.Qt.AlignCenter)
        self.eastlbl.setAlignment(QtCore.Qt.AlignCenter)
        self.grid.addWidget(self.southlbl, 0, 1)
        self.grid.addWidget(self.westlbl, 0, 2)
        self.grid.addWidget(self.midwestlbl, 0, 3)
        self.grid.addWidget(self.eastlbl, 0, 4)

        self.betbutton = QtWidgets.QPushButton('Manage Bets')
        self.grid.addWidget(self.betbutton, 2,1)

        self.roundscombobox = QtWidgets.QComboBox()
        self.roundscombobox.addItems(['Round 1', 'Round 2', 'Round 3', 'Round 4'])
        self.grid.addWidget(self.roundscombobox, 2,3)
        self.exitbutton = QtWidgets.QPushButton('Exit')
        self.grid.addWidget(self.exitbutton, 2,4)


        self.exitbutton.clicked.connect(self.close)
        self.roundscombobox.currentIndexChanged.connect(lambda x: self.getround(self.roundscombobox.currentText()))
        self.betbutton.clicked.connect(self.bet)
        self.setLayout(self.grid)

    def bet(self):
        self.betwindow = BetsWindow()

    def refresh(self):
        try:
            with open('test', 'rb') as f:
                self.fullbracket = pickle.load(f)
                filefound = True
        except FileNotFoundError:
            print("File not found, attempting to create")
            self.fullbracket = mmbrackets.main()
        try:
            self.getround(self.roundscombobox.currentText())
        except AttributeError:
            self.getround('Round 1')

        try:
            self.betwindow.fullbracket = self.fullbracket
        except AttributeError:
            pass



    def getround(self, rnd):
        self.lbls = []
        self.frames = []

        try:
            self.east.hide()
            self.west.hide()
            self.midwest.hide()
            self.south.hide()
        except:
            pass

        self.west = QtWidgets.QFrame()
        self.east = QtWidgets.QFrame()
        self.midwest = QtWidgets.QFrame()
        self.south = QtWidgets.QFrame()


        self.south.setFrameStyle(QtWidgets.QFrame.Box)
        self.gridsouth = QtWidgets.QGridLayout()
        self.south.setLineWidth(2)
        self.south.setFixedHeight(400)
        self.south.setFixedWidth(200)

        self.west.setFrameStyle(QtWidgets.QFrame.Box)
        self.gridwest = QtWidgets.QGridLayout()
        self.west.setLineWidth(2)
        self.west.setFixedHeight(400)
        self.west.setFixedWidth(200)

        self.midwest.setFrameStyle(QtWidgets.QFrame.Box)
        self.gridmidwest = QtWidgets.QGridLayout()
        self.midwest.setLineWidth(2)
        self.midwest.setFixedHeight(400)
        self.midwest.setFixedWidth(200)

        self.east.setFrameStyle(QtWidgets.QFrame.Box)
        self.grideast = QtWidgets.QGridLayout()
        self.east.setLineWidth(2)
        self.east.setFixedHeight(400)
        self.east.setFixedWidth(200)



        for pair in range(len(self.fullbracket[rnd])):
            region = self.fullbracket[rnd][pair][0].region

            self.frames.append([region, QtWidgets.QFrame()])
            self.frames[pair][1].setFrameStyle(QtWidgets.QFrame.Box)
            self.frames[pair][1].setFixedHeight(40)
            self.frames[pair][1].setFixedWidth(150)

            QtWidgets.QLabel(self.fullbracket[rnd][pair][0].name).setParent(self.frames[pair][1])
            QtWidgets.QLabel(self.fullbracket[rnd][pair][1].name).setParent(self.frames[pair][1])
            QtWidgets.QLabel(str(self.fullbracket[rnd][pair][0].points)).setParent(self.frames[pair][1])
            QtWidgets.QLabel(str(self.fullbracket[rnd][pair][1].points)).setParent(self.frames[pair][1])


            self.frames[pair][1].children()[0].setFrameRect(QtCore.QRect(5,5,80,80))
            self.frames[pair][1].children()[1].setFrameRect(QtCore.QRect(5,20,80,80))
            self.frames[pair][1].children()[2].setFrameRect(QtCore.QRect(120,5,10,150))
            self.frames[pair][1].children()[3].setFrameRect(QtCore.QRect(120,20,10,150))

        for i in range(len(self.frames)):
            if self.frames[i][0] == 'South':
                self.frames[i][1].setParent(self.south)
            elif self.frames[i][0] == 'West':
                self.frames[i][1].setParent(self.west)
            elif self.frames[i][0] == 'Midwest':
                self.frames[i][1].setParent(self.midwest)
            elif self.frames[i][0] == 'East':
                self.frames[i][1].setParent(self.east)

        for i, child in enumerate(self.south.children()):
            self.gridsouth.addWidget(child, i+1, 0)
        for i, child in enumerate(self.west.children()):
            self.gridwest.addWidget(child, i, 1)
        for i, child in enumerate(self.midwest.children()):
            self.gridmidwest.addWidget(self.midwest.children()[i], i, 2)
        for i, child in enumerate(self.east.children()):
            self.grideast.addWidget(child, i, 3)



        self.south.setLayout(self.gridsouth)
        self.grid.addWidget(self.south, 1, 1)


        self.west.setLayout(self.gridwest)
        self.grid.addWidget(self.west, 1, 2)

        self.midwest.setLayout(self.gridmidwest)
        self.grid.addWidget(self.midwest, 1, 3)

        self.east.setLayout(self.grideast)
        self.grid.addWidget(self.east, 1, 4)


        self.east.update()
        self.update()
        self.show()

class BetsWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.grid = QtWidgets.QGridLayout()
        try:
            with open('test', 'rb') as f:
                self.fullbracket = pickle.load(f)
        except FileNotFoundError:
            print("File not found, attempting to create")
            self.fullbracket = mmbrackets.main()

        self.playerlbl = QtWidgets.QLabel('Player')
        self.playercmbo = QtWidgets.QComboBox()
        self.playercmbo.addItems(['Guy', 'Joe'])

        self.roundlbl = QtWidgets.QLabel('Rounds')
        self.roundcmbo = QtWidgets.QComboBox()

        self.teamlbl = QtWidgets.QLabel('Team')
        self.teamcmbo = QtWidgets.QComboBox()

        self.roundcmbo.addItems(sorted(list(self.fullbracket.keys())))
        self.roundcmbo.setCurrentText('Round 1')

        self.betamount = QtWidgets.QListWidget()
        self.betamount.addItems([str(x) for x in sorted(list(range(0, 501, 5)),reverse=True)])
        self.betamount.setMaximumSize(100, 20)
        self.betamount.setCurrentRow(100)

        self.betbutton = QtWidgets.QPushButton('Place Bet')


        self.teamsort()

        self.grid.addWidget(self.playerlbl,0,0)
        self.grid.addWidget(self.playercmbo,0,1)
        self.grid.addWidget(self.roundlbl)
        self.grid.addWidget(self.roundcmbo)
        self.grid.addWidget(self.teamlbl)
        self.grid.addWidget(self.teamcmbo)
        self.opponetlbl = QtWidgets.QLabel()
        self.grid.addWidget(self.opponetlbl,5,1)
        self.grid.addWidget(self.betamount)
        self.grid.addWidget(self.betbutton)

        self.roundcmbo.currentIndexChanged.connect(self.teamsort)
        self.teamcmbo.currentIndexChanged.connect(self.getopponet)

        self.setLayout(self.grid)
        self.setWindowTitle('Bet Manager')
        self.show()

    def teamsort(self):
        self.teamcmbo.clear()
        for games in self.fullbracket[self.roundcmbo.currentText()]:
            for team in games:
                self.teamcmbo.addItem(team.name)
        self.teamcmbo.update()

    def getopponet(self):
        for games in self.fullbracket[self.roundcmbo.currentText()]:
            if games[0].name == self.teamcmbo.currentText():
                self.opponetlbl.setText("VS: {}".format(games[1].name))
            if games[1].name == self.teamcmbo.currentText():
                self.opponetlbl.setText("VS: {}".format(games[0].name))

class Update:
    def __init__(self):
        self.x = True
        updatethread = threading.Thread(target=self.update)
        updatethread.start()
    def update(self):
        while self.x:
            mmbrackets.main()


def main():
    updater = Update()

    app = QtWidgets.QApplication(sys.argv)
    mainwindow = mmWindow()
    app.exit(app.exec_())

    updater.x = False


if __name__ == '__main__':
    main()

