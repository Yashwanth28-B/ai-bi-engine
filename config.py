import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API keys from environment variables
MONDAY_API_KEY = os.getenv("MONDAY_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

URL = "https://api.monday.com/v2"

# For backward compatibility
API_KEY = MONDAY_API_KEY

DEALS_BOARD_ID = 5026563623
WORK_ORDERS_BOARD_ID = 5026563580
