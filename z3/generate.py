import matplotlib.pyplot as plt
import mysql.connector
import numpy as np

def getCars():
    try:
        connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="PSZ",
        charset="utf8"
        )

        connection.autocommit = True
        cursor = connection.cursor(buffered=True)
        cursor.execute("SELECT * FROM AUTOMOBILI")
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        for row in rows:
            for i in range(len(cursor.column_names)):
                print(row[i],end=" ")
            print("")
    except Exception as e:
        print(e)
        return -1

def getNumberOfCarsInDatabase():
    try:
        connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="PSZ",
        charset="utf8"
        )

        connection.autocommit = True
        cursor = connection.cursor(buffered=True)
        cursor.execute("SELECT COUNT(*) FROM AUTOMOBILI")
        numberOfEntries = cursor.fetchall()
        cursor.close()
        connection.close()

        return (numberOfEntries[0][0])
    except Exception as e:
        return -1


def GenerateTop10Locations():
    try:
        connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="PSZ",
        charset="utf8"
        )

        connection.autocommit = True
        cursor = connection.cursor(buffered=True)
        cursor.execute("""
        SELECT lokacijaProdavca, COUNT(*)
        FROM AUTOMOBILI
        GROUP BY lokacijaProdavca
        ORDER BY COUNT(*) DESC
        LIMIT 10
        """)
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        values = [0] * 11
        labels = [""] * 11

        index = 0

        for row in rows:
            index += 1
            for i in range(len(cursor.column_names)):
                if(cursor.column_names[i] == "lokacijaProdavca"): labels[index] = row[i]
                else: values[index] = row[i]
        
        plt.pie(values, labels = labels)
        plt.savefig("a.png")
        #plt.show() 
        plt.clf()
    except Exception as e:
        print(e)
        return -1

def getNumberOfCarsByMileage(r1, r2):
    try:
        connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="PSZ",
        charset="utf8"
        )

        connection.autocommit = True
        cursor = connection.cursor(buffered=True)
        cursor.execute("""
        SELECT COUNT(*)
        FROM AUTOMOBILI
        WHERE kilometraza>=%s and kilometraza<=%s
        LIMIT 10
        """,(r1,r2,))
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        return rows[0][0]

    except Exception as e:
        print(e)
        return -1

def GenerateNumberOfCarsByMileage():
    labels = ["[0, 49 999]", "[50 000, 99 999]" , "[100 000, 149 999]" , "[150 000, 199 999]" , "[200 000, 249 999]" , "[250 000, 299 999]" , "[300 000, inf)"]
    values = [0] * len(labels)
    values[0] = getNumberOfCarsByMileage(0,49999)
    values[1] = getNumberOfCarsByMileage(50000,99999)
    values[2] = getNumberOfCarsByMileage(100000, 149999)
    values[3] = getNumberOfCarsByMileage(150000, 199999)
    values[4] = getNumberOfCarsByMileage(200000, 249999)
    values[5] = getNumberOfCarsByMileage(250000, 299999)
    values[6] = getNumberOfCarsByMileage(300000, 99999999999999)

    plt.rc("font", size=5) 
    plt.barh(labels, values)

    for index, value in enumerate(values): plt.text(value, index, str(value))
    plt.savefig("b.png")
    #plt.show()
    plt.clf()

def getNumberOfCarsByYear(r1, r2):
    try:
        connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="PSZ",
        charset="utf8"
        )

        connection.autocommit = True
        cursor = connection.cursor(buffered=True)
        cursor.execute("""
        SELECT COUNT(*)
        FROM AUTOMOBILI
        WHERE godiste>=%s and godiste<=%s
        LIMIT 10
        """,(r1,r2,))
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        return rows[0][0]

    except Exception as e:
        print(e)
        return -1

