import requests

url = "http://balaji.e42.ai/edith/service/get_ocr"

payload = {"scale": 4.17}
files=[
        ('pdf',('BALAJI_Vantari.pdf',open('/mnt/c/Users/balu/Downloads/BALAJI_Vantari.pdf','rb'),'application/pdf'))
    ]
headers = {
    'Authorization': 'Bearer BUT80uJgdxlwkJX15IJ1D3X6QWRpVf'
}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

# print(response.text)
print(" ".join(response.json()['result'][0][0]))