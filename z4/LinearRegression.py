import mysql.connector
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random
import sys
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression as SKLearnLinearRegression

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


class LinearRegression:
    def __init__(self):
        self.W = []
        self.w0 = 0

    def costFunction(self, X, Y):
        cost = np.sum((((X.dot(self.W) + self.w0) - Y) ** 2) / (2*len(Y)))
        return cost

    def fit(self, X, Y, lr=0.01, epochs=1500):
        self.W = np.zeros(X.shape[1])
        self.w0 = 0

        self.cost_by_epoch = [0] * epochs
    
        for epoch in range(epochs):
            Z = X.dot(self.W) + self.w0
            loss = Z - Y
            
            W_gradient = X.T.dot(loss) / len(Y)
            w0_gradient = np.sum(loss) / len(Y)
            
            self.W = self.W - (lr * W_gradient)
            self.w0 = self.w0 - (lr * w0_gradient)
    
            cost = self.costFunction(X, Y)
            self.cost_by_epoch[epoch] = cost
        return

    def predict(self, X):
        return X.dot(self.W) + self.w0

    def R2_coefficient(self, Ypredicted, Y):
        RSS = np.sum((Ypredicted - Y) ** 2)
        TSS = np.sum((Y - Y.mean()) ** 2)
        
        r2 = 1 - (RSS / TSS)
        return r2

    def showCostByEpoch(self):
        plt.plot(self.cost_by_epoch)
        plt.title("Linear Regression Cost Function For Epochs")
        plt.grid(visible=True)
        ax = plt.gca()
        ax.set_xlabel('Epoch')
        ax.set_ylabel('Cost Function value') 
        plt.show()
        plt.clf()



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
# dataset = dataset.drop("menjac", 1)
dataset = dataset.drop("brojVrata", 1)
dataset = dataset.drop("boja", 1)
# dataset = dataset.drop("gorivo", 1)
# dataset = dataset.drop("karoserija", 1)
# dataset = dataset.drop("lokacijaProdavca", 1)

# dataset = dataset.drop("marka", 1)
# dataset = dataset.drop("model", 1)

X = dataset.iloc[:,1:-1].values
Y = dataset.iloc[:,0].values

Xmu = np.mean(X, 0)
Xsigma = np.std(X, 0)

X = (X - Xmu) / Xsigma

Xtrain, Xtest, Ytrain, Ytest = train_test_split(X, Y, test_size=0.3, random_state=0)


linearRegression = LinearRegression()
linearRegression.fit(Xtrain, Ytrain)

linearRegression.showCostByEpoch()

Ypredicted = linearRegression.predict(Xtest)

for i in range(len(Ypredicted)):
    print(f"Real price: {round(Ytest[i])}€, predicted price: {round(Ypredicted[i])}€.")
    i += 1
    
print("Coefficient of determination (R^2) - implemented model: " + str(linearRegression.R2_coefficient(Ypredicted, Ytest)) + ".")

skLinearRegression = SKLearnLinearRegression()
skLinearRegression.fit(Xtrain, Ytrain)

print("Coefficient of determination (R^2) - sklearn model: " + str(skLinearRegression.score(Xtest, Ytest)))