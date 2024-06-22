import csv
import time
import logging
import requests
from bs4 import BeautifulSoup

'''
pip install requests
python -c "import bs4; print(bs4.__version__)"
'''

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scrape_edmunds_inventory(url, csv_file_path):
    try:
        # Craft headers to mimic a real user request
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://www.google.com/",
            "Connection": "keep-alive"
        }

        # Send GET request with headers
        response = requests.get(url, timeout=10, headers=headers)# Timeout set to 10 seconds
        response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)
    
        # Parse content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all car elements
        car_elements = soup.find_all('div', class_='vehicle-card')

        # Extract data from each car element
        data = []
        for car in car_elements:
            try:
                title = car.find('h2', class_='header-4 text-truncate').text.strip()
                price = car.find('span', class_='primary-price').text.strip()
                mileage = car.find('div', class_='miles-for-listing').text.strip()
                year = car.find('div', class_='specs-year-make-model').find('span').text.strip()
                data.append({'Title': title, 'Price': price, 'Mileage': mileage, 'Year': year})
            except Exception as e:
                logger.error(f"Error extracting data for car: {e}")

        # Write data to CSV file
        if data:
            csv_fields = ['Title', 'Price', 'Mileage', 'Year']
            with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=csv_fields)
                writer.writeheader()
                writer.writerows(data)
            
            logger.info(f"Data successfully written to {csv_file_path}")
        else:
            logger.warning("No data collected, CSV file not created.")

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching URL: {e}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    # URL of the Edmunds Ford F-150 inventory page
    url = "https://www.edmunds.com/inventory/srp.html?inventorytype=used%2Ccpo&make=ford&model=ford%7Cf-150&displacement=2-2.9"

    # Define the path to save the CSV file
    csv_file_path = "/Volumes/scire/lib_python_data_analysis/data_analysis_portfolio/edmunds/ford_f150_inventory.csv"

    # Run the scraping function
    scrape_edmunds_inventory(url, csv_file_path)

'''
ERROR:__main__:Error fetching URL: HTTPSConnectionPool(host='www.edmunds.com', port=443): Read timed out. (read timeout=10)
'''