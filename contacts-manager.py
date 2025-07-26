import sqlite3
import re

conn = sqlite3.connect('contacts.sqlite')
cur = conn.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS Contact (
        name TEXT PRIMARY KEY,
        phone_number TEXT,
        email TEXT
    )
''')
conn.commit()

def validate_phone_number(phone_number):
    phone_pattern = re.compile(r'^\+?[\d\s\-\(\)]{7,20}$') # Adjust as per your country's typical phone number format
    if phone_pattern.fullmatch(phone_number):
        return phone_number
    return None

def validate_email(email):
    email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    if email_pattern.fullmatch(email):
        return email
    return None

while True:
    print("\n📇 Contact Manager")
    print("1. Add Contact")
    print("2. Search Contact")
    print("3. Edit Contact")
    print("4. Delete Contact")
    print("5. Show All Contacts")
    print("6. Exit")
    
    choice = input("Enter Your Choice: ").strip()

    if choice == "1":
        name = input("Enter Username: ").strip()
        phone_number_input = input("Enter Mobile Number: ").strip() # Renamed to avoid clash
        email_input = input("Enter Email: ").strip() # Added input for email
        
        # Validate inputs
        validated_phone_number = validate_phone_number(phone_number_input)
        validated_email = validate_email(email_input)

        if validated_phone_number is None:
            print("⚠️ Invalid phone number format. Phone number will not be saved.")
        if validated_email is None:
            print("⚠️ Invalid email format. Email will not be saved.")

        cur.execute('''
            INSERT OR REPLACE INTO Contact(name, phone_number, email)
            VALUES (?, ?, ?)
        ''', (name, validated_phone_number, validated_email)) # Use validated values
        conn.commit()
        print("✅ Contact added successfully!")
        
    #Search Contact
    elif choice == "2":
        search_contact = input("Enter contact name to search:").strip()
        cur.execute('SELECT phone_number,email FROM Contact WHERE name = ?', (search_contact,))
        row = cur.fetchone()
        
        if row:
            phone_display = row[0] if row[0] is not None else "invalid"
            email_display = row[1] if row[1] is not None else "invalid"
            print("Contact Found:")
            print(f"phone_number: {phone_display}")
            print(f"email:{email_display}")
        else:
            print("❌ Contact not found.")
            
    #Edit Contact 
    elif choice == "3":
        edit_contact = input("Enter contact name to edit:").strip() # Changed "data" to "name" for clarity
        cur.execute('SELECT*FROM Contact WHERE name = ?', (edit_contact,))
        if cur.fetchone():
            new_phone_number_input = input("Enter new phone number (leave blank to keep current):").strip()
            new_email_input = input("Enter new email (leave blank to keep current):").strip()
            
            # Fetch current values to allow leaving fields blank
            cur.execute('SELECT phone_number, email FROM Contact WHERE name = ?', (edit_contact,))
            current_phone, current_email = cur.fetchone()

            # Validate and update phone number
            if new_phone_number_input: # Only validate if new input is provided
                validated_new_phone_number = validate_phone_number(new_phone_number_input)
                if validated_new_phone_number is None:
                    print("⚠️ Invalid phone number format. Phone number will not be updated.")
                    new_phone_number_to_save = None # Store as invalid/NULL
                else:
                    new_phone_number_to_save = validated_new_phone_number
            else:
                new_phone_number_to_save = current_phone # Keep current if blank

            # Validate and update email
            if new_email_input: # Only validate if new input is provided
                validated_new_email = validate_email(new_email_input)
                if validated_new_email is None:
                    print("⚠️ Invalid email format. Email will not be updated.")
                    new_email_to_save = None # Store as invalid/NULL
                else:
                    new_email_to_save = validated_new_email
            else:
                new_email_to_save = current_email # Keep current if blank


            cur.execute('''
                UPDATE Contact SET phone_number = ?, email = ? WHERE name = ?''', 
                (new_phone_number_to_save, new_email_to_save, edit_contact))
            conn.commit()
            print("✅ Contact updated successfully!")
        else:
            print("❌ Contact not found")
            
    #Delete Contact 
    elif choice == "4":
        delete_contact = input("Enter contact name to delete: ").strip()
        cur.execute('SELECT*FROM Contact WHERE name = ?', (delete_contact,))
        if cur.fetchone():
            cur.execute('DELETE FROM Contact WHERE name = ?',(delete_contact,))
            conn.commit()
            print("🗑️ Contact deleted successfully!")
        else:
            print("❌ Contact not found.")
            
    #Show All Contacts
    elif choice == "5":
        cur.execute("SELECT name,phone_number,email FROM Contact")
        rows = cur.fetchall()
        
        if not rows:
            print("📭 No Contacts stored yet.")
        else:
            print("📋 All contacts saved:")
            for name,phone_number,email in rows:
                phone_display = phone_number if phone_number is not None else "invalid"
                email_display = email if email is not None else "invalid"
                print(f'\nName: {name}')
                print(f"Phone_number:{phone_display}")
                print(f"email:{email_display}")
                
    #6. Exit
    elif choice == "6":
        conn.close()
        print("👋 Exiting Contact Manager")
        break
    else:
        print("⚠️ Invalid choice. Please enter a number from 1 to 6.")