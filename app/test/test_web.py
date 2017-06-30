# -*- coding: utf-8 -*-
import sys
import unittest
import os
from flask import Flask
from app import app,db
from app.models import User, Party
from selenium.webdriver.common.keys import Keys
from flask_config import basedir
from selenium import webdriver
from flask_testing import LiveServerTestCase

class test_web(LiveServerTestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True
    def create_app(self):
        #app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['LIVESERVER_PORT'] = 8943
        app.config['LIVESERVER_TIMEOUT'] = 10
        db.init_app(app)
        with app.app_context():
            db.drop_all()
            db.create_all()#hi
            self.insert_data_to_db()
        return app

    def insert_data_to_db(self):
        db.session.commit()
        a = User('tomer', 'admon', '123')
        v = Party(u'העבודה','https://www.am-1.org.il/wp-content/uploads/2015/03/%D7%94%D7%A2%D7%91%D7%95%D7%93%D7%94.-%D7%A6%D7%99%D7%9C%D7%95%D7%9D-%D7%99%D7%97%D7%A6.jpg')
        db.session.add(v)
        db.session.add(a)
        db.session.commit()

    def setUp(self):
        self.browser = webdriver.PhantomJS()
        # nevigate to the application home page
        self.browser.get(self.get_server_url())

    def test_good_login(self):
        first_name = self.browser.find_element_by_id("first_name").send_keys('tomer')
        last_name = self.browser.find_element_by_id("last_name").send_keys('admon')
        id = self.browser.find_element_by_id("id").send_keys('123' +Keys.RETURN )
        assert 'Home' in self.browser.title

    def test_bad_login(self):
        first_name = self.browser.find_element_by_id("first_name")
        last_name = self.browser.find_element_by_id("last_name")
        id = self.browser.find_element_by_id("id")
        first_name.send_keys('bad')
        last_name.send_keys('bad')
        id.send_keys('bad')
        id.send_keys(Keys.RETURN)
        assert u'המצביע אינו מופיע בבסיס הנתונים' in self.browser.page_source

    def tearDown(self):
        self.browser.quit()
        with app.app_context():
            db.drop_all()
            db.session.remove()


if __name__ == '__main__':
    unittest.main()

