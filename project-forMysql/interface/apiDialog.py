# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'apiDialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog,QApplication
import sys

class apiDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.baseUrlLineEdit.setText("https://{}.api.riotgames.com/lol")
        self.serverLineEdit.setText("kr")
        self.setWindowTitle("setup api")

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(379, 237)
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 361, 211))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.keyLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.keyLabel.setObjectName("keyLabel")
        self.horizontalLayout.addWidget(self.keyLabel)
        self.keyLineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.keyLineEdit.setObjectName("keyLineEdit")
        self.horizontalLayout.addWidget(self.keyLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.serverLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.serverLabel.setObjectName("serverLabel")
        self.horizontalLayout_2.addWidget(self.serverLabel)
        self.serverLineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.serverLineEdit.setObjectName("serverLineEdit")
        self.horizontalLayout_2.addWidget(self.serverLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.baseUrlLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.baseUrlLabel.setObjectName("baseUrlLabel")
        self.horizontalLayout_3.addWidget(self.baseUrlLabel)
        self.baseUrlLineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.baseUrlLineEdit.setObjectName("baseUrlLineEdit")
        self.horizontalLayout_3.addWidget(self.baseUrlLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.okButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.okButton.setObjectName("okButton")
        self.horizontalLayout_4.addWidget(self.okButton)
        self.cancelButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout_4.addWidget(self.cancelButton)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.keyLabel.setText(_translate("Dialog", "key:"))
        self.serverLabel.setText(_translate("Dialog", "server:"))
        self.baseUrlLabel.setText(_translate("Dialog", "baseUrl:"))
        self.okButton.setText(_translate("Dialog", "ok"))
        self.cancelButton.setText(_translate("Dialog", "cancel"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    interface = apiDialog()
    interface.show()
    app.exec_()