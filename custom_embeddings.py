import typing as t

from openai import AsyncOpenAI
from ragas.embeddings.base import BaseRagasEmbedding


class CustomEmbeddings(BaseRagasEmbedding):
    def __init__(
        self,
        client: AsyncOpenAI,
        model: str,
    ):
        super().__init__()
        self.client = client
        self.model = model

    def embed_text(self, text: str, **kwargs: t.Any) -> list[float]:
        raise RuntimeError("Use aembed_text — client is async.")

    async def aembed_text(self, text: str, **kwargs: t.Any) -> list[float]:
        response = await self.client.embeddings.create(
            model=self.model,
            input=text,
        )
        return response.data[0].embedding

    async def aembed_texts(self, texts: list[str], **kwargs: t.Any) -> list[list[float]]:
        response = await self.client.embeddings.create(
            model=self.model,
            input=texts,
        )
        return [item.embedding for item in response.data]
