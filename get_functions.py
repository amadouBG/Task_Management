from fastapi import FastAPI, HTTPException
import psycopg2


DB_CREDENTIAL = {
    "user": "votre_utilisateur",
    "password": "votre_mot_de_passe",
    "host": "votre_hôte",
    "port": "votre_port",
    "database": "votre_base_de_données"
}


def get_all_task():
    try:
        connection = psycopg2.connect(**DB_CREDENTIAL)
        query = "SELECT * FROM task"
        task_df = pd.read_sql_query(query, connection)
        connection.close()
        return task_df
    except (Exception, psycopg2.Error) as error:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération de la table task : {error}")

def get_all_person():
    try:
        connection = psycopg2.connect(**DB_CREDENTIAL)
        query = "SELECT * FROM person"
        person_df = pd.read_sql_query(query, connection)
        connection.close()
        return person_df
    except (Exception, psycopg2.Error) as error:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération de la table person : {error}")


def get_task_details(task_id: int):
    try:
        connection = psycopg2.connect(**DB_CREDENTIAL)
        cursor = connection.cursor()

        # Exécution de la requête de sélection
        cursor.execute("SELECT * FROM task WHERE id = %s", (task_id,))
        task = cursor.fetchone()

        if not task:
            raise HTTPException(status_code=404, detail="Cette personne n'existe pas.")

        task_id, title, description, creation_date, completed = task
        task_details = {
            "status": "success",
            "message": {
                "id": task_id,
                "title": title,
                "description": description,
                "creation_date": creation_date,
                "completed": completed,
            }
        }

        cursor.close()
        connection.close()

    except (Exception, psycopg2.Error) as error:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des détails de la personne : {error}")

    return task_details



def get_person_details(person_id: int):
    try:
        connection = psycopg2.connect(**DB_CREDENTIAL)
        cursor = connection.cursor()

        # Exécution de la requête de sélection
        cursor.execute("SELECT * FROM person WHERE id = %s", (person_id,))
        person = cursor.fetchone()

        if not person:
            raise HTTPException(status_code=404, detail="Cette personne n'existe pas.")

        person_id, nom, prenom = person
        person_details = {
            "status": "success",
            "message": {
                "id": person_id,
                "nom": nom,
                "prenom": prenom,
            }
        }

        cursor.close()
        connection.close()

    except (Exception, psycopg2.Error) as error:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des détails de la personne : {error}")

    return person_details
