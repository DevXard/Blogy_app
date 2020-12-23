from unittest import TestCase
from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///bogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

#  don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCases(TestCase):
    
    def setUp(self):
        """ Create sample User"""

        User.query.delete()

        user = User(first_name='TestUser', last_name='UserTest', image_url="google.com")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
    
    def tearDown(self):
        """ Clean Up anly leftover transactions"""
        db.session.rollback()


    def test_list_of_users(self):
        with app.test_client() as client:
            res = client.get('/users')
            html = res.get_data(as_text=True)
        
        self.assertEqual(res.status_code, 200)
        self.assertIn('TestUser', html)

    def test_details(self):
        with app.test_client() as client:
            res = client.get(f"/users/{self.user_id}")
            html = res.get_data(as_text=True)

        self.assertEqual(res.status_code, 200)
        self.assertIn('UserTest', html)

    def test_create_new_user(self):
        with app.test_client() as client:
            d = {"first_name": "Bob", "last_name": "Jon", "image_url": "yahoo.com"}
            res = client.post("/users/new", data=d, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Bob", html)