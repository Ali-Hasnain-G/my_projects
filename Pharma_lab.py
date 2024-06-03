from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)
azmedicines = pd.read_csv(r"F:\Full Stack Development\datasets\all_medicines.csv")

# Convert the DataFrame to a list of dictionaries
azmedicines_dict = azmedicines.to_dict(orient='records')

# Display the first few rows of the DataFrame
print(azmedicines_dict[:5])

# Error handler for invalid routes
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not Found"}), 404

# Get all medicines
@app.route('/all_medicines', methods=['GET'])
def get_medicines():
    return jsonify(azmedicines.to_dict(orient='records'))

# Get a specific medicine by id
@app.route('/all_medicines/<int:id>', methods=['GET'])
def get_medicine(id):
    # Check if the ID is valid
    if id < 0:
        return jsonify({"error": "Invalid ID"}), 400

    # Check if the medicine exists
    medicine = azmedicines.loc[azmedicines['id'] == id].to_dict(orient='records')
    if medicine:
        return jsonify(medicine[0])
    else:
        return jsonify({"error": "Medicine not found"}), 404

# Add a new medicine
@app.route('/all_medicines', methods=['POST'])
def add_medicine():
    global azmedicines
    try:
        new_medicine = request.json
        # Ensure the 'id' of the new medicine is unique
        if new_medicine['id'] in azmedicines['id'].tolist():
            return jsonify({"error": "ID already exists"}), 400
        # Append the new medicine to the DataFrame
        new_row = pd.DataFrame([new_medicine])
        azmedicines = pd.concat([azmedicines, new_row], ignore_index=True)
        # Save the updated DataFrame to the CSV file
        azmedicines.to_csv(r"F:\Full Stack Development\datasets\all_medicines.csv", index=False)
        return jsonify(new_medicine), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Update a medicine by id
@app.route('/all_medicines/<int:id>', methods=['PUT'])
def update_medicine(id):
    try:
        medicine_index = azmedicines.index[azmedicines['id'] == id].tolist()
        if medicine_index:
            data = request.json
            azmedicines.loc[medicine_index[0]] = data  # Use the first index value
            # Save the updated DataFrame to the CSV file
            azmedicines.to_csv(r"F:\Full Stack Development\datasets\all_medicines.csv", index=False)
            return jsonify(azmedicines.loc[medicine_index[0]].to_dict()), 200
        else:
            return jsonify({"error": "Medicine not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Delete a medicine by ID
@app.route('/all_medicines/<int:id>', methods=['DELETE'])
def delete_medicine(id):
    try:
        global azmedicines
        medicine_index = azmedicines.index[azmedicines['id'] == id].tolist()
        if medicine_index:
            azmedicines = azmedicines.drop(medicine_index[0])
            # Save the updated DataFrame to the CSV file
            azmedicines.to_csv(r"F:\Full Stack Development\datasets\all_medicines.csv", index=False)
            return jsonify({"message": "Medicine deleted"}), 200
        else:
            return jsonify({"error": "Medicine not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
