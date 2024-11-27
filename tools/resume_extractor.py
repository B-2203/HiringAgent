import requests

url = "http://balaji.e42.ai/edith/service/get_ocr"

payload = {"scale": 4.17}
headers = {
    'Authorization': 'Bearer BUT80uJgdxlwkJX15IJ1D3X6QWRpVf'
}

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
    return resume_data