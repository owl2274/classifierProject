from libraries.nonGuidePipe import chain
import libraries.lol_database as lol_database
from libraries.lol_api import LOLApi
from libraries.eachMinMaxScaler import EachMinMaxScaler
from sklearn.decomposition import PCA
import numpy as np
from sklearn.preprocessing import MinMaxScaler,RobustScaler,StandardScaler,Normalizer
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans,AgglomerativeClustering,DBSCAN
import matplotlib.pyplot as plt
import random

import csv

class appCore():
    def __init__(self):


        self.needPreprocess = True
        self.needSolveAverage = True

        self.data_feature_names = ['kills', 'deaths', 'assists', 'totalMinionsKilled', 'goldEarned', 'timeCCingOthers',
                          'totalDamageDealtToChampions', 'totalDamageTaken', 'visionScore', 'mostUsableSpell',
                          'secondUsableSpell', 'thirdUsableSpell']
        self.__preprocessData__()
        random.seed(0)

    def saveImage(self,path):
        plt.savefig(path)

    def getFigure(self):
        return plt.figure(figsize=(13,13))

    def getFeatureNames(self):
        return self.data_feature_names
    def getFeatureForScale(self):
        return self.data_feature_names[0:-3]+["spell"]

    def adjustFeatureScale(self,scaleList):
        self.scaleList = scaleList
        spellFeatureLen = len(self.theFinalFeature)-len(self.data_feature_names[0:-3])
        self.scaleList = self.scaleList[0:-1] + [self.scaleList[-1]]*spellFeatureLen
    def __preprocessData__(self):
        if self.needPreprocess == True:
            with open("dataOfAverage.csv","rt") as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                data = []
                for row in reader:
                    data.append(row)
                self.theFinalFeature = data[0][1:]
                data = np.array(data[1:])
                self.championNameList = data[:,0].tolist()
                self.theFinalData = data[:,1:].astype(np.float64)
            with open("spellNameList.csv","rt") as csvfile:
                reader = csv.reader(csvfile,delimiter=',')
                data = []
                for row in reader:
                    data.append(row)
                self.spellNameList = data[1:]
            self.needPreprocess = False





    def classifierData(self,pipelineDict):

        self.__preprocessData__()
        if pipelineDict["scaler"] == "MinMaxScaler":
            scaler = EachMinMaxScaler(self.scaleList)
        elif pipelineDict["scaler"] == "RobustScaler":
            scaler = RobustScaler()
        elif pipelineDict["scaler"] == "Normalizer":
            scaler = Normalizer()
        elif pipelineDict["scaler"] == "StandardScaler":
            scaler = StandardScaler()
        elif pipelineDict["scaler"] == "None":
            scaler = None
        else:
            raise TypeError

        if pipelineDict["reduceDim"] == "TSNE":
            reduceDimension = TSNE(random_state=0)
        elif pipelineDict["reduceDim"] == "PCA":
            reduceDimension = PCA(n_components=2)
        elif pipelineDict["reduceDim"] == "None":
            reduceDimension = None
        else:
            raise TypeError

        if pipelineDict["cluster"] == "DBSCAN":
            eps = pipelineDict["params"]["eps"]
            min_samples = pipelineDict["params"]["min_samples"]
            cluster = DBSCAN(eps=float(eps),min_samples=int(min_samples))
        else:
            if pipelineDict["cluster"] == "KMeans":
                n_clusters = pipelineDict["params"]["n_clusters"]
                cluster = KMeans(n_clusters=int(n_clusters))
            elif pipelineDict["cluster"] == "Agglomerative":
                n_clusters = pipelineDict["params"]["n_clusters"]
                cluster = AgglomerativeClustering(n_clusters=int(n_clusters))
            else:
                raise TypeError

        pipe = chain([("scaler", scaler), ("reduceDim",reduceDimension),
                      ("cluster", cluster)])


        labels = pipe.fit_predict(self.theFinalData)

        eachScaledData = pipe.named_steps("scaler_output")


        cluster = pipe.named_steps("cluster")

        championClusters = []
        spellClusters = []
        try:
            for index in range(cluster.n_clusters):
                championClusters.append([])
                spellClusters.append([])
        except AttributeError:
            maxLabel = 0
            for label in labels:
                if label > maxLabel:
                    maxLabel = label
            for index in range(maxLabel + 2):
                championClusters.append([])
                spellClusters.append([])

        labels.tolist()
        for i, label in enumerate(labels.tolist()):
            tableData = []
            tableData.append(self.championNameList[i])
            tableData.extend(self.theFinalData[i][0:len(self.data_feature_names[0:-3])])
            tableData.extend(self.spellNameList[i])
            championClusters[label].append(tableData)
            spellClusters[label].append(self.spellNameList[i])

        dim2Output = pipe.named_steps("reduceDim_output")
        try:
            if dim2Output == None:
                reduceDimension = TSNE(random_state=0)
                scaledData = pipe.named_steps("scaler_output")
                try:
                    if scaledData == None:
                        scaledData = self.theFinalData
                except ValueError:
                    pass
                finally:
                    dim2Output = reduceDimension.fit_transform(scaledData)
        except ValueError:
            pass





        plt.clf()
        plt.xlim(dim2Output[:, 0].min(), dim2Output[:, 0].max() + 1)
        plt.ylim(dim2Output[:, 1].min(), dim2Output[:, 1].max() + 1)

        colors = []
        for _ in championClusters:
            rgbValue = random.randrange(0,16777216-1)
            rgbValue = "%X"%(rgbValue)
            rgbString = ""
            for _ in range(6-len(rgbValue)):
                rgbString = "0"+rgbString
            rgbString = "#"+ rgbString + rgbValue
            colors.append(rgbString)
        colors[-1]="#000000"


        for i in range(len(dim2Output)):
            plt.text(dim2Output[i, 0], dim2Output[i, 1], str(self.championNameList[i]), color=colors[labels[i]])
        return championClusters







if __name__ == "__main__":
    app = appCore()
