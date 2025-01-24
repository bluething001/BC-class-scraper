import sqlite3
import json

def init_db(db_path="/Users/alexguo/Desktop/BC class scraper/scraper_database.db"):
    conn = sqlite3.connect(db_path)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS AvailToEmail (
            availabilityID TEXT PRIMARY KEY,
            email TEXT
        )
    ''')
    return conn

def add_availToEmail(conn, availabilityKey, email):
    """
    Add a (key, email) pair to the AvailToEmail table:
      - If the key doesn't exist, store the email.
      - If the key exists, only add the email if it does not already exist in the list.
    """
    cursor = conn.cursor()

    # Try to fetch the existing row for this key
    cursor.execute("SELECT email FROM AvailToEmail WHERE availabilityID = ?", (availabilityKey,))
    row = cursor.fetchone()

    if row is None:
        # Key not found -> insert new row
        cursor.execute(
            "INSERT INTO AvailToEmail (availabilityID, email) VALUES (?, ?)",
            (availabilityKey, json.dumps([email]))  # Store the email as a list
        )
        print(f"Added email '{email}' to new key: {availabilityKey}")
    else:
        # Key exists -> parse existing JSON
        existing_data = json.loads(row[0])

        # Ensure the data is a list
        if not isinstance(existing_data, list):
            existing_data = [existing_data]

        # Only add the email if it doesn't already exist
        if email not in existing_data:
            existing_data.append(email)
            cursor.execute(
                "UPDATE AvailToEmail SET email = ? WHERE availabilityID = ?",
                (json.dumps(existing_data), availabilityKey)
            )
            print(f"Added email '{email}' to existing key: {availabilityKey}")
        else:
            print(f"Email '{email}' already exists for key: {availabilityKey}")

    conn.commit()

def get_availToEmail(conn, availabilityID):
    """
    Retrieve the value(s) for the given key as Python data.
    Could be a single value or a list of values,
    depending on how many times you've appended.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM AvailToEmail WHERE availabilityID = ?", (availabilityID,))
    row = cursor.fetchone()
    if row is None:
        return None
    return json.loads(row[0])

def remove_availToEmail(conn, availabilityKey, email):
    """
    Remove a specific email from the list of emails mapped to an availabilityKey.
    - If the email exists in the list, remove it.
    - If it's the last email, delete the row for the key.
    - If the key or email doesn't exist, do nothing.
    """
    cursor = conn.cursor()

    # Fetch the existing emails for the given key
    cursor.execute("SELECT email FROM AvailToEmail WHERE availabilityID = ?", (availabilityKey,))
    row = cursor.fetchone()

    if row is None:
        # Key not found -> Nothing to remove
        print(f"No entry found for key: {availabilityKey}")
        return

    # Parse the existing data
    existing_emails = json.loads(row[0])

    if email in existing_emails:
        # Remove the email from the list
        existing_emails.remove(email)

        if not existing_emails:
            # If the list is now empty, delete the row
            cursor.execute("DELETE FROM AvailToEmail WHERE availabilityID = ?", (availabilityKey,))
        else:
            # Update the row with the modified list
            cursor.execute(
                "UPDATE AvailToEmail SET email = ? WHERE availabilityID = ?",
                (json.dumps(existing_emails), availabilityKey)
            )

        conn.commit()
        print(f"Removed email '{email}' for key: {availabilityKey}")
    else:
        # Email not found in the list
        print(f"Email '{email}' not found for key: {availabilityKey}")




conn = init_db()
add_availToEmail(conn, "fruit", "apple")
print(get_availToEmail(conn, "fruit"))  
# Output: "apple"

# Second insert, same key => becomes a list
add_availToEmail(conn, "fruit", "banana")
print(get_availToEmail(conn, "fruit"))  
# Output: ["apple", "banana"]

# Third insert, same key => already a list, so just append
add_availToEmail(conn, "fruit", "orange")
print(get_availToEmail(conn, "fruit"))

add_availToEmail(conn, "color", "orange")
add_availToEmail(conn, "color", "blue")
add_availToEmail(conn, "color", "red")
print(get_availToEmail(conn, "color"))