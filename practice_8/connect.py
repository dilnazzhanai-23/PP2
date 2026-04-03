from config import host,port, database,user,password 
import psycopg2
def connection() :
    return psycopg2.connect(
        host =host,
        port=port,
        dbname=database,
        user=user,
        password=password

    )
    