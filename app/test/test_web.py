import unittest

from flask_testing import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from app import app, db
from app.models import User, Party


class AppTestCase(LiveServerTestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True

    def create_app(self):
        app.config['TESTING'] = True
        app.config['LIVESERVER_PORT'] = 8943
        app.config['LIVESERVER_TIMEOUT'] = 10
        db.init_app(app)
        with app.app_context():
            db.create_all()
            self.insert_data_to_db()
        return app

    def insert_data_to_db(self):
        db.session.commit()
        testuser = User('test', 'user', '123')
        yarok = Party(u'עלה ירוק', 'https://pbs.twimg.com/profile_images/553476099775016960/8Ha40Qym_400x400.jpeg')
        avoda = Party(u'העבודה',
                      'https://www.am-1.org.il/wp-content/uploads/2015/03/%D7%94%D7%A2%D7%91%D7%95%D7%93%D7%94.-%D7%A6%D7%99%D7%9C%D7%95%D7%9D-%D7%99%D7%97%D7%A6.jpg')
        db.session.add(yarok)
        db.session.add(avoda)
        db.session.add(testuser)
        db.session.commit()

    def setUp(self):
        self.browser = webdriver.PhantomJS()
        self.browser.get(self.get_server_url())

    def test_getting_to_voting_page(self):
        first_name = self.browser.find_element_by_name('first_name')
        first_name.send_keys('test')
        last_name = self.browser.find_element_by_name('last_name')
        last_name.send_keys('user')
        id = self.browser.find_element_by_name('id')
        id.send_keys('123')
        id.send_keys(Keys.ENTER)
        assert 'Home' in self.browser.title

    def test_user_not_in_database(self):
        first_name = self.browser.find_element_by_name('first_name')
        first_name.send_keys('wrong')
        last_name = self.browser.find_element_by_name('last_name')
        last_name.send_keys('user')
        Id = self.browser.find_element_by_name('id')
        Id.send_keys('987')
        Id.send_keys(Keys.ENTER)
        assert 'Home' not in self.browser.title

    def tearDown(self):
        self.browser.quit()
        with app.app_context():
            db.drop_all()
            db.session.remove()


if (__name__ == '__main__'):
    unittest.main()