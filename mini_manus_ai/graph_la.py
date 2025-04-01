import os
from dotenv import load_dotenv
import openai
from langchain_core.tools import tool

load_dotenv(r'C:\Users\Admin\Desktop\MS Data Architecture and Management\DAMG 7245 - Big Data Systems and Intelligence Analytics\Hackathon\environment\access.env')


openai_api_key=os.environ["OPENAI_API_KEY"]

@tool("generate_image")
def generate_image(text: str):
    """Generates an AI image using OpenAI's DALL·E 3."""

    # Use the new OpenAI image generation API method
    response = openai.images.generate(
        model="dall-e-3",
        prompt=text,
        size="1024x1024"
    )
    
    return {"image_url": response.data[0].url}