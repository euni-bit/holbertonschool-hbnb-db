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

if __name__ == '__main__':
    unittest.main()
