import os
import requests
import openai


# Paths
PDF_PATH = "Electricity2025.pdf"
EXTRACTED_IMG_DIR = "extracted_images"
GENERATED_IMG_DIR = "generated_images"
REPORT_MD_PATH = "electricity_report.md"
REPORT_PDF_PATH = "electricity_report.pdf"

# Ensure directories exist
os.makedirs(EXTRACTED_IMG_DIR, exist_ok=True)
os.makedirs(GENERATED_IMG_DIR, exist_ok=True)

# OpenAI API Key (Ensure you store this securely)
OPENAI_API_KEY = ""
openai.api_key = OPENAI_API_KEY

### STEP 2: GENERATE AI-POWERED IMAGES ###
def generate_ai_image(prompt):
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
        #img_data = requests.get(image_url).content

        # Save the generated image
        #with open(save_path, "wb") as f:
        #    f.write(img_data)
        
        #print(f"Generated image saved at: {save_path}")
        #return save_path
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

# Sample content structure
report_content = {
    "introduction": "This report presents an analysis of global electricity trends in 2025, focusing on renewable energy, consumption patterns, and future projections.",
    "research_steps": [
        "Data collection from energy reports",
        "OCR-based text extraction",
        "AI-powered visualizations",
        "Analysis of key insights",
    ],
    "main_body": [
        {"title": "Global Energy Trends", "content": "The world is shifting towards renewable energy, with solar and wind leading the transition."},
        {"title": "Electricity Consumption Patterns", "content": "The increase in electric vehicles (EVs) has significantly impacted grid demand."},
        {"title": "Future Projections", "content": "By 2030, over 50% of global energy consumption will be sourced from renewables."}
    ],
    "conclusion": "The transition to renewable energy is inevitable, and investments in smart grids are crucial.",
    "sources": [
        "International Energy Agency (IEA) Report 2025",
        "United Nations Renewable Energy Report",
        "Global Electricity Consumption Data"
    ],
    "extracted_images": [f"{EXTRACTED_IMG_DIR}/page_{i+1}.png" for i in range(5)],  # Assuming 5 pages extracted
    "generated_images": generated_images
}

# Build Markdown report
def build_markdown_report(data):
    research_steps = "\n".join(f"- {r}" for r in data["research_steps"])
    sources = "\n".join(f"- {s}" for s in data["sources"])
    main_body = "\n\n".join(f"## {section['title']}\n{section['content']}" for section in data["main_body"])

    extracted_img_md = "\n".join(f"![Extracted Image {i+1}]({img})" for i, img in enumerate(data["extracted_images"]))
    generated_img_md = "\n".join(f"![AI-Generated Image {i+1}]({img})" for i, img in enumerate(data["generated_images"]))

    return f"""
# GLOBAL ELECTRICITY ANALYSIS REPORT 2025

## INTRODUCTION
{data["introduction"]}

## RESEARCH METHODOLOGY
{research_steps}

## KEY INSIGHTS & ANALYSIS
{main_body}

## EXTRACTED IMAGES FROM REPORT
{extracted_img_md}

## AI-GENERATED VISUALS
{generated_img_md}

## CONCLUSION
{data["conclusion"]}

## SOURCES
{sources}
"""

# Write Markdown report
#with open(REPORT_MD_PATH, "w") as f:
#    f.write(build_markdown_report(report_content))

print("Markdown report generated.")
