import os
from dotenv import load_dotenv

load_dotenv()

# LLM Configuration
LLM_API_KEY = os.getenv("LLM_API_KEY", "sk-PEYZKs0mLr7w9WzP02Xct48X50t4L45ZFrZEN7JsoHQ=")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://mkp-api.fptcloud.com/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-oss-20b")

# External APIs
RXNORM_BASE_URL = "https://rxnav.nlm.nih.gov/REST"
OPENFDA_BASE_URL = "https://api.fda.gov/drug"

# App settings
APP_TITLE = "AI Chăm Sóc Sức Khỏe"
APP_VERSION = "1.0.0"
REQUEST_TIMEOUT = 15
