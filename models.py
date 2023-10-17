import psycopg2
from psycopg2 import Error


def create_person_table(database_credential: dict):
    result = {}
    try:
        # Connexion à la base de données PostgreSQL
        connection = psycopg2.connect(
            user=database_credential.get("user"),
            password=database_credential.get("password"),
            host=database_credential.get("host"),
            port=database_credential.get("port"),
            database=database_credential.get("database")
        )

        cursor = connection.cursor()

        # Commande SQL pour créer la table "Person"
        create_table_query = '''
            CREATE TABLE Person
            (
                id SERIAL PRIMARY KEY,
                nom VARCHAR(255) NOT NULL,
                prenom VARCHAR(255) NOT NULL
            );
        '''

        # Exécution de la commande SQL
        cursor.execute(create_table_query)
        connection.commit()

        result = {
            "status": "success",
            "message": "Table 'Person' créée avec succès."
        }

    except (Exception, Error) as error:
        result = {
            "status": "error",
            "message": f"Erreur lors de la création de la table 'Person' {error}"
        }
    finally:
        # Fermeture du curseur et de la connexion
        if connection:
            cursor.close()
            connection.close()
    
    return result


def create_task_table(database_credential: dict):
    result = {}
    try:
        # Connexion à la base de données PostgreSQL
        connection = psycopg2.connect(
            user=database_credential.get("user"),
            password=database_credential.get("password"),
            host=database_credential.get("host"),
            port=database_credential.get("port"),
            database=database_credential.get("database")
        )

        cursor = connection.cursor()

        # Commande SQL pour créer la table "Task"
        create_table_query = '''
            CREATE TABLE Task
            (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description VARCHAR(255) NOT NULL,
                Date timestamptz DEFAULT NOW()
                completed BOOLEAN DEFAULT FALSE,
            );
        '''

        # Exécution de la commande SQL
        cursor.execute(create_table_query)
        connection.commit()

        result = {
            "status": "success",
            "message": "Table 'Task' créée avec succès."
        }

    except (Exception, Error) as error:
        result = {
            "status": "error",
            "message": f"Erreur lors de la création de la table 'Task':  {error}"
        }
    finally:
        # Fermeture du curseur et de la connexion
        if connection:
            cursor.close()
            connection.close()
    
    return result


def create_task_person_table(database_credential: dict):
    result = {}
    try:
        # Connexion à la base de données PostgreSQL
        connection = psycopg2.connect(
            user=database_credential.get("user"),
            password=database_credential.get("password"),
            host=database_credential.get("host"),
            port=database_credential.get("port"),
            database=database_credential.get("database")
        )

        cursor = connection.cursor()

        # Commande SQL pour créer la table "Task"
        create_table_query = '''
            CREATE TABLE task_person (
                task_id INT,
                person_id INT,
                date_attribution DATE default now(),
                PRIMARY KEY (task_id, person_id),
                FOREIGN KEY (task_id) REFERENCES task(id),
                FOREIGN KEY (person_id) REFERENCES person(id)
            );
        '''

        # Exécution de la commande SQL
        cursor.execute(create_table_query)
        connection.commit()

        result = {
            "status": "success",
            "message": "Table 'Task_person' créée avec succès."
        }

    except (Exception, Error) as error:
        result = {
            "status": "error",
            "message": f"Erreur lors de la création de la table 'Task_person':  {error}"
        }
    finally:
        # Fermeture du curseur et de la connexion
        if connection:
            cursor.close()
            connection.close()
    
    return result


# Fonction pour ajouter une tâche à la table "task"
def add_task(title:str, description: str, creation_date:str, completed: bool, database_credential: dict):
    result = {}
    try:

        # Connexion à la base de données PostgreSQL
        connection = psycopg2.connect(
        user=database_credential.get("user"),
        password=database_credential.get("password"),
        host=database_credential.get("host"),
        port=database_credential.get("port"),
        database=database_credential.get("database")
        )

        cursor = connection.cursor()
        # Exécution de la requête d'insertion
        cursor.execute("INSERT INTO task (title, description,creation_date, completed) VALUES (%s, %s, %s, %s)",
                       (title, description, creation_date, completed))
        connection.commit()
        result = {
            "status": "success",
            "message": f"Tâche {title} ajoutée avec succès."
        }
    except (Exception, psycopg2.Error) as error:
        result = {
            "status": "error",
            "message": f"Erreur lors de l'ajout de la tâche : {error}"
        }
    finally:
        # Fermeture de la connexion à la base de données
        if connection:
            cursor.close()
            connection.close()
    return result

