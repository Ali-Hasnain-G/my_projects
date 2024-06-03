                          # No-SQL_database project

     #01# Write a python program to connect to a NoSQLl database to show following from your 
    #   semi-structured data model.
        # Count of rows of each collection
        # Show a sample of 3 doduments (rows) from each collection
        # Use a join (any type) to show data among two collections using the local key and foreign key 
        #   concepts


import pymongo

# Establishing the connection to MongoDB
client = pymongo.MongoClient('mongodb+srv://ali:12345@cluster0.k4xb5ra.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

# Accessing the database and collection
db = client['database']
collection_customers = db['customers']
collection_orders = db['orders']
collection_users = db['users']
collection_students = db['students']

# Documents to be inserted in customers
customers = [
    {"id": "1", "name": "jery", "city": "lahore"},
    {"id": "2", "name": "harry", "city": "washington"},
    {"id": "3", "name": "john", "city": "konya"},
    {"id": "4", "name": "george", "city": "london"}
]

# Documents to be inserted in orders
orders = [
    {"order_id": "1", "product_name": "phone", "user_id": "1"},
    {"order_id": "2", "product_name": "car", "user_id": "2"},
    {"order_id": "3", "product_name": "watch", "user_id": "3"},
    {"order_id": "4", "product_name": "cloth", "user_id": "4"}
]

# Documents to be inserted in users
users = [
    {"id": "1", "name": "Huxley", "city": "Québec City"},
    {"id": "2", "name": "Oaklee", "city": "Toronto"},
    {"id": "3", "name": "Sutton", "city": "Victoria"},
    {"id": "4", "name": "Jack", "city": "Calgary"}
]

# Documents to be inserted in students
students = [
    {"student_id": "1", "name": "Harper", "Grade": "A", "city": "Edmonton"},
    {"student_id": "2", "name": "Madison", "Grade": "B", "city": "Winnipeg"},
    {"student_id": "3", "name": "Willow", "Grade": "A", "city": "Saskatoon"},
    {"student_id": "4", "name": "Ruby", "Grade": "C", "city": "Windsor"}
]

# Inserting the documents into the collections
collection_customers.insert_many(customers)
collection_orders.insert_many(orders)
collection_users.insert_many(users)
collection_students.insert_many(students)

# Function to count documents in each collection
def count_documents(collection):
    return collection.count_documents({})

# Function to show a sample of 2 documents from each collection
def show_sample_documents(collection):
    return list(collection.find().limit(1))

# Count of documents for each collection
collections = {
    'customers': collection_customers,
    'orders': collection_orders,
    'users': collection_users,
    'students': collection_students
}

for name, collection in collections.items():
    print(f"Count of documents in {name}: {count_documents(collection)}")

# Show sample of 2 documents from each collection
for name, collection in collections.items():
    print(f"\nSample documents from {name}:")
    documents = show_sample_documents(collection)
    for doc in documents:
        print(doc)

# Find a single document
document = collection_students.find_one({"name": "Harper"})
print("\nSingle document found:", document)

# Find multiple documents
documents = collection_students.find({"name": "Jack"})
print("\nMultiple documents found:")
for doc in documents:
    print(doc)

# Update a single document
collection_students.update_one({"name": "Ruby"}, {"$set": {"Grade": "B"}})

# Update multiple documents
collection_students.update_many({"Grade": "A"}, {"$set": {"Grade": "A+"}})

# Delete a single document
collection_students.delete_one({"name": "Willow"})

# Delete multiple documents
collection_students.delete_many({"Grade": "C"})

# Join operation using local key and foreign key relationship
def show_joined_data(limit):
    # Define the aggregation pipeline for a join
    pipeline = [
        {
            "$lookup": {
                "from": "users",           # The collection to join with
                "localField": "user_id",   # Field from the orders collection
                "foreignField": "id",      # Field from the users collection
                "as": "user_info"          # Name for the resulting array
            }
        },
        {
            "$unwind": {
                "path": "$user_info",
                "preserveNullAndEmptyArrays": True  # Include documents with no matches
            }
        },
        {
            "$lookup": {
                "from": "customers",       # The collection to join with
                "localField": "user_info.name",  # Field from the users collection
                "foreignField": "name",    # Field from the customers collection
                "as": "customer_info"      # Name for the resulting array
            }
        },
        {
            "$unwind": {
                "path": "$customer_info",
                "preserveNullAndEmptyArrays": True  # Include documents with no matches
            }
        },
        {
            "$project": {                  # Select the fields to include in the result
                "user_id": 1,
                "product_name": 1,
                "user_info.name": 1,
                "customer_info.city": 1
            }
        },
        {
            "$limit": limit  # Limit the number of results
        }
    ]

    # Execute the aggregation pipeline
    result = db.orders.aggregate(pipeline)

    # Print the results
    print("\nJoined data from orders, users, and customers:")
    for doc in result:
        print(doc)

# Show the joined data with a limit of 2 results
show_joined_data(limit=1)

# Close the connection
client.close()
