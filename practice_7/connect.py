import psycopg2

conn=psycopg2.connect(
    host='localhost',
    port=5432,
    dbname="pp2_db",
    user="postgres",
    password="2313147078Dilnaz"
)

cur=conn.cursor()
print(conn.status)
cur.close()
conn.close()