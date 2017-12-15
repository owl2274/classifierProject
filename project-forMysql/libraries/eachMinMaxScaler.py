import numpy as np
from sklearn.preprocessing import MinMaxScaler

class EachMinMaxScaler():
    def __init__(self,scaleList):

        self.scalerList = scaleList
    def fit_transform(self,dataSet):
        transformedDataSet=np.copy(dataSet)


        for i,scaleSize in enumerate(self.scalerList):

            if scaleSize == 0:
                transformedDataSet[:,i] = np.zeros_like(transformedDataSet[:,i])
            else:
                transformedDataSet[:,i] = MinMaxScaler(feature_range=(0,scaleSize)).fit_transform(transformedDataSet[:,i].reshape(-1,1)).reshape(1,-1)
        return transformedDataSet
