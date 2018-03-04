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
        self.blur = None
        self.blur_tmp = QLabel()
        self.blur_tmp.setScaledContents(True)
        self.blur_effect = QGraphicsBlurEffect()
        self.blur_effect.setBlurRadius(64)
        self.blur_effect.setBlurHints(QGraphicsBlurEffect.PerformanceHint)
        self.blur_tmp.setGraphicsEffect(self.blur_effect)
        self.capturing = False
        self.update_effect()
        self.setMouseTracking(True)
        self.verticalScrollBar().valueChanged.connect(self.update_effect)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        try:
            self.blur_tmp.resize(self.width()/2, self.height()/2)
        except:
            pass

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        self.update_effect()

    def mousePressEvent(self, e):
        super().mouseReleaseEvent(e)
        self.update_effect()

    def mouseMoveEvent(self, e):
        super().mouseReleaseEvent(e)
        if e.buttons() == Qt.LeftButton:
            self.update_effect()

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter()

        if painter.begin(self.viewport()):
            # enable antialiasing
            painter.setRenderHint(QPainter.Antialiasing)

            if not self.capturing:
                painter.setPen(Qt.NoPen)
                painter.setBrush(QBrush(QColor(255, 255, 255)))
                painter.drawRect(0, 0, self.width(), 64)
                # repeatedly draw the blurred pixmap (to make It opaque)
                try:
                    for i in range(3):
                        painter.drawPixmap(QRect(0, 0, self.width(), 64), self.blur, QRect(0, 0, self.width(), 64))
                except:
                    pass

                # draw a white transparent rectangle
                painter.setBrush(QBrush(QColor(255, 255, 255, 50)))
                painter.drawRect(0, 0, self.width(), 64)

                # draw border
                painter.setBrush(QBrush(QColor(150, 150, 150, 100)))
                painter.drawRect(0, 63, self.width(), 1)

                # draw some text over it
                painter.setPen(QPen(QColor(30, 30, 30, 150)))
                a = painter.font()
                a.setPointSize(13)
                painter.setFont(a)
                painter.drawText(QRect(0, 0, self.width(), 64), Qt.AlignCenter, "Blurred Header")

            painter.end()

    def update_effect(self):
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

        # set window properties
        self.setMinimumSize(300, 480)
        self.setCentralWidget(self.browser)
        self.setWindowTitle("iOS 7 - style blur experiment")
        # show
        self.show()
        self.browser.verticalScrollBar().setValue(0)


if __name__ == "__main__":
    # initialise app
    app = QApplication(sys.argv)

    # initialise window
    window = BlurWindow()

    # enter main loop
    sys.exit(app.exec_())
