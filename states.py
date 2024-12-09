from typing import List, TypedDict, Literal, Annotated, Optional
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage, SystemMessage
from langgraph.graph.message import add_messages
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
import pdb


info_gathering_name_prompt = """Your are a interviewer, so introduce yourselves as a recruiter from E42.ai , your job is to ask questions to the user for getting users name.
Design a user-friendly question that effectively prompts users to provide their name.The question should be clear, concise, and inviting, ensuring that users feel comfortable responding.Consider various contexts in which this question might be asked, such as in a registration form, a chatbot interaction, or a survey.Additionally, provide variations of the question to accommodate different tones (formal, casual, friendly).

- STRICTLY ask the full name of the user when you start.
- STRICTLY ONLY ask name.
- STRICTLY DO NOT ask technical interview questions.

"""
info_gathering_skills_prompt = """Your are a technical interviewer, so introduce yourselves as a Technical recruiter from E42.ai, your job is to ask questions to the user for the entities : ['skills'].
  - STRICTLY dont introduce youreself.
  - STRICTLY dont add skills by youreself get it from user only.

"""
info_gathering_experience_prompt = """Your are a technical interviewer,  your job is to ask questions to the user for the entities : ['experience'].
  - STRICTLY dont introduce youreself.

"""
info_gathering_certifications_prompt = """Your are a technical interviewer, so introduce yourselves as a Technical recruiter from E42.ai before you go about the remaining tasks, your job is to ask questions to the user for the entities : ['certifications'].
   - STRICTLY dont introduce youreself. 

"""

gather_entities = """Extract entites from the text if any of them.
Don't introduce yourselves, directly go about extracting entities. 
STRICTLY give json output containing below entities 


The entities you need to extract are:
- `name`: The name of the user.
- `skills`: The skill sets of a user.
- `experience`: The years of experience the user possess.
- `certifications`: Certifications user has completed, keep it blank if the user says no or does not mention.

Note
- If skills is not available,  keep it `['NA']` .
- If certifications is not available,  keep it `['NA'].

"""
p = """
You are an Intelligent Extractor Assistant You will be provided with a message containing an individual’s professional profile. Your task is to extract the following entites:

Name: The name of the individual.
Skills: A list of skills mentioned.
Experience: duration work experience.
Certificates: Any certifications or qualifications mentioned.

Note
- STRICTLY give structured output
- If name is not available,  keep it '' .



"""

ask_queries = """You’re a seasoned technical interviewer with over 15 years of experience in assessing candidates for various roles in technology. You specialize in crafting insightful and challenging interview questions that effectively gauge both technical skills and problem-solving abilities, tailored to each candidate's expertise.

Your task is to generate a technical interview QUESTION based on the skills provided. Here are the details you need to consider:

- Skills to Assess: {skills}

Please note:
- STRICTLY Don't add any additional text other than question.

Please ensure that the questions cover a range of difficulty levels and include both theoretical and practical components, while also being relevant to current industry standards and technologies."""

class InitialState(TypedDict):
    messages: Annotated[list, add_messages]
    counter: int


class InformationGatheringState(TypedDict):
    name: str = ''
    skills: list = []
    experience: str = []
    certifications: list =[]
    messages: Annotated[list, add_messages]
    ai_message: Annotated[list, add_messages] 
    counter: int

class InformationGathered(BaseModel):
    """Information gathered from candidate"""
    name: Optional[str] = Field(..., description='Name of the user')
    skills: Optional[str] = Field(..., description='Skills listed by the user')
    experience: Optional[str] = Field(..., description='Years of experience a user has')
    certifications: Optional[str] = Field(..., description='Certifications listed by the user')

llm = ChatOllama(model = "llama3.2", temperature=0)
llm_structured = llm.with_structured_output(InformationGathered)

def greeting(state: InitialState) -> InitialState:
    
    response = llm.invoke([SystemMessage(content=info_gathering_name_prompt)] +
                                state['messages'])
    
    state["counter"] =  0
   
    state['messages'] = state['messages'] + [response]
    return state
    

def skills_collect(state: InformationGatheringState) -> InformationGatheringState:
    response = llm.invoke([SystemMessage(content=info_gathering_skills_prompt)] +
                                state['messages'])
    
    # state["counter"] +=  1
    data = {}
    state['messages'] = state['messages'] + [response]
    return state

def experience_collect(state: InformationGatheringState) -> InformationGatheringState:
    response = llm.invoke([SystemMessage(content=info_gathering_experience_prompt)] +
                                state['messages'])
    
    state['messages'] = state['messages'] + [response]
    return state

def certifications_collect(state: InformationGatheringState) -> InformationGatheringState:
    response = llm.invoke([SystemMessage(content=info_gathering_certifications_prompt)] +
                                state['messages'])
    
    # state["counter"] +=  1
    data = {}
    
    state['messages'] = state['messages'] + [response]
    pdb.set_trace()
    return state
    # response = llm_structured.invoke([SystemMessage(content=info_gathering_prompt)] +
    #                             messages)
    # if response:
       
    #     data = {}
    #     for entity_name,  entity_value in response:
    #         if entity_name not in state.keys() and entity_value != '--NA--':
    #             data[entity_name] = entity_value

    #     data.setdefault("messages",response)
    #     state.update(data)
    # return state


def info(state: InformationGatheringState):
    
    messages = state['messages']
    # state['conversations'].append(messages)
    # state['conversations'].append(llm.invoke([SystemMessage(content=info_gathering_prompt)] +
    #                             state["conversations"]))
    
    respone = llm_structured.invoke([SystemMessage(content=p)]+
                                messages)
    
    
       
    # if op_:
    #     output_dict = {}
    #     op_dict = op_.dict()
    #     
    #     # keys should be dynamic from Pydantic models
    #     for key in ['name', 'skills', 'experience', 'certifications']:
    #         if not state.get(key, '') and op_dict.get(key):
    #             output_dict[key] = op_dict[key]
    #     if output_dict:
    #         # print('\t DEBUG: Output ', output_dict)
    #         output_dict['counter'] = 
    #         return output_dict
    return respone

def skills_question(state: InformationGatheringState):
    messages = state['messages']
    # state['conversations'].append(messages)
    # state['conversations'].append(llm.invoke([SystemMessage(content=info_gathering_prompt)] +
    #                             state["conversations"])
    print("innn msg skills")
    state["counter"] +=  1
    print(messages)
    prompt = PromptTemplate(
        input_variables=["skills"],
        template=ask_queries,
    )

    
    final_prompt = prompt.format(skills=state["skills"])
    response = llm.invoke([SystemMessage(content=final_prompt)] +
                                state['messages'])
    
    # state["counter"] +=  1
    state['messages'] = state['messages'] + [response]
    return state

