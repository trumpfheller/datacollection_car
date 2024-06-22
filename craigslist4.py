import csv
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Function to extract year from title
def extract_year(title):
    match = re.search(r'\b(19|20)\d{2}\b', title)
    return match.group(0) if match else "Unknown"

# Function to match and extract manufacturer from 'Manufacturers.txt'
def extract_manufacturer(title):
    with open('Manufacturers.txt', 'r') as f:
        manufacturers = f.read().splitlines()
    
    for manufacturer in manufacturers:
        if manufacturer.lower() in title.lower():
            return manufacturer
    
    return None

# Setup Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize the WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL of the Craigslist page
url = "https://sfbay.craigslist.org/search/cta#search=1~gallery~0~0"
driver.get(url)

# Wait for the page to load and ensure the search results are present
try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="search-results-page-1"]/ol/li/div/a'))
    )
except Exception as e:
    print(f"Error waiting for page to load: {e}")
    driver.quit()
    exit(1)

# Locate all the titles
titles = driver.find_elements(By.XPATH, '//*[@id="search-results-page-1"]/ol/li/div/a')

# Extract text from elements
car_titles = [title.text for title in titles if title.text.strip() != '']

# Extract year and manufacturer from title and create DataFrame
data = []
for title in car_titles:
    year = extract_year(title)
    manufacturer = extract_manufacturer(title)
    if manufacturer:
        title = re.sub(re.escape(manufacturer), '', title, flags=re.IGNORECASE)
    data.append({'Title': title.strip(), 'Year': year, 'Make': manufacturer})

df = pd.DataFrame(data)

'''
# Extract year from title and create DataFrame
data = {
    'Title': car_titles,
    'Year': [extract_year(title) for title in car_titles],
    'Make': [extract_manufacturer(title) for title in car_titles]
}
df = pd.DataFrame(data)

# Remove year from title column
df['Title'] = df['Title'].apply(lambda x: re.sub(r'\b(19|20)\d{2}\b', '', x))

# Drop duplicates in 'Make' column and keep the first occurrence
df['Make'].drop_duplicates(keep='first', inplace=True)
'''

# Remove year from title column
df['Title'] = df['Title'].apply(lambda x: re.sub(r'\b(19|20)\d{2}\b', '', x))

# Drop duplicates in 'Make' column and keep the first occurrence
df['Make'].drop_duplicates(keep='first', inplace=True)

# Path to save the CSV file
csv_file_path = "/Volumes/scire/lib_python_data_analysis/data_analysis_portfolio/craigslist/car_titles.csv"

# Write data to CSV file
df.to_csv(csv_file_path, index=False)

# Close the WebDriver
driver.quit()

if not df.empty:
    print(f"Data successfully written to {csv_file_path}")
else:
    print("No car titles found.")
