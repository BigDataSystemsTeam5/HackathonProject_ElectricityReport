from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.programming.language import Python
from diagrams.onprem.container import Docker
from diagrams.custom import Custom

with Diagram("Electricity Report Research Assistant Architecture", show=False, direction="LR"):
    user = User("User")

    with Cluster("Frontend"):
        streamlit = Custom("Streamlit UI", "./icons/streamlit.png")

    with Cluster("FastAPI Backend"):
        fastapi = Python("FastAPI")
        orchestrator = Python("LangGraph")

        with Cluster("Agents"):
            rag = Custom("RAG Agent", "./icons/pinecone.png")
            snowflake = Custom("Snowflake Agent", "./icons/snowflake.png")
            websearch = Custom("Web Search Agent", "./icons/serpapi.png")
            imagegen = Custom("Image Agent", "./icons/dalle3.png")
            llm = Custom("GPT-4o-mini", "./icons/gpt4.png")

        orchestrator >> [rag, snowflake, websearch, imagegen, llm]

    with Cluster("Deployment"):
        docker = Docker("Dockerized App")

    user >> streamlit >> fastapi
    fastapi >> orchestrator
    docker >> [fastapi, streamlit]
