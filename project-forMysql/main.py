from PyQt5.QtWidgets import QApplication,QFileDialog,QMainWindow,QTableWidgetItem



import appCore as ac

from interface.classifierInterface import Ui_classifierInterface
from interface.mysqlDialog import mysqlDialog
from interface.scalerDialog import scalerDialog
from interface.apiDialog import apiDialog
import sys

from matplotlib.pyplot import figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import matplotlib.pyplot as plt
fig = plt.Figure()
canvas = FigureCanvas(fig)

class classifierApp(QMainWindow,Ui_classifierInterface):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.mysqlDialog = mysqlDialog()
        self.apiDialog = apiDialog()

        self.appCore = ac.appCore()
        self.scalerDialog = scalerDialog(self.appCore.getFeatureForScale())

        self.connectNewMysql()
        self.connectApi()


        self.fig = self.appCore.getFigure()
        self.canvas = FigureCanvas(self.fig)
        self.visualizationField.addWidget(self.canvas)

        self.feature_names = self.appCore.getFeatureNames()
        self.tableHeaderLabels = ['champion']
        self.tableHeaderLabels.extend(self.feature_names)
        self.tableWidget.setRowCount(138)
        self.tableWidget.setColumnCount(len(self.tableHeaderLabels))
        self.tableWidget.setHorizontalHeaderLabels(self.tableHeaderLabels)

        self.clusterComboBox.currentIndexChanged.connect(self.changeInputLayout)
        self.classifyPushButton.clicked.connect(self.classifierData)

        self.actionCollect_and_stuff_data.triggered.connect(self.collectData)
        self.actionSolveAverageValues.triggered.connect(self.solveAverage)
        self.actionSaveImage.triggered.connect(self.saveImage)
        self.actionSaveClusters.triggered.connect(self.saveClusters)
        self.actionScaleSize.triggered.connect(self.scalerDialog.show)
        self.actionMysql.triggered.connect(self.mysqlDialog.show)
        self.actionApi.triggered.connect(self.apiDialog.show)
        self.scalerDialog.okButton.clicked.connect(self.adjustFeatureScale)
        self.mysqlDialog.okButton.clicked.connect(self.connectNewMysql)
        self.apiDialog.okButton.clicked.connect(self.connectApi)

        self.stateTextEdit.setReadOnly(True)
        self.clusterComboBox.setCurrentIndex(1)



    def connectNewMysql(self):
        mysqlServer = self.mysqlDialog.serverLineEdit.text()
        user = self.mysqlDialog.userLineEdit.text()
        passwd = self.mysqlDialog.passwordLineEdit.text()
        self.appCore.connectNewMysql(mysqlServer,user,passwd)
        self.stateTextEdit.append(self.appCore.message)
        self.adjustFeatureScale()


    def connectApi(self):
        key = self.apiDialog.keyLineEdit.text()
        apiServer = self.apiDialog.serverLineEdit.text()
        baseUrl = self.apiDialog.baseUrlLineEdit.text()
        self.appCore.connectApi(key, apiServer, baseUrl)
        self.stateTextEdit.append(self.appCore.message)

    def collectData(self):
        path = QFileDialog.getOpenFileName()
        self.appCore.collectAndStuff(path[0])

        self.stateTextEdit.append(self.appCore.message)

    def saveImage(self):
        path = QFileDialog.getSaveFileName()
        self.appCore.saveImage(path[0])
    def adjustFeatureScale(self):
        scaleList = []
        try:
            for i in range(len(self.appCore.getFeatureForScale())):
                scaleList.append(float(self.scalerDialog.lineEdit[i].text()))
        except ValueError:
            self.stateTextEdit.append("invalid value")
            return
        self.appCore.adjustFeatureScale(scaleList)
    def saveClusters(self):
        path = QFileDialog.getSaveFileName()
        clusters=[]
        clusters.append(self.tableHeaderLabels)
        clusters.append([])
        for cluster in self.championClusters:
            for championData in cluster:
                clusters.append(championData)
            clusters.append([])
    def solveAverage(self):
        self.appCore.solveAverage()
        self.stateTextEdit.append(self.appCore.message)

    def classifierData(self):
        scalerName = self.scalerComboBox.currentText()
        clusterName = self.clusterComboBox.currentText()
        reduceDimName = self.reduceDimComboBox.currentText()

        try:
            if clusterName == "DBSCAN":
                eps = float(self.epsLineEdit.text())
                min_samples = int(self.min_samplesLineEdit.text())
                params = {"eps": eps, "min_samples": min_samples}

            else:
                n_clusters = int(self.n_clusterLineEdit.text())
                params = {"n_clusters": n_clusters}
        except ValueError:
            self.stateTextEdit.append("invalid value")
            return
        pipeline = {"scaler": scalerName, "reduceDim": reduceDimName, "cluster": clusterName, "params": params}

        championClusters = self.appCore.classifierData(pipeline)
        if championClusters == []:
            self.stateTextEdit.append(self.appCore.message)
            return
        self.canvas.draw()

        self.tableWidget.setRowCount(138+len(championClusters)*2)
        i = j = 0
        for cluster in championClusters:
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
    app.exec_()
