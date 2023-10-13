from mysql.connector import MySQLConnection, Error, errorcode
import secret
import sys

# Credentials to connect to database
host = secret.host
password = secret.password
user = secret.user

"""
    Establish a connetion to database
"""
def connect_to_db():
    try:
        print('Connecting to MySQL database...')
        conn = MySQLConnection(host=host, password=password, user=user)
 
        if conn.is_connected():
            print('connection established.')
            mycursor = conn.cursor(buffered=True)

            return conn
        else:
            print('connection failed.')
    except Error as err:
        print('connection failed somehow')
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print("Unexpected error")
            print(err)
            sys.exit(1)

"""
    print the result of the previous query
"""
def pres(curs):
    res = curs.fetchall()
    for row in res:
        print(row)

if __name__ == "__main__":
    conn = connect_to_db()
    mycursor = conn.cursor(buffered=True)
    use_query = "USE football;"
    mycursor.execute(use_query)

    mycursor.execute("SHOW TABLES;")
    pres(mycursor)
    
    mycursor.execute("DESCRIBE leagues;")
    pres(mycursor)

    conn.close()