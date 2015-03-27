# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Thu Jan  8 15:31:04 2015
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(958, 628)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.languageLabel = QtWidgets.QLabel(self.centralWidget)
        self.languageLabel.setObjectName("languageLabel")
        self.horizontalLayout_2.addWidget(self.languageLabel)
        self.languagesBox = QtWidgets.QComboBox(self.centralWidget)
        self.languagesBox.setMinimumSize(QtCore.QSize(120, 0))
        self.languagesBox.setObjectName("languagesBox")
        self.horizontalLayout_2.addWidget(self.languagesBox)
        self.projectsLabel = QtWidgets.QLabel(self.centralWidget)
        self.projectsLabel.setObjectName("projectsLabel")
        self.horizontalLayout_2.addWidget(self.projectsLabel)
        self.projectsBox = QtWidgets.QComboBox(self.centralWidget)
        self.projectsBox.setMinimumSize(QtCore.QSize(250, 0))
        self.projectsBox.setObjectName("projectsBox")
        self.horizontalLayout_2.addWidget(self.projectsBox)
        self.runProject = QtWidgets.QPushButton(self.centralWidget)
        self.runProject.setObjectName("runProject")
        self.horizontalLayout_2.addWidget(self.runProject)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.filesTable = QtWidgets.QTableView(self.centralWidget)
        self.filesTable.setObjectName("filesTable")
        self.verticalLayout_3.addWidget(self.filesTable)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.openFile = QtWidgets.QPushButton(self.centralWidget)
        self.openFile.setObjectName("openFile")
        self.horizontalLayout_3.addWidget(self.openFile)
        self.dropFile = QtWidgets.QPushButton(self.centralWidget)
        self.dropFile.setObjectName("dropFile")
        self.horizontalLayout_3.addWidget(self.dropFile)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.openUotput = QtWidgets.QPushButton(self.centralWidget)
        self.openUotput.setObjectName("openUotput")
        self.horizontalLayout_3.addWidget(self.openUotput)
        self.dropOutput = QtWidgets.QPushButton(self.centralWidget)
        self.dropOutput.setObjectName("dropOutput")
        self.horizontalLayout_3.addWidget(self.dropOutput)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.gridLayout.addLayout(self.verticalLayout_3, 1, 0, 3, 1)
        self.wordsTable = QtWidgets.QTableView(self.centralWidget)
        self.wordsTable.setObjectName("wordsTable")
        self.gridLayout.addWidget(self.wordsTable, 1, 1, 1, 1)
        self.dicsTable = QtWidgets.QTableView(self.centralWidget)
        self.dicsTable.setObjectName("dicsTable")
        self.gridLayout.addWidget(self.dicsTable, 2, 1, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.openDic = QtWidgets.QPushButton(self.centralWidget)
        self.openDic.setObjectName("openDic")
        self.horizontalLayout_5.addWidget(self.openDic)
        self.dropDic = QtWidgets.QPushButton(self.centralWidget)
        self.dropDic.setObjectName("dropDic")
        self.horizontalLayout_5.addWidget(self.dropDic)
        self.gridLayout.addLayout(self.horizontalLayout_5, 3, 1, 1, 1)
        self.gridLayout.setColumnStretch(0, 1)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 958, 25))
        self.menuBar.setObjectName("menuBar")
        self.menuFil = QtWidgets.QMenu(self.menuBar)
        self.menuFil.setObjectName("menuFil")
        self.menuLanguages = QtWidgets.QMenu(self.menuBar)
        self.menuLanguages.setObjectName("menuLanguages")
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menuBar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionManage = QtWidgets.QAction(MainWindow)
        self.actionManage.setObjectName("actionManage")
        self.menuFil.addAction(self.actionExit)
        self.menuLanguages.addAction(self.actionManage)
        self.menuHelp.addAction(self.actionAbout)
        self.menuBar.addAction(self.menuFil.menuAction())
        self.menuBar.addAction(self.menuLanguages.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "LangTools"))
        self.languageLabel.setText(_translate("MainWindow", "Language"))
        self.projectsLabel.setText(_translate("MainWindow", "Project"))
        self.runProject.setText(_translate("MainWindow", ">"))
        self.openFile.setText(_translate("MainWindow", "Open File"))
        self.dropFile.setText(_translate("MainWindow", "Delete File"))
        self.openUotput.setText(_translate("MainWindow", "Open Markup"))
        self.dropOutput.setText(_translate("MainWindow", "Delete Markup"))
        self.openDic.setText(_translate("MainWindow", "Open Dic"))
        self.dropDic.setText(_translate("MainWindow", "Delete Dic"))
        self.menuFil.setTitle(_translate("MainWindow", "File"))
        self.menuLanguages.setTitle(_translate("MainWindow", "Languages"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionManage.setText(_translate("MainWindow", "Manage"))

