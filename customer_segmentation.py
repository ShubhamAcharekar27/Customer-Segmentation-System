# -*- coding: utf-8 -*-
"""Customer Segmentation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QcPCjlS6DWGSyPsH7YYljEDXoCJy9JkC

## **Customer Segmentation**

# **Import Libraries**
"""

import numpy as np
import pandas as pd

import matplotlib.pyplot as py
import seaborn as sb

from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.metrics import silhouette_score

from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.cluster import AgglomerativeClustering
from sklearn.mixture import GaussianMixture

from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier

from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay, classification_report

"""# **Load Data**"""

traindt = pd.read_csv('Train.csv', index_col='ID')
trainCluster = traindt['Segmentation']
traindt.drop(['Segmentation'], axis=1, inplace=True)

testdt = pd.read_csv('Test.csv', index_col='ID')
testCluser = pd.read_csv('sample_submission.csv', index_col='ID')

"""# **Exploratory Data Analysis**"""

traindt.head(10)

traindt.info()

pd.DataFrame({'missing':traindt.isnull().sum(),
              'percentage':(traindt.isnull().sum() / np.shape(traindt)[0]) * 100})

traindt.describe()

(len(np.unique(traindt.Work_Experience)) - 1, len(np.unique(traindt.Family_Size)) - 1)

"""**Working with Features**"""

def plot_category(categorical, contenious= traindt.Age, target= trainCluster):
   rn: None


   sb.set_theme(style='ticks')
   py.figure(figsize=(10, 5))
   py.title("Count of each value in " + categorical.name)
   sb.countplot(x=categorical, hue=target); py.show()

   sb.set_theme(style='darkgrid')
   py.figure(figsize=(10, 5))
   py.title("Distribution of " + contenious.name + " based on " + categorical.name)
   sb.stripplot(x=categorical, y=contenious, hue=target); py.show()

   sb.set_theme(style='ticks')
   py.figure(figsize=(10, 5))
   py.title("Distribution of " + contenious.name + " based on " + categorical.name)
   sb.boxenplot(x=categorical, y=contenious, hue=target); py.show()

   pass

"""**Age**"""

sb.histplot(x=traindt['Age'], hue=trainCluster, bins=80)

pd.DataFrame(data=[trainCluster[(traindt['Age'] >= 35) & (traindt['Age'] <= 45)].value_counts(),
                   trainCluster[(traindt['Age'] >= 35) & (traindt['Age'] <= 45)].value_counts() / trainCluster[(traindt['Age'] >= 35) &
                   (traindt['Age'] <= 45)].value_counts().sum() * 100], index=['Segmentation', 'Percentage'])

"""**Gender**"""

pd.DataFrame(data=[(trainCluster[(traindt['Gender'] == 'Male')].value_counts()/ trainCluster.value_counts()) * 100,
                   (trainCluster[(traindt['Gender'] == 'Female')].value_counts()/ trainCluster.value_counts()) * 100],
             index=['Male', 'Female'])

plot_category(categorical=traindt.Gender)

"""**Ever Married**"""

pd.DataFrame(data=[(trainCluster[(traindt['Ever_Married'] == 'No')].value_counts()/ trainCluster.value_counts()) * 100,
                   (trainCluster[(traindt['Ever_Married'] == 'Yes')].value_counts()/ trainCluster.value_counts()) * 100],
             index=['Not Married', 'Married'])

plot_category(categorical=traindt.Ever_Married)

"""**Graduated**"""

pd.DataFrame(data=[(trainCluster[(traindt['Graduated'] == 'No')].value_counts()/ trainCluster.value_counts()) * 100,
                   (trainCluster[(traindt['Graduated'] == 'Yes')].value_counts()/ trainCluster.value_counts()) * 100],
             index=['Not Graduated', 'Graduated'])

plot_category(categorical=traindt.Graduated)

"""**Profession**"""

traindt.Profession.unique()

