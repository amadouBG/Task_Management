from flask import Flask, request, jsonify 
import psycopg2
from psycopg2.extras import RealDictCursor
from models import *
from datetime import datetime

DB_CREDENTIAL = {
    "user": "amadou-bely_guisse",
    "password": "",
    "host": "localhost",
    "port": 5432,
    "database": "sense4data_db"
}

app = Flask(__name__)

# Route pour récupérer toutes les tâches
@app.route('/task/table', methods=['GET'])
def get_all_task_route():
    result = get_all_task(DB_CREDENTIAL)
    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "Aucune tâche trouvée."})


# Route pour récupérer toutes les tâches
@app.route('/person/table', methods=['GET'])
def get_all_person_route():
    result = get_all_person(DB_CREDENTIAL)
    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "Aucune tâche trouvée."})


# Route pour récupérer les détails d'une tâche par son ID
@app.route('/task/<int:task_id>', methods=['GET'])
def get_task(task_id: int):
    task_details = get_task_details(task_id=task_id, database_credential=DB_CREDENTIAL)
    if not task_details:
        task_details = {
            "status": "success",
            "message": f"Cette tâche n'existe pas."
        }
    return task_details

# Route pour récupérer les détails d'une tâche par son ID
@app.route('/person/<int:person_id>', methods=['GET'])
def get_person(person_id: int):
    person_details = get_person_details(person_id=person_id, database_credential=DB_CREDENTIAL)
    if not person_details:
        person_details = {
            "status": "success",
            "message": f"Cette personne n'existe pas."
        }
    return person_details


# Route pour créer une nouvelle tâche
@app.route('/task/add/', methods=['POST'])
def add_task_route():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    creation_date = datetime.now().isoformat()
    completed = False

    if title is None or description is None :
        return jsonify({"error": "Les champs 'title', 'description' sont requis."}), 400
    return add_task(title, description, creation_date, completed, DB_CREDENTIAL)


# Route pour créer une nouvelle tâche
@app.route('/person/add/', methods=['POST'])
def add_person_route():
    data = request.get_json()
    nom = data.get('nom')
    prenom = data.get('prenom')

    if nom is None or prenom is None :
        return jsonify({"error": "Les champs 'nom', 'prenom' sont requis."}), 400
    return add_person(prenom, nom, DB_CREDENTIAL)


@app.route('/task/assign_task/<int:task_id>/<int:person_id>', methods=['POST'])
def assign_task_route(task_id: int , person_id: int):
    data = request.get_json()
    task_id = data.get('task_id')
    person_id = data.get('person_id')

    if task_id is None or person_id is None :
        return jsonify({"error": "les champs 'task_id', 'person_id' sont requis."}), 400
    
    return assign_task_to_person(task_id=task_id, person_id=person_id, database_credential=DB_CREDENTIAL)


@app.route('/person/assign_person/<int:task_id>/<int:person_id>', methods=['POST'])
def assign_person_route(task_id: int , person_id: int):
    data = request.get_json()
    task_id = data.get('task_id')
    person_id = data.get('person_id')

    if task_id is None or person_id is None :
        return jsonify({"error": "les champs 'task_id', 'person_id' sont requis."}), 400
    
    return assign_person_to_task(task_id=task_id, person_id=person_id, database_credential=DB_CREDENTIAL)


# Route pour mettre à jour une tâche par son ID
@app.route('/task/update/<int:task_id>', methods=['POST'])
def update_task_route(task_id):
    data = request.get_json()
    return jsonify(update_task(task_id=task_id, update_values=data, database_credential=DB_CREDENTIAL))


# Route pour mettre à jour une personne par son ID
@app.route('/person/update/<int:person_id>', methods=['POST'])
def update_person_route(person_id):
    data = request.get_json()
    return jsonify(update_person(person_id=person_id, update_values=data, database_credential=DB_CREDENTIAL))


# Route pour supprimer une tâche par son ID
@app.route('/task/delete/<int:task_id>', methods=['DELETE'])
def delete_task_route(task_id: int):
   return delete_task(task_id=task_id, database_credential=DB_CREDENTIAL)

# Route pour supprimer une tâche par son ID
@app.route('/person/delete/<int:person_id>', methods=['DELETE'])
def delete_person_route(person_id: int):
   return delete_person(person_id=person_id, database_credential=DB_CREDENTIAL)


if __name__ == '__main__':

    app.run(debug=True)

