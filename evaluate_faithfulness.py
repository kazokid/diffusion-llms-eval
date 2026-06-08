"""
Faithfulness metric experiments.

Experiment 1 — Statement Granularity:
  Measures how the LLM decomposes answers into atomic statements.
  No pre-generated statements; traces capture what was generated and how many.

Experiment 2 — NLI Scoring with Pre-generated Statements:
  Uses a fixed set of statements per row to isolate the NLI verdict step.
  Traces capture the final score and per-statement reasoning.


Running the experiment:
1. set the llm model and embedding model in the .env variable
2. set the dataset and statements paths
"""

import asyncio
import json

import pandas as pd

from clients import no_ssl_client
from config import LLM_MODEL, EMBEDDINGS_MODEL, INPUT_CSV, OUTPUT_DIR
from latency_tracker import LatencyTrackingLLM
from ragas.llms import llm_factory

from ragas.metrics.collections import Faithfulness


evaluator_llm = llm_factory(model=LLM_MODEL, client=no_ssl_client, max_completion_tokens=16384)
tracked_llm = LatencyTrackingLLM(evaluator_llm)

faithfulness = Faithfulness(llm=tracked_llm)

DATASET_PATH = "/Users/lokovacic/Projects/diffusion-llms-eval/datasets/final_datasets/faithfulness-test.csv"
STATEMENTS_PATH = "/Users/lokovacic/Projects/diffusion-llms-eval/datasets/final_datasets/faithfulness-test-statements.json"

print(f"LLM model: {LLM_MODEL}")
print(f"Embeddings model: {EMBEDDINGS_MODEL}")
print(f"Loading dataset from {DATASET_PATH}")
df = pd.read_csv(DATASET_PATH, encoding="utf-8")
print(f"  Rows: {len(df)}")


def parse_contexts(ctx_json: str) -> list[str]:
    return [item["text"] for item in json.loads(ctx_json)]


df["retrieved_contexts"] = df["retrieved_contexts"].apply(parse_contexts)

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
Examples of how you should respond in a conversation. These are just examples of tone and structure, information is irrelevant:
  Example 1:
  ___
  User: How do I download Python?
  Your answer: To download Python, go to the official Python webpage and follow the instructions regarding your operating system.

  Example 2:
  ___
  User: What monitor is best for gaming?
  Your answer: An ultra wide 2k monitor with a high refresh rate is going to be great for gaming. Avoid 4k monitors since they are usually aimed at office use.
////

"""


def _get_contexts(row) -> list[str]:
    ctx = row["retrieved_contexts"]
    if row.get("inject_system_msg"):
        ctx = [REJECTION_SYSTEM_PROMPT] + ctx
    return ctx


# ── Experiment 1: Statement Granularity ──────────────────────────────────────

async def run_experiment_1():
    """Run faithfulness end-to-end; trace captures LLM-generated statements."""
    print("\n" + "=" * 60)
    print("EXPERIMENT 1: Statement Granularity")
    print("=" * 60)

    results = []
    total = len(df)

    for i, (_, row) in enumerate(df.iterrows(), 1):
        print(f"  [{i}/{total}] {row['question'][:60]}...")
        tracked_llm.set_context("faithfulness_exp1", i - 1, row["question"], str(row.get("case_id", i - 1)))

        try:
            contexts = _get_contexts(row)
            result, trace = await faithfulness.ascore_trace(
                user_input=row["question"],
                response=row["answer"],
                retrieved_contexts=contexts,
            )
            results.append({
                "case_id": row.get("case_id", i),
                "case_description": row.get("case_description"),
                "question": row["question"],
                "answer": row["answer"],
                "retrieved_contexts": contexts,
                "score": result.value,
                **trace,
            })
        except Exception as e:
            print(f"    WARNING: failed: {e}")
            results.append({
                "case_id": row.get("case_id", i),
                "case_description": row.get("case_description"),
                "question": row["question"],
                "answer": row["answer"],
                "retrieved_contexts": _get_contexts(row),
                "score": None,
                "error": str(e),
            })

    return results


# ── Experiment 2: NLI Scoring with Pre-generated Statements ─────────────────


with open(STATEMENTS_PATH, encoding="utf-8") as f:
    pre_generated_statements: dict[str, list[str]] = json.load(f)
print(f"Loaded pre-generated statements from {STATEMENTS_PATH} ({len(pre_generated_statements)} cases)")


async def run_experiment_2():
    """Run faithfulness NLI only; uses pre-generated statements."""
    print("\n" + "=" * 60)
    print("EXPERIMENT 2: NLI Scoring with Pre-generated Statements")
    print("=" * 60)

    results = []
    total = len(df)

    for i, (_, row) in enumerate(df.iterrows(), 1):
        case_id = row.get("case_id", str(i))
        statements = pre_generated_statements.get(case_id)

        if statements is None:
            print(f"  [{i}/{total}] SKIP {case_id} — no pre-generated statements")
            continue

        print(f"  [{i}/{total}] {case_id}: {row['question'][:50]}... ({len(statements)} stmts)")
        tracked_llm.set_context("faithfulness_exp2", i - 1, row["question"], str(case_id))

        try:
            contexts = _get_contexts(row)
            result, trace = await faithfulness.ascore_trace(
                user_input=row["question"],
                response=row["answer"],
                retrieved_contexts=contexts,
                statements=statements,
            )
            results.append({
                "case_id": case_id,
                "case_description": row.get("case_description"),
                "question": row["question"],
                "answer": row["answer"],
                "retrieved_contexts": contexts,
                "score": result.value,
                **trace,
            })
        except Exception as e:
            print(f"    WARNING: failed: {e}")
            results.append({
                "case_id": case_id,
                "case_description": row.get("case_description"),
                "question": row["question"],
                "answer": row["answer"],
                "retrieved_contexts": _get_contexts(row),
                "score": None,
                "error": str(e),
            })

    return results


# ── Main ─────────────────────────────────────────────────────────────────────

async def main():
    exp1_results = await run_experiment_1()
    exp2_results = await run_experiment_2()
    return exp1_results, exp2_results


timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
model_name = LLM_MODEL.replace("/", "_")
model_dir = OUTPUT_DIR / model_name
model_dir.mkdir(parents=True, exist_ok=True)

exp1_results, exp2_results = asyncio.run(main())

exp1_path = model_dir / f"{timestamp}_{model_name}_faithfulness_exp1_granularity.json"
with open(exp1_path, "w", encoding="utf-8") as f:
    json.dump({
        "experiment": "faithfulness_statement_granularity",
        "evaluator_llm": LLM_MODEL,
        "dataset": DATASET_PATH,
        "results": exp1_results,
    }, f, indent=2, ensure_ascii=False)
print(f"\nExperiment 1 saved to: {exp1_path}")

exp2_path = model_dir / f"{timestamp}_{model_name}_faithfulness_exp2_nli.json"
with open(exp2_path, "w", encoding="utf-8") as f:
    json.dump({
        "experiment": "faithfulness_nli_scoring",
        "evaluator_llm": LLM_MODEL,
        "dataset": DATASET_PATH,
        "results": exp2_results,
    }, f, indent=2, ensure_ascii=False)
print(f"\nExperiment 2 saved to: {exp2_path}")

latency_path = model_dir / f"{timestamp}_{model_name}_faithfulness_experiments_latency.csv"
tracked_llm.to_dataframe().to_csv(latency_path, index=False)
print(f"\nLatency log saved to: {latency_path}")