pd.DataFrame(data=[(trainCluster[(traindt['Profession'] == 'Healthcare')].value_counts()/ trainCluster.value_counts()) * 100,
                   (trainCluster[(traindt['Profession'] == 'Engineer')].value_counts()/ trainCluster.value_counts()) * 100,
                   (trainCluster[(traindt['Profession'] == 'Lawyer')].value_counts()/ trainCluster.value_counts()) * 100,
                   (trainCluster[(traindt['Profession'] == 'Entertainment')].value_counts()/ trainCluster.value_counts()) * 100,
                   (trainCluster[(traindt['Profession'] == 'Artist')].value_counts()/ trainCluster.value_counts()) * 100,
                   (trainCluster[(traindt['Profession'] == 'Executive')].value_counts()/ trainCluster.value_counts()) * 100,
                   (trainCluster[(traindt['Profession'] == 'Doctor')].value_counts()/ trainCluster.value_counts()) * 100,
                   (trainCluster[(traindt['Profession'] == 'Homemaker')].value_counts()/ trainCluster.value_counts()) * 100,
                   (trainCluster[(traindt['Profession'] == 'Marketing')].value_counts()/ trainCluster.value_counts()) * 100],
             index=traindt.Profession.unique()[:-1])

plot_category(categorical=traindt.Profession)

"""**Work Experience**"""

traindt.Work_Experience.unique()

"""**Spending Score**"""

traindt.Spending_Score.unique()

pd.DataFrame(data=[(trainCluster[(traindt['Spending_Score'] == 'Low')].value_counts()/ trainCluster.value_counts()) * 100,
                   (trainCluster[(traindt['Spending_Score'] == 'Average')].value_counts()/ trainCluster.value_counts()) * 100,
                   (trainCluster[(traindt['Spending_Score'] == 'High')].value_counts()/ trainCluster.value_counts()) * 100],
             index=traindt.Spending_Score.unique())

"""**Family Size**"""

traindt.Family_Size.unique()

plot_category(categorical=traindt.Family_Size)

"""**Var 1**"""

traindt.Var_1.unique()

"""# **Preprocessing**"""

traindt = traindt.loc[:, ['Ever_Married', 'Graduated', 'Profession', 'Spending_Score', 'Family_Size', 'Age']]
testdt = testdt.loc[:, ['Ever_Married', 'Graduated', 'Profession', 'Spending_Score', 'Family_Size', 'Age']]

traindt.head()

"""**Missing Values**"""

traindt.isnull().sum()

testdt.isnull().sum()

traindt.groupby(['Ever_Married']).Graduated.value_counts()

traindt.groupby(['Spending_Score']).Graduated.value_counts()

traindt['Graduated'][(traindt['Graduated'].isnull()) &  (traindt['Spending_Score'] == 'Average')] = 'Yes'
traindt['Graduated'][(traindt['Graduated'].isnull())] = 'No'

testdt['Graduated'][(testdt['Graduated'].isnull()) &  (testdt['Spending_Score'] == 'Average')] = 'Yes'
testdt['Graduated'][(testdt['Graduated'].isnull())] = 'No'

traindt.groupby(['Spending_Score']).Family_Size.value_counts()

traindt.groupby(['Ever_Married']).Family_Size.value_counts()

traindt['Family_Size'][(traindt['Family_Size'].isnull()) & (traindt['Spending_Score'] == 'High')] = 2
traindt['Family_Size'][(traindt['Family_Size'].isnull()) & (traindt['Ever_Married'] == 'Yes')] = 2
traindt['Family_Size'][(traindt['Family_Size'].isnull()) & (traindt['Spending_Score'] == 'Low')] = 1

testdt['Family_Size'][(testdt['Family_Size'].isnull()) & (testdt['Spending_Score'] == 'High')] = 2
testdt['Family_Size'][(testdt['Family_Size'].isnull()) & (testdt['Ever_Married'] == 'Yes')] = 2
testdt['Family_Size'][(testdt['Family_Size'].isnull()) & (testdt['Spending_Score'] == 'Low')] = 1

traindt.groupby(['Ever_Married']).Profession.value_counts()

traindt.groupby(['Spending_Score']).Profession.value_counts()

