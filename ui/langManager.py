# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'languages.ui'
#
# Created: Sat Dec 13 22:40:27 2014
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_languagesDialog(object):
    def setupUi(self, languagesDialog):
        languagesDialog.setObjectName("languagesDialog")
        languagesDialog.resize(421, 400)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(languagesDialog.sizePolicy().hasHeightForWidth())
        languagesDialog.setSizePolicy(sizePolicy)
        languagesDialog.setMinimumSize(QtCore.QSize(421, 400))
        languagesDialog.setMaximumSize(QtCore.QSize(421, 400))
        self.languagesTable = QtWidgets.QTableWidget(languagesDialog)
        self.languagesTable.setGeometry(QtCore.QRect(10, 30, 401, 251))
        self.languagesTable.setObjectName("languagesTable")
        self.languagesTable.setColumnCount(2)
        self.languagesTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.languagesTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.languagesTable.setHorizontalHeaderItem(1, item)
        self.languagesTable.horizontalHeader().setStretchLastSection(True)
        self.languagesTable.verticalHeader().setVisible(False)
        self.folderButton = QtWidgets.QPushButton(languagesDialog)
        self.folderButton.setGeometry(QtCore.QRect(370, 330, 21, 27))
        self.folderButton.setObjectName("folderButton")
        self.langEdit = QtWidgets.QLineEdit(languagesDialog)
        self.langEdit.setGeometry(QtCore.QRect(10, 330, 113, 27))
        self.langEdit.setObjectName("langEdit")
        self.folderEdit = QtWidgets.QLineEdit(languagesDialog)
        self.folderEdit.setGeometry(QtCore.QRect(130, 330, 231, 27))
        self.folderEdit.setReadOnly(True)
        self.folderEdit.setObjectName("folderEdit")
        self.horizontalLayoutWidget = QtWidgets.QWidget(languagesDialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 360, 401, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.addButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.addButton.setObjectName("addButton")
        self.horizontalLayout_4.addWidget(self.addButton)
        self.removeButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.removeButton.setObjectName("removeButton")
        self.horizontalLayout_4.addWidget(self.removeButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(languagesDialog)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 299, 401, 31))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label.setObjectName("label")
        self.horizontalLayout_5.addWidget(self.label)
        spacerItem2 = QtWidgets.QSpacerItem(16, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_5.addWidget(self.label_2)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)

        self.retranslateUi(languagesDialog)
        QtCore.QMetaObject.connectSlotsByName(languagesDialog)
        languagesDialog.setTabOrder(self.removeButton, self.addButton)
        languagesDialog.setTabOrder(self.addButton, self.languagesTable)

    def retranslateUi(self, languagesDialog):
        _translate = QtCore.QCoreApplication.translate
        languagesDialog.setWindowTitle(_translate("languagesDialog", "Languages"))
        item = self.languagesTable.horizontalHeaderItem(0)
        item.setText(_translate("languagesDialog", "Language"))
        item = self.languagesTable.horizontalHeaderItem(1)
        item.setText(_translate("languagesDialog", "Folder"))
        self.folderButton.setText(_translate("languagesDialog", "..."))
        self.addButton.setText(_translate("languagesDialog", "Add Language"))
        self.removeButton.setText(_translate("languagesDialog", "Remove Language"))
        self.label.setText(_translate("languagesDialog", "New language"))
        self.label_2.setText(_translate("languagesDialog", "Folder"))

