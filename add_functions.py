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


def add_person(prenom: str, nom: str):
    try:
        connection = psycopg2.connect(**DB_CREDENTIAL)
        cursor = connection.cursor()

        cursor.execute("INSERT INTO person (prenom, nom) VALUES (%s, %s)",
                       (prenom, nom))
        connection.commit()
        cursor.close()
        connection.close()

        return {
            "status": "success",
            "message": f"Personne '{prenom} {nom}' ajoutée avec succès."
        }
    except (Exception, psycopg2.Error) as error:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'ajout de la personne : {error}")


def add_task(title: str, description: str, completed: bool):
    try:
        connection = psycopg2.connect(**DB_CREDENTIAL)
        cursor = connection.cursor()

        cursor.execute("INSERT INTO task (title, description, completed) VALUES (%s, %s, %s)",
                       (title, description, completed))
        connection.commit()
        cursor.close()
        connection.close()

        return {
            "status": "success",
            "message": f"Tâche '{title}' ajoutée avec succès."
        }
    except (Exception, psycopg2.Error) as error:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'ajout de la tâche : {error}")
