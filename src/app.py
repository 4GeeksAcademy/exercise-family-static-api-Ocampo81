"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, Response
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Añadir los miembros iniciales
jackson_family.add_member({
    'first_name': 'John',
    'age': 33,
    'id': 1,
    'lucky_numbers': [7, 13, 22]
})

jackson_family.add_member({
    'first_name': 'Jane',
    'age': 35,
    'id': 2,
    'lucky_numbers': [10, 14, 3]
})

jackson_family.add_member({
    'first_name': 'Jimmy',
    'age': 5,
    'id': 3,
    'lucky_numbers': [1]
})


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Obtener todos los miembros de la familia
@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

# Agregar un miembro nuevo
@app.route('/member', methods=['POST'])
def add_member():
    try:
        first_name = request.json.get('first_name')
        age = request.json.get('age')
        lucky_numbers = request.json.get('lucky_numbers')
        id = request.json.get('id')

        if first_name and age and lucky_numbers:
            new_member = {
                'first_name': first_name,
                'id': id,
                'age': age,
                'lucky_numbers': lucky_numbers,
            }
            jackson_family.add_member(new_member)
            return jsonify(new_member), 200
        else:
            return jsonify({'error': 'Fill all inputs'}), 400
    except Exception as e:
        return jsonify({'msg': str(e)}), 500

# Obtener un miembro por su ID
@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    member = jackson_family.get_member(id)
    if member:
        return jsonify(member), 200
    else:
        return jsonify({"error": "Member not found"}), 404

# Eliminar un miembro por su ID
@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    result = jackson_family.delete_member(id)
    if result:
        return jsonify({"done": True}), 200
    else:
        return jsonify({"error": "Member not found"}), 404

# Ejecutar la aplicación
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
