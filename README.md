# HackathonProject_ElectricityReport

Research Assistant with LangGraph

Overview

This project is an integrated research assistant leveraging multiple specialized agents to generate comprehensive research reports. The system utilizes:

Image Agent: Generates images from a given prompt.

RAG Agent: Retrieves relevant historical data from a Pinecone-powered vector database.

Web Search Agent: Provides real-time insights using web search APIs.

The agents collaborate through LangGraph to produce a consolidated research output.

Features

1. Data Handling

The system processes data from sources such as:

Electricity Market Report

Electricity Report for 2025 (Electricity2025.pdf) and other Electricity reports for the following years: 2022, 2023, 2024 

Pinecone metadata filtering ensures efficient retrieval based on Year and Quarter.

2. Multi-Agent System (LangGraph)

Snowflake Agent: Queries Snowflake for structured valuation measures and generates insights.

RAG Agent: Uses Pinecone for metadata-filtered retrieval of NVIDIA’s quarterly report data.

Web Search Agent: Uses real-time search APIs (SerpAPI, Tavily, Bing API) for the latest industry trends.

3. Report Generation

Consolidates findings from all three agents to generate:

Historical performance insights (RAG Agent)

Structured valuation metrics and visuals (Snowflake Agent)

Real-time industry insights (Web Search Agent)

4. User Interface (Streamlit + FastAPI)

Users can:

Pose research questions.

Filter results by Year/Quarter (using Pinecone metadata).

Trigger individual or combined agent responses.

Output includes:

Summaries

Data-driven visualizations

Real-time web insights

5. Deployment (Dockerized)

The project is containerized for seamless deployment.

Components:

Streamlit UI for user interaction.

FastAPI backend to manage LangGraph orchestration.

Snowflake connection for structured data access.

Pinecone for RAG-based retrieval.

Web search integration for real-time insights.
Image generation using DALL E-3
GPT Model for text generation using gpt-4o-mini
RAG Pipeline agent to get data from Pinecone
Web search agent using Serpapi.

Installation & Setup

Prerequisites

Python 3.8+

Docker

API keys for Snowflake, Pinecone, and a web search API (e.g., SerpAPI, Tavily, Bing API)

Steps to Run Locally:
1. Clone the repository
git clone <repo-url>
cd research-assistant

2. Install dependencies:
pip install -r requirements.txt

3. Set up environment variables (add to .env file):
SNOWFLAKE_USER=<your-user>
SNOWFLAKE_PASSWORD=<your-password>
PINECONE_API_KEY=<your-key>
WEB_SEARCH_API_KEY=<your-key>

4. Run FastAPI backend
uvicorn app.main:app --reload

5. Run Streamlit UI
streamlit run app/ui.py

Docker Deployment
Build and run the Docker container
docker build -t research-assistant .
docker run -p 8501:8501 research-assistant

API Endpoints (FastAPI)
GET /query → Query the research assistant with filters.
POST /query → Submit structured queries.

Future Enhancements

Expand metadata filtering for improved relevance.

Add additional data sources for broader insights.

Improve UI with interactive visualizations.

Contributors

Pratik Kanade: 33%
Asavari Shejwal: 33%
Hishita Thakkar: 33%

License
This project is licensed under the MIT License.
