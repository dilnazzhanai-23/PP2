from config import host, dbname, user, password, port
import psycopg2
def get_connection():
    return psycopg2.connect(
        host = host,
        dbname = dbname,
        user = user,
        password = password,
        port = port
    )