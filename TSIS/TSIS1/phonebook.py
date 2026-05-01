import psycopg2
import csv
import json
import os
from connect import get_connection

conn = get_connection()
cur = conn.cursor()

def create_table():
    try:
        
        with open('schema.sql', 'r', encoding='utf-8') as f:
            cur.execute(f.read())
            
       
        cur.execute("DROP FUNCTION IF EXISTS show_with_pagination(integer,integer);")
        cur.execute("DROP FUNCTION IF EXISTS get_user_name_or_phone_number_by_pattern(text);")
            
        
        cur.execute("""
            CREATE OR REPLACE FUNCTION show_with_pagination(limit_val INT, offset_val INT)
            RETURNS TABLE(id INT, first_name TEXT, second_name TEXT, email VARCHAR) AS $$
            BEGIN
                RETURN QUERY
                SELECT phonebook23.id, phonebook23.first_name, phonebook23.second_name, phonebook23.email 
                FROM phonebook23
                ORDER BY phonebook23.id
                LIMIT limit_val OFFSET offset_val;
            END;
            $$ LANGUAGE plpgsql;
        """)

        
        cur.execute("""
            CREATE OR REPLACE FUNCTION get_user_name_or_phone_number_by_pattern(p TEXT)
            RETURNS TABLE(id INT, first_name TEXT, second_name TEXT, email VARCHAR) AS $$
            BEGIN
                RETURN QUERY
                SELECT phonebook23.id, phonebook23.first_name, phonebook23.second_name, phonebook23.email 
                FROM phonebook23
                WHERE phonebook23.first_name ILIKE '%' || p || '%'
                   OR phonebook23.second_name ILIKE '%' || p || '%'
                   OR phonebook23.email ILIKE '%' || p || '%';
            END;
            $$ LANGUAGE plpgsql;
        """)

                
        cur.execute("""
            CREATE OR REPLACE PROCEDURE upsert_contact(p_1_name text, p_2_name text, p_phone_number text)
            LANGUAGE plpgsql AS $$
            DECLARE
                v_contact_id INT;
            BEGIN
                
                SELECT id INTO v_contact_id FROM phonebook23
                WHERE first_name = p_1_name AND second_name = p_2_name;

                IF v_contact_id IS NOT NULL THEN
                    
                    UPDATE phones SET phone = p_phone_number WHERE contact_id = v_contact_id;
                ELSE
                    
                    INSERT INTO phonebook23 (first_name, second_name) 
                    VALUES (p_1_name, p_2_name) RETURNING id INTO v_contact_id;
                    
                    
                    INSERT INTO phones (contact_id, phone, type) 
                    VALUES (v_contact_id, p_phone_number, 'mobile');
                END IF;
            END;
            $$;
        """)

               
        cur.execute("""
            CREATE OR REPLACE PROCEDURE delete_by_name_or_phonenumber(p TEXT)
            AS $$
            BEGIN
                
                DELETE FROM phonebook23
                WHERE first_name = p 
                   OR second_name = p 
                   OR id IN (SELECT contact_id FROM phones WHERE phone = p);
            END;
            $$ LANGUAGE plpgsql;
        """)

                
        cur.execute("""
            CREATE OR REPLACE PROCEDURE validate_phone_correctness(p_1_name TEXT[], p_2_name TEXT[], p_phone_number TEXT[])
            LANGUAGE plpgsql AS $$
            DECLARE
                i INT;
                v_contact_id INT;
            BEGIN
                FOR i IN 1..array_length(p_1_name, 1) LOOP
                    
                    IF p_phone_number[i] ~ '^[+8]{1}[0-9]{10,11}$' THEN
                        
                        INSERT INTO phonebook23 (first_name, second_name) 
                        VALUES (p_1_name[i], p_2_name[i]) RETURNING id INTO v_contact_id;
                        
                        
                        INSERT INTO phones (contact_id, phone, type) 
                        VALUES (v_contact_id, p_phone_number[i], 'mobile');
                    ELSE
                        RAISE NOTICE 'Invalid phone detected: %, %, %', p_1_name[i], p_2_name[i], p_phone_number[i];
                    END IF;
                END LOOP;
            END;
            $$;
        """)
    
        
        
        with open('procedures.sql', 'r', encoding='utf-8') as f:
            cur.execute(f.read())
            
        conn.commit()
        print("Database and procedures successfully initialized.")
    except Exception as e:
        conn.rollback()
        print(f"Error loading schema files: {e}")



