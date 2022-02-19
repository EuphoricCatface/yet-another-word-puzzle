# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'TopFrame.ui'
##
## Created by: Qt User Interface Compiler version 6.2.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide2.QtWidgets import (QApplication, QFrame, QGridLayout, QLabel,
    QSizePolicy, QWidget)

class Ui_Frame(object):
    def setupUi(self, Frame):
        if not Frame.objectName():
            Frame.setObjectName(u"Frame")
        Frame.resize(200, 100)
        self.gridLayout = QGridLayout(Frame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_wordscore = QLabel(Frame)
        self.label_wordscore.setObjectName(u"label_wordscore")

        self.gridLayout.addWidget(self.label_wordscore, 2, 2, 1, 1)

        self.label_score = QLabel(Frame)
        self.label_score.setObjectName(u"label_score")
        self.label_score.setStyleSheet(u"background-color: palette(base)")
        self.label_score.setFrameShape(QFrame.Panel)
        self.label_score.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.label_score, 0, 0, 1, 2)

        self.line = QFrame(Frame)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line, 1, 0, 1, 3)

        self.label_word = QLabel(Frame)
        self.label_word.setObjectName(u"label_word")
        self.label_word.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_word, 2, 0, 1, 2)

        self.label_countdown = QLabel(Frame)
        self.label_countdown.setObjectName(u"label_countdown")
        self.label_countdown.setStyleSheet(u"background-color: palette(base)")
        self.label_countdown.setFrameShape(QFrame.Panel)
        self.label_countdown.setFrameShadow(QFrame.Sunken)
        self.label_countdown.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_countdown, 0, 2, 1, 1)


        self.retranslateUi(Frame)

        QMetaObject.connectSlotsByName(Frame)
    # setupUi

    def retranslateUi(self, Frame):
        Frame.setWindowTitle(QCoreApplication.translate("Frame", u"Frame", None))
        self.label_wordscore.setText(QCoreApplication.translate("Frame", u"TextLabel", None))
        self.label_score.setText(QCoreApplication.translate("Frame", u"Score: 100", None))
        self.label_word.setText(QCoreApplication.translate("Frame", u"TextLabel", None))
        self.label_countdown.setText(QCoreApplication.translate("Frame", u"5 / 10", None))
    # retranslateUi

