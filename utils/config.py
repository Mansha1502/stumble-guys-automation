import os

from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://www.stumbleguys.com/")
TEST_EMAIL = os.getenv("TEST_EMAIL", "")
AUTH_STATE_PATH = "auth/state.json"
SESSION_STORAGE_PATH = "auth/session_storage.json"
SITE_ORIGIN = "https://www.stumbleguys.com"

BROWSERSTACK_USERNAME = os.getenv("BROWSERSTACK_USERNAME", "")
BROWSERSTACK_ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY", "")