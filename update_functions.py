from fastapi import HTTPException
from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2


DB_CREDENTIAL = {
    "user": "amadou-bely_guisse",
    "password": "",
    "host": "localhost",
    "port": 5432,
    "database": "sense4data_db"
}


app = FastAPI()


DB_CREDENTIAL = {
    "user": "amadou-bely_guisse",
    "password": "",
    "host": "localhost",
    "port": 5432,
    "database": "sense4data_db"
}

class PersonUpdate(BaseModel):
    nom: str
    prenom: str


class TaskUpdate(BaseModel):
    title: str
    description: str
    creation_date: str
    completed: bool


def update_task(task_id: int, update_values: TaskUpdate):
    try:
        connection = psycopg2.connect(**DB_CREDENTIAL)
        cursor = connection.cursor()

        # Vérifier si la tâche existe
        cursor.execute("SELECT 1 FROM task WHERE id = %s", (task_id,))
        task_exists = cursor.fetchone()

        if not task_exists:
            raise HTTPException(status_code=404, detail="Cette tâche n'existe pas.")

        # Mettre à jour les données de la tâche
        cursor.execute("UPDATE task SET title = %s, description = %s, creation_date = %s, completed = %s WHERE id = %s",
                       (update_values.title, update_values.description, update_values.creation_date, update_values.completed, task_id))

        connection.commit()
        cursor.close()
        connection.close()

        return {"message": "Tâche mise à jour avec succès."}

    except (Exception, psycopg2.Error) as error:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la mise à jour de la tâche : {error}")


def update_person(person_id: int, update_values: PersonUpdate):
    try:
        connection = psycopg2.connect(**DB_CREDENTIAL)
        cursor = connection.cursor()

        # Vérifier si la personne existe
        cursor.execute("SELECT 1 FROM person WHERE id = %s", (person_id,))
        person_exists = cursor.fetchone()

        if not person_exists:
            raise HTTPException(status_code=404, detail="Cette personne n'existe pas.")

        # Mettre à jour les données de la personne
        cursor.execute("UPDATE person SET nom = %s, prenom = %s WHERE id = %s",
                       (update_values.nom, update_values.prenom, person_id))

        connection.commit()
        cursor.close()
        connection.close()

        return {"message": "Personne mise à jour avec succès."}

    except (Exception, psycopg2.Error) as error:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la mise à jour de la personne : {error}")
