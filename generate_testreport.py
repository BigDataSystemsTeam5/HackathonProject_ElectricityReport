import os
import pdfplumber
import markdown2
import pdfkit
import json
import requests
import openai
import markdown2
import pdfkit
# Paths
PDF_PATH = "Electricity2025.pdf"
REPORT_MD_PATH = "electricity_report.md"
REPORT_PDF_PATH = "electricity_report.pdf"
EXTRACTED_IMG_DIR = "extracted_images"
GENERATED_IMG_DIR = "generated_images"
# Ensure directories exist
os.makedirs("generated_reports", exist_ok=True)
os.makedirs(GENERATED_IMG_DIR, exist_ok=True)

# OpenAI API Key (Ensure you store this securely)
OPENAI_API_KEY = "API KEY" 
openai.api_key = OPENAI_API_KEY

### STEP 2: GENERATE AI-POWERED IMAGES ###
def generate_ai_image(prompt, save_path):
    """Generates an AI image using OpenAI's DALL·E 3."""
    try:
        # Use the new OpenAI image generation API method
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )

        # Get the URL of the generated image
        image_url = response['data'][0]['url']
        img_data = requests.get(image_url).content

        # Save the generated image
        with open(save_path, "wb") as f:
            f.write(img_data)
        
        print(f"Generated image saved at: {save_path}")
        return save_path
    except Exception as e:
        print(f"Error generating image for prompt: {prompt}\n{str(e)}")
        return None


print("Generating AI-powered images for the report...")
image_prompts = [
    "Year-on-year change in electricity generation in India, 2019-2027",
    "Year-on-year change in electricity generation in China, 2019-2027",
    "Change in electricity demand by region, 2021-2027",
    "Evolution of per capita electricity consumption and GDP in selected regions throughout the years, 1990-2027",
    "Growth rates of electricity demand and GDP in selected regions, 2003-2027"
]

generated_images = []
for i, prompt in enumerate(image_prompts):
    img_path = f"{GENERATED_IMG_DIR}/generated_image_{i+1}.png"
    saved_img_path = generate_ai_image(prompt, img_path)
    if saved_img_path:
        generated_images.append(saved_img_path)

print(f"Generated {len(generated_images)} AI-powered images.")


### STEP 3: BUILD THE REPORT ###
print("Building detailed report...")




# Extract text from PDF
def extract_text_from_pdf(pdf_path):
    extracted_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            extracted_text += page.extract_text() + "\n\n"
    return extracted_text



# Extracted text from PDF
electricity_text = extract_text_from_pdf(PDF_PATH)

# Structure the report based on the provided format
report_content = f"""
# Electricity 2025 Report

## A Comprehensive Analysis of the Future of Electricity

# Table of Contents
1. Executive Summary  
2. Introduction  
3. Current State of the Electricity Industry  
4. Emerging Trends and Technologies  
5. Challenges and Opportunities  
6. Strategic Roadmap for 2025  
7. Conclusion  
8. References  
9. Appendix  

---

## Executive Summary
The Electricity 2025 report provides an in-depth analysis of the global electricity landscape, focusing on emerging technologies, regulatory challenges, and strategic initiatives shaping the future of energy. Key insights highlight the rapid adoption of renewable energy, the evolution of smart grids, and the importance of sustainable practices.

## Introduction
### Background
The global electricity sector is undergoing a transformation due to technological advancements, environmental concerns, and evolving consumer demands. This report explores these changes and their implications.

### Scope and Objectives
This report examines the industry's present state, future trends, and strategic initiatives, offering insights for policymakers, investors, and stakeholders.

## Current State of the Electricity Industry
### Market Overview
{electricity_text[:2000]}...

### Key Players and Stakeholders
The energy ecosystem consists of producers, distributors, regulators, and consumers working together to ensure energy security.

## Emerging Trends and Technologies
### Renewable Energy
Advancements in solar, wind, and hydroelectric power are shaping the future of sustainable energy.

### Smart Grids
Smart grids enhance energy efficiency and integrate renewable sources seamlessly.

### Energy Storage Solutions
Innovations in battery technology enable better grid stability and energy storage.

### Electric Vehicles
EV adoption is accelerating, impacting grid demand and infrastructure.

## Challenges and Opportunities
### Regulatory and Policy Landscape
Policy frameworks need to evolve to support modernization and sustainability.

### Environmental Impact
Renewable energy adoption helps reduce carbon footprints and enhances sustainability.

## Strategic Roadmap for 2025
### Short-Term Goals
Accelerate renewable energy projects, implement smart grid solutions, and expand EV infrastructure.

### Long-Term Vision
A sustainable, resilient, and carbon-neutral electricity ecosystem.

### Action Plan
Investment in renewable energy, technology innovation, and cross-industry collaboration.

## Conclusion
The electricity sector must embrace change to achieve sustainability goals by 2025.

## References
1. Electricity 2025 Report, Industry Analysis, 2025.  
2. Renewable Energy Trends, Global Energy Outlook, 2024.  
3. Smart Grid Technologies, Future Energy Systems, 2023.  

## Appendix
- Additional Data Tables  
- Glossary of Terms  
- Acronyms and Abbreviations  

"""

# Write the report to a Markdown file
with open(REPORT_MD_PATH, "w") as f:
    f.write(report_content)

print("Report generated successfully!")
