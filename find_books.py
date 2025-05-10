from selenium import webdriver 
from selenium.webdriver.chrome.service import Service # use to locate path
import pandas as pd
 
web = 'https://www.audible.com/search'
path = './cdriver/chromedriver'
service = Service(executable_path=path)
driver = webdriver.Chrome(service=service)

driver.get(web)

products = driver.find_elements(by='xpath', value='//li[contains(@class, "productListItem")]')
# use xpath //li[contains(@class, "productListItem")]

book_title = []
book_author = []
book_length = []

for product in products:

    book_title.append(product.find_element(by='xpath', value='.//h3[contains(@class, "bc-heading")]').text) # . means using the current element
    book_author.append(product.find_element(by='xpath', value='.//li[contains(@class, "authorLabel")]').text)
    book_length.append(product.find_element(by='xpath', value='.//li[contains(@class, "runtimeLabel")]').text)

df_books = pd.DataFrame({'title': book_title, 'author': book_author, 'length': book_length})
df_books.to_csv('books.csv', index=False)
driver.quit()