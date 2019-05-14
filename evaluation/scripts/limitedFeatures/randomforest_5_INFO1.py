# required for evaluation on Pantora
import matplotlib
matplotlib.use('Agg')

import sys
# Add the ptdraft folder path to the sys.path list
sys.path.append('/home/pkoch/FaultPrediction')

import lib.data as data
import lib.core as core
import lib.plot as plot
import lib.result as result
import numpy as np

from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import RandomOverSampler
from imblearn.pipeline import Pipeline
from sklearn.metrics import precision_score, recall_score

core.hideWarnings()

def GSandCVforEnsembleClassifier(dataset, model, param_grid, exportPath, exportName, scoring=None, sampler=None):

    scaler = StandardScaler()
    if sampler == None:
        sampler = RandomOverSampler()
    #model = core.ThresholdClassifier()
    pipeline = Pipeline(steps=[('1', scaler),
                               ('2', sampler),
                               ('3', model)])

    #define scoring for cross-validatoin

    if scoring == None:
        scoring = [precision_score, recall_score]

    #gridsearch optimization & cv on dataset
    res, estimator = core.compareMetricEnsembleCategorizationPerformance(dataset, pipeline, param_grid, model, scoring)

    print(res)

    #export result data and estimator info

    result.export(res, exportPath + "/" + exportName + ".json")
    result.writeCSV(res, exportPath + "/" + exportName + ".csv")
    result.exportEstimatorInfo([estimator], exportPath + "/" + exportName + "_estimator.txt")


#TEST SCRIPT FOR SMALL DATASET
#analyze SMALL metrics using threshold and voting classifiers

#SMALL
#dataPath = '../metric_data/ENRON_errors_2017-08-01T15-41/cells_small.csv'
#dataName = 'SMALL'

#ENRON
enronPath = '../../../metric_data/journal_2017-12-07/enron.csv'
enronName = 'ENRON'

#INFO1
info1Path = '../../../metric_data/journal_2017-12-07/info1.csv'
info1Name = 'INFO1'

#EUSES
eusesPath = '../../../metric_data/journal_2017-12-07/euses.csv'
eusesName = 'EUSES'

#get data
dataset = data.getData(info1Path, info1Name)

#extract important features
featureIndices = [39,42,0,9,52]
dataset.X = dataset.X[:,featureIndices]

from sklearn.ensemble import RandomForestClassifier

random_state = 42
model = RandomForestClassifier(random_state = random_state)

#build param grid for grid search
param_grid = {"3__criterion" : ["gini", "entropy"],
              "3__n_estimators": [1, 5, 10, 25, 50]
             }

exportPath = "../../../results/2019-04/limitedFeatures"
exportName = "randomforest_5_"+dataset.name

GSandCVforEnsembleClassifier(dataset, model, param_grid, exportPath, exportName)