import sqlite3

# Function to connect to the SQLite database
def connect_db():
    conn = sqlite3.connect('example.db')  # Connect to your database file
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS pictures (
                        name TEXT PRIMARY KEY,
                        status BOOLEAN DEFAULT FALSE)''')
    conn.commit()
    return conn

# Function to insert a new name with status default as False
def insert_name(name):
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''INSERT INTO pictures (name, status) VALUES (?, ?)''', (name, False))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Name '{name}' already exists.")
    
    conn.close()

# Function to fetch all names where status is False
def fetch_names_with_status_false():
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('''SELECT name FROM pictures WHERE status = FALSE''')
    names = cursor.fetchall()
    
    conn.close()
    return [name[0] for name in names]

# Function to update the status of a name to True
def update_status_to_true(name):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('''UPDATE pictures SET status = TRUE WHERE name = ?''', (name,))
    conn.commit()
    
    if cursor.rowcount == 0:
        print(f"No name found for '{name}'.")
    
    conn.close()

# Example Usage
if __name__ == "__main__":
    # Insert some names
    insert_name("Image1")
    insert_name("Image2")

    # Fetch all names with status False
    print("Names with status False:", fetch_names_with_status_false())
    
    # Update Image2's status to True
    update_status_to_true("Image2")
    
    # Fetch again to see the result
    print("Names with status False after update:", fetch_names_with_status_false())
