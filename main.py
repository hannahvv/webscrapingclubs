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

data = []
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
table=driver.get('https://virginia.presence.io/organizations/list')
driver.maximize_window()
#WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='main-content']/organizations/ng-outlet/organizations-list/div/div/dir-pagination-controls/ul/li[4]/a"))).click()
items = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '(//*[@id="main-content"]/organizations/ng-outlet/organizations-list/div/div/dir-pagination-controls/ul/li[2])')))


pattern = r'(\d+)-(\d+) of (\d+)'

match = re.search(pattern, items.text)

end_range = int(match.group(2))
total = int(match.group(3))




# Execute the ng-click JavaScript function

i = 0
while end_range <= total:
    try:
        table = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, '(//td)')))
        for td in table:
            stuff = td.get_attribute('innerHTML')

            if (i == 5):
                #print(stuff)
                i = 0
            else:
                if i == 0:

                    soup = BeautifulSoup(stuff, 'html.parser')
                    # Find the element that follows the </a> element
                    next_element = soup.find('a', class_='ng-binding').text
                    organization_name = next_element

                    #print('Organization: ' + next_element)
                elif i == 1:
                    #print("Description: " + stuff)
                    description = stuff
                elif i == 2:
                    #print("Schedule: " + stuff)
                    schedule = stuff
                elif i == 3:
                    #print("Location: " + stuff)
                    location = stuff
                else:
                    #print("Members: " + stuff)
                    members = stuff
                    data.append({
                        'organization': organization_name,
                        'description': description,
                        'schedule': schedule,
                        'location': location,
                        'member': members,
                    })

                i += 1

        if(end_range == total):
            end_range += 1
            break
        else:
            element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
                                                                                  "//*[@id='main-content']/organizations/ng-outlet/organizations-list/div/div/dir-pagination-controls/ul/li[4]/a")))
            element.click()
            items = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,
                                                                                      '(//*[@id="main-content"]/organizations/ng-outlet/organizations-list/div/div/dir-pagination-controls/ul/li[2])')))

            pattern = r'(\d+)-(\d+) of (\d+)'

            match = re.search(pattern, items.text)
            print(end_range)
            print(total)
            end_range = int(match.group(2))
            total = int(match.group(3))

            # Optionally, you can add a wait for page load or other conditions here


            # Check if you are on the last page (define your own condition)

    except Exception as e:
        print("An error occurred: ", e)
        break  # Exit the loop in case of an error
file_path = "organizationcollection.json"
#
# # Write the JSON data to the file
with open(file_path, 'w') as json_file:
    json.dump(data, json_file, indent=2)  # indent for pretty printing (optional)
#
# print(f"JSON data has been exported to {file_path}")