# Fonction pour ajouter une personne à la table "person"
def add_person(prenom: str, nom: str, database_credential: dict):
    result = {}
    try:

        # Connexion à la base de données PostgreSQL
        connection = psycopg2.connect(
        user=database_credential.get("user"),
        password=database_credential.get("password"),
        host=database_credential.get("host"),
        port=database_credential.get("port"),
        database=database_credential.get("database")
        )

        cursor = connection.cursor()
        # Exécution de la requête d'insertion
        cursor.execute("INSERT INTO person (prenom, nom) VALUES (%s, %s)",
                       (prenom, nom))
        connection.commit()

        result = {
            "status": "success",
            "message": f"Personne {prenom} {nom} ajoutée avec succès."
        }
    except (Exception, psycopg2.Error) as error:
        result = {
            "status": "error",
            "message": f"Erreur lors de l'ajout de la personne : {error}"
        }
        print(f"Erreur lors de l'ajout de la personne : {error}")
    finally:
         # Fermeture de la connexion à la base de données
        if connection:
            connection.close()
    return result


# Fonction pour supprimer une tâche de la table "task" par son ID
def delete_task(task_id: int, database_credential: dict):
    task_supp = {}
    try:
        # Connexion à la base de données PostgreSQL
        connection = psycopg2.connect(
        user=database_credential.get("user"),
        password=database_credential.get("password"),
        host=database_credential.get("host"),
        port=database_credential.get("port"),
        database=database_credential.get("database")
        )

        cursor = connection.cursor()
         # Supprimez d'abord les enregistrements correspondants dans la table "task_person"
        cursor.execute("DELETE FROM task_person WHERE task_id = %s", (task_id,))
        # Ensuite, supprimez la tâche elle-même de la table "task"
        cursor.execute("DELETE FROM task WHERE id = %s", (task_id,))
        connection.commit()

        task_supp = { 
            "status": "success",
            "message": f"Tâche avec l'ID {task_id} supprimée avec succès."
        }
    except (Exception, psycopg2.Error) as error:
        task_supp = {
            "status":"error",
            "message": str(error)
        }
    finally:
         # Fermeture de la connexion à la base de données
        if connection:
            cursor.close()
            connection.close()

    return task_supp 
    

# Fonction pour supprimer une personne de la table "person" par son ID
def delete_person(person_id: int, database_credential: dict):
    try:
        # Connexion à la base de données PostgreSQL
        connection = psycopg2.connect(
        user=database_credential.get("user"),
        password=database_credential.get("password"),
        host=database_credential.get("host"),
        port=database_credential.get("port"),
        database=database_credential.get("database")
        )
        result = {}
        cursor = connection.cursor()
        # Supprimez d'abord les enregistrements correspondants dans la table "task_person"
        cursor.execute("DELETE FROM task_person WHERE person_id = %s", (person_id,))
        # Exécution de la requête de suppression
        cursor.execute("DELETE FROM person WHERE id = %s", (person_id,))
        connection.commit()
        result = {
            "message" : f"Personne avec l'ID {person_id} supprimée avec succès."
        }
    except (Exception, psycopg2.Error) as error:
        result = {
           "message" : f"Erreur lors de la suppression de la personne : {error}"
        }
    finally:
         # Fermeture de la connexion à la base de données
        if connection:
            cursor.close()
            connection.close()
    return result 

# Fonction pour récupérer les détails d'une tâche par son ID
def get_task_details(task_id: int, database_credential: dict):
    try:
        # Connexion à la base de données PostgreSQL
        conn = psycopg2.connect(
        user=database_credential.get("user"),
        password=database_credential.get("password"),
        host=database_credential.get("host"),
        port=database_credential.get("port"),
        database=database_credential.get("database")
        )

        cursor = conn.cursor()
        # Exécution de la requête de sélection
        cursor.execute("SELECT * FROM task WHERE id = %s" % task_id)
        task = cursor.fetchone()
        task_details = {}
        if task: 
            task_id, title, description, creation_date, completed = task
            task_details = {
                "status": "success",
                "message":{
                    "id": task_id, 
                    "title": title,
                    "description": description,
                    "creation_date": creation_date,
                    "completed": completed
                }
            }
    except (Exception, psycopg2.Error) as error:
        task_details = {
            "status": "error",
            "message": f"Erreur lors de la récupération des détails de la tâche : {error}"
        }
    finally:
         # Fermeture de la connexion à la base de données
        if conn:
            cursor.close()
            conn.close()
        
    return task_details


