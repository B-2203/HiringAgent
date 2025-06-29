import requests
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage, SystemMessage

from states import llm_structured, gather_entities

url = "http://<DOMAIN>/edith/service/get_ocr"

payload = {"scale": 4.17}
headers = {
    'Authorization': 'Bearer <TOKEN>'
}

def create_prompt(resume_data):
    resume_extract_prompt = f'''
    Extract relevant information from the following Text into a JSON object.

    Text: {resume_data}

    Output format:
    name: str,
    skills: list[str],
    experience: str,
    certifications: list[str]
    
    Note: All the fields in the output should only be present if it is explicitly mentioned in the text. DON'T ASSUME ANYTHING.
    ONLY ADD THE TEXT WHICH YOU ARE COMPLETELY SURE FITS THE CONTEXT. Don't add LAST NAME if not mentioned in the text. 
    '''
    return resume_extract_prompt

def extract_entities(resume_data):

    resume_entities = {}
    resume_extract_prompt = create_prompt(resume_data)
    response = llm_structured.invoke(resume_extract_prompt)
    if response:
        for entity_name, entity_value in response:
            if entity_name in ["name", "skills", "experience", "certifications"]:
                if entity_name not in resume_entities.keys() or (entity_name in resume_entities.keys() and not resume_entities['entity_name']):
                    resume_entities[entity_name] = entity_value

    return resume_entities

def extract_resume_data(file):
    """
    Extract key entities from resume
    """
    file_type = file.filename.split('.')[-1]
    files=[
            (file_type, (file.filename, file.read(),file.headers[-1][-1] ))
        ]
    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    # print(response.text)
    resume_data = " ".join(response.json()['result'][0][0])
    entities_extracted = extract_entities(resume_data)

    return entities_extracted
