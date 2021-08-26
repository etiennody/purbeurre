"""Functional tests for product app
"""
import time
import unittest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class SearchResultsPageSeleniumTest(unittest.TestCase):
    """Search results functional test with selenium

    Args:
        unittest (module): core framework classes that form the basis of specific test cases
    """

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(
            "/usr/local/bin/chromedriver/chromedriver",
            chrome_options=chrome_options,
        )

    def test_valid_live_search_results_page_title__and_product_present(self):
        """Valid if search results title and product searched are present

        Raises:
            Exception: message to inform access is denied on search results page
        """
        self.driver.get("http://127.0.0.1:8000/search/?q=nutella")
        if not "Résultats recherche produits :: Purbeurre" in self.driver.title:
            raise Exception("Unable to load purbeurre search results page!")
        self.assertIn("Résultats recherche produits :: Purbeurre", self.driver.title)
        self.assertIn("Nutella", self.driver.page_source)

    def tearDown(self):
        self.driver.close()


class SubstituteResultsPageSeleniumTest(unittest.TestCase):
    """Substitute result functional test with selenium

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

    def test_valid_live_substitute_results_page(self):
        """Valid substitute results page"""
        self.driver.get("http://127.0.0.1:8000/")
        text = self.driver.find_element_by_id("inputSearchForm")
        submit = self.driver.find_element_by_class_name("btn")
        time.sleep(5)
        self.driver.implicitly_wait(5)
        text.send_keys("product")
        submit.click()
        self.driver.get("http://127.0.0.1:8000/search?q=nutella")
        product = self.driver.find_element_by_class_name("get-more")
        time.sleep(5)
        self.driver.implicitly_wait(5)
        product.click()
        current_url = self.driver.current_url
        if (self.driver.current_url[len(self.driver.current_url) - 1]) == "/":
            current_url = self.driver.current_url[:-1]
        self.assertEqual(current_url, "http://127.0.0.1:8000/substitute/788894")
        self.assertIn("Résultats recherche substituts :: Purbeurre", self.driver.title)
        self.assertIn(
            "Vous pouvez remplacer cet aliment par :", self.driver.page_source
        )

    def tearDown(self):
        self.driver.close()