# Fonction pour récupérer les détails d'une tâche par son ID
def get_person_details(person_id: int, database_credential: dict):
    try:
        # Connexion à la base de données PostgreSQL
        conn = psycopg2.connect(
        user=database_credential.get("user"),
        password=database_credential.get("password"),
        host=database_credential.get("host"),
        port=database_credential.get("port"),
        database=database_credential.get("database")
        )

        cursor = conn.cursor()
        # Exécution de la requête de sélection
        cursor.execute("SELECT * FROM person WHERE id = %s" % person_id)
        person = cursor.fetchone()
        person_details = {}
        if person: 
            person_id, nom, prenom = person
            person_details = {
                "status": "success",
                "message":{
                    "id": person_id, 
                    "nom": nom,
                    "prenom": prenom,
                }
            }
    except (Exception, psycopg2.Error) as error:
        person_details = {
            "status": "error",
            "message": f"Erreur lors de la récupération des détails de la tâche : {error}"
        }
    finally:
         # Fermeture de la connexion à la base de données
        if conn:
            cursor.close()
            conn.close()
    
    return person_details


# Fonction pour mettre à jour une tâche par son ID
def update_task(task_id: int, update_values: dict, database_credential: dict):
    try:
        # Connexion à la base de données PostgreSQL
        conn = psycopg2.connect(
        user=database_credential.get("user"),
        password=database_credential.get("password"),
        host=database_credential.get("host"),
        port=database_credential.get("port"),
        database=database_credential.get("database")
        )
        update_result = {}
        cursor = conn.cursor()
         # Vérifiez si l'ID de la tâche existe dans la table "task"
        cursor.execute("SELECT id FROM task WHERE id = %s", (task_id,))
        existing_task = cursor.fetchone()
        if existing_task:
            request_part = [f"{col_name} = '{new_value}'" for col_name, new_value in update_values.items()]
            request_part = ", ".join(request_part)
            # Mettez à jour la tâche dans la table "task"
            cursor.execute("UPDATE task SET %s WHERE id = %s" % (request_part, task_id))
            
            # Exécution de la requête de mise à jour
            conn.commit()
            update_result = { 
                "status": "success",   
                "message": f"Tâche avec l'ID {task_id} mise à jour avec succès."
            }
            
        else:
            update_result = {
                "status": "success",
                "message": f"Aucune tâche trouvée avec l'ID {task_id}. Aucune mise à jour effectuée."
            }
    except (Exception, psycopg2.Error) as error:
        update_result = {
            "status": "error",
            "message": str(error)
        }
    finally:
         # Fermeture de la connexion à la base de données
        if conn:
            cursor.close()
            conn.close()

    return update_result


# Fonction pour mettre à jour une tâche par son ID
def update_person(person_id: int, update_values: dict, database_credential: dict):
    try:
        # Connexion à la base de données PostgreSQL
        conn = psycopg2.connect(
        user=database_credential.get("user"),
        password=database_credential.get("password"),
        host=database_credential.get("host"),
        port=database_credential.get("port"),
        database=database_credential.get("database")
        )
        update_result = {}
        cursor = conn.cursor()
         # Vérifiez si l'ID de la tâche existe dans la table "task"
        cursor.execute("SELECT id FROM person WHERE id = %s", (person_id,))
        existing_task = cursor.fetchone()
        if existing_task:
            request_part = [f"{col_name} = '{new_value}'" for col_name, new_value in update_values.items()]
            request_part = ", ".join(request_part)
            # Mettez à jour la tâche dans la table "task"
            cursor.execute("UPDATE person SET %s WHERE id = %s" % (request_part, person_id))
            
            # Exécution de la requête de mise à jour
            conn.commit()
            update_result = { 
                "status": "success",   
                "message": f"Tâche avec l'ID {person_id} mise à jour avec succès."
            }
            
        else:
            update_result = {
                "status": "success",
                "message": f"Aucune tâche trouvée avec l'ID {person_id}. Aucune mise à jour effectuée."
            }
    except (Exception, psycopg2.Error) as error:
        update_result = {
            "status": "error",
            "message": str(error)
        }
    finally:
         # Fermeture de la connexion à la base de données
        if conn:
            cursor.close()
            conn.close()

    return update_result


