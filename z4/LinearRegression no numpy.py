import mysql.connector
import matplotlib.pyplot as plt
import pandas as pd
import random
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression as SKLearnLinearRegression

import warnings
warnings.filterwarnings("ignore")

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

def transpose(M):
    return [[M[j][i] for j in range(len(M))] for i in range(len(M[0]))]

class LinearRegression:
    def __init__(self):
        self.W = []
        self.w0 = 0

    def costFunction(self, X, Y):
        cost = 0 
        temp = X @ self.W
        for i in range(len(temp)):
            cost += (temp[i] + self.w0 - Y[i]) ** 2

        cost /= (2 * len(Y))
        return cost

    def fit(self, X, Y, lr=0.01, epochs=1500):
        self.W = [0] * len(X[1])
        self.w0 = 0

        self.cost_by_epoch = [0] * epochs
    
        for epoch in range(epochs):
            Z = (X @ self.W) + self.w0
            loss = Z - Y
            
            W_gradient = (transpose(X) @ loss) / len(Y)
            w0_gradient = 0
            for i in range(len(loss)): w0_gradient += loss[i];
            w0_gradient /= len(Y)
            
            self.W = self.W - (lr * W_gradient)
            self.w0 = self.w0 - (lr * w0_gradient)
    
            cost = self.costFunction(X, Y)
            self.cost_by_epoch[epoch] = cost
        return

    def predict(self, X):
        ret =  (X @ self.W) + self.w0
        return ret 

    def R2_coefficient(self, Ypredicted, Y):
        RSS = 0
        TSS = 0

        Ymean = 0
        for i in range(len(Y)): Ymean += Y[i]
        Ymean /= len(Y)

        for i in range(len(Ypredicted)):
            RSS += ((Ypredicted[i] - Y[i]) ** 2)
            i += 1

        for i in range(len(Y)):
            TSS += ((Y[i] - Ymean) ** 2)
            i += 1
        
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

dataset = dataset[["cena","idOglasa","stanje","marka","model","godiste","kilometraza","karoserija","gorivo","kubikaza","snagaMotora","menjac","brojVrata","boja","lokacijaProdavca"]]

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
dataset = dataset.drop("lokacijaProdavca", 1)

# dataset = dataset.drop("marka", 1)
# dataset = dataset.drop("model", 1)

X = dataset.iloc[:,1:-1].values
Y = dataset.iloc[:,0].values

sc = StandardScaler()
X = sc.fit_transform(X)

Xtrain, Xtest, Ytrain, Ytest = train_test_split(X, Y, test_size=0.3, random_state=0)


linearRegression = LinearRegression()
linearRegression.fit(Xtrain, Ytrain)

linearRegression.showCostByEpoch()

Ypredicted = linearRegression.predict(Xtest)

i = 0
for y in Ypredicted:
    print(f"Real price: {Ytest[i]}€, predicted price: {Ypredicted[i]}€.")
    i += 1
    
print("Coefficient of determination (R^2) - implemented model: " + str(linearRegression.R2_coefficient(Ypredicted, Ytest)) + ".")




skLinearRegression = SKLearnLinearRegression()
skLinearRegression.fit(Xtrain, Ytrain)

print("Coefficient of determination (R^2) - sklearn model: " + str(skLinearRegression.score(Xtest, Ytest)))