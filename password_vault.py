import sqlite3

# Connect to SQLite DB (will create it if not exists)
conn = sqlite3.connect('password_vault.sqlite')
cur = conn.cursor()

# Create table if not exists
cur.execute('''
CREATE TABLE IF NOT EXISTS Vault (
    website TEXT PRIMARY KEY,
    username TEXT,
    password TEXT
)
''')
conn.commit()

while True:
    print("\n🔐 Password Locker")
    print("1. Add Login")
    print("2. Search Login")
    print("3. Edit Login")
    print("4. Delete Login")
    print("5. Show All Logins")
    print("6. Exit")

    choice = input("Enter Your Choice: ")

    # 1. Add Login
    if choice == "1":
        website = input("Enter Website: ").strip().lower()
        username = input("Enter Username: ")
        password = input("Enter Password: ")

        cur.execute('''
            INSERT OR REPLACE INTO Vault (website, username, password)
            VALUES (?, ?, ?)
        ''', (website, username, password))
        conn.commit()
        print("✅ Login added successfully!")

    # 2. Search Login
    elif choice == "2":
        website_search = input("Enter Website to search: ").strip().lower()
        cur.execute('SELECT username, password FROM Vault WHERE website = ?', (website_search,))
        row = cur.fetchone()

        if row:
            print("🔍 Login Found:")
            print(f"Username: {row[0]}")
            print(f"Password: {row[1]}")
        else:
            print("❌ Login not found.")

    # 3. Edit Login
    elif choice == "3":
        edit_website = input("Enter Website to Edit: ").strip().lower()
        cur.execute('SELECT * FROM Vault WHERE website = ?', (edit_website,))
        if cur.fetchone():
            new_username = input("Enter new username: ")
            new_password = input("Enter new password: ")
            cur.execute('''
                UPDATE Vault SET username = ?, password = ? WHERE website = ?
            ''', (new_username, new_password, edit_website))
            conn.commit()
            print("✅ Login updated successfully!")
        else:
            print("❌ Website not found.")

    # 4. Delete Login
    elif choice == "4":
        delete_website = input("Enter Website to Delete Login: ").strip().lower()
        cur.execute('SELECT * FROM Vault WHERE website = ?', (delete_website,))
        if cur.fetchone():
            cur.execute('DELETE FROM Vault WHERE website = ?', (delete_website,))
            conn.commit()
            print("🗑️ Login deleted successfully!")
        else:
            print("❌ Website not found.")

    # 5. Show All Logins
    elif choice == "5":
        cur.execute('SELECT website, username, password FROM Vault')
        rows = cur.fetchall()

        if not rows:
            print("📭 No logins stored yet.")
        else:
            print("📋 All Saved Logins:")
            for site, user, pwd in rows:
                print(f"\nWebsite: {site}")
                print(f"Username: {user}")
                print(f"Password: {pwd}")

    # 6. Exit
    elif choice == "6":
        conn.close()
        print("👋 Exiting Password Locker. Stay safe!")
        break

    else:
        print("⚠️ Invalid choice. Please enter a number from 1 to 6.")
