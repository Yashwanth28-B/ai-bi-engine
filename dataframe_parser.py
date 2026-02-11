import pandas as pd

def monday_json_to_df(board_json):
    """
    Converts monday.com board JSON into Pandas DataFrame
    """
    
    # Check for API errors
    if "errors" in board_json:
        print(f"API Error: {board_json['errors']}")
        return pd.DataFrame()
    
    # Check if data exists
    if "data" not in board_json:
        print(f"Unexpected response format: {board_json}")
        return pd.DataFrame()

    items = board_json["data"]["boards"][0]["items_page"]["items"]

    rows = []

    for item in items:
        row = {}

        # Item name as main identifier
        row["item_name"] = item["name"]

        for col in item["column_values"]:
            col_name = col["id"].lower().strip()
            col_value = col["text"]

            # Normalize column names
            col_name = col_name.replace(" ", "_")

            row[col_name] = col_value

        rows.append(row)

    df = pd.DataFrame(rows)

    return df
