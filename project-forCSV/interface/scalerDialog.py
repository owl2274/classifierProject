from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog,QApplication


import sys
import time

class scalerDialog(QDialog):
    def __init__(self,featureList):

        self.featureList = featureList
        self.featureLayout = []
        self.label = []
        self.lineEdit = []
        QDialog.__init__(self)
        self.setupUi(self)
    def setupUi(self, scalerDialog):
        scalerDialog.setObjectName("scalerDialog")
        scalerDialog.resize(322, 428)
        self.widget = QtWidgets.QWidget(scalerDialog)
        self.widget.setGeometry(QtCore.QRect(20, 10, 263, 332))
        self.widget.setObjectName("widget")
        self.scalerDialogLayout = QtWidgets.QVBoxLayout(self.widget)
        self.scalerDialogLayout.setContentsMargins(0, 0, 0, 0)
        self.scalerDialogLayout.setObjectName("featureLayout")

        for i, featureName in enumerate(self.featureList):
            self.featureLayout.append(QtWidgets.QHBoxLayout())
            self.featureLayout[i].setObjectName("horizontalLayout")
            self.label.append(QtWidgets.QLabel(self.widget))
            self.label[i].setObjectName(featureName + "FeatureLabel")
            self.featureLayout[i].addWidget(self.label[i])
            self.lineEdit.append(QtWidgets.QLineEdit(self.widget))
            self.lineEdit[i].setObjectName(featureName + "FeatureLineEdit")
            self.lineEdit[i].setText("1.0")
            self.featureLayout[i].addWidget(self.lineEdit[i])
            self.scalerDialogLayout.addLayout(self.featureLayout[i])

        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.buttonLayout.setObjectName("buttonLayout")
        self.okButton = QtWidgets.QPushButton(self.widget)
        self.okButton.setObjectName("okButton")
        self.buttonLayout.addWidget(self.okButton)
        self.cancelButton = QtWidgets.QPushButton(self.widget)
        self.cancelButton.setObjectName("cancelButton")
        self.buttonLayout.addWidget(self.cancelButton)
        self.scalerDialogLayout.addLayout(self.buttonLayout)

        self.retranslateUi(scalerDialog)
        QtCore.QMetaObject.connectSlotsByName(scalerDialog)

    def retranslateUi(self, scalerDialog):
        _translate = QtCore.QCoreApplication.translate
        scalerDialog.setWindowTitle(_translate("scalerDialog", "Dialog"))

        for i, featureName in enumerate(self.featureList):
            self.label[i].setText(_translate("scalerDialog", featureName))

        self.okButton.setText(_translate("scalerDialog", "Ok"))
        self.cancelButton.setText(_translate("scalerDialog", "Cancel"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    interface = scalerDialog(["Hello?","fucking world!"])
    interface.show()
    app.exec_()