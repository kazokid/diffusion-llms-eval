"""Quick connectivity test for LLM and embeddings endpoints."""

import asyncio

from clients import no_ssl_client, embeddings_client
from config import (
    LLM_BASE_URL,
    LLM_MODEL,
    LLM_API_KEY,
    EMBEDDINGS_URL_BASE,
    EMBEDDINGS_MODEL,
    EMBEDDINGS_API_KEY,
)
from constants import ADDITIONAL_HEADERS
from custom_embeddings import CustomEmbeddings



async def test_llm():
    print(f"LLM endpoint: {LLM_BASE_URL}")
    print(f"LLM model:    {LLM_MODEL}")

    # llm_client = client
    llm_client = no_ssl_client

    response = await llm_client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": "Say hello in one word."}],
        max_completion_tokens=10,
    )
    text = response.choices[0].message.content
    print(f"LLM response: {text}")
    return True


async def test_embeddings():
    print(f"\nEmbeddings endpoint: {EMBEDDINGS_URL_BASE}")
    print(f"Embeddings model:    {EMBEDDINGS_MODEL}")
    emb = CustomEmbeddings(
        client=embeddings_client,
        model=EMBEDDINGS_MODEL,
    )

    vector = await emb.aembed_text("test")
    print(f"Embedding dim: {len(vector)}")
    print(f"First 5 values: {vector[:5]}")
    return True


async def main():
    print("=" * 40)
    print("TESTING LLM CONNECTION")
    print("=" * 40)
    try:
        await test_llm()
        print("OK")
    except Exception as e:
        import traceback
        print(f"FAILED: {type(e).__name__}: {e}")
        traceback.print_exc()

    print("\n" + "=" * 40)
    print("TESTING EMBEDDINGS CONNECTION")
    print("=" * 40)
    try:
        await test_embeddings()
        print("OK")
    except Exception as e:
        import traceback
        print(f"FAILED: {type(e).__name__}: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
