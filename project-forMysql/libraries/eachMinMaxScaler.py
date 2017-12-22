import numpy as np
from sklearn.preprocessing import MinMaxScaler

class EachMinMaxScaler():
    def __init__(self,scaleList):
        self.scalerList = scaleList

    def fit_transform(self,dataSet):
        transformedDataSet = MinMaxScaler().fit_transform(np.copy(dataSet))
        transformedDataSet = transformedDataSet * self.scalerList
        return transformedDataSet
