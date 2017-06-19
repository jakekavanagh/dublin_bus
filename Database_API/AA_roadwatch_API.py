import requests

url = "http://schemas.datacontract.org/2004/07/WCF.AAIreland.Data"

response = requests.get(url)
result = response.json()

print(result)