from fastapi import FastAPI, HTTPException
import psycopg2
import pandas as pd

app = FastAPI()

DB_CREDENTIAL = {
    "user": "votre_utilisateur",
    "password": "votre_mot_de_passe",
    "host": "votre_hôte",
    "port": "votre_port",
    "database": "votre_base_de_données"
}


def delete_task(task_id: int):
    try:
        connection = psycopg2.connect(**DB_CREDENTIAL)
        cursor = connection.cursor()

        cursor.execute("DELETE FROM task WHERE id = %s", (task_id,))
        connection.commit()
        cursor.close()
        connection.close()

        return {
            "status": "success",
            "message": f"Tâche avec l'ID {task_id} supprimée avec succès."
        }
    except (Exception, psycopg2.Error) as error:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la suppression de la tâche : {error}")


def delete_person(person_id: int):
    try:
        connection = psycopg2.connect(**DB_CREDENTIAL)
        cursor = connection.cursor()

        cursor.execute("DELETE FROM person WHERE id = %s", (person_id,))
        connection.commit()
        cursor.close()
        connection.close()

        return {
            "status": "success",
            "message": f"Personne avec l'ID {person_id} supprimée avec succès."
        }
    except (Exception, psycopg2.Error) as error:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la suppression de la personne : {error}")
