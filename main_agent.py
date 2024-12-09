import pdb
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.runnables import RunnableConfig
from uuid import uuid4


from states import certifications_collect, experience_collect, greeting, info, skills_collect, skills_question, InformationGatheringState, InitialState

def router(state:InformationGatheringState):
    pdb.set_trace()
    if "name" not in state or not state["name"]:
        return "greeting"
    if "skills" not in state or not state["skills"]:
        return "skills_collect"
    if "experience" not in state or not state["experience"]:
        return "experience_collect"
    if "certifications" not in state or not state["certifications"]:
        return "certifications_collect"
    if  state.get('name', '') and  state.get('skills', '') and  state.get('experience', '') and state.get('certifications', '') and state['counter'] < 4:
        return "skills_question"
    if state['counter'] >= 4:
        "end"
    else:
        return "info"
    

workflow = StateGraph(InitialState)

workflow.add_node("greeting", greeting)
workflow.add_node("skills_collect", skills_collect)
workflow.add_node("experience_collect", experience_collect)
workflow.add_node("certifications_collect", certifications_collect)
workflow.add_node("info", info)
workflow.add_node("skills_question", skills_question)
workflow.add_edge(START, "info")
# workflow.add_edge("greeting", "info")
# workflow.add_edge("skills_collect", "experience_collect")
# workflow.add_edge("experience_collect", "certifications_collect")
# workflow.add_edge("certifications_collect", "info")

workflow.add_conditional_edges(
    "info",
    router,
    {"greeting": "greeting", "info": "info", "skills_collect" : 'skills_collect',"experience_collect":"experience_collect", "skills_question": "skills_question","certifications_collect":"certifications_collect", "end": END}
)
# workflow.add_edge("skills_collect", END)



memory = MemorySaver()

graph = workflow.compile(checkpointer=memory)

run_id = uuid4()
thread_id = str(uuid4())
config = RunnableConfig(configurable={"thread_id": thread_id},run_id=run_id)

def stream_graph_updates(user_input: str):
    input_message = HumanMessage(content=user_input) 
    for event in graph.stream({"messages": [input_message]}, config=config, stream_mode="updates"):
        for value in event.values():
            # print("Assistant:", value["messages"])
            if value and "messages" in value:
                print("Assistant:", value["messages"])
                return value["messages"][-1].content
    else:
        return "Sorry, I don't have a response at this moment!" 
