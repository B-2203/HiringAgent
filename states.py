from typing import List, TypedDict, Literal, Annotated, Optional
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage, SystemMessage
from langgraph.graph.message import add_messages
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field


info_gathering_prompt = """Your are a technical interviewer, so introduce yourselves as a Technical recruiter from E42.ai before you go about the remaining tasks, your job is to ask questions to the user and collect the entities : ['name', 'skills', 'experience', 'certifications'].
- STRICTLY give json output containing the above entities, but do not mention this to the user. 
- STRICTLY ask the full name of the user when you start.
- STRICTLY get only the following information from them:

- What is the user's name
- What skills the user possess
- How many years of experience the user has
- Any certifications done by the user
"""

gather_entities = """Extract entites from the text if any of them not there fill them with --NA--.
Don't introduce yourselves, directly go about extracting entities. 
STRICTLY give json output containing below entities, but do not mention this to the user. 

The entities you need to extract are:
- 'name': The name of the user.
- 'skills': The skill sets of a user.
- 'experience': The years of experience the user possess.
- 'certifications': Certifications user has completed, keep it blank if the user says no or does not mention.
"""

class InitialState(TypedDict):
    messages: Annotated[list, add_messages]

class InformationGatheringState(TypedDict):
    name: str
    skills: list
    experience: str
    certifications: list
    messages: Annotated[list, add_messages]
    ai_message: Annotated[list, add_messages] 

class InformationGathered(BaseModel):
    """Information gathered from candidate"""
    name: Optional[str] = Field(..., description='Name of the user')
    skills: Optional[List[str]] = Field(..., description='Skills listed by the user')
    experience: Optional[str] = Field(..., description='Years of experience a user has')
    certifications: Optional[List[str]] = Field(..., description='Certifications listed by the user')

llm = ChatOllama(model = "llama3.2", temperature=0)
llm_structured = llm.with_structured_output(InformationGathered)


def greeting(state: InitialState) -> InformationGatheringState:
    
    response = llm.invoke([SystemMessage(content=info_gathering_prompt)] +
                                state['messages'])
    return {'messages': response}


def info(state: InformationGatheringState):
    messages = state['messages']
    # state['conversations'].append(messages)
    # state['conversations'].append(llm.invoke([SystemMessage(content=info_gathering_prompt)] +
    #                             state["conversations"]))
    response = llm_structured.invoke([SystemMessage(content=gather_entities),
                                messages[-2]])
    if response:
        data = {}
        for entity_name,  entity_value in response:
            if entity_name not in state.keys() and entity_value != '--NA--':
                data[entity_name] = entity_value

        data.setdefault("messages", messages[-1])
        state.update(data)
    return state

