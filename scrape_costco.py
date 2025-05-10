import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

class CostcoScraper:
    def __init__(self):
        self.driver = uc.Chrome()
        self.driver.get("https://www.costco.ca")

    def close(self):
        self.driver.quit()

    def get_price(self, input):
        try:
            # wait up to 3 seconds for the search box to be present
            search_box = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@aria-label="Search Costco"]'))
            )
        except TimeoutException:
            print("Search box did not load in time, retrying...")
            self.driver.refresh()
            search_box = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@aria-label="Search Costco"]'))
            )
        time.sleep(random.uniform(0.5, 1))
        self.driver.execute_script("arguments[0].scrollIntoView();", search_box)
        time.sleep(random.uniform(0.5, 1))
        search_box.click()
        for char in input:
            search_box.send_keys(char)
            time.sleep(random.uniform(0.05, 0.2))
        search_box.send_keys(Keys.ENTER)
        
        try:
            # wait up to 10 seconds for products to be present
            products = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "mui-ge5uuv")]'))
            )
        except TimeoutException:
            print("Products did not load in time.")
            return
        
        results = []
        for product in products:
            try:
                product_name = product.find_element(By.XPATH, './/h3[contains(@data-testid, "Text_ProductTile")]').text
                product_price = product.find_element(By.XPATH, './/div[contains(@data-testid, "Text_Price")]').text
            except NoSuchElementException:
                print("Product name or price not found.")
                continue
            results.append((product_name, product_price))
        return results