def GenerateNumberOfCarsByYear():
    labels = ["[0, 1960]", "[1961, 1970]" , "[1971, 1980]" , "[1981, 1990]" , "[1991, 2000]" , "[2001, 2005]" , "[2006, 2010]", "[2011, 2015]" , "[2016, 2020]", "[2021, 2022]"]
    values = [0] * len(labels)

    values[0] = getNumberOfCarsByYear(0,1960)
    values[1] = getNumberOfCarsByYear(1961, 1970)
    values[2] = getNumberOfCarsByYear(1971, 1980)
    values[3] = getNumberOfCarsByYear(1981, 1990)
    values[4] = getNumberOfCarsByYear(1991, 2000)
    values[5] = getNumberOfCarsByYear(2001, 2005)
    values[6] = getNumberOfCarsByYear(2006, 2010)
    values[7] = getNumberOfCarsByYear(2011, 2015)
    values[8] = getNumberOfCarsByYear(2016, 2020)
    values[9] = getNumberOfCarsByYear(2021, 2022)

    plt.rc("font", size=5) 
    plt.barh(labels, values)

    for index, value in enumerate(values): plt.text(value, index, str(value))
    plt.savefig("c.png")
    #plt.show()
    plt.clf()

def GenerateNumberOfCarsByGearbox():
    try:
        connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="PSZ",
        charset="utf8"
        )

        connection.autocommit = True

        cursor = connection.cursor(buffered=True)
        cursor.execute("""
        SELECT COUNT(*)
        FROM AUTOMOBILI
        WHERE menjac LIKE "Automatski%"
        """)
        rows = cursor.fetchall()
        cursor.close()
        num1 = rows[0][0]

        cursor = connection.cursor(buffered=True)
        cursor.execute("""
        SELECT COUNT(*)
        FROM AUTOMOBILI
        WHERE menjac LIKE "Manuelni%"
        """)
        rows = cursor.fetchall()
        cursor.close()
        num2 = rows[0][0]
        connection.close()

        values = [num1, num2]
        labels = ["Automatski", "Manuelni"]
        plt.rc("font", size=7) 
        plt.barh(labels, values)

        num = getNumberOfCarsInDatabase()

        for index, value in enumerate(values): plt.text(value, index, str(value) + "(" + str(round((value/num)*100,2)) + "%)")
        plt.savefig("d.png")
        #plt.show()
        plt.clf()
    
    except Exception as e:
        print(e)
        return -1

def getNumberOfCarsByPrice(r1, r2):
    try:
        connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="PSZ",
        charset="utf8"
        )

        connection.autocommit = True
        cursor = connection.cursor(buffered=True)
        cursor.execute("""
        SELECT COUNT(*)
        FROM AUTOMOBILI
        WHERE cena>=%s and cena<=%s
        LIMIT 10
        """,(r1,r2,))
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        return rows[0][0]

    except Exception as e:
        print(e)
        return -1

def GenerateNumberOfCarsByPrice():
    labels = ["[0 €, 2000 €]", "[2000 €, 4999 €]" , "[5000 €, 9999 €]" , "[10000 €, 14999 €]" , "[15000 €, 19999 €]" , "[20000 €, 24999 €]" , "[25000 €, 29999 €]", "[30000 €, inf €)"]
    values = [0] * len(labels)

    values[0] = getNumberOfCarsByPrice(0, 2000)
    values[1] = getNumberOfCarsByPrice(2000, 4999)
    values[2] = getNumberOfCarsByPrice(5000, 9999)
    values[3] = getNumberOfCarsByPrice(10000, 14999)
    values[4] = getNumberOfCarsByPrice(15000, 19999)
    values[5] = getNumberOfCarsByPrice(20000, 24999)
    values[6] = getNumberOfCarsByPrice(25000, 29999)
    values[7] = getNumberOfCarsByPrice(30000, 9999999999)

    plt.rc("font", size=5) 
    plt.barh(labels, values)

    num = getNumberOfCarsInDatabase()

    for index, value in enumerate(values): plt.text(value, index, str(value) + "(" + str(round((value/num)*100,2)) + "%)")
    plt.savefig("e.png")
    #plt.show()
    plt.clf()

GenerateTop10Locations()
GenerateNumberOfCarsByMileage()
GenerateNumberOfCarsByYear()
GenerateNumberOfCarsByGearbox()
GenerateNumberOfCarsByPrice()