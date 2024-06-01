from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)
azmedicines = pd.read_csv('../../Downloads/all_medicines.csv')

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
        # Return the medicine directly if it's a single record
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
        azmedicines = azmedicines.append(new_medicine, ignore_index=True)
        # Save the updated DataFrame to the CSV file
        azmedicines.to_csv('../../Downloads/all_medicines.csv', index=False)
        return jsonify(new_medicine), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Update a medicine by id
@app.route('/all_medicines/<int:id>', methods=['PUT'])
def update_medicine(id):
    try:
        medicine_index = azmedicines.index[azmedicines['id'] == id]
        if not medicine_index.empty:
            data = request.json
            azmedicines.loc[medicine_index[0]] = data  # Use the first index value
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
        azmedicines = azmedicines.drop(azmedicines[azmedicines['id'] == id].index)
        return jsonify({"message": "Medicine deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
