from http.client import HTTPException
from io import BytesIO
from typing import List
from fastapi import FastAPI, Query, Response
from mini_manus_ai.langgraph_main import mini_manus_main


app = FastAPI()

@app.get("/ask_question")
async def ask_question(question: str, agents_names: List[str] = Query(None), years_quarters: List[str] = Query(None)):

    try:
        agents = ["generate_image", "final_answer"]
        years = []

        for agent_name in agents_names:
            if agent_name == 'RAG Agent':
                agent = "rag_search_agent"
                agents.append(agent)
            elif agent_name == 'Web Search Agent':
                agent = "web_search"
                agents.append(agent)

        for year_quarter in years_quarters:
            if year_quarter == '2020':
                year_name = 'market-report-december-2020'
                years.append(year_name)
            elif year_quarter == '2022':
                year_name_1 = 'market-report-january-2022'
                year_name_2 = 'market-report-july-2022'
                years.append(year_name_1)
                years.append(year_name_2)
            elif year_quarter == '2023':
                year_name = 'market-report-update-2023'
                years.append(year_name)
            elif year_quarter == '2024':
                year_name_1 = 'mid-year-update-july-2024'
                year_name_2 = '2024'
                years.append(year_name_1)
                years.append(year_name_2)
            elif year_quarter == '2025':
                year_name = '2025'
                years.append(year_name)

        result = mini_manus_main(question, agents, years)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error returning a response")
    
    # Return the PDF as a StreamingResponse
    return Response(
        content=result,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=report.pdf"}
    )