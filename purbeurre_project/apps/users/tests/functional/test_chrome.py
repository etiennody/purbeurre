"""Functional tests for users app
"""
import time
import unittest

from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


class RegisterSeleniumTest(unittest.TestCase):
    """Register functional test with selenium

    Args:
        unittest (module): core framework classes that form the basis of specific test cases
    """

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(
            "/usr/local/bin/chromedriver/chromedriver", chrome_options=chrome_options
        )

    def test_valid_live_register_page(self):
        """Validate data entries on the registration page"""
        self.driver.get("http://127.0.0.1:8000/register/")
        print(self.driver.title)
        username = self.driver.find_element_by_id("id_username")
        first_name = self.driver.find_element_by_id("id_first_name")
        last_name = self.driver.find_element_by_id("id_last_name")
        email = self.driver.find_element_by_id("id_email")
        password1 = self.driver.find_element_by_id("id_password1")
        password2 = self.driver.find_element_by_id("id_password2")
        submit = self.driver.find_element_by_class_name("btn")
        time.sleep(5)
        self.driver.implicitly_wait(5)
        username.send_keys("BobRobert")
        first_name.send_keys("Bob")
        last_name.send_keys("Robert")
        email.send_keys("bobrobert@test.com")
        password1.send_keys("fglZfYmr%?,")
        password2.send_keys("fglZfYmr%?,")
        submit.click()

        time.sleep(10)
        self.driver.implicitly_wait(10)

        current_url = self.driver.current_url
        if (self.driver.current_url[len(self.driver.current_url) - 1]) == "/":
            current_url = self.driver.current_url[:-1]
        self.assertEqual(current_url, "http://127.0.0.1:8000/register")
        self.assertIn("Vous avez déjà un compte ?", self.driver.page_source)
        self.assertTrue(User.objects.filter(username="BobRobert").exists())

    def tearDown(self):
        self.driver.close()


class LoginSeleniumTest(unittest.TestCase):
    """Login functional test with selenium

    Args:
        unittest (module): core framework classes that form the basis of specific test cases
    """

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(
            "/usr/local/bin/chromedriver/chromedriver", chrome_options=chrome_options
        )
        user = User.objects.create(
            username="BobRobert",
            first_name="Bob",
            last_name="Robert",
            email="test_bob@test.com",
        )
        user.set_password("fglZfYmr%?,")
        user.save()
        super(LoginSeleniumTest, self).setUp()

    def test_valid_live_login_page(self):
        """Validate data entries on the login page"""
        self.driver.get("http://127.0.0.1:8000/login/")
        print(self.driver.title)
        username = self.driver.find_element_by_id("id_username")
        password = self.driver.find_element_by_id("id_password")
        submit = self.driver.find_element_by_id("submit-button")
        username.send_keys("BobRobert")
        password.send_keys("fglZfYmr%?,")
        submit.send_keys(Keys.RETURN)

        time.sleep(10)
        self.driver.implicitly_wait(10)

        current_url = self.driver.current_url
        if (self.driver.current_url[len(self.driver.current_url) - 1]) == "/":
            current_url = self.driver.current_url[:-1]
        self.assertEqual(current_url, "http://127.0.0.1:8000")
        self.assertIn("Accueil :: Purbeurre", self.driver.title)

    def tearDown(self):
        self.driver.close()
        super(LoginSeleniumTest, self).tearDown()
