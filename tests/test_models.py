import unittest
from src import create_app, db
from src.models.user import User

class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_user(self):
        user = User.create({
            "email": "test2@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "password"
        })
        self.assertIsNotNone(user.id)
        self.assertEqual(user.email, "test2@example.com")

    def test_unique_email(self):
        user1 = User.create({
            "email": "unique@example.com",
            "first_name": "User1",
            "last_name": "Test",
            "password": "password"
        })
        with self.assertRaises(ValueError):
            user2 = User.create({
                "email": "unique@example.com",
                "first_name": "User2",
                "last_name": "Test",
                "password": "password"
            })

if __name__ == '__main__':
    unittest.main()
