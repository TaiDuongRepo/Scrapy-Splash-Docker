import requests

response = requests.get("http://splash:8050")
print(response.status_code)
