from mini_manus_ai.final_answer_la import final_answer
from mini_manus_ai.graph_la import generate_image
from mini_manus_ai.rag_la import rag_search_filter
from mini_manus_ai.web_search_la import web_search
from langchain_core.agents import AgentAction

    
tool_str_to_func = {
    "rag_search_filter": rag_search_filter,
    "web_search": web_search,
    "generate_image": generate_image,
    "final_answer": final_answer
}

def run_tool(state: list):
    # use this as helper function so we repeat less code
    tool_name = state["intermediate_steps"][-1].tool
    tool_args = state["intermediate_steps"][-1].tool_input
    print(f"{tool_name}.invoke(input={tool_args})")
    # run tool
    out = tool_str_to_func[tool_name].invoke(input=tool_args)
    action_out = AgentAction(
        tool=tool_name,
        tool_input=tool_args,
        log=str(out)
    )
    return {"intermediate_steps": [action_out]}