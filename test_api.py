import requests

API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjYxOTgzNjEwNSwiYWFpIjoxMSwidWlkIjo5OTcwNjQ0NSwiaWFkIjoiMjAyNi0wMi0xMVQwNjoyNDowOS4yOTJaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MzM3NDgzNTgsInJnbiI6ImFwc2UyIn0.tkRwyX-7rxbt2_A9816kAcSEx8Y70cTM7WUbAGwrIg4"
URL = "https://api.monday.com/v2"

query = {
    "query": "{ boards { id name } }"
}

headers = {
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}

r = requests.post(URL, json=query, headers=headers)
print(r.json())
