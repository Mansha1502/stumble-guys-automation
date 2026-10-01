import os

from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://www.stumbleguys.com/")
AUTH_STATE_PATH = "auth/state.json"

