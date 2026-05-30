import asyncio
import json


import pandas as pd

from clients import embeddings_client, no_ssl_client
from config import (
    LLM_MODEL,
    EMBEDDINGS_MODEL,
    INPUT_CSV,
    OUTPUT_DIR,
)
from latency_tracker import LatencyTrackingLLM
from ragas.llms import llm_factory
from ragas.metrics.collections import (
    AnswerRelevancy,
    ContextRelevance,
    ContextUtilization,
    Faithfulness,
    ResponseGroundedness,
)

from custom_embeddings import CustomEmbeddings


# evaluator_llm = llm_factory(model=LLM_MODEL, client=client)
evaluator_llm = llm_factory(model=LLM_MODEL, client=no_ssl_client, max_tokens=8096)
tracked_evaluator_llm = LatencyTrackingLLM(evaluator_llm)

embeddings = CustomEmbeddings(
        client=embeddings_client,
        model=EMBEDDINGS_MODEL,
    )

metrics = [
    AnswerRelevancy(llm=tracked_evaluator_llm, embeddings=embeddings, strictness=1),
    Faithfulness(llm=tracked_evaluator_llm),
    ContextRelevance(llm=tracked_evaluator_llm),
    ContextUtilization(llm=tracked_evaluator_llm),
    ResponseGroundedness(llm=tracked_evaluator_llm),
]

METRIC_KWARGS = {
    "answer_relevancy": lambda row: {
        "user_input": row["question"],
        "response": row["answer"],
    },
    "faithfulness": lambda row: {
        "user_input": row["question"],
        "response": row["answer"],
        "retrieved_contexts": row["retrieved_contexts"],
    },
    "context_relevance": lambda row: {
        "user_input": row["question"],
        "retrieved_contexts": (
            [REJECTION_SYSTEM_PROMPT] + row["retrieved_contexts"]
            if row["is_rejection"] else row["retrieved_contexts"]
        ),
    },
    "context_utilization": lambda row: {
        "user_input": row["question"],
        "response": row["answer"],
        "retrieved_contexts": [REJECTION_SYSTEM_PROMPT] + row["retrieved_contexts"],
    },
    "response_groundedness": lambda row: {
        "response": row["answer"],
        "retrieved_contexts": (
            [REJECTION_SYSTEM_PROMPT] + row["retrieved_contexts"]
            if row["is_rejection"] else row["retrieved_contexts"]
        ),
    },
}

REJECTION_SYSTEM_PROMPT = """You are a chatbot, your name is Langy.
You represent LangChain. LangChain is an AI infrastructure company focused on helping developers and enterprises build, test, observe, and deploy reliable LLM-powered applications and AI agents.
Its product line includes LangChain, the open-source framework for building LLM applications; LangGraph, an open-source framework for stateful, multi-step agent workflows; and LangSmith, its commercial agent-engineering platform for observability, evaluation, testing, and deployment.
LangChain positions these tools as a full stack for moving AI agents from prototype to production

You will receive context where you can extract data to provide answers to user's questions.
Context will be delimited with: ###
Reply to the user directly, without talking about the context provided.
People can have follow-up questions following the previous questions.
Questions will be delimited with **
You should speak the truth, do not make up facts.
If you don't know the answer, or it's not in the documents, honestly say that you can't help with that question.

////
For the following topics, do not give answers:
[competitors, sex and drugs, politics]

Examples of topics to which you do not provide answers:
-- Is COMPETITOR better than COMPANY => Unfortunately I can't help you with questions related to COMPETITOR, I'm a chatbot for COMPANY.
-- Is POLITICIAN corrupt => Unfortunately I can't help you with the inquiry for POLITICIAN, I'm a chatbot for COMPANY.
////

////
Examples of how you should respond in a conversation:
  Example 1:
  ___
  User: What is LLM-as-a-judge?
  Your answer: LLM-as-a-judge is an approach for evaluating AI agent outputs using a large language model as a scalable substitute for human judgment.

  User: What is agent observability?
  Your answer: Agent observability includes step-by-step visibility into an AI agent's execution showing tool calls and data retrieval.
  ___
////

"""

