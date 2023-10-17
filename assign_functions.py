from fastapi import FastAPI, HTTPException, Body
import psycopg2
from models import *
from datetime import datetime
from add_functions import *
from delete_functions import *
from update_creation import *
from get_functions import *
import uvicorn
import pandas as pd

app = FastAPI()

DB_CREDENTIAL = {
    "user": "amadou-bely_guisse",
    "password": "",
    "host": "localhost",
    "port": 5432,
    "database": "sense4data_db"
}

# Fonction pour ajouter une tâche à la table "task"
@app.post('/task/add/')
def add_task_route(title: str, description: str, creation_date: str, completed: bool):
    result = add_task(title, description, creation_date, completed, DB_CREDENTIAL)
    return result

# Fonction pour ajouter une personne à la table "person"
@app.post('/person/add/')
def add_person_route(prenom: str, nom: str):
    result = add_person(prenom, nom, DB_CREDENTIAL)
    return result

# Fonction pour attribuer une tâche à une personne
@app.post('/task/assign_task')
def assign_task_route(task_id: int, person_id: int):
    result = assign_task_to_person(task_id, person_id, DB_CREDENTIAL)
    return result

# Fonction pour attribuer une personne à une tâche
@app.post('/person/assign_person')
def assign_person_route(task_id: int, person_id: int):
    result = assign_person_to_task(task_id, person_id, DB_CREDENTIAL)
    return result

# Fonction pour mettre à jour une tâche par son ID
@app.put('/task/update/{task_id}')
def update_task_route(task_id: int, update_values: dict):
    result = update_task(task_id, update_values, DB_CREDENTIAL)
    return result

# Fonction pour mettre à jour une personne par son ID
@app.put('/person/update/{person_id}')
def update_person_route(person_id: int, update_values: dict):
    result = update_person(person_id, update_values, DB_CREDENTIAL)
    return result

# Fonction pour supprimer une tâche par son ID
@app.delete('/task/delete/{task_id}')
def delete_task_route(task_id: int):
    result = delete_task(task_id, DB_CREDENTIAL)
    return result

# Fonction pour supprimer une personne par son ID
@app.delete('/person/delete/{person_id}')
def delete_person_route(person_id: int):
    result = delete_person(person_id, DB_CREDENTIAL)
    return result

# Fonction pour récupérer toutes les tâches
@app.get('/task/table')
def get_all_task_route():
    result = get_all_task(DB_CREDENTIAL)
    if result is not None:
        return result
    else:
        raise HTTPException(status_code=404, detail="Aucune tâche trouvée.")

# Fonction pour récupérer toutes les personnes
@app.get('/person/table')
def get_all_person_route():
    result = get_all_person(DB_CREDENTIAL)
    if result is not None:
        return result
    else:
        raise HTTPException(status_code=404, detail="Aucune personne trouvée.")

# Fonction pour récupérer les détails d'une tâche par son ID
@app.get('/task/{task_id}')
def get_task_route(task_id: int):
    result = get_task_details(task_id, DB_CREDENTIAL)
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="Cette tâche n'existe pas.")

# Fonction pour récupérer les détails d'une personne par son ID
@app.get('/person/{person_id}')
def get_person_route(person_id: int):
    result = get_person_details(person_id, DB_CREDENTIAL)
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="Cette personne n'existe pas.")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)