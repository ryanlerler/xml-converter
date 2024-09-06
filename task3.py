import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

# PostgreSQL database connection details
DB_CONNECTION_STRING = os.environ.get("DB")

def scrape_data():
    url = 'https://www.ccilindia.com/web/ccil/security-wise-repo-market-summary'
    
    # Set up Selenium
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get(url)
        logging.info(f"Accessed URL: {url}")
        
        # Wait for the table to be present
        table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "securityWiseRepoTable"))
        )
        
        # Get the page source after JavaScript has loaded the content
        page_source = driver.page_source
        
        soup = BeautifulSoup(page_source, 'html.parser')
        table = soup.find('table', {'id': 'securityWiseRepoTable'})
        
        if not table:
            logging.error("Table not found")
            return pd.DataFrame()
        
        # Extract headers
        headers = [th.text.strip() for th in table.find_all('th')]
        logging.info(f"Found {len(headers)} columns: {headers}")
        
        rows = table.find_all('tr')
        data = []
        for row in rows[1:]:  # Skipping the header row
            cols = row.find_all('td')
            data.append([col.text.strip() for col in cols])
        
        df = pd.DataFrame(data, columns=headers)
        logging.info(f"Scraped {len(df)} rows of data")
        return df
    
    except Exception as e:
        logging.error(f"An error occurred while scraping: {str(e)}")
        return pd.DataFrame()
    
    finally:
        driver.quit()

def store_data_to_db(df, table_name='security_holdings'):
    if df.empty:
        logging.info("No data to store in the database.")
        return
    
    engine = create_engine(DB_CONNECTION_STRING)
    df.to_sql(table_name, engine, if_exists='append', index=False)
    logging.info(f"Stored {len(df)} rows in the database")

def check_and_store_incremental():
    df_new = scrape_data()
    
    if df_new.empty:
        logging.info("No new data scraped.")
        return

    engine = create_engine(DB_CONNECTION_STRING)
    query = 'SELECT MAX("Date") FROM security_holdings'
    last_scrape_date = pd.read_sql(query, engine).iloc[0, 0]

    if pd.isna(last_scrape_date):
        last_scrape_date = pd.Timestamp.min
    else:
        last_scrape_date = pd.to_datetime(last_scrape_date)

    df_new['Date'] = pd.to_datetime(df_new['Date'])
    df_filtered = df_new[df_new['Date'] > last_scrape_date]

    if not df_filtered.empty:
        store_data_to_db(df_filtered)
        logging.info(f"Inserted {len(df_filtered)} new rows.")
    else:
        logging.info("No new data to insert.")

if __name__ == "__main__":
    df = scrape_data()
    if not df.empty:
        df.to_csv('security_data.csv', index=False)
        logging.info("Data saved to CSV file")
        store_data_to_db(df)
        check_and_store_incremental()
    else:
        logging.warning("No data was scraped. Check the website structure or network connection.")