def get_all_task(database_credential:dict):
    try:
       # Connexion à la base de données PostgreSQL
        connection = psycopg2.connect(
        user=database_credential.get("user"),
        password=database_credential.get("password"),
        host=database_credential.get("host"),
        port=database_credential.get("port"),
        database=database_credential.get("database")
        )
        cursor = connection.cursor()

        # Exécuter la requête de sélection pour récupérer tous les éléments de la table "task"
        cursor.execute("SELECT * FROM task")
        tasks = cursor.fetchall()

        task_list = []
        for task in tasks:
            task_id, title, description, creation_date, completed = task
            task_data = {
                "id": task_id,
                "title": title,
                "description": description,
                "creation_date": creation_date,
                "completed": completed
            }
            task_list.append(task_data)

        return task_list
    except (Exception, psycopg2.Error) as error:
        return {"error": f"Erreur lors de la récupération de la table task : {error}"}

    finally:
        # Fermer la connexion à la base de données
        if connection:
            cursor.close()
            connection.close()


def get_all_person(database_credential:dict):
    try:
       # Connexion à la base de données PostgreSQL
        connection = psycopg2.connect(
        user=database_credential.get("user"),
        password=database_credential.get("password"),
        host=database_credential.get("host"),
        port=database_credential.get("port"),
        database=database_credential.get("database")
        )
        cursor = connection.cursor()

        # Exécuter la requête de sélection pour récupérer tous les éléments de la table "person"
        cursor.execute("SELECT * FROM person")
        persons = cursor.fetchall()

        person_list = []
        for person in persons:
            person_id, nom, prenom = person
            person_data = {
                "id": person_id,
                "nom": nom,
                "prenom": prenom
            }
            person_list.append(person_data)

        return person_list
    except (Exception, psycopg2.Error) as error:
        return {"error": f"Erreur lors de la récupération de la table person : {error}"}

    finally:
        # Fermer la connexion à la base de données
        if connection:
            cursor.close()
            connection.close()


def assign_task_to_person(task_id, person_id,database_credential : dict):
    try:
        # Connexion à la base de données PostgreSQL
        connection = psycopg2.connect(
        user=database_credential.get("user"),
        password=database_credential.get("password"),
        host=database_credential.get("host"),
        port=database_credential.get("port"),
        database=database_credential.get("database")
        )
        cursor = connection.cursor()

        # Vérifier que la tâche et la personne existent
        cursor.execute("SELECT 1 FROM task WHERE id = %s", (task_id,))
        task_exists = cursor.fetchone()

        cursor.execute("SELECT 1 FROM person WHERE id = %s", (person_id,))
        person_exists = cursor.fetchone()

        if not task_exists or not person_exists:
            result = {
                "message":"La tâche ou la personne n'existe pas"
            }
            return None

        # Insérer une nouvelle relation dans la table "task_person"
        cursor.execute("INSERT INTO task_person (task_id, person_id, date_attribution) VALUES (%s, %s, NOW())",
                       (task_id, person_id))
        result = {
            "message": f"Tâche (ID de la tâche : {task_id}) est  attribuée avec succès à la personne "
        }
        # Valider la transaction et fermer la connexion
        connection.commit()
        cursor.close()
        connection.close()

        return result  # Retourner l'ID de la tâche attribuée

    except (Exception, psycopg2.Error) as error:
        print("Erreur lors de l'attribution de la tâche à la personne :", error)
        return None


def assign_person_to_task(task_id, person_id,database_credential : dict):
    try:
        # Connexion à la base de données PostgreSQL
        connection = psycopg2.connect(
        user=database_credential.get("user"),
        password=database_credential.get("password"),
        host=database_credential.get("host"),
        port=database_credential.get("port"),
        database=database_credential.get("database")
        )
        cursor = connection.cursor()

        # Vérifier que la tâche et la personne existent
        cursor.execute("SELECT 1 FROM task WHERE id = %s", (task_id,))
        task_exists = cursor.fetchone()

        cursor.execute("SELECT 1 FROM person WHERE id = %s", (person_id,))
        person_exists = cursor.fetchone()

        if not task_exists or not person_exists:
            result = {
                "message":"La tâche ou la personne n'existe pas"
            }
            return None

        # Insérer une nouvelle relation dans la table "task_person"
        cursor.execute("INSERT INTO task_person (task_id, person_id, date_attribution) VALUES (%s, %s, NOW())",
                       (task_id, person_id))
        result = {
            "message": f"La personne (ID de la personne : {person_id}) est assignée avec succès à la tâche "
        }
        # Valider la transaction et fermer la connexion
        connection.commit()
        cursor.close()
        connection.close()

        return result  # Retourner l'ID de la tâche attribuée

    except (Exception, psycopg2.Error) as error:
        print("Erreur lors de l'assignation de la personne à la tâche :", error)
        return None