def upload_data_from_csv_file():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, "contacts.csv")
    
    print(f"Reading file {csv_path}...")
    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader) 
            
            for row in reader:
                first = row[0]
                second = row[1]
                email = row[2] if row[2] else None
                birthday = row[3] if row[3] else None
                group_name = row[4] if row[4] else None
                phone = row[5]
                phone_type = row[6] if row[6] else 'mobile'
                
                group_id = None
                if group_name:
                    cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
                    g_row = cur.fetchone()
                    if g_row:
                        group_id = g_row[0]
                    else:
                        cur.execute("INSERT INTO groups (name) VALUES (%s) RETURNING id", (group_name,))
                        group_id = cur.fetchone()[0]

                cur.execute("""
                    INSERT INTO phonebook23 (first_name, second_name, email, birthday, group_id) 
                    VALUES (%s, %s, %s, %s, %s) RETURNING id
                """, (first, second, email, birthday, group_id))
                contact_id = cur.fetchone()[0]
                
                cur.execute("""
                    INSERT INTO phones (contact_id, phone, type) 
                    VALUES (%s, %s, %s)
                """, (contact_id, phone, phone_type))
                
            conn.commit()
            print("CSV data indexed and imported successfully.")
            
    except FileNotFoundError:
        print(f"Error: contacts.csv file not found in {script_dir}")
    except IndexError:
        print("Error: Incomplete columns in CSV rows.")
    except Exception as e:
        conn.rollback()
        print(f"Database error during CSV import: {e}")

def upload_data_from_console():
    print("How many rows to add?")
    n = int(input())
    for _ in range(n):
        print("Enter first name, second name, and phone:")
        x, z, y = input().split()
        
        cur.execute("""
            INSERT INTO phonebook23 (first_name, second_name) 
            VALUES (%s, %s) RETURNING id
        """, (x, z))
        contact_id = cur.fetchone()[0]
        
        cur.execute("""
            INSERT INTO phones (contact_id, phone, type) 
            VALUES (%s, %s, %s)
        """, (contact_id, y, 'mobile'))
    conn.commit()
    print("Contacts successfully added.")

def change_name_or_phone():
    print("What do you want to change?")
    print("write 1 if you want to change name or write 2 if you want to change phone number")
    a = input()
    if a == "1":
        print("Whats the new name?")
        fnewname1, snewname2 = input().split()
        print("Whats the phone number from the last owner?")
        oldphone = input()
        
        cur.execute("""UPDATE phonebook23 SET first_name = %s, second_name = %s 
                       WHERE id IN (SELECT contact_id FROM phones WHERE phone = %s)""", 
                    (fnewname1, snewname2, oldphone))
        conn.commit()
    else:
        print("Whats the old name?")
        oldname1, oldname2 = input().split()
        print("Whats the new phone number?")
        new_phone_number = input()
        cur.execute("""UPDATE phones SET phone = %s 
                       WHERE contact_id IN (SELECT id FROM phonebook23 WHERE first_name = %s AND second_name = %s)""", 
                    (new_phone_number, oldname1, oldname2))
        conn.commit()
    print("Record updated.")

def querying_data_from_the_table():
    print("1 - get full name typing phone number")
    print("2 - get phone number typing first name or second name")
    print("3 - get the whole table")
    a = int(input())
    if a == 1:
        print("Type phone number:")
        phonenumber = input()
        cur.execute("SELECT c.first_name, c.second_name FROM phonebook23 c JOIN phones p ON c.id = p.contact_id WHERE p.phone = %s", (phonenumber,))
        row = cur.fetchone()
        print(row if row else "Not found")
    elif a == 2:
        print("2 - second or 1 - first name?")
        b = int(input())
        col = "first_name" if b == 1 else "second_name"
        print(f"Type {col.replace('_', ' ')}:")
        val = input()
        cur.execute(f"SELECT p.phone FROM phones p JOIN phonebook23 c ON c.id = p.contact_id WHERE c.{col} = %s", (val,))
        rows = cur.fetchall()
        for r in rows: print(r)
    elif a == 3:
        cur.execute("SELECT * FROM phonebook23 ORDER BY id")
        for r in cur.fetchall(): print(r)

