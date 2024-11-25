import pickle
import bz2
N=float(("28"))
P=float(("67"))
K=float(("21"))
Ph=float(("6"))
sfile = bz2.BZ2File('All Model Soil', 'r')
model=pickle.load(sfile)
names = ["K-Nearest Neighbors", "SVM",
         "Decision Tree", "Random Forest",
         "Naive Bayes","ExtraTreesClassifier"]
for i in range(len(model)):
    print(names[i])
    test_prediction = model[i].predict([[N,P,K,Ph]])
    le=pickle.load(open('le Soil.pkl', 'rb'))
    label=le.inverse_transform(test_prediction)
    print(label[0])