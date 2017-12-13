from sklearn.pipeline import make_pipeline,Pipeline
from sklearn.preprocessing import MinMaxScaler,StandardScaler,RobustScaler,Normalizer

from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn.datasets import load_breast_cancer

from sklearn.cluster import KMeans,AgglomerativeClustering,DBSCAN
from sklearn.svm import SVC

from sklearn.metrics.cluster import adjusted_rand_score
from sklearn.metrics import accuracy_score,roc_auc_score
import numpy as np


from sklearn.utils import tosequence
from sklearn.utils import Bunch
class chain():
    def __init__(self,steps):

        self.steps = steps
       # print(self.steps)
    def fit_predict(self, X):
        X_transformed = X
        self.transformOutputSteps = []
        for name,estimator in self.steps[:-1]:
            if estimator == None:
                self.transformOutputSteps.append(None)
                continue
            X_transformed = estimator.fit_transform(X_transformed)
            self.transformOutputSteps.append(X_transformed)
        X_transformed = self.steps[-1][1].fit_predict(X_transformed)
        self.transformOutputSteps.append(X_transformed)
        return X_transformed





    def named_steps(self,name):
        # Use Bunch object to improve autocomplete
        for i,(fname,step) in enumerate(self.steps):
            if fname == name:
                return step
            elif (fname+"_output") == name:

                return self.transformOutputSteps[i]


if __name__ == "__main__":
    cancer = load_breast_cancer()

    pipe = chain([("scaler",MinMaxScaler()),("tsne",TSNE(random_state=42)),("cluster",KMeans(n_clusters=2))])






    predict_label = pipe.fit_predict(cancer.data)
    print(predict_label)
    nonguide_ml_label = predict_label == 0
    answer_label = cancer.target == 1

    print("총 샘플 갯수: {}".format(len(cancer.data)))
    print("머신러닝 추측 결과")
    print("    양성 판정 샘플 갯수: {}".format((nonguide_ml_label != True).sum()))
    print("    악성 판정 샘플 갯수: {}".format(nonguide_ml_label.sum()))
    print("실제 판정 결과")
    print("    양성 판정 샘플 갯수: {}".format((answer_label != True).sum()))
    print("    악성 판정 샘플 갯수: {}".format(answer_label.sum()))
    print("틀린 갯수: {}".format((nonguide_ml_label != answer_label).sum()))


    print("정답 확률: {}%".format(accuracy_score(nonguide_ml_label,answer_label)))
    print("")
    print("ARI: {}".format(adjusted_rand_score(nonguide_ml_label,answer_label)))
    print("AUC: {}".format(roc_auc_score(answer_label,nonguide_ml_label)))