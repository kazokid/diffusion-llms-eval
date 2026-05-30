import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

LLM_BASE_URL = os.environ["LLM_BASE_URL"]
LLM_API_KEY = os.environ.get("LLM_API_KEY", "no-api-key")
LLM_MODEL = os.environ.get("LLM_MODEL")

EMBEDDINGS_MODEL = os.environ.get("EMBEDDINGS_MODEL")
EMBEDDINGS_URL_BASE = os.environ["EMBEDDINGS_URL_BASE"]
EMBEDDINGS_API_KEY = os.environ.get("EMBEDDINGS_API_KEY", "no-api-key")

# INPUT_CSV = Path(__file__).parent / "datasets/baby-langchain-easy-questions-answered-test.csv"
INPUT_CSV = Path(__file__).parent / "datasets/final_datasets/test.csv"
OUTPUT_DIR = Path(__file__).parent / "results"