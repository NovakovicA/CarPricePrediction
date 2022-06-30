import mysql.connector
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random
import sys
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split 
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

import warnings
warnings.filterwarnings("ignore")
np.set_printoptions(threshold=sys.maxsize)

def getCarsFromDatabase():
    try:
        connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="PSZ",
        charset="utf8"
        )

        ret = pd.read_sql("SELECT * FROM AUTOMOBILI", connection)
        #ret.to_csv("test.csv")
        connection.close()
        
        return ret

    except Exception as e:
        return -1

def getClassByPrice(price):
    if(price < 2000): return 0
    elif(price >= 2000 and price <= 4999): return 1
    elif(price >= 5000 and price <= 9999): return 2
    elif(price >= 10000 and price <= 14999): return 3
    elif(price >= 15000 and price <= 19999): return 4
    elif(price >= 20000 and price <= 24999): return 5
    elif(price >= 25000 and price <= 29999): return 6
    elif(price >= 30000): return 7

def getPriceByPriceClass(priceClass):
    if(priceClass == 0): return "(0,2000€)"
    elif(priceClass == 1): return "[2000€ ; 4999€]"
    elif(priceClass == 2): return "[5000€ ; 9999€]"
    elif(priceClass == 3): return "[10000€ ; 14999€]"
    elif(priceClass == 4): return "[15000€ ; 19999€]"
    elif(priceClass == 5): return "[20000€ ; 24999€]"
    elif(priceClass == 6): return "[25000€ ; 29999€]"
    elif(priceClass == 7): return "[30000€ ; inf)"
    

class KNN:
    def __init__(self, K=171, useEuclideanDistance=True, useManhattanDistance=False):
        self.K = K
        self.useEuclideanDistance = useEuclideanDistance
        self.useManhattanDistance = useManhattanDistance
    
    def fit(self, X, Y):
        self.Xtrain = X
        self.Ytrain = Y

    def euclideanDistance(self, x1, x2):
        return np.sqrt(np.sum(np.square(x1 - x2)))

    def manhattanDistance(self, x1, x2):
        return np.sum(np.abs(x1 - x2))

    def predict(self, X):
        Y = np.zeros(X.shape[0], dtype=int)

        for i in range(len(Y)):
            knn = np.zeros(self.K, dtype=int)

            distances = np.zeros(self.Xtrain.shape[0])

            for j in range(len(distances)):
                if(self.useEuclideanDistance == True):
                    distances[j] = self.euclideanDistance(X[i], self.Xtrain[j])
                elif(self.useManhattanDistance == True):
                    distances[j] = self.euclideanDistance(X[i], self.Xtrain[j])
                else:
                    print("You must select a supported distance metric.")
                    exit()
            
            for j in range(len(knn)):
                index = np.argmin(distances)
                knn[j] = self.Ytrain[index]
                np.delete(distances, index)

            Y[i] = np.bincount(knn).argmax()
            print(str(i) + "/" + str(X.shape[0]) + " " + str(Y[i]))
        return Y
    
    def accuracy_score(self, Ypred, Ytest):
        hits = 0
        for i in range(len(Ytest)): 
            if (Ytest[i] == Ypred[i]): hits += 1
        
        return hits / len(Ytest)



dataset = getCarsFromDatabase()

dataset = dataset.reindex(columns = ["cena", "idOglasa", "stanje", "marka", "model", "godiste", "kilometraza", "karoserija", "gorivo", "kubikaza", "snagaMotora", "menjac", "brojVrata", "boja", "lokacijaProdavca"])

le = LabelEncoder()

dataset["stanje"]= le.fit_transform(dataset["stanje"])
dataset["marka"]= le.fit_transform(dataset["marka"])
dataset["model"]= le.fit_transform(dataset["model"])
dataset["karoserija"]= le.fit_transform(dataset["karoserija"])
dataset["gorivo"]= le.fit_transform(dataset["gorivo"])
dataset["menjac"]= le.fit_transform(dataset["menjac"])
dataset["boja"]= le.fit_transform(dataset["boja"])
dataset["lokacijaProdavca"]= le.fit_transform(dataset["lokacijaProdavca"])

dataset = dataset.drop("idOglasa", 1)
dataset = dataset.drop("menjac", 1)
dataset = dataset.drop("brojVrata", 1)
dataset = dataset.drop("boja", 1)
dataset = dataset.drop("gorivo", 1)
dataset = dataset.drop("karoserija", 1)
dataset = dataset.drop("lokacijaProdavca", 1)
# dataset = dataset.drop("marka", 1)
# dataset = dataset.drop("model", 1)


X = dataset.iloc[:,1:-1].values
Y = dataset.iloc[:,0].values

mu = np.mean(X, 0)
sigma = np.std(X, 0)

X = (X - mu) / sigma

for i in range(len(Y)): Y[i] = getClassByPrice(Y[i])

Xtrain, Xtest, Ytrain, Ytest = train_test_split(X, Y, test_size=0.05, random_state=0)

knn = KNN(171, True, False)
knn.fit(Xtrain, Ytrain)

Ypredicted = knn.predict(Xtest)

for i in range(len(Ypredicted)):
    print(f"Real price range: {getPriceByPriceClass(Ytest[i])}, predicted price range: {getPriceByPriceClass(Ypredicted[i])}.")
    i += 1

skKNN = KNeighborsClassifier(n_neighbors=171)
skKNN.fit(Xtrain, Ytrain)

skKNN_Ypredicted= skKNN.predict(Xtest)
print("Accuracy score - implemented model: " + str(knn.accuracy_score(Ypredicted, Ytest)) + ".")
print("Accuracy score - sklearn model: " + str(accuracy_score(skKNN_Ypredicted, Ytest)) + ".")