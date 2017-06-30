import unittest

from app import app, db

SQLALCHEMY_DATABASE_URI = "sqlite://"
TESTING = True

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        self.check = app.test_client(self)

    def tearDown(self):
        del self.check
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_cant_access_without_login(self):
        # check if the url of accessing index page without logging in is the same of the login page
        response = self.check.get('/app/manager')
        self.assertEqual(response.status_code, 404)

    def test_false_login(self):
        # check that you can't login without id
        invalid_login = self.check.post('login', data=dict(first_name='wrong', last_name='user'))
        self.assertEqual(invalid_login.status_code, 400)

    def test_false_user_id(self):
        # check the error of user who's not in the database
        invalid_login = self.check.post('login', data=dict(first_name='wrong', last_name='user', id='987'))
        str = invalid_login.data.decode('utf-8')
        assert u'המצביע אינו מופיע בבסיס הנתונים' in str

if (__name__ == '__main__'):
    unittest.main()