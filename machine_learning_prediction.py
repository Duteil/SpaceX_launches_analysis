# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 03:29:37 2022

@author: Mathieu Duteil

Trains various models with a range of hyperparameters 
to get a good predictor for the success of a launch.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier    

def plot_confusion_matrix(y,y_predict):
    "this function plots the confusion matrix"
    from sklearn.metrics import confusion_matrix

    cm = confusion_matrix(y, y_predict)
    ax= plt.subplot()
    sns.heatmap(cm, annot=True, ax = ax); #annot=True to annotate cells
    ax.set_xlabel('Predicted labels')
    ax.set_ylabel('True labels')
    ax.set_title('Confusion Matrix'); 
    ax.xaxis.set_ticklabels(['did not land', 'land']); ax.yaxis.set_ticklabels(['did not land', 'landed'])
    
# Preparing the data set:
data = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv")    
X = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_3.csv')
y = X['Class']
X.drop(['Class'], axis=1, inplace=True)
X = preprocessing.StandardScaler().fit_transform(X)

# splitting the data set:
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

models_scores = dict()

# finding the best model and training it:
parameters ={'C':[0.01,0.1,1],
             'penalty':['l2'], # l1 lasso l2 ridge
             'solver':['lbfgs']}
lr = LogisticRegression()
logreg_cv = GridSearchCV(lr, parameters, cv=10)
logreg_cv.fit(X_train, y_train)
logreg_cv.best_estimator_
scores = logreg_cv.cv_results_
print("tuned hyperparameters :(best parameters) ",logreg_cv.best_params_)
print("accuracy :",logreg_cv.best_score_)
models_scores['lr'] = logreg_cv.score(X_test, y_test)

# Confusion matrix:
yhat=logreg_cv.predict(X_test)
plot_confusion_matrix(y_test,yhat)

# Trying again with a SVM model:
parameters = {'kernel':('linear', 'rbf','poly','rbf', 'sigmoid'),
              'C': np.logspace(-3, 3, 5),
              'gamma':np.logspace(-3, 3, 5)}
svm = SVC()
svm_cv = GridSearchCV(svm, parameters, cv=10)
svm_cv.fit(X_train, y_train)
print("tuned hpyerparameters :(best parameters) ",svm_cv.best_params_)
print("accuracy :",svm_cv.best_score_)
models_scores['svm'] = svm_cv.score(X_test, y_test)

# Confusion matrix:
yhat=svm_cv.predict(X_test)
plot_confusion_matrix(y_test,yhat)

# Again with a decision tree classifier:
parameters = {'criterion': ['gini', 'entropy'],
     'splitter': ['best', 'random'],
     'max_depth': [2*n for n in range(1,10)],
     'max_features': ['auto', 'sqrt'],
     'min_samples_leaf': [1, 2, 4],
     'min_samples_split': [2, 5, 10]}
tree = DecisionTreeClassifier()
tree_cv = GridSearchCV(tree, parameters, cv=10)
tree_cv.fit(X_train, y_train)
print("tuned hpyerparameters :(best parameters) ",tree_cv.best_params_)
print("accuracy :",tree_cv.best_score_)
models_scores['tree'] = tree_cv.score(X_test, y_test)

# Confusion matrix:
yhat=tree_cv.predict(X_test)
plot_confusion_matrix(y_test,yhat)

# Next model to try is KNN:
parameters = {'n_neighbors': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
              'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
              'p': [1,2]}
KNN = KNeighborsClassifier()
knn_cv = GridSearchCV(tree, parameters, cv=10)
knn_cv.fit(X_train, y_train)
print("tuned hpyerparameters :(best parameters) ",knn_cv.best_params_)
print("accuracy :",knn_cv.best_score_)
models_scores['knn'] = knn_cv.score(X_test, y_test)

# Confusion matrix:
yhat = knn_cv.predict(X_test)
plot_confusion_matrix(y_test,yhat)

plt.bar(list(models_scores.keys()), models_scores.values(), color='g')
plt.ylim([0.75, 0.90])
plt.title("Scores of the different models")
plt.show()


