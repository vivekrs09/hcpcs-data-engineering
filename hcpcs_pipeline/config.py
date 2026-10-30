
import os
from dotenv import load_dotenv

load_dotenv()

SOURCE_URL = os.getenv(
    "HCPCS_SOURCE_URL",
    "https://clinicaltables.nlm.nih.gov/"
)

REQUEST_TIMEOUT_SECONDS = int(
    os.getenv("REQUEST_TIMEOUT_SECONDS", "30")
)

RAW_DATA_DIR = os.getenv("RAW_DATA_DIR", "data/raw")