def deleting_data_from_table():
    print("1 - delete by first name, 2 - delete by second name, 3 - delete by phone number")
    a = int(input())
    if a == 1:
        print("Enter first name:")
        first = input()
        cur.execute("DELETE FROM phonebook23 WHERE first_name = %s", (first,))
        conn.commit()
    elif a == 2:
        print("Enter second name:")
        second = input()
        cur.execute("DELETE FROM phonebook23 WHERE second_name = %s", (second,))
        conn.commit()
    else:
        print("Enter phone number:")
        phonenumber = input()
        cur.execute("DELETE FROM phonebook23 WHERE id IN (SELECT contact_id FROM phones WHERE phone = %s)", (phonenumber,))
        conn.commit()
    print("Record deleted.")




def pattern():
    print("Search object (pattern):")
    x = input()
    cur.execute("SELECT * FROM get_user_name_or_phone_number_by_pattern(%s)", (x,))
    for row in cur.fetchall(): print(row)

def pagination():
    print("Type limit:")
    lim = int(input())
    print("How many rows you want to skip firstly?")
    off_set = int(input())
    cur.execute("SELECT * FROM show_with_pagination(%s, %s)", (lim, off_set))
    for row in cur.fetchall(): print(row)

def upsert():
    print("Type your first name:")
    name_one = input()
    print("Type your second name:")
    name_two = input()
    print("Type your phone number:")
    p_phone_number = input()
    cur.execute("CALL upsert_contact(%s, %s, %s)", (name_one, name_two, p_phone_number))
    conn.commit()
    print("Upsert executed.")

def delete():
    print("Delete by what object: type it")
    x = input()
    cur.execute("CALL delete_by_name_or_phonenumber(%s)", (x,))
    conn.commit()
    print("Procedure executed.")

def validate():
    print("How many rows?")
    n = int(input())
    print("1name: 2name: phone_number:")
    name_one = []
    name_two = []
    phone = []
    for _ in range(n):
        a, b, c = input().split()
        name_one.append(a)
        name_two.append(b)
        phone.append(c)
    cur.execute("CALL validate_phone_correctness(%s, %s, %s)", (name_one, name_two, phone))
    conn.commit()
    print("Validation finished.")




def filter_by_group():
    print("Enter group name:")
    g_name = input()
    cur.execute("SELECT c.first_name, c.second_name, c.email FROM phonebook23 c JOIN groups g ON c.group_id = g.id WHERE g.name ILIKE %s", (g_name,))
    for row in cur.fetchall(): print(row)

def search_by_email():
    print("Enter part of email:")
    email_q = input()
    cur.execute("SELECT first_name, second_name, email FROM phonebook23 WHERE email ILIKE %s", ('%' + email_q + '%',))
    for row in cur.fetchall(): print(row)

def sort_results():
    print("Select sort order: 1 - By Name, 2 - By Birthday, 3 - By Date Added")
    c = int(input())
    col = "first_name" if c == 1 else "birthday" if c == 2 else "date_added"
    cur.execute(f"SELECT first_name, second_name, email FROM phonebook23 ORDER BY {col}")
    for row in cur.fetchall(): print(row)

def paginated_navigation():
    print("How many records per page?")
    limit = int(input())
    offset = 0
    while True:
        cur.execute("SELECT * FROM show_with_pagination(%s, %s)", (limit, offset))
        rows = cur.fetchall()
        for row in rows: print(row)
        
        print("\nNavigation: [n]ext, [p]rev, [q]uit")
        cmd = input().lower()
        if cmd == 'n': offset += limit
        elif cmd == 'p' and offset >= limit: offset -= limit
        elif cmd == 'q': break

def export_to_json():
    cur.execute("""
        SELECT c.id, c.first_name, c.second_name, c.email, c.birthday, g.name as group_name,
               ARRAY_REMOVE(ARRAY_AGG(p.phone), NULL) as phones
        FROM phonebook23 c
        LEFT JOIN phones p ON c.id = p.contact_id
        LEFT JOIN groups g ON c.group_id = g.id
        GROUP BY c.id, g.name
    """)
    rows = cur.fetchall()
    contacts_data = []
    for r in rows:
        contacts_data.append({
            "id": r[0], "first_name": r[1], "second_name": r[2],
            "email": r[3], "birthday": str(r[4]) if r[4] else None,
            "group": r[5], "phones": r[6]
        })
    with open('contacts.json', 'w', encoding='utf-8') as f:
        json.dump(contacts_data, f, indent=4, ensure_ascii=False)
    print("Data saved to contacts.json.")

