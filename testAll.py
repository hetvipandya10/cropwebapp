import pickle
import bz2
N=float(input("N="))
P=float(input("p="))
K=float(input("K="))
temp=float(input("temp="))
Hum=float(input("Humidity="))
Ph=float(input("ph="))
Rain=float(input("Rain="))
#load model
sfile = bz2.BZ2File('All Model', 'r')
model=pickle.load(sfile)
names = ["K-Nearest Neighbors", "SVM",
         "Decision Tree", "Random Forest",
         "Naive Bayes","ExtraTreesClassifier","VotingClassifier"]
for i in range(len(model)):
    print(names[i])
    test_prediction = model[i].predict([[N,P,K,temp,Hum,Ph,Rain]])
    le=pickle.load(open('le.pkl', 'rb'))
    label=le.inverse_transform(test_prediction)
    print(label[0])