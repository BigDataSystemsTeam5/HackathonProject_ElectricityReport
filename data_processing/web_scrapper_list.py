from bs4 import BeautifulSoup
import requests
from logger_code import get_logger

web_scrape_logger = get_logger("web_scrape", "web_scrape.log")

def scrape_electricity_pdfs_list(base_url):

    links_list = []

    # Request webpage
    response = requests.get(base_url)
    if response.status_code != 200:
        web_scrape_logger.error(f"Failed to scrape the webpage for {base_url}. Status code: {response.status_code}")
        return
    
    web_scrape_logger.info(f"Webpage for {base_url} fetched successfully!")
    soup = BeautifulSoup(response.content, "html.parser")

    # Example: Extract all links on the page
    links = soup.find_all('a', href=True) 
    for link in links:
        href = link['href']
        
        if "reports/electricity" in href.lower() and 'electricity-2025' not in href.lower():
            
            new_url = "https://www.iea.org" 
            full_url = f"{new_url}{href}"
            links_list.append(full_url)

            web_scrape_logger.info(f"Fetched the page url: {full_url}")

    return links_list