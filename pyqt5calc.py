from PyQt5 import QtWidgets, QtCore
import sys

class CalcWindow(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.operator = 'none'
        self.numlist = {'base': 0, 'mem': ''}
        self.firstnumafteroperator = False
        self.grid = QtWidgets.QGridLayout()

        self.posnegbutton = QtWidgets.QPushButton('+/-')
        self.grid.addWidget(self.posnegbutton,5,0)
        self.numbuttons = [QtWidgets.QPushButton('0')]
        self.grid.addWidget(self.numbuttons[0], 5,1)
        self.decibutton = QtWidgets.QPushButton('.')
        self.grid.addWidget(self.decibutton,5,2)

        row = 1
        for i in range(1, 10):
            if (i-1)%3 == 0:
                row += 1
                print(row)
            self.numbuttons.append(QtWidgets.QPushButton(str(i)))
            self.grid.addWidget(self.numbuttons[i], row, (i-1)%3)

        self.addbutton = QtWidgets.QPushButton('+')
        self.subbutton = QtWidgets.QPushButton('-')
        self.multibutton = QtWidgets.QPushButton('x')
        self.divbutton = QtWidgets.QPushButton('/')
        self.equalbutton = QtWidgets.QPushButton('=')
        self.clearbutton = QtWidgets.QPushButton('C')
        self.membutton = QtWidgets.QPushButton('MEM')
        self.memclearbutton = QtWidgets.QPushButton('MEM C')

        self.output = QtWidgets.QLineEdit('0')
        self.output.setAlignment(QtCore.Qt.AlignRight)

        self.grid.addWidget(self.output, 0,0,2,0)
        self.grid.addWidget(self.addbutton, 2,3)
        self.grid.addWidget(self.subbutton, 3,3)
        self.grid.addWidget(self.multibutton,4,3)
        self.grid.addWidget(self.divbutton,5,3)
        self.grid.addWidget(self.equalbutton,6,3)
        self.grid.addWidget(self.clearbutton,6,2)
        self.grid.addWidget(self.membutton, 6,1)
        self.grid.addWidget(self.memclearbutton, 6,0)
        self.setLayout(self.grid)
        self.show()

        self.addbutton.clicked.connect(lambda: self.whichbutton(self.addbutton))
        self.subbutton.clicked.connect(lambda: self.whichbutton(self.subbutton))
        self.divbutton.clicked.connect(lambda: self.whichbutton(self.divbutton))
        self.multibutton.clicked.connect(lambda: self.whichbutton(self.multibutton))
        self.equalbutton.clicked.connect(lambda: self.whichbutton(self.equalbutton))
        self.posnegbutton.clicked.connect(lambda: self.whichbutton(self.posnegbutton))
        self.decibutton.clicked.connect(lambda: self.whichbutton(self.decibutton))
        self.clearbutton.clicked.connect(lambda: self.whichbutton(self.clearbutton))
        self.membutton.clicked.connect(lambda: self.whichbutton(self.membutton))
        self.memclearbutton.clicked.connect(lambda: self.whichbutton(self.memclearbutton))

        for button in self.numbuttons:
            button.clicked.connect(lambda _, button= button: self.whichbutton(button))

    def whichbutton(self, button):
        try:
            error = float(self.output.text())
        except ValueError:
            self.output.setText('Must be integer or float')
        if button.text().isdigit() or button.text() == '.':
            if self.firstnumafteroperator:
                self.output.setText('0')
                self.firstnumafteroperator = False

                if button.text() == '.':
                    self.output.setText('0.')
                else:
                    self.output.setText(button.text())
            else:
                if button.text() == '.':
                    if not self.output.text().__contains__('.'):
                        self.output.setText(str(self.output.text()+button.text()))
                if self.output.text().startswith('0') and not self.output.text().startswith('0.'):
                    print('here')
                    self.output.setText(button.text())
                else:
                    self.output.setText(str(self.output.text()+button.text()))

        elif button.text() == 'C':
            self.output.setText('0')
            self.operator = 'none'
            self.numlist['base'] = 0

        elif button.text() == '+':
            if self.operator == '+':
                self.add()
            self.operator = '+'
            self.numlist['base'] = float(self.output.text())
            self.firstnumafteroperator = True

        elif button.text() == '-':
            if self.operator == '-':
                self.sub()
            self.operator = '-'
            self.numlist['base'] = float(self.output.text())
            self.firstnumafteroperator = True

        elif button.text() == 'x':
            if self.operator == 'x':
                self.add()
            self.operator = 'x'
            self.numlist['base'] = float(self.output.text())
            self.firstnumafteroperator = True

        elif button.text() == '/':
            if self.operator == '/':
                self.add()
            self.operator = '/'
            self.numlist['base'] = float(self.output.text())
            self.firstnumafteroperator = True


        elif button.text() == '=':
            if self.operator == '+':
                self.add()
            if self.operator == '-':
                self.sub()
            if self.operator == 'x':
                self.multi()
            if self.operator == '/':
                self.div()

            #self.operator = 'none'

        elif button.text() == '+/-':
            if self.output.text().startswith('-'):
                self.output.setText(self.output.text().replace('-',''))
            else:
                self.output.setText('-'+self.output.text())
        elif button.text() == 'MEM':
            self.mem()
        elif button.text() == 'MEM C':
            self.memc()

    def mem(self):
        x = self.membutton.styleSheet()
        if x == "color: 'red'":
            self.output.setText(self.numlist['mem'])
        if x == "" or x == "color: ''":
            self.membutton.setStyleSheet("color: 'red'")
            self.numlist['mem'] = self.output.text()

    def memc(self):
        x = self.membutton.styleSheet()
        if x == "color: 'red'":
            self.membutton.setStyleSheet("color: ''")
            self.numlist['mem'] == ''

    def add(self):
        try:
            temp = float(self.numlist['base']) + float(self.output.text())
            if temp.is_integer():
                temp = int(temp)
            self.output.setText(str(temp))
        except ValueError:
            self.output.setText('Cannot compute number')

    def sub(self):
        try:
            temp = float(self.numlist['base']) - float(self.output.text())
            if temp.is_integer():
                temp = int(temp)
            self.output.setText(str(temp))
        except ValueError:
            self.output.setText('Cannot compute number')

    def multi(self):
        try:
            temp = float(self.numlist['base']) * float(self.output.text())
            if temp.is_integer():
                temp = int(temp)
            self.output.setText(str(temp))
        except ValueError:
            self.output.setText('Cannot compute number')

    def div(self):
        try:
            temp = float(self.numlist['base']) / float(self.output.text())
            if temp.is_integer():
                temp = int(temp)
            self.output.setText(str(temp))
        except ValueError:
            self.output.setText('Cannot compute number')
        except ZeroDivisionError:
            self.output.setText('Can not divide by zero!')



app = QtWidgets.QApplication(sys.argv)
mainwindow = CalcWindow()
app.exit(app.exec_())

