from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from matplotlib.pyplot import figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import interface.classifierInterface as classifierInterface
import appCore as ac
import interface.scalerDialog as dialog
import sys
import csv
import time



import matplotlib.pyplot as plt
fig = plt.Figure()
canvas = FigureCanvas(fig)

class classifierApp(QMainWindow,classifierInterface.Ui_classifierInterface):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.appCore = ac.appCore()

        self.actionSaveImage.triggered.connect(self.saveImage)
        self.actionSaveClusters.triggered.connect(self.saveClusters)
        self.clusterComboBox.currentIndexChanged.connect(self.changeInputLayout)
        self.classifyPushButton.clicked.connect(self.classifierData)

        self.clusterComboBox.setCurrentIndex(1)
        self.fig = self.appCore.getFigure()
        self.canvas = FigureCanvas(self.fig)

        self.visualizaionField.addWidget(self.canvas)
        self.feature_names = self.appCore.getFeatureNames()
        self.tableHeaderLabels = ['champion']
        self.tableHeaderLabels.extend(self.feature_names)




        self.tableWidget.setRowCount(138)
        self.tableWidget.setColumnCount(len(self.tableHeaderLabels))

        self.tableWidget.setHorizontalHeaderLabels(self.tableHeaderLabels)
        self.scalerDialog = dialog.scalerDialog(self.appCore.getFeatureForScale())
        self.actionScaleSize.triggered.connect(self.scalerDialog.show)
        #self.adjustFeatureScale()
        self.scalerDialog.okButton.clicked.connect(self.adjustFeatureScale)

        self.adjustFeatureScale()
        self.stateTextEdit.setReadOnly(True)

    def saveImage(self):
        path = QFileDialog.getSaveFileName()
        self.appCore.saveImage(path[0])
    def saveClusters(self):
        path = QFileDialog.getSaveFileName()
        clusters=[]
        clusters.append(self.tableHeaderLabels)
        clusters.append([])
        for cluster in self.championClusters:
            for championData in cluster:
                clusters.append(championData)
            clusters.append([])

        with open(path[0], "wt", newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            dataset = []
            writer.writerows(clusters)

    def adjustFeatureScale(self):
        scaleList = []

        try:
            for i in range(len(self.appCore.getFeatureForScale())):
                scaleList.append(float(self.scalerDialog.lineEdit[i].text()))
        except ValueError:
            self.stateTextEdit.append("invalid value")
            return

        self.appCore.adjustFeatureScale(scaleList)

    def classifierData(self):
        scalerName = self.scalerComboBox.currentText()
        clusterName = self.clusterComboBox.currentText()
        reduceDimName = self.reduceDimComboBox.currentText()
        try:
            if clusterName == "DBSCAN":
                eps = float(self.epsLineEdit.text())
                min_samples = int(self.min_samplesLineEdit.text())
                params = {"eps":eps,"min_samples":min_samples}

            else:
                n_clusters = int(self.n_clusterLineEdit.text())
                params = {"n_clusters": n_clusters}
        except ValueError:
            self.stateTextEdit.append("invalid value")
            return
        pipeline = {"scaler": scalerName, "reduceDim": reduceDimName, "cluster": clusterName, "params": params}

        self.championClusters = self.appCore.classifierData(pipeline)

        self.canvas.draw()

        self.tableWidget.setRowCount(138+len(self.championClusters)*2)
        i = j = 0
        for cluster in self.championClusters:
            for championData in cluster:
                for data in championData:
                    self.tableWidget.setItem(i,j,QTableWidgetItem(str(data)+"  "))
                    j+=1
                i+=1
                j=0
            for k in range(len(self.feature_names)+1):
                self.tableWidget.setItem(i, k, QTableWidgetItem("      "))
                self.tableWidget.setItem(i+1, k, QTableWidgetItem("      "))
            i+=2







    def changeInputLayout(self):

        clusterName = self.clusterComboBox.currentText()

        if clusterName == "KMeans" or clusterName == "Agglomerative":
            self.epsLabel.hide()
            self.epsLineEdit.hide()
            self.min_samplesLabel.hide()
            self.min_samplesLineEdit.hide()
            self.n_clusterLabel.show()
            self.n_clusterLineEdit.show()
        elif clusterName == "DBSCAN":
            self.epsLabel.show()
            self.epsLineEdit.show()
            self.min_samplesLabel.show()
            self.min_samplesLineEdit.show()
            self.n_clusterLabel.hide()
            self.n_clusterLineEdit.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    interface = classifierApp()
    interface.show()
    #interface.scalerDialog.show()

    app.exec()

