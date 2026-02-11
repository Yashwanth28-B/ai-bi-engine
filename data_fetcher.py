import requests
from config import API_KEY, URL

API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjYxOTgzNjEwNSwiYWFpIjoxMSwidWlkIjo5OTcwNjQ0NSwiaWFkIjoiMjAyNi0wMi0xMVQwNjoyNDowOS4yOTJaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MzM3NDgzNTgsInJnbiI6ImFwc2UyIn0.tkRwyX-7rxbt2_A9816kAcSEx8Y70cTM7WUbAGwrIg4"
URL = "https://api.monday.com/v2"

headers = {
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}

def get_board_data(board_id):
    query = {
        "query": f"""
        {{
          boards(ids: {board_id}) {{
            items_page(limit: 100) {{
              items {{
                name
                column_values {{
                  id
                  text
                }}
              }}
            }}
          }}
        }}
        """
    }
    r = requests.post(URL, json=query, headers=headers)
    return r.json()