print(f"Loading dataset from {INPUT_CSV}")
df = pd.read_csv(INPUT_CSV, encoding="utf-8")
print(f"  Rows: {len(df)}")


def parse_contexts(ctx_json: str) -> list[str]:
    contexts = json.loads(ctx_json)
    return [item["text"] for item in contexts]


df["retrieved_contexts"] = df["retrieved_contexts"].apply(parse_contexts)
df["is_rejection"] = df["case_description"].str.contains("rejection", case=False, na=False)


async def run_evaluation():
    results = {m.name: [] for m in metrics}
    traces = []
    total = len(df)

    for i, (_, row) in enumerate(df.iterrows(), 1):
        print(f"  [{i}/{total}] {row['question'][:60]}...")
        case_id = str(row.get("case_id", i - 1))
        row_traces = {"case_id": case_id, "question": row["question"], "answer": row["answer"]}

        for metric in metrics:
            tracked_evaluator_llm.set_context(metric.name, i - 1, row["question"], case_id)
            kwargs = METRIC_KWARGS[metric.name](row)
            try:
                result, trace = await metric.ascore_trace(**kwargs)
                results[metric.name].append(result.value)
                row_traces[metric.name] = {"score": result.value, **trace}
            except Exception as e:
                print(f"    WARNING: {metric.name} failed: {e}")
                results[metric.name].append(None)
                row_traces[metric.name] = {"score": None, "error": str(e)}

        traces.append(row_traces)

    return results, traces


timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
model_name = LLM_MODEL.replace("/", "_")
input_csv_stem = INPUT_CSV.stem
model_dir = OUTPUT_DIR / model_name
model_dir.mkdir(parents=True, exist_ok=True)
output_path = model_dir / f"{timestamp}_{model_name}_{input_csv_stem}_results.csv"
traces_path = model_dir / f"{timestamp}_{model_name}_{input_csv_stem}_details.json"

print("\nRunning evaluation...")
print(f"  LLM model: {LLM_MODEL}")
print(f"  Embeddings model: {EMBEDDINGS_MODEL}\n")

results, traces = asyncio.run(run_evaluation())

print("\n" + "=" * 60)
print("EVALUATION RESULTS")
print("=" * 60)

for metric_name, scores in results.items():
    valid = [s for s in scores if s is not None]
    if valid:
        avg = sum(valid) / len(valid)
        print(f"  {metric_name}: {avg:.4f} ({len(valid)}/{len(scores)} successful)")

results_df = pd.DataFrame(results)
results_df["evaluator_llm"] = LLM_MODEL
results_df["embeddings_model"] = EMBEDDINGS_MODEL
results_df["input_csv"] = INPUT_CSV.name
base_cols = ["question", "answer"]
if "topic" in df.columns:
    base_cols.append("topic")
if "case_id" in df.columns:
    base_cols.insert(0, "case_id")
final_df = pd.concat(
    [
        df[base_cols].reset_index(drop=True),
        results_df.reset_index(drop=True),
    ],
    axis=1,
)

final_df.to_csv(output_path, index=False)
print(f"\nPer-row results saved to: {output_path}")

traces_output = {
    "input_csv": INPUT_CSV.name,
    "evaluator_llm": LLM_MODEL,
    "embeddings_model": EMBEDDINGS_MODEL,
    "traces": traces,
}
with open(traces_path, "w", encoding="utf-8") as f:
    json.dump(traces_output, f, indent=2, ensure_ascii=False)
print(f"Detailed traces saved to: {traces_path}")

latency_path = model_dir / f"{timestamp}_{model_name}_{input_csv_stem}_latency.csv"
tracked_evaluator_llm.to_dataframe().to_csv(latency_path, index=False)
print(f"Latency log saved to: {latency_path}")
