import psycopg2
from connect import connection
conn=connection()
cur=conn.cursor()
def table():
    cur.execute("""CREATE TABLE IF NOT EXISTS phonebook2 (
    id      SERIAL          PRIMARY KEY,
    name    VARCHAR(100)    NOT NULL,
    number  VARCHAR(100)    UNIQUE
    );
    """)
    conn.commit()

def show():
    print("Search:")
    x=input()
    cur.execute("SELECT * FROM show_name_or_phone(%s);", (x,))
    rows=cur.fetchall()
    for row in rows:
        print(row)

def insert_or_update():
    name=input("Enter name: ")
    number=input("Enter phone: ")
    cur.execute("CALL insert_or_update(%s,%s);",(name, number))
    conn.commit()


def insert_many_users():
    n = int(input("How many users to insert? "))
    names = []
    numbers = []

    for i in range(n):
        name = input(f"Enter name {i+1}: ")
        number = input(f"Enter phone {i+1}: ")
        names.append(name)
        numbers.append(number)

    cur.execute("CALL insert_many_users(%s, %s);",(names, numbers))
    conn.commit()
    print("Insertion complete")

def pagination():
    limit = int(input("Limit: "))
    offset = int(input("Offset: "))
    cur.execute("SELECT * FROM get_phonebook_paginated(%s, %s);", (limit, offset))
    rows = cur.fetchall()
    for row in rows:
        print(row)

def delete():
    value=input("Enter name or phone: ")
    cur.execute("CALL delete(%s);",(value,))
    conn.commit()

def menu():
    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1 - Search")
        print("2 - Insert / Update")
        print("3 - Insert Many")
        print("4 - Pagination")
        print("5 - Delete")
        print("0 - Exit")

        choice = input("Choose: ")
        if choice == "1":
            show()
        elif choice == "2":
            insert_or_update()
        elif choice == "3":
            insert_many_users()
        elif choice == "4":
            pagination()
        elif choice == "5":
            delete()
        elif choice == "0":
            break
        else:
            print("Invalid choice")


menu()
cur.close()
conn.close()
