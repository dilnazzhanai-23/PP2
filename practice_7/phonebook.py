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


# INSERT FROM CSV
def insert() :
    with open("contacts.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            cur.execute("""INSERT INTO phonebook (name, phone) VALUES
                (%s, %s)""",
                (row[0], row[1])
                )
        conn.commit()
        print("SV inserted")


# INSERT FROM CONSOLE
def con():
    name=input("Name: ")
    phone=input("Phone: ")
    cur.execute("""INSERT INTO phonebook (name,phone) VALUES (%s,%s)""",
                (name,phone)
                )
    conn.commit()

# UPDATE
def update() :
    name=input("Name: ")
    new_name=input("Update_name: ")
    phone=input("Phone: ")
    new_phone=input("Update_phone: ")
    if new_name:
        cur.execute("UPDATE phonebook SET name=%s WHERE name=%s",(new_name,name))

    if new_phone:
        cur.execute("UPDATE phonebook SET name=%s WHERE name=%s",(new_phone,phone))
    conn.commit()

# DELETE
def delete() :
    print("1 - Delete by name")
    print("2 - Delete by phone")

    choice=input()
   
    if choice=="1" :
        name=input("Name: ")
        cur.execute("DELETE FROM phonebook WHERE name=%s", (name,))
    
    elif choice=="2" :
        phone=input("Phone: ")
        cur.execute("DELETE FROM phonebook WHERE phone=%s", (phone,))

    conn.commit()

# QUERY
def query_contacts():
    print("1 - Show all")
    print("2 -  Find phone by name")
    print("3 -  Find name by phone phone")

    choice = input()

    if choice == "1":
        cur.execute("SELECT * FROM phonebook")
        rows = cur.fetchall()
        for row in rows:
            print(row)

    elif choice == "2":
        name = input("Name: ")
        cur.execute("SELECT phone FROM phonebook WHERE name=%s", ( name, ))
        result=cur.fetchone()
        if result:
            print("Phone:",result[0])

    elif choice == "3":
        phone=input("Phone: ")
        cur.execute("SELECT name FROM phonebook WHERE phone=%s", (phone,))
        result=cur.fetchone()
        if result:
            print("Name:",result[0])
           

# MENU
def menu():
    while True:
        print("PHONEBOOK MENU")
        print("1 - Insert from CSV")
        print("2 - Add contact")
        print("3 - Update contact")
        print("4 - Query contacts")
        print("5 - Delete contact")
        print("0 - Exit")

        choice = input("Choose: ")

        if choice == "1":
            insert()
        elif choice == "2":
            con()
        elif choice == "3":
            update()
        elif choice == "4":
            query_contacts()
        elif choice == "5":
            delete()
        elif choice == "0":
            break


menu()
cur.close()

conn.close()