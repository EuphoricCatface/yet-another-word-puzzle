# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.2.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide2.QtWidgets import (QAction, QApplication, QFrame, QMainWindow, QMenu,
    QMenuBar, QSizePolicy, QStatusBar, QVBoxLayout,
    QWidget)

from widget.BoardFrame import BoardWidget
from widget.TopFrame import TopFrame

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(218, 377)
        self.actionNew = QAction(MainWindow)
        self.actionNew.setObjectName(u"actionNew")
        self.actionUndo = QAction(MainWindow)
        self.actionUndo.setObjectName(u"actionUndo")
        self.actionRedo = QAction(MainWindow)
        self.actionRedo.setObjectName(u"actionRedo")
        self.actionSet_Get_seed = QAction(MainWindow)
        self.actionSet_Get_seed.setObjectName(u"actionSet_Get_seed")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame_Top = TopFrame(self.centralwidget)
        self.frame_Top.setObjectName(u"frame_Top")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_Top.sizePolicy().hasHeightForWidth())
        self.frame_Top.setSizePolicy(sizePolicy)
        self.frame_Top.setMinimumSize(QSize(200, 100))
        self.frame_Top.setMaximumSize(QSize(200, 100))
        self.frame_Top.setFrameShape(QFrame.StyledPanel)
        self.frame_Top.setFrameShadow(QFrame.Raised)

        self.verticalLayout.addWidget(self.frame_Top)

        self.frame_Board = BoardWidget(self.centralwidget)
        self.frame_Board.setObjectName(u"frame_Board")
        sizePolicy.setHeightForWidth(self.frame_Board.sizePolicy().hasHeightForWidth())
        self.frame_Board.setSizePolicy(sizePolicy)
        self.frame_Board.setMinimumSize(QSize(200, 200))
        self.frame_Board.setMaximumSize(QSize(200, 200))
        self.frame_Board.setFrameShape(QFrame.StyledPanel)
        self.frame_Board.setFrameShadow(QFrame.Raised)

        self.verticalLayout.addWidget(self.frame_Board)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 218, 27))
        self.menuNew_Game = QMenu(self.menubar)
        self.menuNew_Game.setObjectName(u"menuNew_Game")
        self.menuUndo = QMenu(self.menubar)
        self.menuUndo.setObjectName(u"menuUndo")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuNew_Game.menuAction())
        self.menubar.addAction(self.menuUndo.menuAction())
        self.menuNew_Game.addAction(self.actionNew)
        self.menuNew_Game.addAction(self.actionSet_Get_seed)
        self.menuUndo.addAction(self.actionUndo)
        self.menuUndo.addAction(self.actionRedo)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionNew.setText(QCoreApplication.translate("MainWindow", u"New", None))
#if QT_CONFIG(shortcut)
        self.actionNew.setShortcut(QCoreApplication.translate("MainWindow", u"F5", None))
#endif // QT_CONFIG(shortcut)
        self.actionUndo.setText(QCoreApplication.translate("MainWindow", u"Undo...", None))
#if QT_CONFIG(shortcut)
        self.actionUndo.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Z", None))
#endif // QT_CONFIG(shortcut)
        self.actionRedo.setText(QCoreApplication.translate("MainWindow", u"Redo...", None))
#if QT_CONFIG(shortcut)
        self.actionRedo.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+Z", None))
#endif // QT_CONFIG(shortcut)
        self.actionSet_Get_seed.setText(QCoreApplication.translate("MainWindow", u"Set/Get seed...", None))
#if QT_CONFIG(shortcut)
        self.actionSet_Get_seed.setShortcut(QCoreApplication.translate("MainWindow", u"Shift+F5", None))
#endif // QT_CONFIG(shortcut)
        self.menuNew_Game.setTitle(QCoreApplication.translate("MainWindow", u"Game", None))
        self.menuUndo.setTitle(QCoreApplication.translate("MainWindow", u"Move", None))
    # retranslateUi

