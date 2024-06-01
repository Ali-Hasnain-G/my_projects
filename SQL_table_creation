import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Dropping tables if they exist to ensure a fresh start
cursor.execute('DROP TABLE IF EXISTS users')

# Creating users tables with schema
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    age INTEGER,
                    address TEXT,
                    contact_method TEXT)''')

# Inserting sample data into users, orders, Customers and Students
cursor.execute('''INSERT INTO users (name, age) VALUES
                  ('Alice', 30),
                  ('Bob', 24),
                  ('Charlie', 29)''')
conn.commit()

# Function to count rows in each table
def count_rows(table_name):
    cursor.execute(f'SELECT COUNT(*) FROM {table_name}')
    count = cursor.fetchone()[0]
    return count

# Function to show a sample of 3 rows from each table
def show_sample_rows(table_name):
    cursor.execute(f'SELECT * FROM {table_name} LIMIT 3')
    rows = cursor.fetchall()
    return rows

# Count of rows for each table
tables = ['users']
for table in tables:
    print(f"Count of rows in {table}: {count_rows(table)}")

# Show sample of 3 rows from each table
for table in tables:
    print(f"\nSample rows from {table}:")
    rows = show_sample_rows(table)
    for row in rows:
        print(row)


# Close the connection
conn.close()
