import pickle
import bz2

temp=float(("21.7"))
Hum=float(("63"))
Rain=float(("46"))
sfile = bz2.BZ2File('All Model Weather', 'r')
model=pickle.load(sfile)
names = ["K-Nearest Neighbors", "SVM",
         "Decision Tree", "Random Forest",
         "Naive Bayes","ExtraTreesClassifier"]
for i in range(len(model)):
    print(names[i])
    test_prediction = model[i].predict([[temp,Hum,Rain]])
    le=pickle.load(open('le Weather.pkl', 'rb'))
    label=le.inverse_transform(test_prediction)
    print(label[0])