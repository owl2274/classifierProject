from libraries.pipeForUnsupervised import chain
from libraries.lol_database import LOLDatabase
from libraries.lol_api import LOLApi
from libraries.eachMinMaxScaler import EachMinMaxScaler

from sklearn.preprocessing import MinMaxScaler,RobustScaler,StandardScaler,Normalizer
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans,AgglomerativeClustering,DBSCAN

import numpy as np
import time

import matplotlib.pyplot as plt
import random


class appCore():
    def __init__(self):

        self.data_feature_names = ['kills', 'deaths', 'assists', 'totalMinionsKilled', 'goldEarned', 'timeCCingOthers',
                                   'totalDamageDealtToChampions', 'totalDamageTaken', 'visionScore', 'mostUsableSpell',
                                   'secondUsableSpell', 'thirdUsableSpell']
        self.needPreprocess = True
        self.isConnectedMysql = False
        self.isConnectedApi = False
        self.lol_api = None
        self.database = None
        self.message = ""

        random.seed(0)

    def connectApi(self,key,server="kr",base_url = "https://{}.api.riotgames.com/lol"):
        lol_api = self.lol_api

        try:
            self.lol_api = LOLApi(key,server,base_url)
            self.lol_api.test()
            self.message = "Api is correct"
            self.isConnectedApi = True
        except:
            self.lol_api = lol_api
            self.message = "Api is incorrect"

        return self.isConnectedApi

    def connectNewMysql(self,mysqlServer,mysqlUser,mysqlPasswd):
        database = self.database

        try:
            self.database = LOLDatabase(host=mysqlServer, user=mysqlUser, passwd=mysqlPasswd)
            self.database.useDatabase()
            self.__preprocessData__()
            self.message = "Mysql is correct"
            self.isConnectedMysql = True
        except:
            self.database = database
            self.message = "Mysql is incorrect"

        return self.isConnectedMysql

    def saveImage(self,path):
        plt.savefig(path)

    def getFigure(self):
        return plt.figure(figsize=(13,13))

    def getFeatureNames(self):
        return self.data_feature_names

    def getFeatureForScale(self):
        return self.data_feature_names[0:-3]+["spell"]

    def adjustFeatureScale(self,scaleList):
        if self.needPreprocess == False:
            self.scaleList = scaleList
            spellFeatureLen = len(self.theFinalFeature)-len(self.data_feature_names[0:-3])
            self.scaleList = self.scaleList[0:-1] + [self.scaleList[-1]]*spellFeatureLen
        else:
            self.message = "Preprocess is not done"

    def __preprocessData__(self):
        if self.needPreprocess == True:
            choosedata = ""
            for s in self.data_feature_names:
                choosedata += s + ","
            choosedata = choosedata[0:-1]
            championData = np.array(self.database.showChmpionAverage(choosedata="championId," + choosedata))

            #championList = self.database.showChampionId()
            self.championNameList = []
            for i in championData[:, 0]:
                name = self.database.showChampionId(championId=i.astype(int), choosedata='championName')
                self.championNameList.append(name[0][0])

            self.spellNameList = []
            for spell1, spell2,spell3 in zip(championData[:, -3],championData[:, -2], championData[:, -1]):
                mostSpell = self.database.showSummonerSpell(spellId=spell1)
                secondSpell = self.database.showSummonerSpell(spellId=spell2)
                thirdSpell = self.database.showSummonerSpell(spellId=spell3)
                self.spellNameList.append((mostSpell[0][1], secondSpell[0][1],thirdSpell[0][1]))

            spellids = self.database.showSummonerSpell()

            spelldata = []

            spellNameList = []
            spellIDList = []
            for spellid in spellids:
                spellIDList.append(spellid[0])
                spellNameList.append(spellid[1])
#######################################################################################
            for rowindex in range(len(championData[:, 0])):
                spellPrefer = []
                for n in spellIDList:
                    spellPrefer.append(0)
                for point, column in enumerate(championData[rowindex][10:13]):
                    for j, id in enumerate(spellIDList):
                        if column == id:
                            spellPrefer[j] = (3 - point)

                spelldata.append(spellPrefer)

            spellNPdata = np.array(spelldata)
