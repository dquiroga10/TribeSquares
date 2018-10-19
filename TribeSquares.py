import sys, threading, time
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QBrush
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QDialog, QInputDialog, QErrorMessage

ROWS = 8
COLUMNS = 8
CELL_SIZE = 50
GRID_ORIGINX = 50
GRID_ORIGINY = 50

class TribeSquares(QWidget):

    def __init__(self):
        super().__init__()
        self.__board = [['' for i in range(COLUMNS)] for j in range(ROWS)]
        self.ply0_brd = [['' for i in range(COLUMNS)] for j in range(ROWS)]
        self.ply1_brd = [['' for i in range(COLUMNS)] for j in range(ROWS)]
        self.setWindowTitle('TribeSquares')
        self.setGeometry(300, 300, 2 * GRID_ORIGINX + CELL_SIZE * COLUMNS, 3 * GRID_ORIGINY + CELL_SIZE * ROWS)
        self.__turn = 0
        self.cord0 = list()
        self.cord1 = list()
        self.ply0score = 0
        self.ply0score_act = 0
        self.ply1score = 0
        self.ply1score_act = 0
        self.counter = 0
        self.ply1mul = 1
        self.ply0mul = 1
        text0, okPressed = QInputDialog.getText(self, "Player 0","Enter your name (less than 10 characters): ")
        while okPressed and text0 == '':
            text0, okPressed = QInputDialog.getText(self, "Player 0","Enter your name (less than 10 characters): ")
        if okPressed and text0 != '' and len(text0)>10:
            while len(text0)>10:
                text0, okPressed = QInputDialog.getText(self, "Player 0","Enter your name (less than 10 characters): ")
        if okPressed and text0 != '' and len(text0)<10:
            self._ply0nam = text0
        text1, okPressed = QInputDialog.getText(self, "Player 1","Enter your name (less than 10 characters): ")
        while okPressed and text1 == '':
            text1, okPressed = QInputDialog.getText(self, "Player 1","Enter your name (less than 10 characters): ")
        if okPressed and text1 != '' and len(text1)>10:
            while len(text1)>10:
                text1, okPressed = QInputDialog.getText(self, "Player 1","Enter your name (less than 10 characters): ")
        if okPressed and text1 != '' and len(text1)<10:
            self._ply1nam = text1
        self.show()

    def paintEvent(self, event):
        qp = QPainter()
        blackPen = QPen(Qt.black)
        qp.begin(self)
        qp.setPen(blackPen)
        for r in range(ROWS):
          for c in range(COLUMNS):
            qp.drawRect(GRID_ORIGINX + c * CELL_SIZE, GRID_ORIGINY + r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if self.__board[r][c] == 0:
                qp.setBrush(QColor(Qt.green))
                qp.setPen(QPen(QColor(Qt.black)))
                qp.drawRect(GRID_ORIGINX + c * CELL_SIZE + 6, GRID_ORIGINY + r * CELL_SIZE + 6, 40, 40)
            if self.__board[r][c] == 1:
                qp.setBrush(QColor(Qt.yellow))
                qp.setPen(QPen(QColor(Qt.black)))
                qp.drawRect(GRID_ORIGINX + c * CELL_SIZE + 6, GRID_ORIGINY + r * CELL_SIZE + 6, 40, 40)
            if self.__turn == 0:
                qp.setPen(QPen(Qt.yellow))
                qp.drawText(300, 475, self._ply1nam + ', YOUR TURN!')
            elif self.__turn == 1:
                qp.setPen(QPen(Qt.green))
                qp.drawText(300, 525, self._ply0nam + ', YOUR TURN!')
            qp.setPen(QPen(Qt.yellow))
            qp.drawText(150, 475, str(self.ply0score_act))
            qp.drawText(200, 475, 'x'+str(self.ply0mul))
            qp.setPen(QPen(Qt.green))
            qp.drawText(150, 525, str(self.ply1score_act))
            qp.drawText(200, 525, 'x'+str(self.ply1mul))
            qp.setPen(blackPen)
            qp.setBrush(Qt.NoBrush)
        if int(self.ply0score_act) > int(self.ply1score_act):
            qp.setPen(QPen(Qt.yellow, 10))
            qp.drawText(15,15, self._ply1nam + ' is winning')
            qp.setPen(blackPen)
        elif int(self.ply1score_act) > int(self.ply0score_act):
            qp.setPen(QPen(Qt.green, 10))
            qp.drawText(15,15, self._ply0nam + ' is winning')
            qp.setPen(blackPen)
        elif int(self.ply1score_act) == int(self.ply0score_act):
            qp.setPen(QPen(Qt.black, 10))
            qp.drawText(15,15, 'Game is Tied')
        qp.drawText(250,15, 'Press SpaceBar to restart the Game')
        self.CheckSquare(qp)
        qp.end()

    def Alternate(self):
        if self.__turn == 0:
            self.__turn = 1
            return self.__turn
        elif self.__turn == 1:
            self.__turn = 0
            return self.__turn
        self.update()

    def mousePressEvent(self, event):
        row = (event.y() - GRID_ORIGINY) // CELL_SIZE
        col = (event.x() - GRID_ORIGINX) // CELL_SIZE
        if 0 <= row < ROWS and 0 <= col < COLUMNS:
            if self.ply0_brd[row][col] == '' and self.ply1_brd[row][col] == '':
                self.counter = 0
                self.Alternate()
                if self.__turn == 0:
                    self.ply0_brd[row][col] = 0
                    self.__board[row][col] = 0
                    self.update()
                elif self.__turn == 1:
                    self.ply1_brd[row][col] = 1
                    self.__board[row][col] = 1
                    self.update()

    def keyPressEvent(self, event):
        if event.text().isspace():
            self.__turn = 0
            self.cord0.clear()
            self.cord1.clear()
            self.ply0score = 0
            self.ply0score_act = 0
            self.ply1score = 0
            self.ply1score_act = 0
            self.counter = 0
            self.ply1mul = 1
            self.ply0mul = 1
            self.__board = [['' for i in range(COLUMNS)] for j in range(ROWS)]
            self.ply0_brd = [['' for i in range(COLUMNS)] for j in range(ROWS)]
            self.ply1_brd = [['' for i in range(COLUMNS)] for j in range(ROWS)]
        self.update()

    def Multiplier(self):
        if self.counter == 0 or self.counter == 1:
            if self.__turn == 0: 
                self.ply1score_act += self.ply1score
                self.ply1score = 0
                self.ply1mul = 1
            elif self.__turn == 1:
                self.ply0score_act += self.ply0score
                self.ply0score = 0
                self.ply0mul = 1
        elif self.counter >= 2:
            if self.__turn == 0:
                self.ply1score_act += (self.ply1score * self.counter)
                self.ply1mul = self.counter
                self.ply1score = 0
            elif self.__turn == 1: 
                self.ply0score_act += (self.ply0score * self.counter)
                self.ply0mul = self.counter
                self.ply0score = 0
        self.update()

    def CheckSquare(self, qp):

        #an easier way to condense the entire code base
        for k in range(1,8):
            for i in range(len(self.__board)-k):
                for j in range(len(self.__board)-k):
                    if self.ply0_brd[i][j] == 0 and self.ply0_brd[i][j+k] == 0 and self.ply0_brd[i+k][j] == 0 and self.ply0_brd[i+k][j+k] == 0:
                        if ((i,j) not in self.cord0) or ((i,j+k) not in self.cord0) or ((i+k,j) not in self.cord0) or ((i+k,j+k) not in self.cord0):
                            self.cord0.append((i,j))
                            self.cord0.append((i,j+k))
                            self.cord0.append((i+k,j))
                            self.cord0.append((i+k,j+k))
                            self.ply1score += ((k+1)**2)
                            self.counter += 1
                            self.update()
                        else:
                            qp.setPen(QPen(Qt.green, 5))
                            qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i) * CELL_SIZE + 25,GRID_ORIGINX + (j+k) * CELL_SIZE + 25,GRID_ORIGINY + i * CELL_SIZE + 25)
                            qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i) * CELL_SIZE + 25,GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY +  (i+k) * CELL_SIZE + 25)
                            qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+k) * CELL_SIZE + 25,GRID_ORIGINX + (j+k) * CELL_SIZE + 25, GRID_ORIGINY +  (i+k) * CELL_SIZE + 25)
                            qp.drawLine(GRID_ORIGINX + (j+k) * CELL_SIZE + 25, GRID_ORIGINY + (i) * CELL_SIZE + 25,GRID_ORIGINX + (j+k) * CELL_SIZE + 25, GRID_ORIGINY +  (i+k) * CELL_SIZE + 25)
                            qp.setPen(QPen(Qt.black))

        for l in range(1,4):
            for i in range(len(self.__board) - (2*l)):
                for j in range(len(self.__board) - (2*l)):
                    if self.ply0_brd[i+l][j] == 1 and self.ply0_brd[i][j+l] == 1 and self.ply0_brd[i+(2*l)][j+l] == 1 and self.ply0_brd[i+l][j+(2*l)] == 1:
                        if ((i+l,j) not in self.cord0) or ((i,j+l) not in self.cord0) or ((i+(2*l),j+l) not in self.cord0) or ((i+l,j+(2*l)) not in self.cord0):
                            self.cord0.append((i+l,j))
                            self.cord0.append((i,j+l))
                            self.cord0.append((i+(2*l),j+l))
                            self.cord0.append((i+l,j+(2*l)))
                            self.ply1score += (((2*l)+1)**2)
                            self.counter += 2
                            self.update()
                        else:
                            qp.setPen(QPen(Qt.green, 5))
                            qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+l) * CELL_SIZE + 10,GRID_ORIGINX + (j+l) * CELL_SIZE + 10,GRID_ORIGINY + i * CELL_SIZE + 25)
                            qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+l) * CELL_SIZE + 40,GRID_ORIGINX + (j+l) * CELL_SIZE + 10, GRID_ORIGINY +  (i+(2*l)) * CELL_SIZE + 25)
                            qp.drawLine(GRID_ORIGINX + (j+l) * CELL_SIZE + 25, GRID_ORIGINY + (i+(2*l)) * CELL_SIZE + 40,GRID_ORIGINX + (j+(2*l)) * CELL_SIZE + 40, GRID_ORIGINY +  (i+l) * CELL_SIZE + 25)
                            qp.drawLine(GRID_ORIGINX + (j+(2*l)) * CELL_SIZE + 25, GRID_ORIGINY + (i+l) * CELL_SIZE + 10,GRID_ORIGINX + (j+l) * CELL_SIZE + 40, GRID_ORIGINY +  (i) * CELL_SIZE + 25)
                            qp.setPen(QPen(Qt.black))

        for l in range(3,8):
            for i in range(len(self.__board)-l):
                for j in range(len(self.__board)-l):
                    if self.ply0_brd[i+(l-1)][j] == 1 and self.ply0_brd[i][j+1] == 1 and self.ply0_brd[i+l][j+(l-1)] == 1 and self.ply0_brd[i+1][j+l] == 1:
                        if ((i+(l-1),j) not in self.cord0) or ((i,j+1) not in self.cord0) or ((i+l,j+(l-1)) not in self.cord0) or ((i+1,j+l) not in self.cord0):
                            self.cord0.append((i+(l-1),j))
                            self.cord0.append((i,j+1))
                            self.cord0.append((i+l,j+(l-1)))
                            self.cord0.append((i+1,j+l))
                            self.ply1score += (l**2)
                            self.counter += 2
                            self.update()
                        else:
                            qp.setPen(QPen(Qt.green, 5))
                            qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+(l-1)) * CELL_SIZE + 10,GRID_ORIGINX + (j+1) * CELL_SIZE + 10,GRID_ORIGINY + i * CELL_SIZE + 25) #1 -> 2
                            qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+(l-1)) * CELL_SIZE + 40,GRID_ORIGINX + (j+(l-1)) * CELL_SIZE + 10, GRID_ORIGINY +  (i+l) * CELL_SIZE + 25)#1 -> 3
                            qp.drawLine(GRID_ORIGINX + (j+(l-1)) * CELL_SIZE + 25, GRID_ORIGINY + (i+l) * CELL_SIZE + 40,GRID_ORIGINX + (j+l) * CELL_SIZE + 40, GRID_ORIGINY +  (i+1) * CELL_SIZE + 25)#3 -> 4
                            qp.drawLine(GRID_ORIGINX + (j+l) * CELL_SIZE + 25, GRID_ORIGINY + (i+1) * CELL_SIZE + 10,GRID_ORIGINX + (j+1) * CELL_SIZE + 40, GRID_ORIGINY +  (i) * CELL_SIZE + 25)#4 -> 2
                            qp.setPen(QPen(Qt.black))
                    if self.ply0_brd[i+1][j] == 1 and self.ply0_brd[i][j+(l-1)] == 1 and self.ply0_brd[i+l][j+1] == 1 and self.ply0_brd[i+(l-1)][j+l] == 1:
                        if ((i+1,j) not in self.cord0) or ((i,j+(l-1)) not in self.cord0) or ((i+l,j+1) not in self.cord0) or ((i+(l-1),j+l) not in self.cord0):
                            self.cord0.append((i+1,j))
                            self.cord0.append((i,j+(l-1)))
                            self.cord0.append((i+l,j+1))
                            self.cord0.append((i+(l-1),j+l))
                            self.ply1score += (l**2)
                            self.counter += 2
                            self.update()
                        else:
                            qp.setPen(QPen(Qt.green, 5))
                            qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+1) * CELL_SIZE + 10,GRID_ORIGINX + (j+(l-1)) * CELL_SIZE + 10,GRID_ORIGINY + i * CELL_SIZE + 25) #1 -> 2
                            qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+1) * CELL_SIZE + 40,GRID_ORIGINX + (j+1) * CELL_SIZE + 10, GRID_ORIGINY +  (i+l) * CELL_SIZE + 25)#1 -> 3
                            qp.drawLine(GRID_ORIGINX + (j+1) * CELL_SIZE + 25, GRID_ORIGINY + (i+l) * CELL_SIZE + 40,GRID_ORIGINX + (j+l) * CELL_SIZE + 40, GRID_ORIGINY +  (i+(l-1)) * CELL_SIZE + 25)#3 -> 4
                            qp.drawLine(GRID_ORIGINX + (j+l) * CELL_SIZE + 25, GRID_ORIGINY + (i+(l-1)) * CELL_SIZE + 10,GRID_ORIGINX + (j+(l-1)) * CELL_SIZE + 40, GRID_ORIGINY +  (i) * CELL_SIZE + 25)#4 -> 2
                            qp.setPen(QPen(Qt.black))

        #an easier way to condense the entire code base
        for k in range(1,8):
            for i in range(len(self.__board)-k):
                for j in range(len(self.__board)-k):
                    if self.ply1_brd[i][j] == 1 and self.ply1_brd[i][j+k] == 1 and self.ply1_brd[i+k][j] == 1 and self.ply1_brd[i+k][j+k] == 1:
                        if ((i,j) not in self.cord1) or ((i,j+k) not in self.cord1) or ((i+k,j) not in self.cord1) or ((i+k,j+k) not in self.cord1):
                            self.cord1.append((i,j))
                            self.cord1.append((i,j+k))
                            self.cord1.append((i+k,j))
                            self.cord1.append((i+k,j+k))
                            self.ply0score += ((k+1)**2)
                            self.counter += 1
                            self.update()
                        else:
                            qp.setPen(QPen(Qt.yellow, 5))
                            qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i) * CELL_SIZE + 25,GRID_ORIGINX + (j+k) * CELL_SIZE + 25,GRID_ORIGINY + i * CELL_SIZE + 25)
                            qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i) * CELL_SIZE + 25,GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY +  (i+k) * CELL_SIZE + 25)
                            qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+k) * CELL_SIZE + 25,GRID_ORIGINX + (j+k) * CELL_SIZE + 25, GRID_ORIGINY +  (i+k) * CELL_SIZE + 25)
                            qp.drawLine(GRID_ORIGINX + (j+k) * CELL_SIZE + 25, GRID_ORIGINY + (i) * CELL_SIZE + 25,GRID_ORIGINX + (j+k) * CELL_SIZE + 25, GRID_ORIGINY +  (i+k) * CELL_SIZE + 25)
                            qp.setPen(QPen(Qt.black))
        for l in range(1,4):
            for i in range(len(self.__board) - (2*l)):
                for j in range(len(self.__board) - (2*l)):
                    if self.ply1_brd[i+l][j] == 1 and self.ply1_brd[i][j+l] == 1 and self.ply1_brd[i+(2*l)][j+l] == 1 and self.ply1_brd[i+l][j+(2*l)] == 1:
                        if ((i+l,j) not in self.cord1) or ((i,j+l) not in self.cord1) or ((i+(2*l),j+l) not in self.cord1) or ((i+l,j+(2*l)) not in self.cord1):
                            self.cord1.append((i+l,j))
                            self.cord1.append((i,j+l))
                            self.cord1.append((i+(2*l),j+l))
                            self.cord1.append((i+l,j+(2*l)))
                            self.ply0score += (((2*l)+1)**2)
                            self.counter += 2
                            self.update()
                        else:
                            qp.setPen(QPen(Qt.yellow, 5))
                            qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+l) * CELL_SIZE + 10,GRID_ORIGINX + (j+l) * CELL_SIZE + 10,GRID_ORIGINY + i * CELL_SIZE + 25)
                            qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+l) * CELL_SIZE + 40,GRID_ORIGINX + (j+l) * CELL_SIZE + 10, GRID_ORIGINY +  (i+(2*l)) * CELL_SIZE + 25)
                            qp.drawLine(GRID_ORIGINX + (j+l) * CELL_SIZE + 25, GRID_ORIGINY + (i+(2*l)) * CELL_SIZE + 40,GRID_ORIGINX + (j+(2*l)) * CELL_SIZE + 40, GRID_ORIGINY +  (i+l) * CELL_SIZE + 25)
                            qp.drawLine(GRID_ORIGINX + (j+(2*l)) * CELL_SIZE + 25, GRID_ORIGINY + (i+l) * CELL_SIZE + 10,GRID_ORIGINX + (j+l) * CELL_SIZE + 40, GRID_ORIGINY +  (i) * CELL_SIZE + 25)
                            qp.setPen(QPen(Qt.black))

        for l in range(3,8):
            for i in range(len(self.__board)-l):
                for j in range(len(self.__board)-l):
                    if self.ply1_brd[i+(l-1)][j] == 1 and self.ply1_brd[i][j+1] == 1 and self.ply1_brd[i+l][j+(l-1)] == 1 and self.ply1_brd[i+1][j+l] == 1:
                        if ((i+(l-1),j) not in self.cord1) or ((i,j+1) not in self.cord1) or ((i+l,j+(l-1)) not in self.cord1) or ((i+1,j+l) not in self.cord1):
                            self.cord1.append((i+(l-1),j))
                            self.cord1.append((i,j+1))
                            self.cord1.append((i+l,j+(l-1)))
                            self.cord1.append((i+1,j+l))
                            self.ply0score += (l**2)
                            self.counter += 2
                            self.update()
                        else:
                            qp.setPen(QPen(Qt.yellow, 5))
                            qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+(l-1)) * CELL_SIZE + 10,GRID_ORIGINX + (j+1) * CELL_SIZE + 10,GRID_ORIGINY + i * CELL_SIZE + 25) #1 -> 2
                            qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+(l-1)) * CELL_SIZE + 40,GRID_ORIGINX + (j+(l-1)) * CELL_SIZE + 10, GRID_ORIGINY +  (i+l) * CELL_SIZE + 25)#1 -> 3
                            qp.drawLine(GRID_ORIGINX + (j+(l-1)) * CELL_SIZE + 25, GRID_ORIGINY + (i+l) * CELL_SIZE + 40,GRID_ORIGINX + (j+l) * CELL_SIZE + 40, GRID_ORIGINY +  (i+1) * CELL_SIZE + 25)#3 -> 4
                            qp.drawLine(GRID_ORIGINX + (j+l) * CELL_SIZE + 25, GRID_ORIGINY + (i+1) * CELL_SIZE + 10,GRID_ORIGINX + (j+1) * CELL_SIZE + 40, GRID_ORIGINY +  (i) * CELL_SIZE + 25)#4 -> 2
                            qp.setPen(QPen(Qt.black))
                    if self.ply1_brd[i+1][j] == 1 and self.ply1_brd[i][j+(l-1)] == 1 and self.ply1_brd[i+l][j+1] == 1 and self.ply1_brd[i+(l-1)][j+l] == 1:
                        if ((i+1,j) not in self.cord1) or ((i,j+(l-1)) not in self.cord1) or ((i+l,j+1) not in self.cord1) or ((i+(l-1),j+l) not in self.cord1):
                            self.cord1.append((i+1,j))
                            self.cord1.append((i,j+(l-1)))
                            self.cord1.append((i+l,j+1))
                            self.cord1.append((i+(l-1),j+l))
                            self.ply0score += (l**2)
                            self.counter += 2
                            self.update()
                        else:
                            qp.setPen(QPen(Qt.yellow, 5))
                            qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+1) * CELL_SIZE + 10,GRID_ORIGINX + (j+(l-1)) * CELL_SIZE + 10,GRID_ORIGINY + i * CELL_SIZE + 25) #1 -> 2
                            qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+1) * CELL_SIZE + 40,GRID_ORIGINX + (j+1) * CELL_SIZE + 10, GRID_ORIGINY +  (i+l) * CELL_SIZE + 25)#1 -> 3
                            qp.drawLine(GRID_ORIGINX + (j+1) * CELL_SIZE + 25, GRID_ORIGINY + (i+l) * CELL_SIZE + 40,GRID_ORIGINX + (j+l) * CELL_SIZE + 40, GRID_ORIGINY +  (i+(l-1)) * CELL_SIZE + 25)#3 -> 4
                            qp.drawLine(GRID_ORIGINX + (j+l) * CELL_SIZE + 25, GRID_ORIGINY + (i+(l-1)) * CELL_SIZE + 10,GRID_ORIGINX + (j+(l-1)) * CELL_SIZE + 40, GRID_ORIGINY +  (i) * CELL_SIZE + 25)#4 -> 2
                            qp.setPen(QPen(Qt.black))
        self.Multiplier()

            # for i in range(len(self.__board)-1):#check each possible 2x2 square for player1
            #     for j in range(len(self.__board)-1):
            #         if self.ply0_brd[i][j] == 0 and self.ply0_brd[i][j+1] == 0 and self.ply0_brd[i+1][j] == 0 and self.ply0_brd[i+1][j+1] == 0:
            #             if ((i,j) not in self.cord0) or ((i,j+1) not in self.cord0) or ((i+1,j) not in self.cord0) or ((i+1,j+1) not in self.cord0):
            #                 self.cord0.append((i,j))
            #                 self.cord0.append((i,j+1))
            #                 self.cord0.append((i+1,j))
            #                 self.cord0.append((i+1,j+1))
            #                 self.ply1score += 4
            #                 self.counter += 1
            #                 self.update()
            #             else:
            #                 qp.setPen(QPen(Qt.green, 5))
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i) * CELL_SIZE + 25,GRID_ORIGINX + (j+1) * CELL_SIZE + 25,GRID_ORIGINY + i * CELL_SIZE + 25)
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i) * CELL_SIZE + 25,GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY +  (i+1) * CELL_SIZE + 25)
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+1) * CELL_SIZE + 25,GRID_ORIGINX + (j+1) * CELL_SIZE + 25, GRID_ORIGINY +  (i+1) * CELL_SIZE + 25)
            #                 qp.drawLine(GRID_ORIGINX + (j+1) * CELL_SIZE + 25, GRID_ORIGINY + (i) * CELL_SIZE + 25,GRID_ORIGINX + (j+1) * CELL_SIZE + 25, GRID_ORIGINY +  (i+1) * CELL_SIZE + 25)
            #                 qp.setPen(QPen(Qt.black))
                
            # for i in range(len(self.__board)-2):#check each possible 3x3 square for player1
            #     for j in range(len(self.__board)-2):
            #         if self.ply0_brd[i][j] == 0 and self.ply0_brd[i][j+2] == 0 and self.ply0_brd[i+2][j] == 0 and self.ply0_brd[i+2][j+2] == 0:
            #             if ((i,j) not in self.cord0) or ((i,j+2) not in self.cord0) or ((i+2,j) not in self.cord0) or ((i+2,j+2) not in self.cord0):
            #                 self.cord0.append((i,j))
            #                 self.cord0.append((i,j+2))
            #                 self.cord0.append((i+2,j))
            #                 self.cord0.append((i+2,j+2))
            #                 self.ply1score += 9
            #                 self.counter += 1
            #                 self.update()
            #             else:
            #                 qp.setPen(QPen(Qt.green, 5))
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i) * CELL_SIZE + 25,GRID_ORIGINX + (j+2) * CELL_SIZE + 25,GRID_ORIGINY + i * CELL_SIZE + 25)
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i) * CELL_SIZE + 25,GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY +  (i+2) * CELL_SIZE + 25)
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+2) * CELL_SIZE + 25,GRID_ORIGINX + (j+2) * CELL_SIZE + 25, GRID_ORIGINY +  (i+2) * CELL_SIZE + 25)
            #                 qp.drawLine(GRID_ORIGINX + (j+2) * CELL_SIZE + 25, GRID_ORIGINY + (i) * CELL_SIZE + 25,GRID_ORIGINX + (j+2) * CELL_SIZE + 25, GRID_ORIGINY +  (i+2) * CELL_SIZE + 25)
            #                 qp.setPen(QPen(Qt.black))
                
            # for i in range(len(self.__board)-3):#check each possible 4x4 square for player1
            #     for j in range(len(self.__board) - 3):
            #         if self.ply0_brd[i][j] == 0 and self.ply0_brd[i][j+3] == 0 and self.ply0_brd[i+3][j] == 0 and self.ply0_brd[i+3][j+3] == 0:
            #             if ((i,j) not in self.cord0) or ((i,j+3) not in self.cord0) or ((i+3,j) not in self.cord0) or ((i+3,j+3) not in self.cord0):
            #                 self.cord0.append((i,j))
            #                 self.cord0.append((i,j+3))
            #                 self.cord0.append((i+3,j))
            #                 self.cord0.append((i+3,j+3))
            #                 self.ply1score += 9
            #                 self.counter += 1
            #                 self.update()
            #             else:
            #                 qp.setPen(QPen(Qt.green, 5))
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i) * CELL_SIZE + 25,GRID_ORIGINX + (j+3) * CELL_SIZE + 25,GRID_ORIGINY + i * CELL_SIZE + 25)
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i) * CELL_SIZE + 25,GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY +  (i+3) * CELL_SIZE + 25)
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+3) * CELL_SIZE + 25,GRID_ORIGINX + (j+3) * CELL_SIZE + 25, GRID_ORIGINY +  (i+3) * CELL_SIZE + 25)
            #                 qp.drawLine(GRID_ORIGINX + (j+3) * CELL_SIZE + 25, GRID_ORIGINY + (i) * CELL_SIZE + 25,GRID_ORIGINX + (j+3) * CELL_SIZE + 25, GRID_ORIGINY +  (i+3) * CELL_SIZE + 25)
            #                 qp.setPen(QPen(Qt.black))
                
            # for i in range(len(self.__board)-4):#check each possible 5x5 square for player1
            #     for j in range(len(self.__board)-4):
            #         if self.ply0_brd[i][j] == 0 and self.ply0_brd[i][j+4] == 0 and self.ply0_brd[i+4][j] == 0 and self.ply0_brd[i+4][j+4] == 0:
            #             if ((i,j) not in self.cord0) or ((i,j+4) not in self.cord0) or ((i+4,j) not in self.cord0) or ((i+4,j+4) not in self.cord0):
            #                 self.cord0.append((i,j))
            #                 self.cord0.append((i,j+4))
            #                 self.cord0.append((i+4,j))
            #                 self.cord0.append((i+4,j+4))
            #                 self.ply1score += 25
            #                 self.counter += 1
            #                 self.update()
            #             else:
            #                 qp.setPen(QPen(Qt.green, 5))
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i) * CELL_SIZE + 25,GRID_ORIGINX + (j+4) * CELL_SIZE + 25,GRID_ORIGINY + i * CELL_SIZE + 25)
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i) * CELL_SIZE + 25,GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY +  (i+4) * CELL_SIZE + 25)
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+4) * CELL_SIZE + 25,GRID_ORIGINX + (j+4) * CELL_SIZE + 25, GRID_ORIGINY +  (i+4) * CELL_SIZE + 25)
            #                 qp.drawLine(GRID_ORIGINX + (j+4) * CELL_SIZE + 25, GRID_ORIGINY + (i) * CELL_SIZE + 25,GRID_ORIGINX + (j+4) * CELL_SIZE + 25, GRID_ORIGINY +  (i+4) * CELL_SIZE + 25)
            #                 qp.setPen(QPen(Qt.black))
                
            # for i in range(len(self.__board)-5):#check each possible 6x6 square for player1
            #     for j in range(len(self.__board)-5):
            #         if self.ply0_brd[i][j] == 0 and self.ply0_brd[i][j+5] == 0 and self.ply0_brd[i+5][j] == 0 and self.ply0_brd[i+5][j+5] == 0:
            #             if ((i,j) not in self.cord0) or ((i,j+5) not in self.cord0) or ((i+5,j) not in self.cord0) or ((i+5,j+5) not in self.cord0):
            #                 self.cord0.append((i,j))
            #                 self.cord0.append((i,j+5))
            #                 self.cord0.append((i+5,j))
            #                 self.cord0.append((i+5,j+5))
            #                 self.ply1score += 36
            #                 self.counter += 1
            #                 self.update()
            #             else:
            #                 qp.setPen(QPen(Qt.green, 5))
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i) * CELL_SIZE + 25,GRID_ORIGINX + (j+5) * CELL_SIZE + 25,GRID_ORIGINY + i * CELL_SIZE + 25)
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i) * CELL_SIZE + 25,GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY +  (i+5) * CELL_SIZE + 25)
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+5) * CELL_SIZE + 25,GRID_ORIGINX + (j+5) * CELL_SIZE + 25, GRID_ORIGINY +  (i+5) * CELL_SIZE + 25)
            #                 qp.drawLine(GRID_ORIGINX + (j+5) * CELL_SIZE + 25, GRID_ORIGINY + (i) * CELL_SIZE + 25,GRID_ORIGINX + (j+5) * CELL_SIZE + 25, GRID_ORIGINY +  (i+5) * CELL_SIZE + 25)
            #                 qp.setPen(QPen(Qt.black))
            
            # for i in range(len(self.__board)-6):#check each possible 7x7 square for player1
            #     for j in range(len(self.__board)-6):
            #         if self.ply0_brd[i][j] == 0 and self.ply0_brd[i][j+6] == 0 and self.ply0_brd[i+6][j] == 0 and self.ply0_brd[i+6][j+6] == 0:
            #             if ((i,j) not in self.cord0) or ((i,j+6) not in self.cord0) or ((i+6,j) not in self.cord0) or ((i+6,j+6) not in self.cord0):
            #                 self.cord0.append((i,j))
            #                 self.cord0.append((i,j+6))
            #                 self.cord0.append((i+6,j))
            #                 self.cord0.append((i+6,j+6))
            #                 self.ply1score += 49
            #                 self.counter += 1
            #                 self.update()
            #             else:
            #                 qp.setPen(QPen(Qt.green, 5))
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i) * CELL_SIZE + 25,GRID_ORIGINX + (j+6) * CELL_SIZE + 25,GRID_ORIGINY + i * CELL_SIZE + 25)
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i) * CELL_SIZE + 25,GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY +  (i+6) * CELL_SIZE + 25)
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+6) * CELL_SIZE + 25,GRID_ORIGINX + (j+6) * CELL_SIZE + 25, GRID_ORIGINY +  (i+6) * CELL_SIZE + 25)
            #                 qp.drawLine(GRID_ORIGINX + (j+6) * CELL_SIZE + 25, GRID_ORIGINY + (i) * CELL_SIZE + 25,GRID_ORIGINX + (j+6) * CELL_SIZE + 25, GRID_ORIGINY +  (i+6) * CELL_SIZE + 25)
            #                 qp.setPen(QPen(Qt.black))

            # for i in range(len(self.__board)-7):#check each possible 8x8 square for player1
            #     if self.ply0_brd[i][0] == 0 and self.ply0_brd[i][7] == 0 and self.ply0_brd[i+7][0] == 0 and self.ply0_brd[i+7][7] == 0:
            #         if ((i,0) not in self.cord0) or ((i,7) not in self.cord0) or ((i+7,0) not in self.cord0) or ((i+7,7) not in self.cord0):
            #             self.cord0.append((i,0))
            #             self.cord0.append((i,7))
            #             self.cord0.append((i+7,0))
            #             self.cord0.append((i+7,7))
            #             self.ply1score += 64
            #             self.counter += 1
            #             self.update()
            #         else:
            #             qp.setPen(QPen(Qt.green, 5))
            #             qp.drawLine(GRID_ORIGINX + 0 * CELL_SIZE + 25, GRID_ORIGINY + (i) * CELL_SIZE + 25,GRID_ORIGINX + 7 * CELL_SIZE + 25,GRID_ORIGINY + i * CELL_SIZE + 25)
            #             qp.drawLine(GRID_ORIGINX + 0 * CELL_SIZE + 25, GRID_ORIGINY + (i) * CELL_SIZE + 25,GRID_ORIGINX + 0 * CELL_SIZE + 25, GRID_ORIGINY +  (i+7) * CELL_SIZE + 25)
            #             qp.drawLine(GRID_ORIGINX + 0 * CELL_SIZE + 25, GRID_ORIGINY + (i+7) * CELL_SIZE + 25,GRID_ORIGINX + 7 * CELL_SIZE + 25, GRID_ORIGINY +  (i+7) * CELL_SIZE + 25)
            #             qp.drawLine(GRID_ORIGINX + 7 * CELL_SIZE + 25, GRID_ORIGINY + (i) * CELL_SIZE + 25,GRID_ORIGINX + 7 * CELL_SIZE + 25, GRID_ORIGINY +  (i+7) * CELL_SIZE + 25)
            #             qp.setPen(QPen(Qt.black))

            # for i in range(len(self.__board) - 2):#check for diagonal 3x3 square
            #     for j in range(len(self.__board) - 2):
            #         if self.ply0_brd[i+1][j] == 0 and self.ply0_brd[i][j+1] == 0 and self.ply0_brd[i+2][j+1] == 0 and self.ply0_brd[i+1][j+2] == 0:
            #             if ((i+1,j) not in self.cord0) or ((i,j+1) not in self.cord0) or ((i+2,j+1) not in self.cord0) or ((i+1,j+2) not in self.cord0):
            #                 self.cord0.append((i+1,j))
            #                 self.cord0.append((i,j+1))
            #                 self.cord0.append((i+2,j+1))
            #                 self.cord0.append((i+1,j+2))
            #                 self.ply1score += 9
            #                 self.counter += 2
            #                 self.update()
            #             else:
            #                 qp.setPen(QPen(Qt.green, 5))
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+1) * CELL_SIZE + 10,GRID_ORIGINX + (j+1) * CELL_SIZE + 10,GRID_ORIGINY + i * CELL_SIZE + 25)
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+1) * CELL_SIZE + 40,GRID_ORIGINX + (j+1) * CELL_SIZE + 10, GRID_ORIGINY +  (i+2) * CELL_SIZE + 25)
            #                 qp.drawLine(GRID_ORIGINX + (j+1) * CELL_SIZE + 25, GRID_ORIGINY + (i+2) * CELL_SIZE + 40,GRID_ORIGINX + (j+2) * CELL_SIZE + 40, GRID_ORIGINY +  (i+1) * CELL_SIZE + 25)
            #                 qp.drawLine(GRID_ORIGINX + (j+2) * CELL_SIZE + 25, GRID_ORIGINY + (i+1) * CELL_SIZE + 10,GRID_ORIGINX + (j+1) * CELL_SIZE + 40, GRID_ORIGINY +  (i) * CELL_SIZE + 25)
            #                 qp.setPen(QPen(Qt.black))

            # for i in range(len(self.__board)-4):#check for diagonal 5x5 square
            #     for j in range(len(self.__board)-4):
            #         if self.ply0_brd[i+2][j] == 0 and self.ply0_brd[i][j+2] == 0 and self.ply0_brd[i+4][j+2] == 0 and self.ply0_brd[i+2][j+4] == 0:
            #             if ((i+2,j) not in self.cord0) or ((i,j+2) not in self.cord0) or ((i+4,j+2) not in self.cord0) or ((i+2,j+4) not in self.cord0):
            #                 self.cord0.append((i+2,j))
            #                 self.cord0.append((i,j+2))
            #                 self.cord0.append((i+4,j+2))
            #                 self.cord0.append((i+2,j+4))
            #                 self.ply1score += 25
            #                 self.counter += 2
            #                 self.update()
            #             else:
            #                 qp.setPen(QPen(Qt.green, 5))
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+2) * CELL_SIZE + 10,GRID_ORIGINX + (j+2) * CELL_SIZE + 10,GRID_ORIGINY + i * CELL_SIZE + 25) #1 -> 2
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+2) * CELL_SIZE + 40,GRID_ORIGINX + (j+2) * CELL_SIZE + 10, GRID_ORIGINY +  (i+4) * CELL_SIZE + 25)#1 -> 3
            #                 qp.drawLine(GRID_ORIGINX + (j+2) * CELL_SIZE + 25, GRID_ORIGINY + (i+4) * CELL_SIZE + 40,GRID_ORIGINX + (j+4) * CELL_SIZE + 40, GRID_ORIGINY +  (i+2) * CELL_SIZE + 25)#3 -> 4
            #                 qp.drawLine(GRID_ORIGINX + (j+4) * CELL_SIZE + 25, GRID_ORIGINY + (i+2) * CELL_SIZE + 10,GRID_ORIGINX + (j+2) * CELL_SIZE + 40, GRID_ORIGINY +  (i) * CELL_SIZE + 25)#4 -> 2
            #                 qp.setPen(QPen(Qt.black))

            # for i in range(len(self.__board)-6):#check for diagonal 7x7 square
            #     for j in range(len(self.__board)-6):
            #         if self.ply0_brd[i+3][j] == 0 and self.ply0_brd[i][j+3] == 0 and self.ply0_brd[i+6][j+3] == 0 and self.ply0_brd[i+3][j+6] == 0:
            #             if ((i+3,j) not in self.cord0) or ((i,j+3) not in self.cord0) or ((i+6,j+3) not in self.cord0) or ((i+3,j+6) not in self.cord0):
            #                 self.cord0.append((i+3,j))
            #                 self.cord0.append((i,j+3))
            #                 self.cord0.append((i+6,j+3))
            #                 self.cord0.append((i+3,j+6))
            #                 self.ply1score += 49
            #                 self.counter += 2
            #                 self.update()
            #             else:
            #                 qp.setPen(QPen(Qt.green, 5))
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+3) * CELL_SIZE + 10,GRID_ORIGINX + (j+3) * CELL_SIZE + 10,GRID_ORIGINY + i * CELL_SIZE + 25) #1 -> 2
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+3) * CELL_SIZE + 40,GRID_ORIGINX + (j+3) * CELL_SIZE + 10, GRID_ORIGINY +  (i+6) * CELL_SIZE + 25)#1 -> 3
            #                 qp.drawLine(GRID_ORIGINX + (j+3) * CELL_SIZE + 25, GRID_ORIGINY + (i+6) * CELL_SIZE + 40,GRID_ORIGINX + (j+6) * CELL_SIZE + 40, GRID_ORIGINY +  (i+3) * CELL_SIZE + 25)#3 -> 4
            #                 qp.drawLine(GRID_ORIGINX + (j+6) * CELL_SIZE + 25, GRID_ORIGINY + (i+3) * CELL_SIZE + 10,GRID_ORIGINX + (j+3) * CELL_SIZE + 40, GRID_ORIGINY +  (i) * CELL_SIZE + 25)#4 -> 2
            #                 qp.setPen(QPen(Qt.black))

            # for i in range(len(self.__board)-3):
            #     for j in range(len(self.__board)-3):
            #         if self.ply0_brd[i+2][j] == 0 and self.ply0_brd[i][j+1] == 0 and self.ply0_brd[i+3][j+2] == 0 and self.ply0_brd[i+1][j+3] == 0:#check 3x3 right sideways
            #             if ((i+2,j) not in self.cord0) or ((i,j+1) not in self.cord0) or ((i+3,j+2) not in self.cord0) or ((i+1,j+3) not in self.cord0):
            #                 self.cord0.append((i+2,j))
            #                 self.cord0.append((i,j+1))
            #                 self.cord0.append((i+3,j+2))
            #                 self.cord0.append((i+1,j+3))
            #                 self.ply1score += 9
            #                 self.counter += 2
            #                 self.update()
            #             else:
            #                 qp.setPen(QPen(Qt.green, 5))
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+2) * CELL_SIZE + 10,GRID_ORIGINX + (j+1) * CELL_SIZE + 10,GRID_ORIGINY + i * CELL_SIZE + 25) #1 -> 2
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+2) * CELL_SIZE + 40,GRID_ORIGINX + (j+2) * CELL_SIZE + 10, GRID_ORIGINY +  (i+3) * CELL_SIZE + 25)#1 -> 3
            #                 qp.drawLine(GRID_ORIGINX + (j+2) * CELL_SIZE + 25, GRID_ORIGINY + (i+3) * CELL_SIZE + 40,GRID_ORIGINX + (j+3) * CELL_SIZE + 40, GRID_ORIGINY +  (i+1) * CELL_SIZE + 25)#3 -> 4
            #                 qp.drawLine(GRID_ORIGINX + (j+3) * CELL_SIZE + 25, GRID_ORIGINY + (i+1) * CELL_SIZE + 10,GRID_ORIGINX + (j+1) * CELL_SIZE + 40, GRID_ORIGINY +  (i) * CELL_SIZE + 25)#4 -> 2
            #                 qp.setPen(QPen(Qt.black))
            #         if self.ply0_brd[i+1][j] == 0 and self.ply0_brd[i][j+2] == 0 and self.ply0_brd[i+3][j+1] == 0 and self.ply0_brd[i+2][j+3] == 0:#check 3x3 left sideways
            #             if ((i+1,j) not in self.cord0) or ((i,j+2) not in self.cord0) or ((i+3,j+1) not in self.cord0) or ((i+2,j+3) not in self.cord0):
            #                 self.cord0.append((i+1,j))
            #                 self.cord0.append((i,j+2))
            #                 self.cord0.append((i+3,j+1))
            #                 self.cord0.append((i+2,j+3))
            #                 self.ply1score += 9
            #                 self.counter += 2
            #                 self.update()
            #             else:
            #                 qp.setPen(QPen(Qt.green, 5))
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+1) * CELL_SIZE + 10,GRID_ORIGINX + (j+2) * CELL_SIZE + 10,GRID_ORIGINY + i * CELL_SIZE + 25) #1 -> 2
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+1) * CELL_SIZE + 40,GRID_ORIGINX + (j+1) * CELL_SIZE + 10, GRID_ORIGINY +  (i+3) * CELL_SIZE + 25)#1 -> 3
            #                 qp.drawLine(GRID_ORIGINX + (j+1) * CELL_SIZE + 25, GRID_ORIGINY + (i+3) * CELL_SIZE + 40,GRID_ORIGINX + (j+3) * CELL_SIZE + 40, GRID_ORIGINY +  (i+2) * CELL_SIZE + 25)#3 -> 4
            #                 qp.drawLine(GRID_ORIGINX + (j+3) * CELL_SIZE + 25, GRID_ORIGINY + (i+2) * CELL_SIZE + 10,GRID_ORIGINX + (j+2) * CELL_SIZE + 40, GRID_ORIGINY +  (i) * CELL_SIZE + 25)#4 -> 2
            #                 qp.setPen(QPen(Qt.black))

            # for i in range(len(self.__board)-4):
            #     for j in range(len(self.__board)-4):
            #         if self.ply0_brd[i+3][j] == 0 and self.ply0_brd[i][j+1] == 0 and self.ply0_brd[i+4][j+3] == 0 and self.ply0_brd[i+1][j+4] == 0:#check 4x4 right sideways
            #             if ((i+3,j) not in self.cord0) or ((i,j+1) not in self.cord0) or ((i+4,j+3) not in self.cord0) or ((i+1,j+4) not in self.cord0):
            #                 self.cord0.append((i+3,j))
            #                 self.cord0.append((i,j+1))
            #                 self.cord0.append((i+4,j+3))
            #                 self.cord0.append((i+1,j+4))
            #                 self.ply1score += 16
            #                 self.counter += 2
            #                 self.update()
            #             else:
            #                 qp.setPen(QPen(Qt.green, 5))
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+3) * CELL_SIZE + 10,GRID_ORIGINX + (j+1) * CELL_SIZE + 10,GRID_ORIGINY + i * CELL_SIZE + 25) #1 -> 2
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+3) * CELL_SIZE + 40,GRID_ORIGINX + (j+3) * CELL_SIZE + 10, GRID_ORIGINY +  (i+4) * CELL_SIZE + 25)#1 -> 3
            #                 qp.drawLine(GRID_ORIGINX + (j+3) * CELL_SIZE + 25, GRID_ORIGINY + (i+4) * CELL_SIZE + 40,GRID_ORIGINX + (j+4) * CELL_SIZE + 40, GRID_ORIGINY +  (i+1) * CELL_SIZE + 25)#3 -> 4
            #                 qp.drawLine(GRID_ORIGINX + (j+4) * CELL_SIZE + 25, GRID_ORIGINY + (i+1) * CELL_SIZE + 10,GRID_ORIGINX + (j+1) * CELL_SIZE + 40, GRID_ORIGINY +  (i) * CELL_SIZE + 25)#4 -> 2
            #                 qp.setPen(QPen(Qt.black))
            #         if self.ply0_brd[i+1][j] == 0 and self.ply0_brd[i][j+3] == 0 and self.ply0_brd[i+4][j+1] == 0 and self.ply0_brd[i+3][j+4] == 0:#check 4x4 left sideways
            #             if ((i+1,j) not in self.cord0) or ((i,j+3) not in self.cord0) or ((i+4,j+1) not in self.cord0) or ((i+3,j+4) not in self.cord0):
            #                 self.cord0.append((i+1,j))
            #                 self.cord0.append((i,j+3))
            #                 self.cord0.append((i+4,j+1))
            #                 self.cord0.append((i+3,j+4))
            #                 self.ply1score += 16
            #                 self.counter += 2
            #                 self.update()
            #             else:
            #                 qp.setPen(QPen(Qt.green, 5))
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+1) * CELL_SIZE + 10,GRID_ORIGINX + (j+3) * CELL_SIZE + 10,GRID_ORIGINY + i * CELL_SIZE + 25) #1 -> 2
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+1) * CELL_SIZE + 40,GRID_ORIGINX + (j+1) * CELL_SIZE + 10, GRID_ORIGINY +  (i+4) * CELL_SIZE + 25)#1 -> 3
            #                 qp.drawLine(GRID_ORIGINX + (j+1) * CELL_SIZE + 25, GRID_ORIGINY + (i+4) * CELL_SIZE + 40,GRID_ORIGINX + (j+4) * CELL_SIZE + 40, GRID_ORIGINY +  (i+3) * CELL_SIZE + 25)#3 -> 4
            #                 qp.drawLine(GRID_ORIGINX + (j+4) * CELL_SIZE + 25, GRID_ORIGINY + (i+3) * CELL_SIZE + 10,GRID_ORIGINX + (j+3) * CELL_SIZE + 40, GRID_ORIGINY +  (i) * CELL_SIZE + 25)#4 -> 2
            #                 qp.setPen(QPen(Qt.black))

            # for i in range(len(self.__board)-5):
            #     for j in range(len(self.__board)-5):
            #         if self.ply0_brd[i+4][j] == 0 and self.ply0_brd[i][j+1] == 0 and self.ply0_brd[i+5][j+4] == 0 and self.ply0_brd[i+1][j+5] == 0:#check 5x5 right sideways
            #             if ((i+4,j) not in self.cord0) or ((i,j+1) not in self.cord0) or ((i+5,j+4) not in self.cord0) or ((i+1,j+5) not in self.cord0):
            #                 self.cord0.append((i+4,j))
            #                 self.cord0.append((i,j+1))
            #                 self.cord0.append((i+5,j+4))
            #                 self.cord0.append((i+1,j+5))
            #                 self.ply1score += 25
            #                 self.counter += 2
            #                 self.update()
            #             else:
            #                 qp.setPen(QPen(Qt.green, 5))
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+4) * CELL_SIZE + 10,GRID_ORIGINX + (j+1) * CELL_SIZE + 10,GRID_ORIGINY + i * CELL_SIZE + 25) #1 -> 2
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+4) * CELL_SIZE + 40,GRID_ORIGINX + (j+4) * CELL_SIZE + 10, GRID_ORIGINY +  (i+5) * CELL_SIZE + 25)#1 -> 3
            #                 qp.drawLine(GRID_ORIGINX + (j+4) * CELL_SIZE + 25, GRID_ORIGINY + (i+5) * CELL_SIZE + 40,GRID_ORIGINX + (j+5) * CELL_SIZE + 40, GRID_ORIGINY +  (i+1) * CELL_SIZE + 25)#3 -> 4
            #                 qp.drawLine(GRID_ORIGINX + (j+5) * CELL_SIZE + 25, GRID_ORIGINY + (i+1) * CELL_SIZE + 10,GRID_ORIGINX + (j+1) * CELL_SIZE + 40, GRID_ORIGINY +  (i) * CELL_SIZE + 25)#4 -> 2
            #                 qp.setPen(QPen(Qt.black))
            #         if self.ply0_brd[i+1][j] == 0 and self.ply0_brd[i][j+4] == 0 and self.ply0_brd[i+5][j+1] == 0 and self.ply0_brd[i+4][j+5] == 0:#check 5x5 left sideways
            #             if ((i+1,j) not in self.cord0) or ((i,j+4) not in self.cord0) or ((i+5,j+1) not in self.cord0) or ((i+4,j+5) not in self.cord0):
            #                 self.cord0.append((i+1,j))
            #                 self.cord0.append((i,j+4))
            #                 self.cord0.append((i+5,j+1))
            #                 self.cord0.append((i+4,j+5))
            #                 self.ply1score += 25
            #                 self.counter += 2
            #                 self.update()
            #             else:
            #                 qp.setPen(QPen(Qt.green, 5))
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+1) * CELL_SIZE + 10,GRID_ORIGINX + (j+4) * CELL_SIZE + 10,GRID_ORIGINY + i * CELL_SIZE + 25) #1 -> 2
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+1) * CELL_SIZE + 40,GRID_ORIGINX + (j+1) * CELL_SIZE + 10, GRID_ORIGINY +  (i+5) * CELL_SIZE + 25)#1 -> 3
            #                 qp.drawLine(GRID_ORIGINX + (j+1) * CELL_SIZE + 25, GRID_ORIGINY + (i+5) * CELL_SIZE + 40,GRID_ORIGINX + (j+5) * CELL_SIZE + 40, GRID_ORIGINY +  (i+4) * CELL_SIZE + 25)#3 -> 4
            #                 qp.drawLine(GRID_ORIGINX + (j+5) * CELL_SIZE + 25, GRID_ORIGINY + (i+4) * CELL_SIZE + 10,GRID_ORIGINX + (j+4) * CELL_SIZE + 40, GRID_ORIGINY +  (i) * CELL_SIZE + 25)#4 -> 2
            #                 qp.setPen(QPen(Qt.black))

            # for i in range(len(self.__board)-6):
            #     for j in range(len(self.__board)-6):
            #         if self.ply0_brd[i+5][j] == 0 and self.ply0_brd[i][j+1] == 0 and self.ply0_brd[i+6][j+5] == 0 and self.ply0_brd[i+1][j+6] == 0:#check 6x6 right sideways
            #             if ((i+5,j) not in self.cord0) or ((i,j+1) not in self.cord0) or ((i+6,j+5) not in self.cord0) or ((i+1,j+6) not in self.cord0):
            #                 self.cord0.append((i+5,j))
            #                 self.cord0.append((i,j+1))
            #                 self.cord0.append((i+6,j+5))
            #                 self.cord0.append((i+1,j+6))
            #                 self.ply1score += 36
            #                 self.counter += 2
            #                 self.update()
            #             else:
            #                 qp.setPen(QPen(Qt.green, 5))
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+5) * CELL_SIZE + 10,GRID_ORIGINX + (j+1) * CELL_SIZE + 10,GRID_ORIGINY + i * CELL_SIZE + 25) #1 -> 2
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+5) * CELL_SIZE + 40,GRID_ORIGINX + (j+5) * CELL_SIZE + 10, GRID_ORIGINY +  (i+6) * CELL_SIZE + 25)#1 -> 3
            #                 qp.drawLine(GRID_ORIGINX + (j+5) * CELL_SIZE + 25, GRID_ORIGINY + (i+6) * CELL_SIZE + 40,GRID_ORIGINX + (j+6) * CELL_SIZE + 40, GRID_ORIGINY +  (i+1) * CELL_SIZE + 25)#3 -> 4
            #                 qp.drawLine(GRID_ORIGINX + (j+6) * CELL_SIZE + 25, GRID_ORIGINY + (i+1) * CELL_SIZE + 10,GRID_ORIGINX + (j+1) * CELL_SIZE + 40, GRID_ORIGINY +  (i) * CELL_SIZE + 25)#4 -> 2
            #                 qp.setPen(QPen(Qt.black))
            #         if self.ply0_brd[i+1][j] == 0 and self.ply0_brd[i][j+5] == 0 and self.ply0_brd[i+6][j+1] == 0 and self.ply0_brd[i+5][j+6] == 0:#check 6x6 left sideways
            #             if ((i+1,j) not in self.cord0) or ((i,j+5) not in self.cord0) or ((i+6,j+1) not in self.cord0) or ((i+5,j+6) not in self.cord0):
            #                 self.cord0.append((i+1,j))
            #                 self.cord0.append((i,j+5))
            #                 self.cord0.append((i+6,j+1))
            #                 self.cord0.append((i+5,j+6))
            #                 self.ply1score += 36
            #                 self.counter += 2
            #                 self.update()
            #             else:
            #                 qp.setPen(QPen(Qt.green, 5))
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+1) * CELL_SIZE + 10,GRID_ORIGINX + (j+5) * CELL_SIZE + 10,GRID_ORIGINY + i * CELL_SIZE + 25) #1 -> 2
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+1) * CELL_SIZE + 40,GRID_ORIGINX + (j+1) * CELL_SIZE + 10, GRID_ORIGINY +  (i+6) * CELL_SIZE + 25)#1 -> 3
            #                 qp.drawLine(GRID_ORIGINX + (j+1) * CELL_SIZE + 25, GRID_ORIGINY + (i+6) * CELL_SIZE + 40,GRID_ORIGINX + (j+6) * CELL_SIZE + 40, GRID_ORIGINY +  (i+5) * CELL_SIZE + 25)#3 -> 4
            #                 qp.drawLine(GRID_ORIGINX + (j+6) * CELL_SIZE + 25, GRID_ORIGINY + (i+5) * CELL_SIZE + 10,GRID_ORIGINX + (j+5) * CELL_SIZE + 40, GRID_ORIGINY +  (i) * CELL_SIZE + 25)#4 -> 2
            #                 qp.setPen(QPen(Qt.black))

            # for i in range(len(self.__board)-7):
            #     for j in range(len(self.__board)-7):
            #         if self.ply0_brd[i+6][j] == 0 and self.ply0_brd[i][j+1] == 0 and self.ply0_brd[i+7][j+6] == 0 and self.ply0_brd[i+1][j+7] == 0:#check 7x7 right sideways
            #             if ((i+6,j) not in self.cord0) or ((i,j+1) not in self.cord0) or ((i+7,j+6) not in self.cord0) or ((i+1,j+7) not in self.cord0):
            #                 self.cord0.append((i+6,j))
            #                 self.cord0.append((i,j+1))
            #                 self.cord0.append((i+7,j+6))
            #                 self.cord0.append((i+1,j+7))
            #                 self.ply1score += 49
            #                 self.counter += 2
            #                 self.update()
            #             else:
            #                 qp.setPen(QPen(Qt.green, 5))
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+6) * CELL_SIZE + 10,GRID_ORIGINX + (j+1) * CELL_SIZE + 10,GRID_ORIGINY + i * CELL_SIZE + 25) #1 -> 2
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+6) * CELL_SIZE + 40,GRID_ORIGINX + (j+6) * CELL_SIZE + 10, GRID_ORIGINY +  (i+7) * CELL_SIZE + 25)#1 -> 3
            #                 qp.drawLine(GRID_ORIGINX + (j+6) * CELL_SIZE + 25, GRID_ORIGINY + (i+7) * CELL_SIZE + 40,GRID_ORIGINX + (j+7) * CELL_SIZE + 40, GRID_ORIGINY +  (i+1) * CELL_SIZE + 25)#3 -> 4
            #                 qp.drawLine(GRID_ORIGINX + (j+7) * CELL_SIZE + 25, GRID_ORIGINY + (i+1) * CELL_SIZE + 10,GRID_ORIGINX + (j+1) * CELL_SIZE + 40, GRID_ORIGINY +  (i) * CELL_SIZE + 25)#4 -> 2
            #                 qp.setPen(QPen(Qt.black))
            #         if self.ply0_brd[i+1][j] == 0 and self.ply0_brd[i][j+6] == 0 and self.ply0_brd[i+7][j+1] == 0 and self.ply0_brd[i+6][j+7] == 0:#check 7x7 left sideways
            #             if ((i+1,j) not in self.cord0) or ((i,j+6) not in self.cord0) or ((i+7,j+1) not in self.cord0) or ((i+6,j+7) not in self.cord0):
            #                 self.cord0.append((i+1,j))
            #                 self.cord0.append((i,j+6))
            #                 self.cord0.append((i+7,j+1))
            #                 self.cord0.append((i+6,j+7))
            #                 self.ply1score += 49
            #                 self.counter += 2
            #                 self.update()
            #             else:
            #                 qp.setPen(QPen(Qt.green, 5))
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+1) * CELL_SIZE + 10,GRID_ORIGINX + (j+6) * CELL_SIZE + 10,GRID_ORIGINY + i * CELL_SIZE + 25) #1 -> 2
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+1) * CELL_SIZE + 40,GRID_ORIGINX + (j+1) * CELL_SIZE + 10, GRID_ORIGINY +  (i+7) * CELL_SIZE + 25)#1 -> 3
            #                 qp.drawLine(GRID_ORIGINX + (j+1) * CELL_SIZE + 25, GRID_ORIGINY + (i+7) * CELL_SIZE + 40,GRID_ORIGINX + (j+7) * CELL_SIZE + 40, GRID_ORIGINY +  (i+6) * CELL_SIZE + 25)#3 -> 4
            #                 qp.drawLine(GRID_ORIGINX + (j+7) * CELL_SIZE + 25, GRID_ORIGINY + (i+6) * CELL_SIZE + 10,GRID_ORIGINX + (j+6) * CELL_SIZE + 40, GRID_ORIGINY +  (i) * CELL_SIZE + 25)#4 -> 2
            #                 qp.setPen(QPen(Qt.black))




        #if self.__turn == 1 or self.__turn == 0:


        

            # for i in range(len(self.__board)-1):#check each possible 2x2 square for player0
            #     for j in range(len(self.__board)-1):
            #         if self.ply1_brd[i][j] == 1 and self.ply1_brd[i][j+1] == 1 and self.ply1_brd[i+1][j] == 1 and self.ply1_brd[i+1][j+1] == 1:
            #             if ((i,j) not in self.cord1) or ((i,j+1) not in self.cord1) or ((i+1,j) not in self.cord1) or ((i+1,j+1) not in self.cord1):
            #                 self.cord1.append((i,j))
            #                 self.cord1.append((i,j+1))
            #                 self.cord1.append((i+1,j))
            #                 self.cord1.append((i+1,j+1))
            #                 self.ply0score += 4
            #                 self.counter += 1
            #                 self.update()
            #             else:
            #                 qp.setPen(QPen(Qt.yellow, 5))
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i) * CELL_SIZE + 25,GRID_ORIGINX + (j+1) * CELL_SIZE + 25,GRID_ORIGINY + i * CELL_SIZE + 25)
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i) * CELL_SIZE + 25,GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY +  (i+1) * CELL_SIZE + 25)
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+1) * CELL_SIZE + 25,GRID_ORIGINX + (j+1) * CELL_SIZE + 25, GRID_ORIGINY +  (i+1) * CELL_SIZE + 25)
            #                 qp.drawLine(GRID_ORIGINX + (j+1) * CELL_SIZE + 25, GRID_ORIGINY + (i) * CELL_SIZE + 25,GRID_ORIGINX + (j+1) * CELL_SIZE + 25, GRID_ORIGINY +  (i+1) * CELL_SIZE + 25)
            #                 qp.setPen(QPen(Qt.black))
                

            # for i in range(len(self.__board)-2):#check each possible 3x3 square for player0
            #     for j in range(len(self.__board)-2):
            #         if self.ply1_brd[i][j] == 1 and self.ply1_brd[i][j+2] == 1 and self.ply1_brd[i+2][j] == 1 and self.ply1_brd[i+2][j+2] == 1:
            #             if ((i,j) not in self.cord1) or ((i,j+2) not in self.cord1) or ((i+2,j) not in self.cord1) or ((i+2,j+2) not in self.cord1):
            #                 self.cord1.append((i,j))
            #                 self.cord1.append((i,j+2))
            #                 self.cord1.append((i+2,j))
            #                 self.cord1.append((i+2,j+2))
            #                 self.ply0score += 9
            #                 self.counter += 1
            #                 self.update()
            #             else:
            #                 qp.setPen(QPen(Qt.yellow, 5))
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i) * CELL_SIZE + 25,GRID_ORIGINX + (j+2) * CELL_SIZE + 25,GRID_ORIGINY + i * CELL_SIZE + 25)
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i) * CELL_SIZE + 25,GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY +  (i+2) * CELL_SIZE + 25)
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+2) * CELL_SIZE + 25,GRID_ORIGINX + (j+2) * CELL_SIZE + 25, GRID_ORIGINY +  (i+2) * CELL_SIZE + 25)
            #                 qp.drawLine(GRID_ORIGINX + (j+2) * CELL_SIZE + 25, GRID_ORIGINY + (i) * CELL_SIZE + 25,GRID_ORIGINX + (j+2) * CELL_SIZE + 25, GRID_ORIGINY +  (i+2) * CELL_SIZE + 25)
            #                 qp.setPen(QPen(Qt.black))
                

            # for i in range(len(self.__board)-3):#check each possible 4x4 square for player0
            #     for j in range(len(self.__board) - 3):
            #         if self.ply1_brd[i][j] == 1 and self.ply1_brd[i][j+3] == 1 and self.ply1_brd[i+3][j] == 1 and self.ply1_brd[i+3][j+3] == 1:
            #             if ((i,j) not in self.cord1) or ((i,j+3) not in self.cord1) or ((i+3,j) not in self.cord1) or ((i+3,j+3) not in self.cord1):
            #                 self.cord1.append((i,j))
            #                 self.cord1.append((i,j+3))
            #                 self.cord1.append((i+3,j))
            #                 self.cord1.append((i+3,j+3))
            #                 self.ply0score += 16
            #                 self.counter += 1
            #                 self.update()
            #             else:
            #                 qp.setPen(QPen(Qt.yellow, 5))
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i) * CELL_SIZE + 25,GRID_ORIGINX + (j+3) * CELL_SIZE + 25,GRID_ORIGINY + i * CELL_SIZE + 25)
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i) * CELL_SIZE + 25,GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY +  (i+3) * CELL_SIZE + 25)
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+3) * CELL_SIZE + 25,GRID_ORIGINX + (j+3) * CELL_SIZE + 25, GRID_ORIGINY +  (i+3) * CELL_SIZE + 25)
            #                 qp.drawLine(GRID_ORIGINX + (j+3) * CELL_SIZE + 25, GRID_ORIGINY + (i) * CELL_SIZE + 25,GRID_ORIGINX + (j+3) * CELL_SIZE + 25, GRID_ORIGINY +  (i+3) * CELL_SIZE + 25)
            #                 qp.setPen(QPen(Qt.black))
                

            # for i in range(len(self.__board)-4):#check each possible 5x5 square for player0
            #     for j in range(len(self.__board)-4):
            #         if self.ply1_brd[i][j] == 1 and self.ply1_brd[i][j+4] == 1 and self.ply1_brd[i+4][j] == 1 and self.ply1_brd[i+4][j+4] == 1:
            #             if ((i,j) not in self.cord1) or ((i,j+4) not in self.cord1) or ((i+4,j) not in self.cord1) or ((i+4,j+4) not in self.cord1):
            #                 self.cord1.append((i,j))
            #                 self.cord1.append((i,j+4))
            #                 self.cord1.append((i+4,j))
            #                 self.cord1.append((i+4,j+4))
            #                 self.ply0score += 25
            #                 self.counter += 1
            #                 self.update()
            #             else:
            #                 qp.setPen(QPen(Qt.yellow, 5))
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i) * CELL_SIZE + 25,GRID_ORIGINX + (j+4) * CELL_SIZE + 25,GRID_ORIGINY + i * CELL_SIZE + 25)
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i) * CELL_SIZE + 25,GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY +  (i+4) * CELL_SIZE + 25)
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+4) * CELL_SIZE + 25,GRID_ORIGINX + (j+4) * CELL_SIZE + 25, GRID_ORIGINY +  (i+4) * CELL_SIZE + 25)
            #                 qp.drawLine(GRID_ORIGINX + (j+4) * CELL_SIZE + 25, GRID_ORIGINY + (i) * CELL_SIZE + 25,GRID_ORIGINX + (j+4) * CELL_SIZE + 25, GRID_ORIGINY +  (i+4) * CELL_SIZE + 25)
            #                 qp.setPen(QPen(Qt.black))
                

            # for i in range(len(self.__board)-5):#check each possible 6x6 square for player0
            #     for j in range(len(self.__board)-5):
            #         if self.ply1_brd[i][j] == 1 and self.ply1_brd[i][j+5] == 1 and self.ply1_brd[i+5][j] == 1 and self.ply1_brd[i+5][j+5] == 1:
            #             if ((i,j) not in self.cord1) or ((i,j+5) not in self.cord1) or ((i+5,j) not in self.cord1) or ((i+5,j+5) not in self.cord1):
            #                 self.cord1.append((i,j))
            #                 self.cord1.append((i,j+5))
            #                 self.cord1.append((i+5,j))
            #                 self.cord1.append((i+5,j+5))
            #                 self.ply0score += 36
            #                 self.counter += 1
            #                 self.update()
            #             else:
            #                 qp.setPen(QPen(Qt.yellow, 5))
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i) * CELL_SIZE + 25,GRID_ORIGINX + (j+5) * CELL_SIZE + 25,GRID_ORIGINY + i * CELL_SIZE + 25)
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i) * CELL_SIZE + 25,GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY +  (i+5) * CELL_SIZE + 25)
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+5) * CELL_SIZE + 25,GRID_ORIGINX + (j+5) * CELL_SIZE + 25, GRID_ORIGINY +  (i+5) * CELL_SIZE + 25)
            #                 qp.drawLine(GRID_ORIGINX + (j+5) * CELL_SIZE + 25, GRID_ORIGINY + (i) * CELL_SIZE + 25,GRID_ORIGINX + (j+5) * CELL_SIZE + 25, GRID_ORIGINY +  (i+5) * CELL_SIZE + 25)
            #                 qp.setPen(QPen(Qt.black))
            
            # for i in range(len(self.__board)-6):#check each possible 7x7 square for player0
            #     for j in range(len(self.__board)-6):
            #         if self.ply1_brd[i][j] == 1 and self.ply1_brd[i][j+6] == 1 and self.ply1_brd[i+6][j] == 1 and self.ply1_brd[i+6][j+6] == 1:
            #             if ((i,j) not in self.cord1) or ((i,j+6) not in self.cord1) or ((i+6,j) not in self.cord1) or ((i+6,j+6) not in self.cord1):
            #                 self.cord1.append((i,j))
            #                 self.cord1.append((i,j+6))
            #                 self.cord1.append((i+6,j))
            #                 self.cord1.append((i+6,j+6))
            #                 self.ply0score += 49
            #                 self.counter += 1
            #                 self.update()
            #             else:
            #                 qp.setPen(QPen(Qt.yellow, 5))
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i) * CELL_SIZE + 25,GRID_ORIGINX + (j+6) * CELL_SIZE + 25,GRID_ORIGINY + i * CELL_SIZE + 25)
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i) * CELL_SIZE + 25,GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY +  (i+6) * CELL_SIZE + 25)
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+6) * CELL_SIZE + 25,GRID_ORIGINX + (j+6) * CELL_SIZE + 25, GRID_ORIGINY +  (i+6) * CELL_SIZE + 25)
            #                 qp.drawLine(GRID_ORIGINX + (j+6) * CELL_SIZE + 25, GRID_ORIGINY + (i) * CELL_SIZE + 25,GRID_ORIGINX + (j+6) * CELL_SIZE + 25, GRID_ORIGINY +  (i+6) * CELL_SIZE + 25)
            #                 qp.setPen(QPen(Qt.black))

            # for i in range(len(self.__board)-7):#check each possible 8x8 square for player0
            #     if self.ply1_brd[i][0] == 1 and self.ply1_brd[i][7] == 1 and self.ply1_brd[i+7][0] == 1 and self.ply1_brd[i+7][7] == 1:
            #         if ((i,0) not in self.cord1) or ((i,7) not in self.cord1) or ((i+7,0) not in self.cord1) or ((i+7,7) not in self.cord1):
            #             self.cord1.append((i,0))
            #             self.cord1.append((i,7))
            #             self.cord1.append((i+7,0))
            #             self.cord1.append((i+7,7))
            #             self.ply0score += 64
            #             self.counter += 1
            #             self.update()
            #         else:
            #             qp.setPen(QPen(Qt.yellow, 5))
            #             qp.drawLine(GRID_ORIGINX + 0 * CELL_SIZE + 25, GRID_ORIGINY + (i) * CELL_SIZE + 25,GRID_ORIGINX + 7 * CELL_SIZE + 25,GRID_ORIGINY + i * CELL_SIZE + 25)
            #             qp.drawLine(GRID_ORIGINX + 0 * CELL_SIZE + 25, GRID_ORIGINY + (i) * CELL_SIZE + 25,GRID_ORIGINX + 0 * CELL_SIZE + 25, GRID_ORIGINY +  (i+7) * CELL_SIZE + 25)
            #             qp.drawLine(GRID_ORIGINX + 0 * CELL_SIZE + 25, GRID_ORIGINY + (i+7) * CELL_SIZE + 25,GRID_ORIGINX + 7 * CELL_SIZE + 25, GRID_ORIGINY +  (i+7) * CELL_SIZE + 25)
            #             qp.drawLine(GRID_ORIGINX + 7 * CELL_SIZE + 25, GRID_ORIGINY + (i) * CELL_SIZE + 25,GRID_ORIGINX + 7 * CELL_SIZE + 25, GRID_ORIGINY +  (i+7) * CELL_SIZE + 25)
            #             qp.setPen(QPen(Qt.black))

            #for k in range(2,8,2):
            

            # for i in range(len(self.__board) - 2):#check for diagonal 3x3 square
            #     for j in range(len(self.__board) - 2):
            #         if self.ply1_brd[i+1][j] == 1 and self.ply1_brd[i][j+1] == 1 and self.ply1_brd[i+2][j+1] == 1 and self.ply1_brd[i+1][j+2] == 1:
            #             if ((i+1,j) not in self.cord1) or ((i,j+1) not in self.cord1) or ((i+2,j+1) not in self.cord1) or ((i+1,j+2) not in self.cord1):
            #                 self.cord1.append((i+1,j))
            #                 self.cord1.append((i,j+1))
            #                 self.cord1.append((i+2,j+1))
            #                 self.cord1.append((i+1,j+2))
            #                 self.ply0score += 9
            #                 self.counter += 2
            #                 self.update()
            #             else:
            #                 qp.setPen(QPen(Qt.yellow, 5))
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+1) * CELL_SIZE + 10,GRID_ORIGINX + (j+1) * CELL_SIZE + 10,GRID_ORIGINY + i * CELL_SIZE + 25)
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+1) * CELL_SIZE + 40,GRID_ORIGINX + (j+1) * CELL_SIZE + 10, GRID_ORIGINY +  (i+2) * CELL_SIZE + 25)
            #                 qp.drawLine(GRID_ORIGINX + (j+1) * CELL_SIZE + 25, GRID_ORIGINY + (i+2) * CELL_SIZE + 40,GRID_ORIGINX + (j+2) * CELL_SIZE + 40, GRID_ORIGINY +  (i+1) * CELL_SIZE + 25)
            #                 qp.drawLine(GRID_ORIGINX + (j+2) * CELL_SIZE + 25, GRID_ORIGINY + (i+1) * CELL_SIZE + 10,GRID_ORIGINX + (j+1) * CELL_SIZE + 40, GRID_ORIGINY +  (i) * CELL_SIZE + 25)
            #                 qp.setPen(QPen(Qt.black))

            # for i in range(len(self.__board)-4):#check for diagonal 5x5 square
            #     for j in range(len(self.__board)-4):
            #         if self.ply1_brd[i+2][j] == 1 and self.ply1_brd[i][j+2] == 1 and self.ply1_brd[i+4][j+2] == 1 and self.ply1_brd[i+2][j+4] == 1:
            #             if ((i+2,j) not in self.cord1) or ((i,j+2) not in self.cord1) or ((i+4,j+2) not in self.cord1) or ((i+2,j+4) not in self.cord1):
            #                 self.cord1.append((i+2,j))
            #                 self.cord1.append((i,j+2))
            #                 self.cord1.append((i+4,j+2))
            #                 self.cord1.append((i+2,j+4))
            #                 self.ply0score += 25
            #                 self.counter += 2
            #                 self.update()
            #             else:
            #                 qp.setPen(QPen(Qt.yellow, 5))
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+2) * CELL_SIZE + 10,GRID_ORIGINX + (j+2) * CELL_SIZE + 10,GRID_ORIGINY + i * CELL_SIZE + 25) #1 -> 2
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+2) * CELL_SIZE + 40,GRID_ORIGINX + (j+2) * CELL_SIZE + 10, GRID_ORIGINY +  (i+4) * CELL_SIZE + 25)#1 -> 3
            #                 qp.drawLine(GRID_ORIGINX + (j+2) * CELL_SIZE + 25, GRID_ORIGINY + (i+4) * CELL_SIZE + 40,GRID_ORIGINX + (j+4) * CELL_SIZE + 40, GRID_ORIGINY +  (i+2) * CELL_SIZE + 25)#3 -> 4
            #                 qp.drawLine(GRID_ORIGINX + (j+4) * CELL_SIZE + 25, GRID_ORIGINY + (i+2) * CELL_SIZE + 10,GRID_ORIGINX + (j+2) * CELL_SIZE + 40, GRID_ORIGINY +  (i) * CELL_SIZE + 25)#4 -> 2
            #                 qp.setPen(QPen(Qt.black))

            # for i in range(len(self.__board)-6):#check for diagonal 7x7 square
            #     for j in range(len(self.__board)-6):
            #         if self.ply1_brd[i+3][j] == 1 and self.ply1_brd[i][j+3] == 1 and self.ply1_brd[i+6][j+3] == 1 and self.ply1_brd[i+3][j+6] == 1:
            #             if ((i+3,j) not in self.cord1) or ((i,j+3) not in self.cord1) or ((i+6,j+3) not in self.cord1) or ((i+3,j+6) not in self.cord1):
            #                 self.cord1.append((i+3,j))
            #                 self.cord1.append((i,j+3))
            #                 self.cord1.append((i+6,j+3))
            #                 self.cord1.append((i+3,j+6))
            #                 self.ply0score += 49
            #                 self.counter += 2
            #                 self.update()
            #             else:
            #                 qp.setPen(QPen(Qt.yellow, 5))
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+3) * CELL_SIZE + 10,GRID_ORIGINX + (j+3) * CELL_SIZE + 10,GRID_ORIGINY + i * CELL_SIZE + 25) #1 -> 2
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+3) * CELL_SIZE + 40,GRID_ORIGINX + (j+3) * CELL_SIZE + 10, GRID_ORIGINY +  (i+6) * CELL_SIZE + 25)#1 -> 3
            #                 qp.drawLine(GRID_ORIGINX + (j+3) * CELL_SIZE + 25, GRID_ORIGINY + (i+6) * CELL_SIZE + 40,GRID_ORIGINX + (j+6) * CELL_SIZE + 40, GRID_ORIGINY +  (i+3) * CELL_SIZE + 25)#3 -> 4
            #                 qp.drawLine(GRID_ORIGINX + (j+6) * CELL_SIZE + 25, GRID_ORIGINY + (i+3) * CELL_SIZE + 10,GRID_ORIGINX + (j+3) * CELL_SIZE + 40, GRID_ORIGINY +  (i) * CELL_SIZE + 25)#4 -> 2
            #                 qp.setPen(QPen(Qt.black))
            

            # for i in range(len(self.__board)-3):
            #     for j in range(len(self.__board)-3):
            #         if self.ply1_brd[i+2][j] == 1 and self.ply1_brd[i][j+1] == 1 and self.ply1_brd[i+3][j+2] == 1 and self.ply1_brd[i+1][j+3] == 1:#check 3x3 right sideways
            #             if ((i+2,j) not in self.cord1) or ((i,j+1) not in self.cord1) or ((i+3,j+2) not in self.cord1) or ((i+1,j+3) not in self.cord1):
            #                 self.cord1.append((i+2,j))
            #                 self.cord1.append((i,j+1))
            #                 self.cord1.append((i+3,j+2))
            #                 self.cord1.append((i+1,j+3))
            #                 self.ply0score += 9
            #                 self.counter += 2
            #                 self.update()
            #             else:
            #                 qp.setPen(QPen(Qt.yellow, 5))
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+2) * CELL_SIZE + 10,GRID_ORIGINX + (j+1) * CELL_SIZE + 10,GRID_ORIGINY + i * CELL_SIZE + 25) #1 -> 2
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+2) * CELL_SIZE + 40,GRID_ORIGINX + (j+2) * CELL_SIZE + 10, GRID_ORIGINY +  (i+3) * CELL_SIZE + 25)#1 -> 3
            #                 qp.drawLine(GRID_ORIGINX + (j+2) * CELL_SIZE + 25, GRID_ORIGINY + (i+3) * CELL_SIZE + 40,GRID_ORIGINX + (j+3) * CELL_SIZE + 40, GRID_ORIGINY +  (i+1) * CELL_SIZE + 25)#3 -> 4
            #                 qp.drawLine(GRID_ORIGINX + (j+3) * CELL_SIZE + 25, GRID_ORIGINY + (i+1) * CELL_SIZE + 10,GRID_ORIGINX + (j+1) * CELL_SIZE + 40, GRID_ORIGINY +  (i) * CELL_SIZE + 25)#4 -> 2
            #                 qp.setPen(QPen(Qt.black))
            #         if self.ply1_brd[i+1][j] == 1 and self.ply1_brd[i][j+2] == 1 and self.ply1_brd[i+3][j+1] == 1 and self.ply1_brd[i+2][j+3] == 1:#check 3x3 left sideways
            #             if ((i+1,j) not in self.cord1) or ((i,j+2) not in self.cord1) or ((i+3,j+1) not in self.cord1) or ((i+2,j+3) not in self.cord1):
            #                 self.cord1.append((i+1,j))
            #                 self.cord1.append((i,j+2))
            #                 self.cord1.append((i+3,j+1))
            #                 self.cord1.append((i+2,j+3))
            #                 self.ply0score += 9
            #                 self.counter += 2
            #                 self.update()
            #             else:
            #                 qp.setPen(QPen(Qt.yellow, 5))
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+1) * CELL_SIZE + 10,GRID_ORIGINX + (j+2) * CELL_SIZE + 10,GRID_ORIGINY + i * CELL_SIZE + 25) #1 -> 2
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+1) * CELL_SIZE + 40,GRID_ORIGINX + (j+1) * CELL_SIZE + 10, GRID_ORIGINY +  (i+3) * CELL_SIZE + 25)#1 -> 3
            #                 qp.drawLine(GRID_ORIGINX + (j+1) * CELL_SIZE + 25, GRID_ORIGINY + (i+3) * CELL_SIZE + 40,GRID_ORIGINX + (j+3) * CELL_SIZE + 40, GRID_ORIGINY +  (i+2) * CELL_SIZE + 25)#3 -> 4
            #                 qp.drawLine(GRID_ORIGINX + (j+3) * CELL_SIZE + 25, GRID_ORIGINY + (i+2) * CELL_SIZE + 10,GRID_ORIGINX + (j+2) * CELL_SIZE + 40, GRID_ORIGINY +  (i) * CELL_SIZE + 25)#4 -> 2
            #                 qp.setPen(QPen(Qt.black))

            # for i in range(len(self.__board)-4):
            #     for j in range(len(self.__board)-4):
            #         if self.ply1_brd[i+3][j] == 1 and self.ply1_brd[i][j+1] == 1 and self.ply1_brd[i+4][j+3] == 1 and self.ply1_brd[i+1][j+4] == 1:#check 4x4 right sideways
            #             if ((i+3,j) not in self.cord1) or ((i,j+1) not in self.cord1) or ((i+4,j+3) not in self.cord1) or ((i+1,j+4) not in self.cord1):
            #                 self.cord1.append((i+3,j))
            #                 self.cord1.append((i,j+1))
            #                 self.cord1.append((i+4,j+3))
            #                 self.cord1.append((i+1,j+4))
            #                 self.ply0score += 16
            #                 self.counter += 2
            #                 self.update()
            #             else:
            #                 qp.setPen(QPen(Qt.yellow, 5))
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+3) * CELL_SIZE + 10,GRID_ORIGINX + (j+1) * CELL_SIZE + 10,GRID_ORIGINY + i * CELL_SIZE + 25) #1 -> 2
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+3) * CELL_SIZE + 40,GRID_ORIGINX + (j+3) * CELL_SIZE + 10, GRID_ORIGINY +  (i+4) * CELL_SIZE + 25)#1 -> 3
            #                 qp.drawLine(GRID_ORIGINX + (j+3) * CELL_SIZE + 25, GRID_ORIGINY + (i+4) * CELL_SIZE + 40,GRID_ORIGINX + (j+4) * CELL_SIZE + 40, GRID_ORIGINY +  (i+1) * CELL_SIZE + 25)#3 -> 4
            #                 qp.drawLine(GRID_ORIGINX + (j+4) * CELL_SIZE + 25, GRID_ORIGINY + (i+1) * CELL_SIZE + 10,GRID_ORIGINX + (j+1) * CELL_SIZE + 40, GRID_ORIGINY +  (i) * CELL_SIZE + 25)#4 -> 2
            #                 qp.setPen(QPen(Qt.black))
            #         if self.ply1_brd[i+1][j] == 1 and self.ply1_brd[i][j+3] == 1 and self.ply1_brd[i+4][j+1] == 1 and self.ply1_brd[i+3][j+4] == 1:#check 4x4 left sideways
            #             if ((i+1,j) not in self.cord1) or ((i,j+3) not in self.cord1) or ((i+4,j+1) not in self.cord1) or ((i+3,j+4) not in self.cord1):
            #                 self.cord1.append((i+1,j))
            #                 self.cord1.append((i,j+3))
            #                 self.cord1.append((i+4,j+1))
            #                 self.cord1.append((i+3,j+4))
            #                 self.ply0score += 16
            #                 self.counter += 2
            #                 self.update()
            #             else:
            #                 qp.setPen(QPen(Qt.yellow, 5))
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+1) * CELL_SIZE + 10,GRID_ORIGINX + (j+3) * CELL_SIZE + 10,GRID_ORIGINY + i * CELL_SIZE + 25) #1 -> 2
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+1) * CELL_SIZE + 40,GRID_ORIGINX + (j+1) * CELL_SIZE + 10, GRID_ORIGINY +  (i+4) * CELL_SIZE + 25)#1 -> 3
            #                 qp.drawLine(GRID_ORIGINX + (j+1) * CELL_SIZE + 25, GRID_ORIGINY + (i+4) * CELL_SIZE + 40,GRID_ORIGINX + (j+4) * CELL_SIZE + 40, GRID_ORIGINY +  (i+3) * CELL_SIZE + 25)#3 -> 4
            #                 qp.drawLine(GRID_ORIGINX + (j+4) * CELL_SIZE + 25, GRID_ORIGINY + (i+3) * CELL_SIZE + 10,GRID_ORIGINX + (j+3) * CELL_SIZE + 40, GRID_ORIGINY +  (i) * CELL_SIZE + 25)#4 -> 2
            #                 qp.setPen(QPen(Qt.black))

            # for i in range(len(self.__board)-5):
            #     for j in range(len(self.__board)-5):
            #         if self.ply1_brd[i+4][j] == 1 and self.ply1_brd[i][j+1] == 1 and self.ply1_brd[i+5][j+4] == 1 and self.ply1_brd[i+1][j+5] == 1:#check 5x5 right sideways
            #             if ((i+4,j) not in self.cord1) or ((i,j+1) not in self.cord1) or ((i+5,j+4) not in self.cord1) or ((i+1,j+5) not in self.cord1):
            #                 self.cord1.append((i+4,j))
            #                 self.cord1.append((i,j+1))
            #                 self.cord1.append((i+5,j+4))
            #                 self.cord1.append((i+1,j+5))
            #                 self.ply0score += 25
            #                 self.counter += 2
            #                 self.update()
            #             else:
            #                 qp.setPen(QPen(Qt.yellow, 5))
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+4) * CELL_SIZE + 10,GRID_ORIGINX + (j+1) * CELL_SIZE + 10,GRID_ORIGINY + i * CELL_SIZE + 25) #1 -> 2
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+4) * CELL_SIZE + 40,GRID_ORIGINX + (j+4) * CELL_SIZE + 10, GRID_ORIGINY +  (i+5) * CELL_SIZE + 25)#1 -> 3
            #                 qp.drawLine(GRID_ORIGINX + (j+4) * CELL_SIZE + 25, GRID_ORIGINY + (i+5) * CELL_SIZE + 40,GRID_ORIGINX + (j+5) * CELL_SIZE + 40, GRID_ORIGINY +  (i+1) * CELL_SIZE + 25)#3 -> 4
            #                 qp.drawLine(GRID_ORIGINX + (j+5) * CELL_SIZE + 25, GRID_ORIGINY + (i+1) * CELL_SIZE + 10,GRID_ORIGINX + (j+1) * CELL_SIZE + 40, GRID_ORIGINY +  (i) * CELL_SIZE + 25)#4 -> 2
            #                 qp.setPen(QPen(Qt.black))
            #         if self.ply1_brd[i+1][j] == 1 and self.ply1_brd[i][j+4] == 1 and self.ply1_brd[i+5][j+1] == 1 and self.ply1_brd[i+4][j+5] == 1:#check 5x5 left sideways
            #             if ((i+1,j) not in self.cord1) or ((i,j+4) not in self.cord1) or ((i+5,j+1) not in self.cord1) or ((i+4,j+5) not in self.cord1):
            #                 self.cord1.append((i+1,j))
            #                 self.cord1.append((i,j+4))
            #                 self.cord1.append((i+5,j+1))
            #                 self.cord1.append((i+4,j+5))
            #                 self.ply0score += 25
            #                 self.counter += 2
            #                 self.update()
            #             else:
            #                 qp.setPen(QPen(Qt.yellow, 5))
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+1) * CELL_SIZE + 10,GRID_ORIGINX + (j+4) * CELL_SIZE + 10,GRID_ORIGINY + i * CELL_SIZE + 25) #1 -> 2
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+1) * CELL_SIZE + 40,GRID_ORIGINX + (j+1) * CELL_SIZE + 10, GRID_ORIGINY +  (i+5) * CELL_SIZE + 25)#1 -> 3
            #                 qp.drawLine(GRID_ORIGINX + (j+1) * CELL_SIZE + 25, GRID_ORIGINY + (i+5) * CELL_SIZE + 40,GRID_ORIGINX + (j+5) * CELL_SIZE + 40, GRID_ORIGINY +  (i+4) * CELL_SIZE + 25)#3 -> 4
            #                 qp.drawLine(GRID_ORIGINX + (j+5) * CELL_SIZE + 25, GRID_ORIGINY + (i+4) * CELL_SIZE + 10,GRID_ORIGINX + (j+4) * CELL_SIZE + 40, GRID_ORIGINY +  (i) * CELL_SIZE + 25)#4 -> 2
            #                 qp.setPen(QPen(Qt.black))

            # for i in range(len(self.__board)-6):
            #     for j in range(len(self.__board)-6):
            #         if self.ply1_brd[i+5][j] == 1 and self.ply1_brd[i][j+1] == 1 and self.ply1_brd[i+6][j+5] == 1 and self.ply1_brd[i+1][j+6] == 1:#check 6x6 right sideways
            #             if ((i+5,j) not in self.cord1) or ((i,j+1) not in self.cord1) or ((i+6,j+5) not in self.cord1) or ((i+1,j+6) not in self.cord1):
            #                 self.cord1.append((i+5,j))
            #                 self.cord1.append((i,j+1))
            #                 self.cord1.append((i+6,j+5))
            #                 self.cord1.append((i+1,j+6))
            #                 self.ply0score += 36
            #                 self.counter += 2
            #                 self.update()
            #             else:
            #                 qp.setPen(QPen(Qt.yellow, 5))
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+5) * CELL_SIZE + 10,GRID_ORIGINX + (j+1) * CELL_SIZE + 10,GRID_ORIGINY + i * CELL_SIZE + 25) #1 -> 2
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+5) * CELL_SIZE + 40,GRID_ORIGINX + (j+5) * CELL_SIZE + 10, GRID_ORIGINY +  (i+6) * CELL_SIZE + 25)#1 -> 3
            #                 qp.drawLine(GRID_ORIGINX + (j+5) * CELL_SIZE + 25, GRID_ORIGINY + (i+6) * CELL_SIZE + 40,GRID_ORIGINX + (j+6) * CELL_SIZE + 40, GRID_ORIGINY +  (i+1) * CELL_SIZE + 25)#3 -> 4
            #                 qp.drawLine(GRID_ORIGINX + (j+6) * CELL_SIZE + 25, GRID_ORIGINY + (i+1) * CELL_SIZE + 10,GRID_ORIGINX + (j+1) * CELL_SIZE + 40, GRID_ORIGINY +  (i) * CELL_SIZE + 25)#4 -> 2
            #                 qp.setPen(QPen(Qt.black))
            #         if self.ply1_brd[i+1][j] == 1 and self.ply1_brd[i][j+5] == 1 and self.ply1_brd[i+6][j+1] == 1 and self.ply1_brd[i+5][j+6] == 1:#check 6x6 left sideways
            #             if ((i+1,j) not in self.cord1) or ((i,j+5) not in self.cord1) or ((i+6,j+1) not in self.cord1) or ((i+5,j+6) not in self.cord1):
            #                 self.cord1.append((i+1,j))
            #                 self.cord1.append((i,j+5))
            #                 self.cord1.append((i+6,j+1))
            #                 self.cord1.append((i+5,j+6))
            #                 self.ply0score += 36
            #                 self.counter += 2
            #                 self.update()
            #             else:
            #                 qp.setPen(QPen(Qt.yellow, 5))
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+1) * CELL_SIZE + 10,GRID_ORIGINX + (j+5) * CELL_SIZE + 10,GRID_ORIGINY + i * CELL_SIZE + 25) #1 -> 2
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+1) * CELL_SIZE + 40,GRID_ORIGINX + (j+1) * CELL_SIZE + 10, GRID_ORIGINY +  (i+6) * CELL_SIZE + 25)#1 -> 3
            #                 qp.drawLine(GRID_ORIGINX + (j+1) * CELL_SIZE + 25, GRID_ORIGINY + (i+6) * CELL_SIZE + 40,GRID_ORIGINX + (j+6) * CELL_SIZE + 40, GRID_ORIGINY +  (i+5) * CELL_SIZE + 25)#3 -> 4
            #                 qp.drawLine(GRID_ORIGINX + (j+6) * CELL_SIZE + 25, GRID_ORIGINY + (i+5) * CELL_SIZE + 10,GRID_ORIGINX + (j+5) * CELL_SIZE + 40, GRID_ORIGINY +  (i) * CELL_SIZE + 25)#4 -> 2
            #                 qp.setPen(QPen(Qt.black))

            # for i in range(len(self.__board)-7):
            #     for j in range(len(self.__board)-7):
            #         if self.ply1_brd[i+6][j] == 1 and self.ply1_brd[i][j+1] == 1 and self.ply1_brd[i+7][j+6] == 1 and self.ply1_brd[i+1][j+7] == 1:#check 7x7 right sideways
            #             if ((i+6,j) not in self.cord1) or ((i,j+1) not in self.cord1) or ((i+7,j+6) not in self.cord1) or ((i+1,j+7) not in self.cord1):
            #                 self.cord1.append((i+6,j))
            #                 self.cord1.append((i,j+1))
            #                 self.cord1.append((i+7,j+6))
            #                 self.cord1.append((i+1,j+7))
            #                 self.ply0score += 49
            #                 self.counter += 2
            #                 self.update()
            #             else:
            #                 qp.setPen(QPen(Qt.yellow, 5))
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+6) * CELL_SIZE + 10,GRID_ORIGINX + (j+1) * CELL_SIZE + 10,GRID_ORIGINY + i * CELL_SIZE + 25) #1 -> 2
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+6) * CELL_SIZE + 40,GRID_ORIGINX + (j+6) * CELL_SIZE + 10, GRID_ORIGINY +  (i+7) * CELL_SIZE + 25)#1 -> 3
            #                 qp.drawLine(GRID_ORIGINX + (j+6) * CELL_SIZE + 25, GRID_ORIGINY + (i+7) * CELL_SIZE + 40,GRID_ORIGINX + (j+7) * CELL_SIZE + 40, GRID_ORIGINY +  (i+1) * CELL_SIZE + 25)#3 -> 4
            #                 qp.drawLine(GRID_ORIGINX + (j+7) * CELL_SIZE + 25, GRID_ORIGINY + (i+1) * CELL_SIZE + 10,GRID_ORIGINX + (j+1) * CELL_SIZE + 40, GRID_ORIGINY +  (i) * CELL_SIZE + 25)#4 -> 2
            #                 qp.setPen(QPen(Qt.black))
            #         if self.ply1_brd[i+1][j] == 1 and self.ply1_brd[i][j+6] == 1 and self.ply1_brd[i+7][j+1] == 1 and self.ply1_brd[i+6][j+7] == 1:#check 7x7 left sideways
            #             if ((i+1,j) not in self.cord1) or ((i,j+6) not in self.cord1) or ((i+7,j+1) not in self.cord1) or ((i+6,j+7) not in self.cord1):
            #                 self.cord1.append((i+1,j))
            #                 self.cord1.append((i,j+6))
            #                 self.cord1.append((i+7,j+1))
            #                 self.cord1.append((i+6,j+7))
            #                 self.ply0score += 49
            #                 self.counter += 2
            #                 self.update()
            #             else:
            #                 qp.setPen(QPen(Qt.yellow, 5))
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+1) * CELL_SIZE + 10,GRID_ORIGINX + (j+6) * CELL_SIZE + 10,GRID_ORIGINY + i * CELL_SIZE + 25) #1 -> 2
            #                 qp.drawLine(GRID_ORIGINX + j * CELL_SIZE + 25, GRID_ORIGINY + (i+1) * CELL_SIZE + 40,GRID_ORIGINX + (j+1) * CELL_SIZE + 10, GRID_ORIGINY +  (i+7) * CELL_SIZE + 25)#1 -> 3
            #                 qp.drawLine(GRID_ORIGINX + (j+1) * CELL_SIZE + 25, GRID_ORIGINY + (i+7) * CELL_SIZE + 40,GRID_ORIGINX + (j+7) * CELL_SIZE + 40, GRID_ORIGINY +  (i+6) * CELL_SIZE + 25)#3 -> 4
            #                 qp.drawLine(GRID_ORIGINX + (j+7) * CELL_SIZE + 25, GRID_ORIGINY + (i+6) * CELL_SIZE + 10,GRID_ORIGINX + (j+6) * CELL_SIZE + 40, GRID_ORIGINY +  (i) * CELL_SIZE + 25)#4 -> 2
            #                 qp.setPen(QPen(Qt.black))
        #self.Multiplier() 743 -> 152




if __name__ == '__main__':
  app = QApplication(sys.argv)
  ex = TribeSquares()
  sys.exit(app.exec_())