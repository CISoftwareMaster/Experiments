import sys
from math import floor
from random import random
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class BlurView(QTextBrowser):
    def __init__(self):
        super().__init__()
        self.capturing = True
        self.blur = self.grab(QRect(0, 0, self.width(), self.height()))
        self.blur_tmp = QLabel()
        self.blur_tmp.setScaledContents(True)
        self.blur_effect = QGraphicsBlurEffect()
        self.blur_effect.setBlurRadius(64)
        self.blur_effect.setBlurHints(QGraphicsBlurEffect.AnimationHint)
        self.blur_tmp.setGraphicsEffect(self.blur_effect)
        self.capturing = False
        self.repaint()

    def resizeEvent(self, e):
        super().resizeEvent(e)
        try:
            self.blur_tmp.resize(self.width()/2, self.height()/2)
        except:
            pass

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter()

        if painter.begin(self.viewport()):
            if not self.capturing:
                # repeatedly draw the blurred pixmap (to make It opaque)
                try:
                    for i in range(32):
                        painter.drawPixmap(QRect(0, 0, self.width(), 64), self.blur, QRect(0, 0, self.width(), 64))
                except:
                    pass
                painter.setPen(Qt.NoPen)

                # draw a white transparent rectangle
                painter.setBrush(QBrush(QColor(255, 255, 255, 50)))
                painter.drawRect(0, 0, self.width(), 64)
            painter.end()

    def wheelEvent(self, e):
        # handle default scroll event
        super().wheelEvent(e)
        # disable drawing of the blurred header
        self.capturing = True
        # capture a screenshot of the widget
        self.blur = self.grab(QRect(0, 0, self.width(), self.height()))
        self.blur_tmp.setPixmap(self.blur)
        # capture a screenshot of the blurred pixmap
        self.blur = self.blur_tmp.grab(QRect(0, 0, self.width(), 64))
        # enable drawing of the blurred header
        self.capturing = False
        # redraw
        self.viewport().repaint()


class BlurWindow(QMainWindow):
    def __init__(self):
        # initialise as QMainWindow
        super().__init__()
        self.browser = BlurView()

        # generate a colourful text document
        for i in range(1000):
            r = floor(random() * 255)
            g = floor(random() * 255)
            b = floor(random() * 255)
            s = 1 + floor(random() * 5)
            text = "Some Text"
            self.browser.insertHtml("<h{} style=color:rgb({},{},{})>{}</h{}>".format(s, r, g, b, text, s))
        self.setMinimumSize(300, 300)
        self.setCentralWidget(self.browser)
        # show
        self.show()


if __name__ == "__main__":
    # initialise app
    app = QApplication(sys.argv)

    # initialise window
    window = BlurWindow()

    # enter main loop
    sys.exit(app.exec_())
 
