from langgraph.graph import StateGraph, END
from data_processing.logger_code import get_logger
from mini_manus_ai.agentstate_la import AgentState
from mini_manus_ai.langgraph_llm import router, run_mini_manus
from mini_manus_ai.graph_la import generate_image
from mini_manus_ai.report_builder import build_report
from mini_manus_ai.tool_runner import run_tool
from mini_manus_ai.rag_la import rag_search_filter
from mini_manus_ai.web_search_la import web_search
from mini_manus_ai.final_answer_la import final_answer
from langchain_core.runnables import RunnableConfig
#from IPython.display import Image

manus_logger = get_logger("manus_info", "manus_info.log")

def mini_manus_main(question, agents, years):

    graph = StateGraph(AgentState)
    #graph = Graph(config={"recursion_limit": 50})

    graph.add_node("mini_manus", run_mini_manus)
    graph.add_node("rag_search_filter", run_tool)
    graph.add_node("web_search", run_tool)
    graph.add_node("generate_image", run_tool)
    graph.add_node("final_answer", run_tool)


    graph.set_entry_point("mini_manus")

    graph.add_conditional_edges(
        source="mini_manus",  # where in graph to start
        path=router  # function to determine which node is called
    )

    tools=[
        rag_search_filter,
        web_search,
        generate_image,
        final_answer
    ]


    # create edges from each tool back to the mini_manus
    for tool_obj in tools:
        if tool_obj.name != "final_answer":
            graph.add_edge(tool_obj.name, "mini_manus")

    # if anything goes to final answer, it must then move to END
    graph.add_edge("final_answer", END)

    #Image(runnable.get_graph().draw_png())

    runnable = graph.compile()

    out = runnable.invoke({
        "input": f"""A string list of years is provided: {years}. Give response to the 
        question: {question} about Electricity Comsumption. If the query is not related to Electricity 
        Consumption, you must not answer the question and return a response stating it. A list of tools 
        is provided: {agents}. You must use the tools in the agents list. Do NOT use any other
        tools. The response should be solely related to the query an years provided.""",
        "chat_history": [],
    },
    config=RunnableConfig(recursion_limit=100))

    manus_logger.info(out)

    result = build_report(
            output=out["intermediate_steps"][-1].tool_input
        )
    
    return result


# Test

#question = "tell me something in short"
#years = [2024]
#quarters = [3, 4]
#agents = ["rag_search_filter"]
#
#result = mini_manus_main(question, agents, years, quarters)
#print(result)