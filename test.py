import psycopg2
import csv

conn=psycopg2.connect(
    host='localhost',
    port=5432,
    dbname="pp2_db",
    user="postgres",
    password="2313147078Dilnaz"
)

cur=conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS phonebook (
        id         SERIAL       PRIMARY KEY,
        name       VARCHAR(100) NOT NULL,
        phone      VARCHAR(100) UNIQUE NOT NULL,
        created_at TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
    );
""")
conn.commit()

def upd() :
    old_name=input()
    new_name=input()
    cur.execute("UPDATE phonebook SET name=%s WHERE name=%s",(new_name,old_name))
    if new_name:
        print("Updated")
upd()
cur.close()
conn.close()