# CarPricePrediction
Car price prediction using machine learning algorithms - KNN and Linear Regression, implemented from scratch in Python and compared with existing SKLearn implementations (accuracy and speed of execution). Data used within the project was scrapped from one of the largest Serbian websites (www.polovniautomobili.com) where people list ads to sell their cars. The project also includes a multithreaded scraper that uses HTTPS (SSL) proxies, since the website works only with HTTPS protocol.

You will need a MySQL database, since the scraper stores the data within it and the data analysis scripts/machine learning models read from the same database in order to conduct the process of training and testing (you may need to change the password within the script).

The database created contains only one table - Automobili (cars on english) with the following columns:
  idOglasa VARCHAR(50) PRIMARY KEY - ID of the selling page, used as a primary key so we don't get doubles within the database for one reason or another
  cena INT - car price
  stanje VARCHAR(30) - car state (new/used)
  marka VARCHAR(30) - car brand
  model VARCHAR(30) - car model
  godiste INT - year when car was produced
  kilometraza INT - mileage in kilometers
  karoserija VARCHAR(30) - type of chassis
  gorivo VARCHAR(30) - type of fuel
  kubikaza INT - car engine cubic capacity
  snagaMotora INT - car engine horsepower
  menjac VARCHAR(30) - type of gearbox
  brojVrata INT - number of doors
  boja VARCHAR(30) - car color
  lokacijaProdavca VARCHAR(100) - seller location
  
Within the machine learning models all data that was a string was encoded using SKLearn LabelEncoder and then all of the data was scaled so that the mean value is 0, with a standard deviation of 1 (data is in ranges [-1;1]). Training and test sets for models were generated using the train_test_split method from SKLearn.

File/Folder description:
  - PSZ_Projekat_Jun_Jul_2022_v1.0.pdf - this PDF document contains the assignment details and expectations for the project/machine learning models.
  - z1 - this folder contains the solution of the first task of the assignment - web scraper and the result database:
    - create_database.py - this file contains the Python script to create the MySQL database.
    - proxies.txt - input file for the scraper to use, so it can scrap and download a large amount of data in the same time.
    - web_scraper.py - file which contains the multithreaded Python Web scraper with proxies, using BeautifulSoup4 for parsing the Web page contents.
    - database.sql - the result database after scraping ~30,000 selling ads from the website (only the ones with price present, as this is our target data).
  - z2 - this folder contains the solution of the second task of the assignment - data analysis for cars using SQL (models, most expensive cars, most frequent cities etc):
    - upiti.docx - this Word document contains all the SQL queries needed to extract the data by the different task criteria.
    - a.csv, b.csv, c.csv, d1.csv, d2.csv, e.csv, f.csv - files which contain the results exported in CSV format from MySQL Workbench.
  - z3 - this folder contains the solution of the second task of the assignment - data analysis for cars using charts (models, most expensive cars, most frequent cities etc):
    - generate.py - within this file is a Python script which uses the car data from the database and matplotlib to plot various graphs which indicate different patterns across the data sample.
    - a.png, b.png, c.png, d.png, e.png - saved matplot graphs.
  - z4 - this folder contains two Linear Regression implementations - one with and one without numpy (considerably slower):
    - LinearRegression.py - this file contains the model with Linear Regression using numpy, data is encoded (if a string) then scaled and used to train the model, after this a graph with the Linear Regression Cost Function is shown per training epoch. After this the python program outputs the predicted price by model and the real price (from the test data set) and lastly it trains the SKLearn Linear Regression model using the same data and then prints both R^2 coefficients for comparison.
    - LinearRegression no numpy.py - this file contains the Linear Regression model without the usage of numpy, and as a result it is significantly slower, does everything the same.
  - z5 - this folder contains the KNN model implementation with two distance functions - Euclidean and Manhattan:
    - KNN.py - this file contains the Python implementation of KNN, where the number of neighbours used in decision is 171 (approx. the square root of the number of database entries). Similar to Linear Regression it also encodes and scales the data. It also translates the price from a continuous value to a class based one (as defined in the assignment), in order for the KNN training to take place. It takes a random test set size of 5% so the execution time isn't too long and predicts the price class and prints the real price class. In the end the SKLearn KNN model is used on the same dataset and the accuracy scores are printed for the implemented model and the SKLearn one.
