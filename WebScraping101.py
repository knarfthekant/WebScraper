from selenium import webdriver # allow launching browser
from selenium.webdriver.chrome.service import Service # use to locate path
from selenium.webdriver.common.by import By # search with parameters
from selenium.webdriver.support.ui import WebDriverWait # allow waiting for page to load
from selenium.webdriver.support import expected_conditions as EC # determine whether the web page has loaded
from selenium.common.exceptions import TimeoutException
import pandas as pd

driver_option = webdriver.ChromeOptions()
driver_option.add_argument("--incognito")
chromedriver_path = './cdriver/chromedriver'
service = Service(executable_path=chromedriver_path)

def create_webdriver():
    return webdriver.Chrome(service=service, options=driver_option)

# Open the website
browser = create_webdriver()
browser.get("https://github.com/collections/machine-learning")

# Extract all projects:
projects = browser.find_elements(By.XPATH, "//h1[@class='h3 lh-condensed']")

# Extract information for each project
project_list = {}
for proj in projects:
    proj_name = proj.text
    proj_url = proj.find_elements(By.TAG_NAME, "a")[0].get_attribute('href') # project URL
    project_list[proj_name] = proj_url
''' 
x.text - extract the raw text from the element x
x.get_attribute('y') - extract the value in attribute y from element x
'''

# Close connection
browser.quit()

# Extracting data
project_df = pd.DataFrame.from_dict(project_list, orient = 'index')
# manipulate the table
project_df['project_name'] = project_df.index
project_df.columns = ['project_url', 'project_name']
project_df = project_df.reset_index(drop=True)

# Export project dataframe to CSV
project_df.to_csv('project_list.csv')
