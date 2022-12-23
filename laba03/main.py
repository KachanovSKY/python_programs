from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

import turtle
from math import sqrt
import sys


def get_mid_point(p_1: list, p_2: list):
    return ((p_1[0] + p_2[0]) / 2, (p_1[1] + p_2[1]) / 2)


def serpinskyF(p, n):
    turtle.penup()
    turtle.goto(p[0][0], p[0][1])
    turtle.speed(30)

    turtle.pendown()
    turtle.goto(p[1][0], p[1][1])
    turtle.goto(p[2][0], p[2][1])
    turtle.goto(p[0][0], p[0][1])

    if n > 0:
        serpinskyF([p[0], get_mid_point(p[0], p[1]), get_mid_point(p[0], p[2])],
                   n - 1)
        serpinskyF([p[1], get_mid_point(p[0], p[1]), get_mid_point(p[1], p[2])],
                   n - 1)
        serpinskyF([p[2], get_mid_point(p[2], p[1]), get_mid_point(p[0], p[2])],
                   n - 1)


def piphagorF(aturt, n, maxdepth):
    if n > maxdepth:
        return
    turtle.speed(30)
    length = 180 * ((sqrt(2) / 2) ** n)
    anotherturt = aturt.clone()
    aturt.forward(length)
    aturt.left(45)
    piphagorF(aturt, n + 1, maxdepth)
    anotherturt.right(90)
    anotherturt.forward(length)
    anotherturt.left(90)
    anotherturt.forward(length)
    if n != maxdepth:
        turt3 = anotherturt.clone()
        turt3.left(45)
        turt3.forward(180 * ((sqrt(2) / 2) ** (1 + n)))
        turt3.right(90)
        piphagorF(turt3, n + 1, maxdepth)
    anotherturt.left(90)
    anotherturt.forward(length)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Holst")
        self.setGeometry(0, 0, 1200, 800)
        self.image = QImage(QSize(self.size()), QImage.Format.Format_RGB32)
        self.image.fill(QColor('white'))

        self.drawing = False
        self.brushSize = 4
        self.brushColor = QColor('black')
        self.lastPoint = QPoint()

        # Buttons
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("File")
        brush = mainMenu.addMenu("Brush")
        window = mainMenu.addMenu("Holst")
        fractal = mainMenu.addMenu("Fractal")
        brushSize = brush.addMenu("Brush Size")
        brushColor = brush.addMenu("Brush Color")
        background = window.addMenu("Background Color")

        saveButton = QAction("Save", self)
        loadButton = QAction("Load", self)
        clearButton = QAction("Clear", self)

        fileMenu.addAction(saveButton)
        fileMenu.addAction(loadButton)
        window.addAction(clearButton)

        saveButton.triggered.connect(self.save)
        loadButton.triggered.connect(self.load)
        clearButton.triggered.connect(self.clear)

        # Brush Sizes
        pix_4 = QAction("4px", self)
        pix_7 = QAction("7px", self)
        pix_9 = QAction("9px", self)
        pix_12 = QAction("12px", self)

        brushSize.addAction(pix_4)
        brushSize.addAction(pix_7)
        brushSize.addAction(pix_9)
        brushSize.addAction(pix_12)

        pix_4.triggered.connect(self.Pixel_4)
        pix_7.triggered.connect(self.Pixel_7)
        pix_9.triggered.connect(self.Pixel_9)
        pix_12.triggered.connect(self.Pixel_12)

        # Colors
        black = QAction("Black", self)
        white = QAction("White", self)
        grey = QAction("Grey", self)
        green = QAction("Green", self)
        pink = QAction("Pink", self)
        red = QAction("Red", self)
        backgroundLight = QAction("Light", self)
        backgroundDark = QAction("Dark", self)


        brushColor.addAction(black)
        brushColor.addAction(white)
        brushColor.addAction(grey)
        brushColor.addAction(green)
        brushColor.addAction(pink)
        brushColor.addAction(red)
        background.addAction(backgroundLight)
        background.addAction(backgroundDark)

        black.triggered.connect(self.blackColor)
        white.triggered.connect(self.whiteColor)
        grey.triggered.connect(self.greyColor)
        green.triggered.connect(self.greenColor)
        pink.triggered.connect(self.pinkColor)
        red.triggered.connect(self.redColor)
        backgroundLight.triggered.connect(self.light)
        backgroundDark.triggered.connect(self.dark)


    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = True
            self.lastPoint = event.position()

    def mouseMoveEvent(self, event):
        if bool(event.buttons() & Qt.MouseButton.LeftButton) & self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.PenStyle.SolidLine))
            painter.drawLine(self.lastPoint, event.position())

            self.lastPoint = event.position()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())

    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")

        if filePath == "":
            return
        self.image.save(filePath)

    def load(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Load Image", "", "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")

        if filePath == "":
            return
        self.image = QImage(filePath)


    def clear(self):
        self.image.fill(QColor('white'))
        self.update()

    def light(self):
        self.image.fill(QColor('white'))
        self.update()

    def dark(self):
        self.image.fill(QColor('grey'))
        self.update()

    def Pixel_4(self):
        self.brushSize = 4

    def Pixel_7(self):
        self.brushSize = 7

    def Pixel_9(self):
        self.brushSize = 9

    def Pixel_12(self):
        self.brushSize = 12

    def blackColor(self):
        self.brushColor = QColor('black')

    def whiteColor(self):
        self.brushColor = QColor('white')

    def greyColor(self):
        self.brushColor = QColor('grey')

    def greenColor(self):
        self.brushColor = QColor('green')

    def pinkColor(self):
        self.brushColor = QColor('pink')

    def redColor(self):
        self.brushColor = QColor('red')


App = QApplication(sys.argv)

window = Window()

window.show()

sys.exit(App.exec())