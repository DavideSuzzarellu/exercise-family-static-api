"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# From models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)
jackson_family = FamilyStructure("Jackson") # Create the jackson family object


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET', 'POST'])
def handle_hello():
    response_body = {}
    # This is how you can use the Family datastructure by calling its methods
    if request.method == 'GET':
        members = jackson_family.get_all_members()
        response_body['hello'] = 'world'
        response_body['family'] = members   
        return jsonify(response_body), 200
    if request.method == 'POST':
        response_body = {}
        data = request.json
        result = jackson_family.add_member(data)
        response_body['message'] = 'Miembro agreagado correctamente'
        response_body['result' ]= result
        return response_body, 200


@app.route('/members/<int:id>', methods=['GET', 'DELETE'])
def handle_member(id):
    response_body = {}
    if request.method == 'GET':
        result = jackson_family.get_member(id)
        if result == []:
            response_body = {'message' : 'No encontrado'}
            return response_body, 405
        response_body['member'] = result
        return response_body, 200
    if request.method == 'DELETE':
        members = jackson_family.get_all_members()
        result = jackson_family.delete_member(id)
        if result != members:
            response_body['message'] = 'Miembro eliminado'
            return response_body, 200
        response_body['message'] = 'Miembro no encontrado'
        return response_body, 400
        


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
