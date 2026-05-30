from config import EMBEDDINGS_URL_BASE, EMBEDDINGS_API_KEY, LLM_BASE_URL, LLM_API_KEY
from constants import ADDITIONAL_HEADERS

from openai import AsyncOpenAI
import httpx

embeddings_client = AsyncOpenAI(
            base_url=EMBEDDINGS_URL_BASE,
            api_key=EMBEDDINGS_API_KEY,
            default_headers=ADDITIONAL_HEADERS,
            http_client=httpx.AsyncClient(verify=False),
            timeout=httpx.Timeout(60),
        )

client = AsyncOpenAI(
    base_url=LLM_BASE_URL,
    api_key=LLM_API_KEY,
    default_headers=ADDITIONAL_HEADERS,
    timeout=httpx.Timeout(60),
)

no_ssl_client = AsyncOpenAI(
        base_url=LLM_BASE_URL,
        api_key=LLM_API_KEY,
        default_headers=ADDITIONAL_HEADERS,
        http_client=httpx.AsyncClient(verify=False),
        timeout=httpx.Timeout(60),
    )