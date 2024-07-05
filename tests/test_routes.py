import unittest
from src import create_app, db
from src.models.user import User

class UserRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_user(self):
        response = self.client.post('/api/users', json={
            "email": "test2@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "password"
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('email', response.json)
        self.assertEqual(response.json['email'], "test2@example.com")

    def test_create_user_with_existing_email(self):
        User.create({
            "email": "test2@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "password"
        })
        response = self.client.post('/api/users', json={
            "email": "test2@example.com",
            "first_name": "Test2",
            "last_name": "User2",
            "password": "password"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)

    def test_get_users(self):
        User.create({
            "email": "test3@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "password"
        })
        response = self.client.get('/api/users')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertGreater(len(response.json), 0)

    def test_get_user_by_id(self):
        user = User.create({
            "email": "test4@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "password"
        })
        response = self.client.get(f'/api/users/{user.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['email'], "test4@example.com")

    def test_get_user_by_invalid_id(self):
        response = self.client.get('/api/users/invalid-id')
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json)

    def test_update_user(self):
        user = User.create({
            "email": "test5@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "password"
        })
        response = self.client.put(f'/api/users/{user.id}', json={
            "first_name": "Updated"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['first_name'], "Updated")

    def test_delete_user(self):
        user = User.create({
            "email": "test6@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "password"
        })
        response = self.client.delete(f'/api/users/{user.id}')
        self.assertEqual(response.status_code, 204)
        self.assertIsNone(User.query.get(user.id))

if __name__ == '__main__':
    unittest.main()
