import unittest
from src import create_app, db
from src.models.user import User
from src.models.place import Place

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

    def test_update_user(self):
        user = User.create({
            "email": "test_update@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "password"
        })
        user.first_name = "Updated"
        user.save()
        self.assertEqual(User.query.filter_by(email="test_update@example.com").first().first_name, "Updated")

    def test_delete_user(self):
        user = User.create({
            "email": "test_delete@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "password"
        })
        user_id = user.id
        user.delete()
        self.assertIsNone(User.query.get(user_id))

    def test_user_place_relationship(self):
        user = User.create({
            "email": "test_relationship@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "password"
        })
        place = Place.create({
            "name": "Test Place",
            "user_id": user.id
        })
        self.assertEqual(user.places.count(), 1)
        self.assertEqual(user.places.first().name, "Test Place")

    def test_dynamic_persistence_switch(self):
        # Test with database
        user = User.create({
            "email": "test_db@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "password"
        })
        self.assertIsNotNone(User.query.filter_by(email="test_db@example.com").first())

        self.app.config['USE_DATABASE'] = False

if __name__ == '__main__':
    unittest.main()
