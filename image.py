import json
import pandas as pd
from lxml.html.builder import HTML

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
import json
with open('finalorg.json', 'r') as file:
    data = json.load(file)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
table=driver.get('https://virginia.presence.io/organizations/')
driver.maximize_window()




# table = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@id='main-content']/organizations/ng-outlet/organizations-tile/div/div/div/div/div")))
# for td in table:
#

items = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="main-content"]/organizations/ng-outlet/organizations-tile/div/div/dir-pagination-controls/ul/li[2]')))

pattern = r'(\d+)-(\d+) of (\d+)'

match = re.search(pattern, items.text)

end_range = int(match.group(2))
total = int(match.group(3))

x = 0

while end_range <= total:
    try:
        table = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@id='main-content']/organizations/ng-outlet/organizations-tile/div/div/div/div/div")))
        for td in table:
            td.click()
            WebDriverWait(driver, 20)
            driver.back()

        if (end_range == total):
            end_range += 1
            break
        else:
            element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
                                                                                      "//*[@id='main-content']/organizations/ng-outlet/organizations-tile/div/div/dir-pagination-controls/ul/li[4]/a")))
            element.click()
            items = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,
                                                                                      '//*[@id="main-content"]/organizations/ng-outlet/organizations-tile/div/div/dir-pagination-controls/ul/li[2]')))

            pattern = r'(\d+)-(\d+) of (\d+)'

            match = re.search(pattern, items.text)
            print(end_range)
            print(total)
            end_range = int(match.group(2))
            total = int(match.group(3))
    except Exception as e:
        print("An error occurred: ", e)
        break  # Exit the loop in case of an error



#
# # Function to add the "image" field to each dictionary
# def add_image_field(data):
#     for i, entry in enumerate(data):
#         # Here, you can provide the image URL based on your requirements
#         # For this example, we are using a placeholder URL
#         entry["image"] = f"https://example.com/image{i+1}.jpg"
#
# # Call the function to add the "image" field
# add_image_field(data)

# Save the modified JSON data back to org.json
with open('finalorgimg.json', 'w') as file:
    json.dump(data, file, indent=2)