traindt['Profession'][(traindt['Profession'].isnull()) & ((traindt['Ever_Married'] == 'Yes') | (traindt['Spending_Score'] == 'Average'))] = 'Artist'
traindt['Profession'][(traindt['Profession'].isnull()) & (traindt['Ever_Married'] == 'No')] = 'Healthcare'
traindt['Profession'][(traindt['Profession'].isnull()) & (traindt['Spending_Score'] == 'High')] = 'Executive'

testdt['Profession'][(testdt['Profession'].isnull()) & ((testdt['Ever_Married'] == 'Yes') | (testdt['Spending_Score'] == 'Average'))] = 'Artist'
testdt['Profession'][(testdt['Profession'].isnull()) & (testdt['Ever_Married'] == 'No')] = 'Healthcare'
testdt['Profession'][(testdt['Profession'].isnull()) & (testdt['Spending_Score'] == 'High')] = 'Executive'

traindt['Ever_Married'].replace(np.nan, traindt['Ever_Married'].mode()[0], inplace=True)
testdt['Ever_Married'].replace(np.nan, testdt['Ever_Married'].mode()[0], inplace=True)

traindt.isnull().sum()

testdt.isnull().sum()

"""**Encodong**"""

traindt = pd.get_dummies(traindt, columns=['Ever_Married', 'Graduated', 'Profession'], drop_first=True)
traindt['Spending_Score'].replace(['Low', 'Average', 'High'], [0,1,2], inplace=True)

testdt = pd.get_dummies(testdt, columns=['Ever_Married', 'Graduated', 'Profession'], drop_first=True)
testdt['Spending_Score'].replace(['Low', 'Average', 'High'], [0,1,2], inplace=True)

trainCluster.replace(['A', 'B', 'C', 'D'], [0,1,2, 3], inplace=True)
testCluser.replace(['A', 'B', 'C', 'D'], [0,1,2, 3], inplace=True)

traindt.info()

"""**Correlation**"""

py.figure(figsize=(15,5))
sb.heatmap(traindt.corr(), annot=True)

"""# **Clustering Model**"""

random_state = 45
max_itr = 500

def kmean(traindt=traindt, actualClusters=trainCluster, testdt=testdt, testClusters=testCluser, type_='k-means++',  clusters=4):

    model = KMeans(n_clusters=clusters, init=type_, random_state=random_state, max_iter=max_itr)
    model.fit(traindt)
    preds = model.predict(traindt)
    preds_test = model.predict(testdt)

    print("silhouette score Train =", silhouette_score(traindt, preds))
    print("silhouette score Test = ", silhouette_score(testdt, preds_test))
    return preds, preds_test

preds_train_or, preds_test_or = kmean()

tsne = TSNE(random_state=random_state, init='pca')

low_dim_tsne = pd.DataFrame(tsne.fit_transform(traindt))
low_dim_tsne['Segmentation KMeans'] = preds_train_or

low_dim_tsne_test = pd.DataFrame(tsne.fit_transform(testdt))
low_dim_tsne_test['Segmentation KMeans'] = preds_test_or

sb.pairplot(data=low_dim_tsne.loc[:, [0,1, 'Segmentation KMeans']], hue='Segmentation KMeans')

"""# **Classification Model**"""

def knn_fit(traindt=traindt, trainClasess=trainCluster, testdt=testdt, testClasses=testCluser):

    train_error, test_error = [], []

    for k in range(3, 12, 2):
      model = KNeighborsClassifier(n_neighbors=k)
      model.fit(traindt, trainClasess)
      train_error.append(np.mean(model.predict(traindt) != trainClasess.values))
      test_error.append(np.mean(model.predict(testdt) != testClasses.values))
      pass

    py.plot(range(3, 12, 2), train_error, label='Train Error')
    py.plot(range(3, 12, 2), test_error, label='Test Error')
    py.xlabel('K values')
    py.ylabel('Error')
    py.legend()
    py.show()
    pass

