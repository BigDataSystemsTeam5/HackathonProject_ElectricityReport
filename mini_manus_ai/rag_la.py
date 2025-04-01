import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone


load_dotenv(r'C:\Users\Admin\Desktop\MS Data Architecture and Management\DAMG 7245 - Big Data Systems and Intelligence Analytics\Hackathon\environment\access.env')

# Configure Pinecone Connection
pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))


index_name = "hackathon"
index = pc.Index(index_name)

# Embedding settings
embedding_model = "all-MiniLM-L6-v2"

# Initialize the embedding model
embedding_model = SentenceTransformer(embedding_model)

def format_rag_contexts(matches: list):
    contexts = []
    for x in matches:
        text = (
            f"Year: {x['metadata']['year']}\n"
            f"Content: {x['metadata']['content']}\n"
        )
        contexts.append(text)
    context_str = "\n---\n".join(contexts)
    return context_str

@tool("rag_search_filter")
def rag_search_filter(query: str, year: str):
    """Finds information from Pinecone database using a natural language query
    and a specific year and quarter. Allows us to learn more details about a specific report."""

    namespaces = []

    if year == '2020':
        year_name = 'market-report-december-2020'
        namespaces.append(year_name)
    elif year == '2022':
        year_name_1 = 'market-report-january-2022'
        year_name_2 = 'market-report-july-2022'
        namespaces.append(year_name_1)
        namespaces.append(year_name_2)
    elif year == '2023':
        year_name = 'market-report-update-2023'
        namespaces.append(year_name)
    elif year == '2024':
        year_name_1 = 'mid-year-update-july-2024'
        year_name_2 = '2024'
        namespaces.append(year_name_1)
        namespaces.append(year_name_2)
    elif year == '2025':
        year_name = '2025'
        namespaces.append(year_name)

    result = embedding_model.encode([query])
    embed_query = result.tolist()

    xc = index.query_namespaces(vector=embed_query, metric="cosine", top_k=5, include_metadata=True, namespaces=namespaces)
    context_str = format_rag_contexts(xc["matches"])
    return context_str
