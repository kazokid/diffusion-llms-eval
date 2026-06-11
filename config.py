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

# INPUT_CSV = Path(__file__).parent / "datasets/final_datasets/answer-relevancy-test.csv"
# INPUT_CSV = Path(__file__).parent / "datasets/final_datasets/context-relevance-test.csv"
# INPUT_CSV = Path(__file__).parent / "datasets/final_datasets/response-groundedness-test.csv"
INPUT_CSV = Path(__file__).parent / "datasets/final_datasets/context-utilization-test.csv"

OUTPUT_DIR = Path(__file__).parent / "results"

# METRIC = "answer_relevancy"
# METRIC = "context_relevance"
# METRIC = "response_groundedness"
METRIC = "context_utilization"



# ANNOTATED_CSV = Path(__file__).parent / "datasets/final_datasets/answer_relevancy-test-annotated.csv"
ANNOTATED_CSV = None

QWEN_ENABLE_THINKING = os.environ.get("QWEN_ENABLE_THINKING", "false").lower() in ("true", "1", "yes")


def llm_extra_kwargs() -> dict:
    if LLM_MODEL and "qwen" in LLM_MODEL.lower():
        return {"extra_body": {"chat_template_kwargs": {"enable_thinking": QWEN_ENABLE_THINKING}}}
    return {}