def knn_apply(k, traindt=traindt, trainClasess=trainCluster, testdt=testdt, testClasses=testCluser):


    model = KNeighborsClassifier(n_neighbors=k)
    model.fit(traindt, trainClasess)

    preds_train = model.predict(traindt)
    print("In Train Set")
    print('\t\t Accuracy Score = ', accuracy_score(trainClasess, preds_train))
    ConfusionMatrixDisplay(confusion_matrix(trainClasess, preds_train)).plot()
    py.title("Display Confusion Matrix for Train Set")
    py.show()
    print('\t\t Classification Report = ', classification_report(trainClasess, preds_train))

    preds_test = model.predict(testdt)
    print("In Test Set")
    print('\t\t Accuracy Score = ', accuracy_score(testClasses, preds_test))
    ConfusionMatrixDisplay(confusion_matrix(testClasses, preds_test)).plot()
    py.title("Display Confusion Matrix for Test Set")
    py.show()
    print('\t\t Classification Report = ', classification_report(testClasses, preds_test))

    return model

def random_forest(traindt=traindt, trainClasess=trainCluster, testdt=testdt, testClasses=testCluser):

    model = RandomForestClassifier(random_state=random_state, n_estimators=300)
    model.fit(traindt, trainClasess)

    preds_train = model.predict(traindt)
    print("In Train Set")
    print('\t\t Accuracy Score = ', accuracy_score(trainClasess, preds_train))
    ConfusionMatrixDisplay(confusion_matrix(trainClasess, preds_train)).plot()
    py.title("Display Confusion Matrix for Train Set")
    py.show()
    print('\t\t Classification Report = ', classification_report(trainClasess, preds_train))

    preds_test = model.predict(testdt)
    print("In Test Set")
    print('\t\t Accuracy Score = ', accuracy_score(testClasses, preds_test))
    ConfusionMatrixDisplay(confusion_matrix(testClasses, preds_test)).plot()
    py.title("Display Confusion Matrix for Test Set")
    py.show()
    print('\t\t Classification Report = ', classification_report(testClasses, preds_test))

    return model

def svm(traindt=traindt, trainClasess=trainCluster, testdt=testdt, testClasses=testCluser):

    model = SVC(C=0.8, probability=True, kernel='linear', random_state=random_state, max_iter=max_itr)
    model.fit(traindt, trainClasess)

    preds_train = model.predict(traindt)
    print("In Train Set")
    print('\t\t Accuracy Score = ', accuracy_score(trainClasess, preds_train))
    ConfusionMatrixDisplay(confusion_matrix(trainClasess, preds_train)).plot()
    py.title("Display Confusion Matrix for Train Set")
    py.show()
    print('\t\t Classification Report = ', classification_report(trainClasess, preds_train))

    preds_test = model.predict(testdt)
    print("In Test Set")
    print('\t\t Accuracy Score = ', accuracy_score(testClasses, preds_test))
    ConfusionMatrixDisplay(confusion_matrix(testClasses, preds_test)).plot()
    py.title("Display Confusion Matrix for Test Set")
    py.show()
    print('\t\t Classification Report = ', classification_report(testClasses, preds_test))

    return model

def adaboost(traindt=traindt, trainClasess=trainCluster, testdt=testdt, testClasses=testCluser):

    model = AdaBoostClassifier(random_state=random_state, n_estimators=300)
    model.fit(traindt, trainClasess)

    preds_train = model.predict(traindt)
    print("In Train Set")
    print('\t\t Accuracy Score = ', accuracy_score(trainClasess, preds_train))
    ConfusionMatrixDisplay(confusion_matrix(trainClasess, preds_train)).plot()
    py.title("Display Confusion Matrix for Train Set")
    py.show()
    print('\t\t Classification Report = ', classification_report(trainClasess, preds_train))

    preds_test = model.predict(testdt)
    print("In Test Set")
    print('\t\t Accuracy Score = ', accuracy_score(testClasses, preds_test))
    ConfusionMatrixDisplay(confusion_matrix(testClasses, preds_test)).plot()
    py.title("Display Confusion Matrix for Test Set")
    py.show()
    print('\t\t Classification Report = ', classification_report(testClasses, preds_test))

    return model

knn_fit()

knn_model = knn_apply(k=5)

knn_fit(trainClasess=pd.Series(preds_train_or), testClasses=pd.Series(preds_test_or))

knn_model = knn_apply(k=11, trainClasess=pd.Series(preds_train_or), testClasses=pd.Series(preds_test_or))