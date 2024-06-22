'''
1. collect data from source: https://www.carmax.com/cars/?adcode=SEMGACF&vzmadcode=SEM43700072620457016&utm_source=sem_google&utm_content=sem_carmax_sales&utm_term=used%20cars&utm_campaign=139810565909&physical_loc=9032188&interest_loc=&gad_source=1&gclid=CjwKCAjwydSzBhBOEiwAj0XN4DJiS-T0XLbwDlrIQ4W93nq0fhL8JD_MJ1eVA-ZIbYPV_TmuPN33rBoCsYAQAvD_BwE&gclsrc=aw.ds
2. //*[@id="cars-listing"]/div[1]/div[1]/article/div[2]/div[2]/div[2]/h3/a
//*[@id="cars-listing"]/div[2]/div[1]/article/div[2]/div[2]
//*[@id="cars-listing"]/div[2]/div[1]/article/div[2]
//*[@id="cars-listing"]/div[2]/div[2]/article/div[2]/div[2]
3. put it in a csv file in the folder /Volumes/scire/lib_python_data_analysis/data_analysis_portfolio/carmax
4. using python and selenium
'''


import re
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # To run Chrome in headless mode (no GUI)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize the WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL of the CarMax page
# url = "https://www.carmax.com/cars/?adcode=SEMGACF&vzmadcode=SEM43700072620457016&utm_source=sem_google&utm_content=sem_carmax_sales&utm_term=used%20cars&utm_campaign=139810565909&physical_loc=9032188&interest_loc=&gad_source=1&gclid=CjwKCAjwydSzBhBOEiwAj0XN4DJiS-T0XLbwDlrIQ4W93nq0fhL8JD_MJ1eVA-ZIbYPV_TmuPN33rBoCsYAQAvD_BwE&gclsrc=aw.ds"
url = "https://www.carmax.com/cars/ford/f150"
driver.get(url)

# Wait for the page to load
time.sleep(5)  # Adjust the sleep time as needed to ensure the page fully loads

# Find all car elements using XPath
# car_elements = driver.find_elements(By.XPATH, '//*[@id="cars-listing"]/div[1]/div[1]/article')
car_elements = driver.find_elements(By.XPATH, '//*[@id="cars-listing"]/div[2]/div[2]/article/div[2]/div[2]')

# Extract data from each car element
data = []
for car in car_elements:
    try:
        title = car.find_element(By.XPATH, './/div[2]/div[2]/div[2]/h3/a').text
        data.append({'Title': title})
    except Exception as e:
        print(f"Error extracting data for car: {e}")

# Close the WebDriver
driver.quit()

# Create a DataFrame from the collected data
df = pd.DataFrame(data)

# Define the path to save the CSV file
csv_file_path = "/Volumes/scire/lib_python_data_analysis/data_analysis_portfolio/carmax/car_titles.csv"

# Write data to CSV file
df.to_csv(csv_file_path, index=False)

print(f"Data successfully written to {csv_file_path}")
