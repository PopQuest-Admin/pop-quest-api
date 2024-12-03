import requests

def websrc(link):
    response = requests.get(link)
    return response.text