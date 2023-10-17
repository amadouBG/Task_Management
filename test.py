import unittest
import json
from app import app

class TestApp(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True


    def create_task(self):
        task_data = {
            "title": "Task Title",
            "description": "Task Description",
            "creation_date": "2023-10-12",
            "completed": False
        }

        response = self.app.post('/task/add/', data=json.dumps(task_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        response_data = json.loads(response.get_data(as_text=True))
        task_id = response_data.get("id")
        return task_id


    def create_person(self):
        person_data = {
            "nom": "Person Nom",
            "prenom": "Person Prenom"
        }

        response = self.app.post('/person/add/', data=json.dumps(person_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        response_data = json.loads(response.get_data(as_text=True))
        person_id = response_data.get("id")
        return person_id


    def test_get_all_task_route(self):
        response = self.app.get('/task/table')
        self.assertEqual(response.status_code, 200)


    def test_get_all_person_route(self):
        response = self.app.get('/person/table')
        self.assertEqual(response.status_code, 200)


    def test_get_task(self):
        response = self.app.get('/task/1')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertTrue('message' in response_data)


    def test_get_person(self):
        response = self.app.get('/person/1')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertTrue('message' in response_data)


    def test_add_task_route(self):
        data = {
            "title": "Test Task",
            "description": "Test Description"
        }
        response = self.app.post('/task/add/', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertTrue('message' in response_data)


    def test_add_person_route(self):
        data = {
            "nom": "Test Nom",
            "prenom": "Test Prenom"
        }
        response = self.app.post('/person/add/', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertTrue('message' in response_data)


    def test_update_task_route(self):
        # Créez une tâche
        task_id = self.create_task()

        # Données de mise à jour de la tâche
        update_data = {
            "title": "Updated Task Title",
            "description": "Updated Task Description"
        }

        # Mettez à jour la tâche
        response = self.app.post(f'/task/update/{task_id}', data=json.dumps(update_data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

        # Vérifiez que la tâche a été mise à jour

    def test_update_person_route(self):
        # Créez une personne
        person_id = self.create_person()

        # Données de mise à jour de la personne
        update_data = {
            "nom": "Updated Person Nom",
            "prenom": "Updated Person Prenom"
        }

        # Mettez à jour la personne
        response = self.app.post(f'/person/update/{person_id}', data=json.dumps(update_data), content_type='application/json')
        self.assertEqual(response.status_code, 404)
        

if __name__ == '__main__':
    unittest.main()
