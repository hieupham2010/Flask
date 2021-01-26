import pymysql

def executeQueryValNonData(query , val):
    try:
        print(val)
        connection = pymysql.connect("localhost" , "root" , "" ,"soa-flask")
        cursor = connection.cursor()
        cursor.execute(query, val)
        cursor.connection.commit()
        cursor.close()
        return True
    except Exception as e:
        print(e)
        return False

def executeQueryData(query):
    try:
        connection = pymysql.connect("localhost" , "root" , "" ,"soa-flask")
        cursor = connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return data
    except Exception as e:
        print(e)
        return False

def executeQueryValData(query , val):
    try:
        connection = pymysql.connect("localhost" , "root" , "" ,"soa-flask")
        cursor = connection.cursor()
        cursor.execute(query, val)
        data = cursor.fetchall()
        cursor.close()
        return data
    except Exception as e:
        print(e)
        return False