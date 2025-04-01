# graph_la.py
from langchain_core.tools import tool
import pandas as pd
from graph_code_gen_tool import generate_graph_image
from docling_markdown import convert_and_save_document
import boto3
import os
from dotenv import load_dotenv

# Load AWS S3 credentials
load_dotenv(r'C:\Users\Admin\Desktop\MS Data Architecture and Management\DAMG 7245 - Big Data Systems and Intelligence Analytics\Assignment 5 A\environment\access.env')

s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

BUCKET_NAME = "bigdatasystems2"
PDF_KEY = "Electricity2025.pdf"

@tool("generate_graph_code")
def generate_graph_code(query: str) -> dict:
    """
    Given a user query, this tool extracts data from the Electricity2025 PDF,
    generates a graph image using code from GPT, and returns the image path.
    """
    # Step 1: Download the PDF
    response = s3.get_object(Bucket=BUCKET_NAME, Key=PDF_KEY)
    pdf_bytes = response['Body'].read()

    # Step 2: Extract text from PDF
    parsed_text = convert_and_save_document(pdf_bytes)

    # Step 3: Attempt to extract tabular data from text
    import re
    def extract_tabular_data(text):
        lines = text.split("\n")
        data = []
        for line in lines:
            # Matches lines like: 2020 123 456
            if re.match(r"^\d{4}\s+", line):
                parts = line.split()
                if len(parts) >= 2:
                    data.append(parts)
        df = pd.DataFrame(data)
        return df

    df = extract_tabular_data(parsed_text)

    if df.empty:
        return {"error": "No structured data could be extracted from the report."}

    # Step 4: Generate and run graph code
    image_path = generate_graph_image(query, df)

    return {"image_path": image_path}
