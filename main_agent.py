from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.runnables import RunnableConfig
from uuid import uuid4


from states import greeting, info, InformationGatheringState, InitialState, questions

    

workflow = StateGraph(InformationGatheringState, input=InitialState, output=InformationGatheringState)

workflow.add_node("greeting", greeting)
workflow.add_node("info", info)
workflow.add_node("questions", questions)
workflow.add_edge(START, "greeting")
workflow.add_edge("greeting", "info")
workflow.add_edge("info", "questions")
workflow.add_edge("questions", END)



memory = MemorySaver()

graph = workflow.compile(checkpointer=memory)

run_id = uuid4()
thread_id = str(uuid4())
config = RunnableConfig(configurable={"thread_id": thread_id},run_id=run_id)

def stream_graph_updates(user_input: str):
    input_message = HumanMessage(content=user_input) 
    for event in graph.stream({"messages": [input_message]}, config=config, stream_mode="updates"):
        for value in event.values():
            # print("Assistant:", value["messages"][-1].pretty_print())
            if value:
                print("Assistant:", value["messages"].content)
                return value["messages"].content
    else:
        return "Sorry, I don't have a response at this moment!" 
