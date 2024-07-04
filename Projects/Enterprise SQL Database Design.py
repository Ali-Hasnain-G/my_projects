                          # SQL_database project


        #01# Python program to connect to a relational database to show following from your 
        #structured data model.
          # Count of rows of each table
          # Show a sample of 3 rows from each table
          # Use a join (any type) to show data among two tables using the primary key and foreign key 
          #relationship


import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Dropping tables if they exist to ensure a fresh start
cursor.execute('DROP TABLE IF EXISTS users')
cursor.execute('DROP TABLE IF EXISTS orders')
cursor.execute('DROP TABLE IF EXISTS Customers')
cursor.execute('DROP TABLE IF EXISTS Students')

# Creating users tables with schema
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    age INTEGER,
                    address TEXT)''')

# Creating orders tables with schema
cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                    order_id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    product TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(id))''')

# Creating Customers tables with schema
cursor.execute('''CREATE TABLE IF NOT EXISTS Customers (
                    Customer_id INTEGER PRIMARY KEY,
                    Customer_name TEXT,
                    products TEXT,
                    city TEXT,
                    Address TEXT)''')

# Creating Students tables with schema
cursor.execute('''CREATE TABLE IF NOT EXISTS Students (
                    Student_id INTEGER PRIMARY KEY,
                    Student_name TEXT,
                    Student_Roll_no INTEGER,
                    Grade TEXT,
                    Address TEXT)''')

# Inserting sample data into users, orders, Customers and Students
cursor.execute('''INSERT INTO users (name, age) VALUES
                  ('Alice', 30),
                  ('Bob', 24),
                  ('Charlie', 29)''')

# Inserting sample data into orders
cursor.execute('''INSERT INTO orders (user_id, product) VALUES
                  (1, 'Laptop'),
                  (2, 'Smartphone'),
                  (3, 'Tablet'),
                  (4, 'America')''')

# Inserting sample data into Customers
cursor.execute('''INSERT INTO Customers (Customer_name, products, city, Address) VALUES
                  ('Alice', 'PC', 'Lahore', 'pk'),
                  ('Bob', 'Mobile_phone', 'Quetta', 'pk'),
                  ('Charlie', 'Tab', 'Sahiwal', 'pk')''')

# Data insertion into Students table
cursor.execute('''INSERT INTO Students (Student_id, Student_name, Student_Roll_no, Grade, Address) VALUES
                  (1, 'John Doe', 101, 'A', '123 Elm St'),
                  (2, 'Jane Doe', 102, 'B', '456 Oak St'),
                  (3, 'Jim Beam', 103, 'C', '789 Pine St')''')

conn.commit()

# Function to count rows in each table
def count_rows(table_name):
    cursor.execute(f'SELECT COUNT(*) FROM {table_name}')
    count = cursor.fetchone()[0]
    return count

# Function to show a sample of 3 rows from each table
def show_sample_rows(table_name):
    cursor.execute(f'SELECT * FROM {table_name} LIMIT 1')
    rows = cursor.fetchall()
    return rows

# Count of rows for each table
tables = ['users', 'orders', 'Customers', 'Students']
for table in tables:
    print(f"Count of rows in {table}: {count_rows(table)}")

# Show sample of 3 rows from each table
for table in tables:
    print(f"\nSample rows from {table}:")
    rows = show_sample_rows(table)
    for row in rows:
        print(row)

# Join operations using primary key and foreign key relationship with LIMIT
def show_inner_join(limit):
    cursor.execute(f'''SELECT users.id, users.name, orders.product, Customers.city
                      FROM users
                      INNER JOIN orders ON users.id = orders.user_id
                      INNER JOIN Customers ON users.name = Customers.Customer_name
                      LIMIT {limit}''')
    rows = cursor.fetchall()
    return rows

def show_left_join(limit):
    cursor.execute(f'''SELECT users.id, users.name, orders.product, Customers.city
                      FROM users
                      LEFT JOIN orders ON users.id = orders.user_id
                      LEFT JOIN Customers ON users.name = Customers.Customer_name
                      LIMIT {limit}''')
    rows = cursor.fetchall()
    return rows

# Simulating RIGHT JOIN using LEFT JOIN by reversing the order of tables
def show_right_join(limit):
    cursor.execute(f'''SELECT users.id, users.name, orders.product, Customers.city
                      FROM orders
                      LEFT JOIN users ON orders.user_id = users.id
                      LEFT JOIN Customers ON users.name = Customers.Customer_name
                      LIMIT {limit}''')
    rows = cursor.fetchall()
    return rows

# Simulating FULL OUTER JOIN using UNION of LEFT JOIN and RIGHT JOIN with LIMIT
def show_full_outer_join(limit):
    cursor.execute(f'''SELECT users.id, users.name, orders.product, Customers.city
                      FROM users
                      LEFT JOIN orders ON users.id = orders.user_id
                      LEFT JOIN Customers ON users.name = Customers.Customer_name
                      UNION
                      SELECT users.id, users.name, orders.product, Customers.city
                      FROM orders
                      LEFT JOIN users ON orders.user_id = users.id
                      LEFT JOIN Customers ON users.name = Customers.Customer_name
                      LIMIT {limit}''')
    rows = cursor.fetchall()
    return rows

# Show joined data with limit
limit = ()
print("\nInner Join data from users, orders, and Customers:")
inner_joined_rows = show_inner_join(limit=1)
for row in inner_joined_rows:
    print(row)

print("\nLeft Join data from users, orders, and Customers:")
left_joined_rows = show_left_join(limit=1)
for row in left_joined_rows:
    print(row)

print("\nRight Join data from users, orders, and Customers (simulated):")
right_joined_rows = show_right_join(limit=1)
for row in right_joined_rows:
    print(row)

print("\nFull Outer Join data from users, orders, and Customers (simulated):")
full_outer_joined_rows = show_full_outer_join(limit=1)
for row in full_outer_joined_rows:
    print(row)

# Close the connection
conn.close()