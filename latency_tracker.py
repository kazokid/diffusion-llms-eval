import time
import typing as t
from datetime import datetime, timezone

import pandas as pd

from ragas.llms.base import InstructorBaseRagasLLM

InstructorTypeVar = t.TypeVar("T")


class LatencyTrackingLLM(InstructorBaseRagasLLM):
    def __init__(self, llm: InstructorBaseRagasLLM):
        self._llm = llm
        self._call_log: list[dict] = []
        self._metric_name: str = ""
        self._example_idx: int = -1
        self._question: str = ""
        self._case_id: str = ""
        self._call_index: int = 0

    def set_context(self, metric_name: str, example_idx: int, question: str, case_id: str = ""):
        self._metric_name = metric_name
        self._example_idx = example_idx
        self._question = question
        self._case_id = case_id
        self._call_index = 0

    def _record(self, prompt: str, response_model_name: str, response: t.Any, latency_s: float):
        usage = getattr(self._llm, "last_usage", None) or {}
        self._call_log.append({
            "case_id": self._case_id,
            "example_idx": self._example_idx,
            "question": self._question,
            "metric_name": self._metric_name,
            "call_index": self._call_index,
            "prompt": prompt,
            "response_model": response_model_name,
            "response": str(response),
            "latency_s": round(latency_s, 4),
            "prompt_tokens": usage.get("prompt_tokens", 0),
            "completion_tokens": usage.get("completion_tokens", 0),
            "total_tokens": usage.get("total_tokens", 0),
            "cached_tokens": usage.get("cached_tokens", 0),
            "reasoning_tokens": usage.get("reasoning_tokens", 0),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "model": getattr(self._llm, "model", "unknown"),
        })
        self._call_index += 1

    def generate(
        self, prompt: str, response_model: t.Type[InstructorTypeVar]
    ) -> InstructorTypeVar:
        start = time.perf_counter()
        result = self._llm.generate(prompt, response_model)
        self._record(prompt, response_model.__name__, result, time.perf_counter() - start)
        return result

    async def agenerate(
        self, prompt: str, response_model: t.Type[InstructorTypeVar]
    ) -> InstructorTypeVar:
        start = time.perf_counter()
        result = await self._llm.agenerate(prompt, response_model)
        self._record(prompt, response_model.__name__, result, time.perf_counter() - start)
        return result

    def get_call_log(self) -> list[dict]:
        return list(self._call_log)

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self._call_log)
