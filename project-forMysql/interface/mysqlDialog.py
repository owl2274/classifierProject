# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mysqlDialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog,QApplication
import sys
class mysqlDialog(QDialog):
    def __init__(self):

        QDialog.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("setup mysql")
        self.serverLineEdit.setText("127.0.0.1")
        self.userLineEdit.setText("root")
        self.passwordLineEdit.setText("13252122")
    def setupUi(self, mysqlDialog):
        mysqlDialog.setObjectName("mysqlDialog")
        mysqlDialog.resize(306, 242)
        self.verticalLayoutWidget = QtWidgets.QWidget(mysqlDialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 291, 221))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.serverLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.serverLabel.setObjectName("serverLabel")
        self.horizontalLayout.addWidget(self.serverLabel)
        self.serverLineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.serverLineEdit.setObjectName("serverLineEdit")
        self.horizontalLayout.addWidget(self.serverLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.userLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.userLabel.setObjectName("userLabel")
        self.horizontalLayout_2.addWidget(self.userLabel)
        self.userLineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.userLineEdit.setObjectName("userLineEdit")
        self.horizontalLayout_2.addWidget(self.userLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.passwordLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.passwordLabel.setObjectName("passwordLabel")
        self.horizontalLayout_3.addWidget(self.passwordLabel)
        self.passwordLineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.passwordLineEdit.setObjectName("passwordLineEdit")
        self.horizontalLayout_3.addWidget(self.passwordLineEdit)
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
        self.verticalLayoutWidget.raise_()
        self.serverLabel.raise_()

        self.retranslateUi(mysqlDialog)
        QtCore.QMetaObject.connectSlotsByName(mysqlDialog)

    def retranslateUi(self, mysqlDialog):
        _translate = QtCore.QCoreApplication.translate
        mysqlDialog.setWindowTitle(_translate("mysqlDialog", "Dialog"))
        self.serverLabel.setText(_translate("mysqlDialog", "server:"))
        self.userLabel.setText(_translate("mysqlDialog", "user:"))
        self.passwordLabel.setText(_translate("mysqlDialog", "password:"))
        self.okButton.setText(_translate("mysqlDialog", "OK"))
        self.cancelButton.setText(_translate("mysqlDialog", "cancel"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    interface = mysqlDialog()
    interface.show()
    app.exec_()