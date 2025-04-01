from io import BytesIO
import os
import boto3
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from logger_code import get_logger

web_scrape_logger = get_logger("web_scrape", "web_scrape.log")

def get_s3_client():

    #load_dotenv()
    load_dotenv(r'C:\Users\Admin\Desktop\MS Data Architecture and Management\DAMG 7245 - Big Data Systems and Intelligence Analytics\Hackathon\environment\access.env')

    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION')
    )

    return s3


# Function to upload a file to S3
def upload_to_s3(file_url, pdf_content, bucket_name):

    filename = os.path.basename(file_url)
    object_name = f'ElectricityConsumptionFiles/{filename}'
    file_content = BytesIO(pdf_content)
    
    # Upload the file content to S3
    s3_client = get_s3_client()

    try:
        s3_client.upload_fileobj(file_content, bucket_name, object_name)
        web_scrape_logger.info(f"Uploaded: {object_name} to bucket: {bucket_name}")

    except Exception as e:
            web_scrape_logger.error(f"Failed to upload {object_name} to S3: {e}")

    return filename


def scrape_upload_electricity_pdfs(base_url, bucket_name):

    # Request webpage
    response = requests.get(base_url)
    if response.status_code != 200:
        web_scrape_logger.error(f"Failed to scrape the webpage. Status code: {response.status_code}")
        return
    
    web_scrape_logger.info(f"Webpage for {base_url} fetched successfully!")
    soup = BeautifulSoup(response.content, "html.parser")

    # Example: Extract all links on the page
    links = soup.find_all('a', href=True) 
    for link in links:
        href = link['href']

        if "electricity" in href.lower() and "pdf" in href.lower():
            full_url = href if href.startswith("http") else f"{base_url.rstrip('/')}/{href}"
            web_scrape_logger.info(f"Fetched the pdf url: {full_url}")
            

    pdf_response = requests.get(full_url)

    if pdf_response.status_code == 200:
        filename = upload_to_s3(full_url, pdf_response.content, bucket_name)
    else:
        web_scrape_logger.error(f"Failed to get a response for {full_url}")

    return pdf_response, filename
    

# Test

# Base URL for NVIDIA investor relations
#url_list = ["https://www.iea.org/reports/electricity-2025", "https://www.iea.org/reports/electricity-2024"]
#base_url = "https://www.iea.org/reports/electricity-2025"
#bucket_name = "bigdatasystems2"

#for base_url in url_list:
#    scrape_electricity_pdfs(base_url)