import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from mini_manus_ai.final_answer_la import final_answer
from mini_manus_ai.graph_la import generate_image
from mini_manus_ai.rag_la import rag_search_filter
from mini_manus_ai.web_search_la import web_search
from langchain_core.agents import AgentAction
from langchain_deepseek.chat_models import ChatDeepSeek
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv(r'C:\Users\Admin\Desktop\MS Data Architecture and Management\DAMG 7245 - Big Data Systems and Intelligence Analytics\Hackathon\environment\access.env')


system_prompt = """You are Mini Manus, the great AI research assistant.
Given the user's query you must write a research report with it based on the
list of tools provided to you. The reponse must be a comprehensive, well-structured research report.
You must generate multiple structured paragraphs for each section. Continue writing until you reach the maximum token limit. 
Do not stop early. Give the main body of the generated report in a html format. Structure the response 
into multiple sections with headings, paragraphs and bullet points wherever necessary. Each section should be
large enough to produce 2000 completion tokens. Give a response that amounts to 8000 tokens. Give a response 
that is equivalent to a pdf of 20 pahes.

The input query has a list of tools. You are allowed to use only the tools mentioned 
in the input query. Do NOT use any other tools that are not mentioned in the input query.
If you see that a tool has been used (in the scratchpad) with a particular
query, do NOT use that same tool with the same query again. Use all the tools atleast once (All tools 
must be present in scratchpad atleast once). Also, do NOT use any tool more than thrice (ie, if the tool 
appears in the scratchpad thrice, do not use it again).

Pinecone database has elctricity consumption yearly reports. Use the metadata filtering to search for 
information based on years in Pincone database. You can also web search any information 
related to the given query. You must provide all the links to the websites.

Generate a simple and clear image that is relevant to the information. Do not give any types of graphs 
or visualizations as or in the image. The image should NOT be chaotic. 

You should aim to collect information from a diverse range of sources before providing the answer to the 
user. You must NOT make any information up. Once you have collected plenty of information to generate a 
report use the final_answer tool."""



prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    ("assistant", "scratchpad: {scratchpad}"),
])


llm = ChatOpenAI(
    model="gpt-4o-mini",
    openai_api_key=os.environ["OPENAI_API_KEY"],
    max_completion_tokens=16000,
    temperature=0.7,
    top_p=0.9
)


#llm = ChatDeepSeek(
#    model="deepseek-chat",  
#    temperature=0.7,       
#    max_tokens=8000,       
#    api_key=os.environ["DEEPSEEK_API_KEY"]        
#)


tools=[
    rag_search_filter,
    web_search,
    generate_image,
    final_answer
]

# define a function to transform intermediate_steps from list
# of AgentAction to scratchpad string
def create_scratchpad(intermediate_steps: list[AgentAction]):
    research_steps = []
    for i, action in enumerate(intermediate_steps):
        if action.log != "TBD":
            # this was the ToolExecution
            research_steps.append(
                f"Tool: {action.tool}, input: {action.tool_input}\n"
                f"Output: {action.log}"
            )
    return "\n---\n".join(research_steps)


mini_manus = (
    {
        "input": lambda x: x["input"],
        "chat_history": lambda x: x["chat_history"],
        "scratchpad": lambda x: create_scratchpad(
            intermediate_steps=x["intermediate_steps"]
        ),
    }
    | prompt
    | llm.bind_tools(tools, tool_choice="any")
)



def run_mini_manus(state: list):
    print("run_mini_manus")
    print(f"intermediate_steps: {state['intermediate_steps']}")
    out = mini_manus.invoke(state)
    tool_name = out.tool_calls[0]["name"]
    tool_args = out.tool_calls[0]["args"]
    action_out = AgentAction(
        tool=tool_name,
        tool_input=tool_args,
        log="TBD"
    )
    return {
        "intermediate_steps": [action_out]
    }


def router(state: list):
    # return the tool name to use
    if isinstance(state["intermediate_steps"], list):
        return state["intermediate_steps"][-1].tool
    else:
        # if we output bad format go to final answer
        print("Router invalid format")
        return "final_answer"



# Test
#inputs = {
#    "input": "tell me something interesting about dogs",
#    "chat_history": [],
#    "intermediate_steps": [],
#}

#out = mini_manus.invoke(inputs)

#print(out.tool_calls[0]["name"])
#print(out.tool_calls[0]["args"])
