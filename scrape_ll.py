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

class LoblawsScraper:
    def __init__(self):
        self.driver = uc.Chrome()
        self.driver.get("https://www.loblaws.ca/en")

    def close(self):
        self.driver.quit()

    def get_price(self, input):
        try:
            self.driver.find_element(By.XPATH, '//button[@id="onetrust-reject-all-handler"]').click()
        except NoSuchElementException:
            pass # No cookie banner found, continue

        try:
            # wait up to 3 seconds for the search box to be present
            search_box = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Search for Product"]'))
            )
        except TimeoutException:
            print("Search box did not load in time, retrying...")
            self.driver.refresh()
            search_box = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Search for Product"]'))
            )

        time.sleep(random.uniform(0.5, 1))
        self.driver.execute_script("arguments[0].scrollIntoView();", search_box)
        time.sleep(random.uniform(0.5, 1))
        search_box.click()
        for char in input:
            search_box.send_keys(char)
            time.sleep(random.uniform(0.05, 0.2))
        search_box.send_keys(Keys.ENTER)
        
        results = []
        time.sleep(5)
        elements = self.driver.find_elements(By.XPATH, '//div[@class="css-yyn1h"]')
        for element in elements:
            name = element.find_element(By.XPATH, './/h3[@data-testid="product-title"]').text
            price = element.find_element(By.XPATH, './/span[@data-testid="regular-price"]|.//span[@data-testid="sale-price"]').text
            results.append((name, price))
        return results
        