#######################위 부분은 범주형 특성인 스펠을 연속형 특성으로 바꾸기 위한 처리 과정입니다.

            self.championData = championData[:, 1:-3]
            self.theFinalData = np.concatenate((self.championData, spellNPdata), axis=1)#최종적으로 분류기에 들어가게 될 데이터
            self.theFinalFeature = self.data_feature_names[0:-3] + spellNameList#최종데이터의 특성목록-'mostUsableSpell','secondUsableSpell','thirdUsableSpell' 이 세 특성이 각 스펠의 이름으로 바뀌었다.

            self.needPreprocess = False

    def classifierData(self,pipelineDict):
        if self.isConnectedMysql == True:
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
            try:
                for index in range(cluster.n_clusters):
                    championClusters.append([])
            except AttributeError:
                maxLabel = 0
                for label in labels:
                    if label > maxLabel:
                        maxLabel = label
                for index in range(maxLabel + 2):
                    championClusters.append([])

            labels.tolist()
            for i, label in enumerate(labels.tolist()):
                tableData = []
                tableData.append(self.championNameList[i])
                tableData.extend(self.championData[i].tolist())
                tableData.extend(self.spellNameList[i])
                championClusters[label].append(tableData)


            dim2Output = pipe.named_steps("reduceDim_output")
            try:#
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
        else:
            self.message = "need Connecting mysql"
            return []

    def solveAverage(self):
        if self.isConnectedMysql == True:
            championList = self.database.showChampionId()

            rnlen = "{:.2f}"
            formatlist = ["kills: ", "deaths: ", "assists: ", "totalMinionsKilled: ", "goldEarned: ", "timeCCingOthers: ",
                          "totalDamageDealtToChampions: ", "totalDamageTaken: ", "visionScore: "]
            spellDict = {}
            spellCount = {}
            spellbase = self.database.showSummonerSpell()
            for spell in spellbase:
                spellDict[spell[0]] = spell[1]
                spellCount[spell[0]] = 0
            self.database.removeChampionAverage()
            for champion in championList:
                dataset = self.database.showIndividualGamer(championId=champion[0],
                                                       choosedata="kills,deaths,assists,totalMinionsKilled,goldEarned,timeCCingOthers,totalDamageDealtToChampions,totalDamageTaken,visionScore,gameDuration")
                spellset = self.database.showIndividualGamer(championId=champion[0], choosedata="spell1Id,spell2Id")

                dataAverage = np.zeros(12)
                for data, spell in zip(dataset, spellset):
                    dataAverage[0:-3] += np.array(data[0:-1]) / (data[-1] - 60) * 1800
                    try:
                        spellCount[spell[0]] = spellCount[spell[0]] + 1
                        spellCount[spell[1]] = spellCount[spell[1]] + 1
                    except KeyError:
                        pass
                maxSpell = 0
                nextmaxSpell = 0
                thirdmaxSpell = 0


                for i, key in enumerate(spellCount):
                    if i == 0:
                        rowkey = key
                    elif spellCount[key]<spellCount[rowkey]:
                        rowkey = key
                for i, key in enumerate(spellCount):
                    if i == 0:
                        maxSpell = rowkey
                        nextmaxSpell = rowkey
                        thirdmaxSpell = rowkey
                    else:
                        if spellCount[key] > spellCount[maxSpell]:
                            thirdmaxSpell = nextmaxSpell
                            nextmaxSpell = maxSpell
                            maxSpell = key
                        elif spellCount[key] > spellCount[nextmaxSpell]:
                            thirdmaxSpell = nextmaxSpell
                            nextmaxSpell = key
                        elif spellCount[key] > spellCount[thirdmaxSpell]:
                            thirdmaxSpell = key

                dataAverage = dataAverage / len(dataset)
                dataAverage[-3] = maxSpell
                dataAverage[-2] = nextmaxSpell
                dataAverage[-1] = thirdmaxSpell
                output = champion[1] + "  "
                for format, data in zip(formatlist, dataAverage):
                    output += format + rnlen.format(data) + ", "
                output += "\n    most usable spell: "

                for i in range(3):
                    output += spellDict[int(dataAverage[-(3 - i)])] + ", "


                self.database.insertChampionAverage(champion[0], dataAverage)


                for key in spellCount:
                    spellCount[key] = 0
            self.needPreprocess=True
            self.needSolveAverage = False
        else:
            self.message = "need Connecting Mysql"

    def collectAndStuff(self,summonerListPath):
        if self.isConnectedApi == True:
            with open(summonerListPath, "rt") as f:
                data = f.read()

            summonerList = data.split("\n")
            import pymysql

            for summoner in summonerList:
                if summoner == '':
                    continue
                summonerJson = self.lol_api.getSummoner(summoner)
                try:
                    self.database.insertSummoner(summonerJson)
                except KeyError as e:
                    print(e)
                time.sleep(1)

            summonerIdList = self.database.showSummoner(choosedata="accountId")

            for Id in summonerIdList:
                try:
                    matchList = self.lol_api.getMatchIDs(Id[0])
                    self.database.insertMatchID(matchList)
                except KeyError as e:
                    print(e)
                time.sleep(1)

            gameIdList = self.database.showMatchID(season=9, choosedata="gameId")
            for i,gameId in enumerate(gameIdList):
                try:
                    matchDetailList = self.lol_api.getMatchDetail(gameId[0])
                    self.database.insertIndividualGamer(matchDetailList)
                except KeyError as e:
                    print(e)
                time.sleep(1)

            keys = self.lol_api.getChampionId()
            self.database.insertChampionId(keys)

            spellList = self.lol_api.getSummonerSpell()
            self.database.insertSummonerSpell(spellList)
            self.needSolveAverage = True
            self.message = "CollecData is finished" + "\n"
        else:
            self.message = "need Connecting Api" + "\n"


if __name__ == "__main__":
    app = appCore()
    app.collectAndStuff("summonerList.txt")