def import_from_json():
    if not os.path.exists('contacts.json'):
        print("contacts.json file not found."); return
        
    with open('contacts.json', 'r', encoding='utf-8') as f:
        contacts = json.load(f)
        
    for c in contacts:
        cur.execute("SELECT id FROM phonebook23 WHERE first_name = %s AND second_name = %s", (c['first_name'], c['second_name']))
        exists = cur.fetchone()
        
        action = 'i'
        if exists:
            print(f"Duplicate found for {c['first_name']} {c['second_name']}. Press [s] to skip or [o] to overwrite:")
            action = input().lower()
            if action == 's': continue

        group_id = None
        if c.get('group'):
            cur.execute("SELECT id FROM groups WHERE name = %s", (c['group'],))
            g_row = cur.fetchone()
            if g_row: 
                group_id = g_row[0]
            else:
                cur.execute("INSERT INTO groups (name) VALUES (%s) RETURNING id", (c['group'],))
                group_id = cur.fetchone()[0]

        if action == 'o' and exists:
            cur.execute("UPDATE phonebook23 SET email = %s, birthday = %s, group_id = %s WHERE id = %s", 
                        (c.get('email'), c.get('birthday'), group_id, exists[0]))
            contact_id = exists[0]
        else:
            cur.execute("INSERT INTO phonebook23 (first_name, second_name, email, birthday, group_id) VALUES (%s, %s, %s, %s, %s) RETURNING id", 
                        (c['first_name'], c['second_name'], c.get('email'), c.get('birthday'), group_id))
            contact_id = cur.fetchone()[0]
            
        cur.execute("DELETE FROM phones WHERE contact_id = %s", (contact_id,))
        for phone in c.get('phones', []):
            cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, 'mobile')", (contact_id, phone))
            
    conn.commit()
    print("JSON import completed.")

def add_phone_proc():
    name = input("Contact name: ")
    phone = input("Phone number: ")
    t = input("Type (home/work/mobile): ")
    cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, t))
    conn.commit()
    print("Procedure executed.")

def move_to_group_proc():
    name = input("Contact name: ")
    group = input("Group name: ")
    cur.execute("CALL move_to_group(%s, %s)", (name, group))
    conn.commit()
    print("Procedure executed.")

def advanced_search_proc():
    q = input("Enter search query: ")
    cur.execute("SELECT * FROM search_contacts(%s)", (q,))
    for row in cur.fetchall(): print(row)



def menu():
    create_table()
    while True:
        print("\n=== FULL PHONEBOOK MENU ===")
        print("1 - Exit")
        print("2 - Import from CSV")
        print("3 - Add contact via console (P7)")
        print("4 - Update data (P7)")
        print("5 - Basic querying (P7)")
        print("6 - Delete record via Python (P7)")
        print("7 - Search by pattern function (P8)")
        print("8 - Fetch with pagination function (P8)")
        print("9 - Upsert procedure (P8)")
        print("10 - Delete via procedure (P8)")
        print("11 - Validate phone correctness procedure (P8)")
        print("12 - Filter by group (Task 3)")
        print("13 - Search by email (Task 3)")
        print("14 - Sort results (Task 3)")
        print("15 - Paginated loop navigation (Task 3)")
        print("16 - Export to JSON (Task 3)")
        print("17 - Import from JSON (Task 3)")
        print("18 - Procedure: Add phone (Task 3)")
        print("19 - Procedure: Move to group (Task 3)")
        print("20 - Function: Advanced search (Task 3)")
        
        a = int(input("\nEnter choice number: "))
        if a == 1: break
        elif a == 2: upload_data_from_csv_file()
        elif a == 3: upload_data_from_console()
        elif a == 4: change_name_or_phone()
        elif a == 5: querying_data_from_the_table()
        elif a == 6: deleting_data_from_table()
        elif a == 7: pattern()
        elif a == 8: pagination()
        elif a == 9: upsert()
        elif a == 10: delete()
        elif a == 11: validate()
        elif a == 12: filter_by_group()
        elif a == 13: search_by_email()
        elif a == 14: sort_results()
        elif a == 15: paginated_navigation()
        elif a == 16: export_to_json()
        elif a == 17: import_from_json()
        elif a == 18: add_phone_proc()
        elif a == 19: move_to_group_proc()
        elif a == 20: advanced_search_proc()

menu()
cur.close()
conn.close()