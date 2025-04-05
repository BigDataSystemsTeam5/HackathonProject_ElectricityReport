# ⚡ HackathonProject_ElectricityReport

## 🔍 Research Assistant with LangGraph

---

## 📘 Overview

CodeLab: https://bigdatasystemsteam5.github.io/HackathonProject_ElectricityReport/#0
This project is an integrated research assistant leveraging multiple specialized agents to generate comprehensive research reports. The system utilizes:

- 🖼️ **Image Agent**: Generates images from a given prompt.
- 📚 **RAG Agent**: Retrieves relevant historical data from a Pinecone-powered vector database.
- 🌐 **Web Search Agent**: Provides real-time insights using web search APIs.

These agents collaborate through **LangGraph** to produce a consolidated research output.

---

## 🚀 Features

### 📊 Data Handling

The system processes data from sources such as:

- **Electricity Market Report**
- **Electricity Reports (PDFs) for the years**: 2022, 2023, 2024, and 2025 (e.g., `Electricity2025.pdf`)

📌 Pinecone metadata filtering ensures efficient retrieval based on **Year** and **Quarter**.

---

### 🤖 Multi-Agent System (LangGraph)

- **Snowflake Agent**: Queries Snowflake for structured valuation measures and generates insights.
- **RAG Agent**: Uses Pinecone for metadata-filtered retrieval of Electricity report data.
- **Web Search Agent**: Uses real-time search APIs (SerpAPI) for the latest industry trends.

---

### 📝 Report Generation

Consolidates findings from all three agents to generate:

- Historical performance insights (**RAG Agent**)
- Structured valuation metrics and visuals (**Snowflake Agent**)
- Real-time industry insights (**Web Search Agent**)

---

### 🖥️ User Interface (Streamlit + FastAPI)

Users can:

- Pose research questions
- Filter results by Year/Quarter (via Pinecone metadata)
- Trigger individual or combined agent responses

📦 Output includes:

- Summaries
- Data-driven visualizations
- Real-time web insights

---

## 🐳 Deployment (Dockerized)

The project is containerized for seamless deployment.

### 🔧 Components:

- Streamlit UI for user interaction
- FastAPI backend to manage LangGraph orchestration
- Snowflake connection for structured data access
- Pinecone for RAG-based retrieval
- Web search integration for real-time insights
- Image generation using **DALL·E 3**
- GPT-4o-mini for text generation
- RAG Pipeline agent to fetch data from Pinecone
- Web search agent using SerpAPI

---

## ⚙️ Installation & Setup

### ✅ Prerequisites

- Python 3.8+
- Docker
- API keys for:
  - Snowflake
  - Pinecone
  - Web search API (SerpAPI)

---

### 🐋 Docker Deployment

```bash
# Build and run the Docker container
docker build -t research-assistant .
docker run -p 8501:8501 research-assistant
```

---

## 📡 API Endpoints (FastAPI)

- `GET /query` → Query the research assistant with filters
- `POST /query` → Submit structured queries

---

## 🌱 Future Enhancements

- Expand metadata filtering for improved relevance
- Add additional data sources for broader insights
- Improve UI with interactive visualizations

---

## 👥 Contributors

- **Pratik Kanade** – 33%
- **Asavari Shejwal** – 33%
- **Hishita Thakkar** – 33%

---

## 📄 License

This project is licensed under the **MIT License**.
