import pandas as pd
#data reading
data=pd.read_csv("Crop_recommendation.csv")

#data pre-process
data=data.dropna(how='any')
colums=data.columns

#seperate data and labels
X=data.loc[:,colums[:7]]  #datas
y=data.loc[:,colums[7]]   #labels

#array Conver
X=X.to_numpy()

#label Encoding
from sklearn import preprocessing
le = preprocessing.LabelEncoder()
le.fit(y)
y=le.transform(y)
import pickle
pickle.dump(le, open('le.pkl', 'wb'))

#spilit data 80% train 20% test
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

import warnings
warnings.filterwarnings("ignore")
names = ["K-Nearest Neighbors", "SVM",
         "Decision Tree", "Random Forest",
         "Naive Bayes","ExtraTreesClassifier","VotingClassifier"]

#process in steps
from sklearn.pipeline import make_pipeline
#pre-process data/max value scale 0-1 so calculation fast
from sklearn.preprocessing import Normalizer
#load models
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import VotingClassifier
#parameters
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report


classifiers = [
    make_pipeline(Normalizer(),KNeighborsClassifier()),
    make_pipeline(Normalizer(),LinearSVC()),
    make_pipeline(Normalizer(),DecisionTreeClassifier()),
    make_pipeline(Normalizer(),RandomForestClassifier()),
    make_pipeline(Normalizer(),GaussianNB()),
    make_pipeline(Normalizer(),ExtraTreesClassifier()),
    make_pipeline(Normalizer(),VotingClassifier(estimators=[('DT', DecisionTreeClassifier()), ('rf', RandomForestClassifier()), ('et', ExtraTreesClassifier())], voting='hard'))]

clfF=[]
for name, clf in zip(names, classifiers):
    clf.fit(X_train, y_train)
    y_pred=clf.predict(X_test)
    print(name)
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))
    print('--------------------------------------------------------------')
    clfF.append(clf)
import bz2
sfile = bz2.BZ2File("All Model", 'w')
#pickle.dump(clfF, sfile)   
    
    
    
    
    
    
    
    
    
    
    