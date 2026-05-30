"""Generate all LLM-as-a-judge test datasets from the chunk library."""

import csv
import json
import os
import sys

DATASETS_DIR = os.path.join(os.path.dirname(__file__), "..", "datasets")
CHUNK_LIB_PATH = os.path.join(DATASETS_DIR, "chunk_library.json")

with open(CHUNK_LIB_PATH, encoding="utf-8") as f:
    _CHUNKS = {c["id"]: c for c in json.load(f)}


def C(chunk_id: str) -> dict:
    """Return a context dict ready for the retrieved_contexts JSON array."""
    c = _CHUNKS[chunk_id]
    return {"text": c["text"], "filename": c["filename"]}


def ctx_json(*chunk_ids: str) -> str:
    """Build the retrieved_contexts JSON string from chunk IDs."""
    return json.dumps([C(cid) for cid in chunk_ids], ensure_ascii=False)


def write_csv(filename: str, rows: list[dict]):
    path = os.path.join(DATASETS_DIR, filename)
    fieldnames = ["case_id", "case_description", "question", "answer", "retrieved_contexts", "expected_score_range"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  {filename}: {len(rows)} rows")


# ── Shorthand chunk IDs ─────────────────────────────────────────────────────
# These are frequently referenced chunks, aliased for readability.

# LLM-as-a-judge
JUDGE_WHAT = "_articles_llm-as-a-judge_annotated.docx:0"
JUDGE_WHY = "_articles_llm-as-a-judge_annotated.docx:1"
JUDGE_TYPES = "_articles_llm-as-a-judge_annotated.docx:2"
JUDGE_CONFIG = "_articles_llm-as-a-judge_annotated.docx:3"
JUDGE_BIASES = "_articles_llm-as-a-judge_annotated.docx:10"
JUDGE_PROD = "_articles_llm-as-a-judge_annotated.docx:8"
JUDGE_ALIGN = "_articles_llm-as-a-judge_annotated.docx:4"
JUDGE_FEWSHOT = "_articles_llm-as-a-judge_annotated.docx:6"

# Evaluation framework
EVAL_TRAJ = "_articles_llm-evaluation-framework_annotated.docx:6"
EVAL_RAG = "_articles_llm-evaluation-framework_annotated.docx:15"
EVAL_RETR_REASON = "_articles_llm-evaluation-framework_annotated.docx:16"
EVAL_HIDDEN = "_articles_llm-evaluation-framework_annotated.docx:4"
EVAL_TRAJ_SCORE = "_articles_llm-evaluation-framework_annotated.docx:11"
EVAL_MULTISTEP = "_articles_llm-evaluation-framework_annotated.docx:18"
EVAL_RETR_TABLE = "_articles_llm-evaluation-framework_annotated.docx:17"
EVAL_METRICS = "_articles_llm-evaluation-framework_annotated.docx:5"
EVAL_TRAJ_CAPTURE = "_articles_llm-evaluation-framework_annotated.docx:8"

# Evaluation metrics
METRICS_WHAT = "_articles_llm-evaluation-metrics_annotated.docx:0"
METRICS_TRAD = "_articles_llm-evaluation-metrics_annotated.docx:1"
METRICS_RAG = "_articles_llm-evaluation-metrics_annotated.docx:14"
METRICS_OFFLINE = "_articles_llm-evaluation-metrics_annotated.docx:11"
METRICS_SCORING = "_articles_llm-evaluation-metrics_annotated.docx:8"
METRICS_MULTITURN = "_articles_llm-evaluation-metrics_annotated.docx:13"
METRICS_JUDGE_LIMITS = "_articles_llm-evaluation-metrics_annotated.docx:18"

# Continual learning
CL_MODEL = "_blog_continual-learning-for-ai-agents_annotated.docx:0"
CL_HARNESS = "_blog_continual-learning-for-ai-agents_annotated.docx:1"
CL_CONTEXT = "_blog_continual-learning-for-ai-agents_annotated.docx:2"
CL_TRACES = "_blog_continual-learning-for-ai-agents_annotated.docx:3"

# Agent observability
AOBS_WHAT = "_articles_agent-observability_annotated.docx:0"
AOBS_VALUE = "_articles_agent-observability_annotated.docx:1"
AOBS_EVAL = "_articles_agent-observability_annotated.docx:9"
AOBS_DATASETS = "_articles_agent-observability_annotated.docx:10"
AOBS_DEEP = "_articles_agent-observability_annotated.docx:5"
AOBS_THREADS = "_articles_agent-observability_annotated.docx:8"

# AI observability
AIOBS_WHAT = "_articles_ai-observability_annotated.docx:0"
AIOBS_PILLARS = "_articles_ai-observability_annotated.docx:1"
AIOBS_STACK = "_articles_ai-observability_annotated.docx:5"
AIOBS_GAP = "_articles_ai-observability_annotated.docx:8"
AIOBS_TRAD = "_articles_ai-observability_annotated.docx:9"
AIOBS_ANNOT = "_articles_ai-observability_annotated.docx:12"
AIOBS_COMPLIANCE = "_articles_ai-observability_annotated.docx:14"

# LangSmith vs Langfuse
VS_INTRO = "_articles_langsmith-vs-langfuse_annotated.docx:0"
VS_LIMITS = "_articles_langsmith-vs-langfuse_annotated.docx:3"
VS_ALERT = "_articles_langsmith-vs-langfuse_annotated.docx:8"
VS_FAQ = "_articles_langsmith-vs-langfuse_annotated.docx:16"

# MongoDB partnership
MONGO_DELIVERS = "_blog_announcing-the-langchain-mongodb-partnership-the-ai-agent-stack-that-runs-on-the-database-you-already-trust_annotated.docx:2"
MONGO_TEAMS = "_blog_announcing-the-langchain-mongodb-partnership-the-ai-agent-stack-that-runs-on-the-database-you-already-trust_annotated.docx:3"

# Agentic engineering
AGENG_WHAT = "_blog_agentic-engineering-redefining-software-engineering_annotated.docx:0"
AGENG_ARCH = "_blog_agentic-engineering-redefining-software-engineering_annotated.docx:6"
AGENG_FINDINGS = "_blog_agentic-engineering-redefining-software-engineering_annotated.docx:11"
AGENG_RESULTS = "_blog_agentic-engineering-redefining-software-engineering_annotated.docx:1"

# Harness hill climbing
HARNESS_RECIPE = "_blog_better-harness-a-recipe-for-harness-hill-climbing-with-evals_annotated.docx:4"
HARNESS_CHANGES = "_blog_better-harness-a-recipe-for-harness-hill-climbing-with-evals_annotated.docx:5"
HARNESS_EVALS = "_blog_better-harness-a-recipe-for-harness-hill-climbing-with-evals_annotated.docx:1"

# Credit Genie
CGENIE_APP = "_blog_credit-genie-insights-agent-financial-assistant_annotated.docx:4"
CGENIE_GAPS = "_blog_credit-genie-insights-agent-financial-assistant_annotated.docx:8"

# Arcade Fleet
ARCADE_WHAT = "_blog_arcade-dev-tools-now-in-langsmith-fleet_annotated.docx:0"
ARCADE_WRAPPER = "_blog_arcade-dev-tools-now-in-langsmith-fleet_annotated.docx:4"

# Context compression
COMPRESS_WHEN = "_blog_autonomous-context-compression_annotated.docx:0"
COMPRESS_EXP = "_blog_autonomous-context-compression_annotated.docx:3"

# Kensho
KENSHO_CHALLENGE = "_blog_customers-kensho_annotated.docx:3"
KENSHO_FRAMEWORK = "_blog_customers-kensho_annotated.docx:4"
KENSHO_LEARNINGS = "_blog_customers-kensho_annotated.docx:6"

# LangChain company
COMPANY_ABOUT = "_about_annotated.docx:0"

# Observability powers evaluation
OBSPOW_PRIMITIVES = "_blog_agent-observability-powers-agent-evaluation_annotated.docx:3"
OBSPOW_EVAL = "_blog_agent-observability-powers-agent-evaluation_annotated.docx:4"

# Evaluation readiness
READY_BEFORE = "_blog_agent-evaluation-readiness-checklist_annotated.docx:2"
READY_DATASET = "_blog_agent-evaluation-readiness-checklist_annotated.docx:4"


# ═══════════════════════════════════════════════════════════════════════════════
# ANSWER RELEVANCY — 25 cases
# ═══════════════════════════════════════════════════════════════════════════════

def gen_answer_relevancy() -> list[dict]:
    rows = []

    # --- Relevant answers (5) ---
    rows.append(dict(
        case_id="AR1", case_description="RELEVANT: complete answer to single question",
        question="What is LLM-as-a-judge and how does it work?",
        answer="LLM-as-a-judge uses a large language model to evaluate AI agent outputs as a scalable substitute for human judgment. You provide the LLM with a prompt describing evaluation criteria alongside the output to evaluate, and the model returns a score or judgment. It works well because evaluating text is a more focused, constrained task than generating it.",
        retrieved_contexts=ctx_json(JUDGE_WHAT),
        expected_score_range="0.7-1.0",
    ))
    rows.append(dict(
        case_id="AR2", case_description="RELEVANT: detailed answer covering multiple aspects",
        question="What are the three layers of continual learning for AI agents?",
        answer="Continual learning for AI agents happens at three layers: (1) the model layer, which involves updating weights through techniques like SFT or RLHF, (2) the harness layer, which means modifying orchestration logic, tool selection, or routing rules, and (3) the context layer, which involves updating instructions, few-shot examples, or retrieval knowledge at inference time without changing the model or harness code.",
        retrieved_contexts=ctx_json(CL_MODEL, CL_HARNESS, CL_CONTEXT),
        expected_score_range="0.7-1.0",
    ))
    rows.append(dict(
        case_id="AR3", case_description="RELEVANT: accurate concise answer",
        question="What is agent observability?",
        answer="Agent observability provides step-by-step visibility into an AI agent's execution, showing which tools were called, what data was retrieved, and where reasoning diverged from the intended path. It's essential because AI agents make autonomous decisions that aren't visible in the code.",
        retrieved_contexts=ctx_json(AOBS_WHAT),
        expected_score_range="0.7-1.0",
    ))
    rows.append(dict(
        case_id="AR4", case_description="RELEVANT: answer with specific details",
        question="What biases affect LLM-as-a-judge evaluators?",
        answer="LLM judges have several known biases: position bias causes judges to favor outputs in certain positions during pairwise comparison, verbosity bias leads to preferring longer responses, and self-enhancement bias causes models to rate their own outputs higher. These can be mitigated through techniques like randomizing response order, using multiple judge models, and calibrating against human annotations.",
        retrieved_contexts=ctx_json(JUDGE_BIASES),
        expected_score_range="0.7-1.0",
    ))
    rows.append(dict(
        case_id="AR5", case_description="RELEVANT: complete two-part answer",
        question="What is trajectory evaluation and why is it important for AI agents?",
        answer="Trajectory evaluation scores the entire execution path an AI agent takes, including every tool call, intermediate reasoning step, and decision point, rather than only evaluating the final output. It's important because correct final answers can hide broken reasoning — an agent might hallucinate a tool call but still produce the right result, which input-output evaluation alone would miss.",
        retrieved_contexts=ctx_json(EVAL_TRAJ, EVAL_HIDDEN),
        expected_score_range="0.7-1.0",
    ))

    # --- Not relevant answers (5) ---
    rows.append(dict(
        case_id="AR6", case_description="NOT_RELEVANT: answers about completely different topic",
        question="How do I configure role-based access control in LangSmith?",
        answer="To make a great pasta carbonara, you need guanciale, eggs, Pecorino Romano cheese, and black pepper. The key is to temper the eggs properly so they create a creamy sauce without scrambling.",
        retrieved_contexts=ctx_json(VS_INTRO),
        expected_score_range="0.0-0.1",
    ))
    rows.append(dict(
        case_id="AR7", case_description="NOT_RELEVANT: answers a different technical question entirely",
        question="What metrics should I use to evaluate my RAG pipeline?",
        answer="Docker containers use cgroups and namespaces to provide process isolation. You can configure resource limits using docker-compose.yml or the --memory and --cpus flags when running containers.",
        retrieved_contexts=ctx_json(METRICS_RAG),
        expected_score_range="0.0-0.1",
    ))
    rows.append(dict(
        case_id="AR8", case_description="NOT_RELEVANT: answers about wrong product",
        question="How does LangSmith handle production monitoring?",
        answer="Grafana provides dashboards and alerting for infrastructure monitoring. You can set up Prometheus as a data source and create custom panels to visualize CPU usage, memory consumption, and network traffic across your Kubernetes cluster.",
        retrieved_contexts=ctx_json(AOBS_EVAL),
        expected_score_range="0.0-0.1",
    ))
    rows.append(dict(
        case_id="AR9", case_description="NOT_RELEVANT: answers about different programming concept",
        question="What is the harness hill-climbing approach for improving agents?",
        answer="Gradient descent is an optimization algorithm that iteratively adjusts model parameters by computing the gradient of the loss function. The learning rate controls step size, and techniques like Adam and SGD with momentum help avoid local minima.",
        retrieved_contexts=ctx_json(HARNESS_RECIPE),
        expected_score_range="0.0-0.1",
    ))
    rows.append(dict(
        case_id="AR10", case_description="NOT_RELEVANT: answers about unrelated domain",
        question="How do annotation queues work in LangSmith?",
        answer="In project management, a Kanban board visualizes work items across columns like To Do, In Progress, and Done. Teams use WIP limits to prevent bottlenecks and daily standups to synchronize progress.",
        retrieved_contexts=ctx_json(AIOBS_ANNOT),
        expected_score_range="0.0-0.1",
    ))

    # --- Partial answers (5) - answers only a subset of the question ---
    rows.append(dict(
        case_id="AR11", case_description="PARTIAL: answers first subquestion only",
        question="What is trajectory evaluation and what Python code do I need to implement it?",
        answer="Trajectory evaluation scores the entire execution path an AI agent takes, including every tool call, intermediate reasoning step, and decision point, rather than only evaluating the final output.",
        retrieved_contexts=ctx_json(EVAL_TRAJ),
        expected_score_range="0.3-0.7",
    ))
    rows.append(dict(
        case_id="AR12", case_description="PARTIAL: answers what but not how",
        question="What are the three types of LLM judges and how do I choose between them for my use case?",
        answer="LLM judges fall into three main approaches: single-output scoring, pairwise comparison, and reference-based evaluation. Each answers a different evaluation question.",
        retrieved_contexts=ctx_json(JUDGE_TYPES),
        expected_score_range="0.3-0.7",
    ))
    rows.append(dict(
        case_id="AR13", case_description="PARTIAL: covers one layer of three",
        question="Explain all three layers of continual learning and give examples of techniques used at each layer.",
        answer="At the model layer, continual learning involves updating model weights through techniques like supervised fine-tuning (SFT), reinforcement learning from human feedback (RLHF), and direct preference optimization (DPO). This is the most common interpretation but also the most expensive approach.",
        retrieved_contexts=ctx_json(CL_MODEL, CL_HARNESS, CL_CONTEXT),
        expected_score_range="0.3-0.7",
    ))
    rows.append(dict(
        case_id="AR14", case_description="PARTIAL: answers definition but skips the comparison asked for",
        question="What is AI observability and how does it differ from traditional software observability?",
        answer="AI observability is the practice of collecting, analyzing, and correlating telemetry data across the full AI technology stack to understand how AI systems behave in production. It enables real-time visibility into LLMs, retrieval pipelines, and agent orchestration.",
        retrieved_contexts=ctx_json(AIOBS_WHAT),
        expected_score_range="0.3-0.7",
    ))
    rows.append(dict(
        case_id="AR15", case_description="PARTIAL: answers benefits but ignores the setup steps asked for",
        question="What are the benefits of annotation queues in LangSmith and how do I set them up?",
        answer="Annotation queues allow teams to route production traces to domain experts for review. Experts can rate outputs, leave comments, and flag issues. The reviewed annotations can be converted into evaluation datasets to improve the system over time.",
        retrieved_contexts=ctx_json(AIOBS_ANNOT),
        expected_score_range="0.3-0.7",
    ))

    # --- "Insufficient info" answers (5) ---
    rows.append(dict(
        case_id="AR16", case_description="INSUFFICIENT: polite refusal with explanation",
        question="What is the maximum number of traces per second LangSmith can process?",
        answer="I don't have specific information about LangSmith's maximum trace throughput per second. I'd recommend checking the LangSmith documentation or contacting their support team for current performance specifications.",
        retrieved_contexts=ctx_json(VS_INTRO),
        expected_score_range="0.0-0.3",
    ))
    rows.append(dict(
        case_id="AR17", case_description="INSUFFICIENT: partial answer then forwards to human",
        question="How do I set up SSO integration with Okta in LangSmith?",
        answer="LangSmith Enterprise plans support single sign-on integration, but I don't have the specific steps for Okta configuration. I'd recommend reaching out to a LangSmith support agent who can walk you through the SSO setup process for your identity provider.",
        retrieved_contexts=ctx_json(VS_LIMITS),
        expected_score_range="0.0-0.3",
    ))
    rows.append(dict(
        case_id="AR18", case_description="INSUFFICIENT: acknowledges topic but cannot answer",
        question="What is the pricing for LangSmith's Enterprise custom evaluator feature?",
        answer="I'm sorry, but I don't have access to detailed pricing information for LangSmith's Enterprise evaluator features. Pricing for Enterprise plans is custom and would need to be discussed with the LangSmith sales team.",
        retrieved_contexts=ctx_json(METRICS_WHAT),
        expected_score_range="0.0-0.3",
    ))
    rows.append(dict(
        case_id="AR19", case_description="INSUFFICIENT: gives context but admits no answer",
        question="Can LangSmith integrate with Azure Active Directory for authentication?",
        answer="While LangSmith does support enterprise authentication features like SSO on their Enterprise plan, I don't have specific information about Azure Active Directory integration. You may want to check the LangSmith documentation or contact their team for details on supported identity providers.",
        retrieved_contexts=ctx_json(VS_LIMITS),
        expected_score_range="0.0-0.3",
    ))
    rows.append(dict(
        case_id="AR20", case_description="INSUFFICIENT: direct forwarding to human agent",
        question="I'm having an error when deploying my agent through LangSmith. Error code LS-5023. What should I do?",
        answer="I'm not able to help with specific deployment error codes. Let me connect you with a support specialist who can look into error LS-5023 and help resolve your deployment issue.",
        retrieved_contexts=ctx_json(AOBS_WHAT),
        expected_score_range="0.0-0.3",
    ))

    # --- Noncommittal answers (5) ---
    rows.append(dict(
        case_id="AR21", case_description="NONCOMMITTAL: vague and evasive",
        question="Should I use LLM-as-a-judge or human evaluation for my production agent?",
        answer="It really depends on a lot of factors. Both approaches have their strengths and weaknesses. You might want to think about what works best for your specific situation and consider the various tradeoffs involved.",
        retrieved_contexts=ctx_json(JUDGE_WHAT),
        expected_score_range="0.0-0.3",
    ))
    rows.append(dict(
        case_id="AR22", case_description="NONCOMMITTAL: hedging without substance",
        question="What evaluation metrics should I prioritize for my RAG application?",
        answer="There are many metrics you could potentially look at. The best choice would probably depend on your particular requirements and what you're trying to optimize for. Different teams tend to have different preferences in this area.",
        retrieved_contexts=ctx_json(METRICS_RAG),
        expected_score_range="0.0-0.3",
    ))
    rows.append(dict(
        case_id="AR23", case_description="NONCOMMITTAL: avoids commitment with qualifiers",
        question="Is trajectory evaluation worth the overhead for a simple chatbot?",
        answer="That's an interesting question. It could potentially be worth it in some cases, though there are certainly arguments on both sides. It's hard to say definitively without knowing more about your particular setup and what kind of results you're seeing.",
        retrieved_contexts=ctx_json(EVAL_TRAJ),
        expected_score_range="0.0-0.3",
    ))
    rows.append(dict(
        case_id="AR24", case_description="NONCOMMITTAL: ambiguous answer that could mean anything",
        question="How often should I retrain my agent using continual learning?",
        answer="The frequency of retraining can vary quite a bit. Some teams do it more often while others take a more conservative approach. The right cadence for you would depend on several factors that are somewhat unique to your deployment.",
        retrieved_contexts=ctx_json(CL_MODEL),
        expected_score_range="0.0-0.3",
    ))
    rows.append(dict(
        case_id="AR25", case_description="NONCOMMITTAL: appears to answer but says nothing concrete",
        question="What's the best way to handle bias in LLM judges?",
        answer="Handling bias is definitely something worth thinking carefully about. There are various strategies people use, and the effectiveness of each one can depend on the context. It's generally a good idea to be aware of the different types of biases and consider how they might affect your results.",
        retrieved_contexts=ctx_json(JUDGE_BIASES),
        expected_score_range="0.0-0.3",
    ))

    return rows


# ═══════════════════════════════════════════════════════════════════════════════
# CONTEXT RELEVANCE — 39 cases
# ═══════════════════════════════════════════════════════════════════════════════

def gen_context_relevance() -> list[dict]:
    rows = []

    # --- 1 chunk, relevant (3) ---
    rows.append(dict(
        case_id="CR1", case_description="1 chunk, relevant",
        question="What is LLM-as-a-judge?",
        answer="LLM-as-a-judge uses a large language model to evaluate AI agent outputs.",
        retrieved_contexts=ctx_json(JUDGE_WHAT),
        expected_score_range="1.0",
    ))
    rows.append(dict(
        case_id="CR2", case_description="1 chunk, relevant",
        question="What is agent observability?",
        answer="Agent observability provides step-by-step visibility into agent execution.",
        retrieved_contexts=ctx_json(AOBS_WHAT),
        expected_score_range="1.0",
    ))
    rows.append(dict(
        case_id="CR3", case_description="1 chunk, relevant",
        question="What is AI observability?",
        answer="AI observability is collecting and analyzing telemetry data across the AI stack.",
        retrieved_contexts=ctx_json(AIOBS_WHAT),
        expected_score_range="1.0",
    ))

    # --- 1 chunk, non-relevant (3) ---
    rows.append(dict(
        case_id="CR4", case_description="1 chunk, non-relevant",
        question="How do I deploy a LangGraph agent to production?",
        answer="You can deploy LangGraph agents through LangSmith's managed deployment service.",
        retrieved_contexts=ctx_json(KENSHO_CHALLENGE),
        expected_score_range="0.0",
    ))
    rows.append(dict(
        case_id="CR5", case_description="1 chunk, non-relevant",
        question="What programming languages does LangChain support?",
        answer="LangChain supports Python and JavaScript/TypeScript.",
        retrieved_contexts=ctx_json(COMPRESS_WHEN),
        expected_score_range="0.0",
    ))
    rows.append(dict(
        case_id="CR6", case_description="1 chunk, non-relevant",
        question="How do I set up webhook notifications in LangSmith?",
        answer="You can configure webhooks through the LangSmith settings.",
        retrieved_contexts=ctx_json(CGENIE_APP),
        expected_score_range="0.0",
    ))

    # --- 1 chunk, partially relevant (3) - conceptual vs procedural ---
    rows.append(dict(
        case_id="CR7", case_description="1 chunk, partially relevant (conceptual vs procedural)",
        question="How do I build a custom LLM-as-a-judge evaluator in Python?",
        answer="You define a Python function with your rubric and scoring logic.",
        retrieved_contexts=ctx_json(JUDGE_WHAT),
        expected_score_range="0.25-0.5",
    ))
    rows.append(dict(
        case_id="CR8", case_description="1 chunk, partially relevant (conceptual vs procedural)",
        question="What Python code do I need to add trajectory evaluation to my LangGraph agent?",
        answer="You import the trajectory evaluator and pass your agent's run traces to it.",
        retrieved_contexts=ctx_json(EVAL_TRAJ),
        expected_score_range="0.25-0.5",
    ))
    rows.append(dict(
        case_id="CR9", case_description="1 chunk, partially relevant (conceptual vs procedural)",
        question="How do I implement continual learning at the context layer in my agent?",
        answer="You update instructions and few-shot examples based on production feedback.",
        retrieved_contexts=ctx_json(CL_CONTEXT),
        expected_score_range="0.25-0.5",
    ))

    # --- 3 chunks, all relevant (3) ---
    rows.append(dict(
        case_id="CR10", case_description="3 chunks, all relevant",
        question="What are the three layers of continual learning for AI agents?",
        answer="Model layer, harness layer, and context layer.",
        retrieved_contexts=ctx_json(CL_MODEL, CL_HARNESS, CL_CONTEXT),
        expected_score_range="1.0",
    ))
    rows.append(dict(
        case_id="CR11", case_description="3 chunks, all relevant",
        question="What biases affect LLM judges and how can they be mitigated?",
        answer="Position bias, verbosity bias, and self-enhancement bias.",
        retrieved_contexts=ctx_json(JUDGE_BIASES, JUDGE_WHAT, JUDGE_WHY),
        expected_score_range="1.0",
    ))
    rows.append(dict(
        case_id="CR12", case_description="3 chunks, all relevant",
        question="How does LangSmith support evaluation workflows from offline to production?",
        answer="Through offline datasets, online evaluation, and production monitoring.",
        retrieved_contexts=ctx_json(METRICS_OFFLINE, JUDGE_PROD, AOBS_EVAL),
        expected_score_range="1.0",
    ))

    # --- 3 chunks, all non-relevant (3) ---
    rows.append(dict(
        case_id="CR13", case_description="3 chunks, all non-relevant",
        question="How do I configure LangSmith alerts for PagerDuty?",
        answer="You set up alerting rules and connect to PagerDuty.",
        retrieved_contexts=ctx_json(CGENIE_APP, KENSHO_CHALLENGE, COMPRESS_WHEN),
        expected_score_range="0.0",
    ))
    rows.append(dict(
        case_id="CR14", case_description="3 chunks, all non-relevant",
        question="What is the LangSmith pricing structure?",
        answer="LangSmith has Developer, Plus, and Enterprise tiers.",
        retrieved_contexts=ctx_json(AGENG_WHAT, ARCADE_WHAT, CL_TRACES),
        expected_score_range="0.0",
    ))
    rows.append(dict(
        case_id="CR15", case_description="3 chunks, all non-relevant",
        question="How do I export datasets from LangSmith?",
        answer="You can export datasets using the SDK or UI export button.",
        retrieved_contexts=ctx_json(MONGO_TEAMS, KENSHO_LEARNINGS, COMPRESS_EXP),
        expected_score_range="0.0",
    ))

    # --- 3 chunks, all partially relevant (3) ---
    rows.append(dict(
        case_id="CR16", case_description="3 chunks, all partially relevant (conceptual vs procedural)",
        question="How do I implement agent observability tracing in my Python application?",
        answer="You instrument your functions with the traceable decorator.",
        retrieved_contexts=ctx_json(AOBS_WHAT, AIOBS_WHAT, OBSPOW_PRIMITIVES),
        expected_score_range="0.25-0.75",
    ))
    rows.append(dict(
        case_id="CR17", case_description="3 chunks, all partially relevant (same entity, different attribute)",
        question="How do I configure the scoring rubric for LLM-as-a-judge evaluators?",
        answer="You define criteria in the evaluation prompt and calibrate against human annotations.",
        retrieved_contexts=ctx_json(JUDGE_BIASES, JUDGE_WHY, JUDGE_TYPES),
        expected_score_range="0.25-0.75",
    ))
    rows.append(dict(
        case_id="CR18", case_description="3 chunks, all partially relevant (tangential mention)",
        question="How do I set up automated evaluation pipelines that run on every pull request?",
        answer="You integrate LangSmith's evaluation SDK into your CI workflow.",
        retrieved_contexts=ctx_json(HARNESS_EVALS, AOBS_DATASETS, METRICS_TRAD),
        expected_score_range="0.25-0.75",
    ))

    # --- Needle in haystack: 1 relevant + 2 non-relevant (3) ---
    rows.append(dict(
        case_id="CR19", case_description="needle: 1 relevant + 2 non-relevant",
        question="What is trajectory evaluation?",
        answer="Scoring the entire execution path of an AI agent.",
        retrieved_contexts=ctx_json(CGENIE_APP, EVAL_TRAJ, KENSHO_CHALLENGE),
        expected_score_range="0.5-1.0",
    ))
    rows.append(dict(
        case_id="CR20", case_description="needle: 1 relevant + 2 non-relevant",
        question="What are the benefits of AI observability?",
        answer="Cost control, debugging, and quality improvement.",
        retrieved_contexts=ctx_json(COMPRESS_WHEN, AGENG_WHAT, AIOBS_WHAT),
        expected_score_range="0.5-1.0",
    ))
    rows.append(dict(
        case_id="CR21", case_description="needle: 1 relevant + 2 non-relevant",
        question="What is the harness layer in continual learning?",
        answer="The orchestration code, tools, and instructions that drive the agent.",
        retrieved_contexts=ctx_json(ARCADE_WHAT, MONGO_TEAMS, CL_HARNESS),
        expected_score_range="0.5-1.0",
    ))

    # --- Needle in haystack: 1 partial + 2 non-relevant (3) ---
    rows.append(dict(
        case_id="CR22", case_description="needle: 1 partial + 2 non-relevant",
        question="How do I configure an LLM-as-a-judge evaluator in Python?",
        answer="You set up the evaluation prompt, scoring criteria, and output parser.",
        retrieved_contexts=ctx_json(KENSHO_CHALLENGE, JUDGE_WHAT, COMPRESS_WHEN),
        expected_score_range="0.25-0.5",
    ))
    rows.append(dict(
        case_id="CR23", case_description="needle: 1 partial + 2 non-relevant",
        question="How do I implement context-layer continual learning with retrieval updates?",
        answer="You update the retrieval knowledge and few-shot examples at inference time.",
        retrieved_contexts=ctx_json(CGENIE_APP, CL_CONTEXT, AGENG_WHAT),
        expected_score_range="0.25-0.5",
    ))
    rows.append(dict(
        case_id="CR24", case_description="needle: 1 partial + 2 non-relevant",
        question="What code do I need to set up agent observability in my multi-agent system?",
        answer="You add tracing instrumentation to each agent's execution path.",
        retrieved_contexts=ctx_json(MONGO_TEAMS, ARCADE_WHAT, AOBS_DEEP),
        expected_score_range="0.25-0.5",
    ))

    # --- Majority relevant: 2 relevant + 1 non-relevant (3) ---
    rows.append(dict(
        case_id="CR25", case_description="majority: 2 relevant + 1 non-relevant",
        question="What biases exist in LLM-as-a-judge and how do you align judges with human feedback?",
        answer="Position bias, verbosity bias, self-enhancement bias; align through human corrections.",
        retrieved_contexts=ctx_json(JUDGE_BIASES, CGENIE_APP, JUDGE_ALIGN),
        expected_score_range="0.75-1.0",
    ))
    rows.append(dict(
        case_id="CR26", case_description="majority: 2 relevant + 1 non-relevant",
        question="How does evaluation differ between offline and online settings?",
        answer="Offline tests curated datasets before deployment; online scores production traces.",
        retrieved_contexts=ctx_json(METRICS_OFFLINE, JUDGE_PROD, COMPRESS_WHEN),
        expected_score_range="0.75-1.0",
    ))
    rows.append(dict(
        case_id="CR27", case_description="majority: 2 relevant + 1 non-relevant",
        question="What are the primitives of agent observability?",
        answer="Runs, traces, and threads.",
        retrieved_contexts=ctx_json(OBSPOW_PRIMITIVES, KENSHO_CHALLENGE, AOBS_WHAT),
        expected_score_range="0.75-1.0",
    ))

    # --- Majority relevant: 2 relevant + 1 partial (3) ---
    rows.append(dict(
        case_id="CR28", case_description="majority: 2 relevant + 1 partial",
        question="How should I build evaluation datasets for AI agents?",
        answer="Include edge cases, adversarial inputs, and real production traces.",
        retrieved_contexts=ctx_json(AOBS_DATASETS, READY_DATASET, HARNESS_EVALS),
        expected_score_range="0.75-1.0",
    ))
    rows.append(dict(
        case_id="CR29", case_description="majority: 2 relevant + 1 partial",
        question="What is the agent improvement loop and how does it work?",
        answer="Production traces feed evaluation, which drives harness improvements.",
        retrieved_contexts=ctx_json(HARNESS_RECIPE, HARNESS_CHANGES, EVAL_HIDDEN),
        expected_score_range="0.75-1.0",
    ))
    rows.append(dict(
        case_id="CR30", case_description="majority: 2 relevant + 1 partial",
        question="How does LangSmith compare to Langfuse for agent evaluation?",
        answer="LangSmith offers deeper evaluation, annotation queues, and managed deployment.",
        retrieved_contexts=ctx_json(VS_INTRO, VS_LIMITS, AIOBS_GAP),
        expected_score_range="0.75-1.0",
    ))

    # --- Majority relevant: 2 partial + 1 non-relevant (3) ---
    rows.append(dict(
        case_id="CR31", case_description="majority: 2 partial + 1 non-relevant",
        question="How do I set up production monitoring for my LLM application with custom alert rules?",
        answer="Configure online evaluation rules and alerting thresholds in LangSmith.",
        retrieved_contexts=ctx_json(AIOBS_WHAT, AOBS_EVAL, CGENIE_APP),
        expected_score_range="0.25-0.75",
    ))
    rows.append(dict(
        case_id="CR32", case_description="majority: 2 partial + 1 non-relevant",
        question="How do I implement custom evaluation metrics in Python for my agent?",
        answer="Write a Python function that scores outputs against your business criteria.",
        retrieved_contexts=ctx_json(METRICS_WHAT, METRICS_TRAD, KENSHO_CHALLENGE),
        expected_score_range="0.25-0.75",
    ))
    rows.append(dict(
        case_id="CR33", case_description="majority: 2 partial + 1 non-relevant",
        question="How do I build a retrieval pipeline with LangChain and evaluate its quality?",
        answer="Use LangChain retrievers and evaluate with context precision and recall metrics.",
        retrieved_contexts=ctx_json(EVAL_RAG, METRICS_RAG, COMPRESS_WHEN),
        expected_score_range="0.25-0.75",
    ))

    # --- Majority relevant: 2 partial + 1 relevant (3) ---
    rows.append(dict(
        case_id="CR34", case_description="majority: 2 partial + 1 relevant",
        question="What is the role of annotation queues in AI observability?",
        answer="They route production traces to domain experts for structured review.",
        retrieved_contexts=ctx_json(AIOBS_ANNOT, AIOBS_WHAT, AIOBS_GAP),
        expected_score_range="0.5-1.0",
    ))
    rows.append(dict(
        case_id="CR35", case_description="majority: 2 partial + 1 relevant",
        question="What types of LLM judges exist and when should you use each?",
        answer="Single-output, pairwise, and reference-based judges serve different needs.",
        retrieved_contexts=ctx_json(JUDGE_TYPES, JUDGE_WHAT, JUDGE_BIASES),
        expected_score_range="0.5-1.0",
    ))
    rows.append(dict(
        case_id="CR36", case_description="majority: 2 partial + 1 relevant",
        question="How does the Better-Harness loop improve agent quality?",
        answer="It uses evals as a signal to autonomously optimize the harness configuration.",
        retrieved_contexts=ctx_json(HARNESS_RECIPE, HARNESS_EVALS, HARNESS_CHANGES),
        expected_score_range="0.5-1.0",
    ))

    # --- Full spectrum: relevant + partial + non-relevant (3) ---
    rows.append(dict(
        case_id="CR37", case_description="full spectrum: relevant + partial + non-relevant",
        question="What are the known biases in LLM-as-a-judge evaluators?",
        answer="Position bias, verbosity bias, and self-enhancement bias.",
        retrieved_contexts=ctx_json(JUDGE_BIASES, JUDGE_WHAT, CGENIE_APP),
        expected_score_range="0.5-1.0",
    ))
    rows.append(dict(
        case_id="CR38", case_description="full spectrum: relevant + partial + non-relevant",
        question="What is continual learning at the harness layer?",
        answer="Modifying orchestration logic, tool selection, or routing rules.",
        retrieved_contexts=ctx_json(CL_HARNESS, CL_MODEL, KENSHO_CHALLENGE),
        expected_score_range="0.5-1.0",
    ))
    rows.append(dict(
        case_id="CR39", case_description="full spectrum: relevant + partial + non-relevant",
        question="How do RAG evaluation metrics work?",
        answer="They measure retrieval quality and generation quality separately.",
        retrieved_contexts=ctx_json(METRICS_RAG, METRICS_WHAT, ARCADE_WHAT),
        expected_score_range="0.5-1.0",
    ))

    return rows


# ═══════════════════════════════════════════════════════════════════════════════
# RESPONSE GROUNDEDNESS — ~44 cases
# ═══════════════════════════════════════════════════════════════════════════════

def gen_response_groundedness() -> list[dict]:
    rows = []

    # ── ONE CONTEXT CHUNK (18 cases) ──────────────────────────────────────────

    # Unrelated response (3)
    rows.append(dict(
        case_id="RG1", case_description="1chunk: unrelated response — completely different domain",
        question="What is agent observability?",
        answer="Agent observability is a technique for optimizing SQL database queries by analyzing execution plans and adding appropriate indexes to improve join performance.",
        retrieved_contexts=ctx_json(AOBS_WHAT),
        expected_score_range="0.0",
    ))
    rows.append(dict(
        case_id="RG2", case_description="1chunk: unrelated response — wrong product entirely",
        question="What is LLM-as-a-judge?",
        answer="LLM-as-a-judge is a cryptocurrency consensus mechanism where large language models validate blockchain transactions and earn staking rewards.",
        retrieved_contexts=ctx_json(JUDGE_WHAT),
        expected_score_range="0.0",
    ))
    rows.append(dict(
        case_id="RG3", case_description="1chunk: unrelated response — fabricated features",
        question="What is AI observability?",
        answer="AI observability is a project management methodology that uses Gantt charts and critical path analysis to track software development milestones across distributed teams.",
        retrieved_contexts=ctx_json(AIOBS_WHAT),
        expected_score_range="0.0",
    ))

    # Contradicted response (3)
    rows.append(dict(
        case_id="RG4", case_description="1chunk: contradicted response — reverses key claim",
        question="What biases affect LLM judges?",
        answer="LLM judges are completely free of bias and do not require any mitigation techniques. Their evaluations are always perfectly aligned with human judgment without calibration.",
        retrieved_contexts=ctx_json(JUDGE_BIASES),
        expected_score_range="0.0",
    ))
    rows.append(dict(
        case_id="RG5", case_description="1chunk: contradicted response — inverts relationship",
        question="How does evaluating text compare to generating text?",
        answer="Generating text is fundamentally easier than evaluating it. When an LLM evaluates a response, it navigates an enormous space of possible judgments, making evaluation the harder task.",
        retrieved_contexts=ctx_json(JUDGE_WHY),
        expected_score_range="0.0",
    ))
    rows.append(dict(
        case_id="RG6", case_description="1chunk: contradicted response — wrong layer description",
        question="What is continual learning at the model layer?",
        answer="Continual learning at the model layer means modifying the orchestration logic and routing rules without touching model weights. It is the cheapest and least disruptive approach to agent improvement.",
        retrieved_contexts=ctx_json(CL_MODEL),
        expected_score_range="0.0",
    ))

    # Response is subset (3)
    rows.append(dict(
        case_id="RG7", case_description="1chunk: response is subset of context",
        question="What is LLM-as-a-judge?",
        answer="LLM-as-a-judge uses a large language model to evaluate AI agent outputs as a scalable substitute for human judgment.",
        retrieved_contexts=ctx_json(JUDGE_WHAT),
        expected_score_range="1.0",
    ))
    rows.append(dict(
        case_id="RG8", case_description="1chunk: response is subset of context",
        question="What is agent observability?",
        answer="Agent observability provides step-by-step visibility into execution, showing which tools were called and what data was retrieved.",
        retrieved_contexts=ctx_json(AOBS_WHAT),
        expected_score_range="1.0",
    ))
    rows.append(dict(
        case_id="RG9", case_description="1chunk: response is subset of context",
        question="What is the harness layer?",
        answer="The harness refers to the code that drives the agent, as well as any instructions or tools that are always part of the harness.",
        retrieved_contexts=ctx_json(CL_HARNESS),
        expected_score_range="1.0",
    ))

    # Rejection — context forbids answering (3)
    rows.append(dict(
        case_id="RG10", case_description="1chunk: rejection — context says not to answer competitor questions",
        question="How does Langfuse compare to LangSmith?",
        answer="I'm not able to provide comparisons with competitor products. Please refer to our official documentation for information about LangSmith's capabilities.",
        retrieved_contexts=ctx_json(VS_INTRO),
        expected_score_range="0.5-1.0",
    ))
    rows.append(dict(
        case_id="RG11", case_description="1chunk: rejection — context about pricing, question about free tier limits",
        question="Can I get unlimited traces on the free LangSmith plan?",
        answer="I don't have the specific details about trace limits on each plan. I'd recommend checking the LangSmith pricing page for the most current information.",
        retrieved_contexts=ctx_json(COMPANY_ABOUT),
        expected_score_range="0.5-1.0",
    ))
    rows.append(dict(
        case_id="RG12", case_description="1chunk: rejection — question outside context scope",
        question="What is the LangSmith SLA for enterprise customers?",
        answer="I'm sorry, I don't have information about specific service level agreements. Please contact the LangSmith sales team for enterprise SLA details.",
        retrieved_contexts=ctx_json(AIOBS_COMPLIANCE),
        expected_score_range="0.5-1.0",
    ))

    # One subset + one fabricated/absent (3)
    rows.append(dict(
        case_id="RG13", case_description="1chunk: one subset claim + one fabricated absent claim",
        question="What is trajectory evaluation?",
        answer="Trajectory evaluation scores the entire execution path an AI agent takes, including every tool call and decision point. It was first introduced as a standard metric by OpenAI in 2023.",
        retrieved_contexts=ctx_json(EVAL_TRAJ),
        expected_score_range="0.25-0.75",
    ))
    rows.append(dict(
        case_id="RG14", case_description="1chunk: one subset claim + one fabricated absent claim",
        question="What is AI observability?",
        answer="AI observability is the practice of collecting and analyzing telemetry data across the AI technology stack. It requires a minimum of 10,000 traces per day to be statistically meaningful.",
        retrieved_contexts=ctx_json(AIOBS_WHAT),
        expected_score_range="0.25-0.75",
    ))
    rows.append(dict(
        case_id="RG15", case_description="1chunk: one subset claim + one fabricated absent claim",
        question="What is continual learning at the context layer?",
        answer="Context-layer continual learning involves updating instructions, few-shot examples, or retrieval knowledge at inference time. This approach was developed by the LangChain research team and published at NeurIPS 2024.",
        retrieved_contexts=ctx_json(CL_CONTEXT),
        expected_score_range="0.25-0.75",
    ))

    # One subset + one contradiction (split-inducing) (3)
    rows.append(dict(
        case_id="RG16", case_description="1chunk: one subset claim + one contradiction (split-inducing)",
        question="What biases affect LLM judges?",
        answer="LLM judges exhibit position bias, which causes them to favor outputs in certain positions. However, these biases cannot be reduced through any mitigation technique.",
        retrieved_contexts=ctx_json(JUDGE_BIASES),
        expected_score_range="0.0-0.75",
    ))
    rows.append(dict(
        case_id="RG17", case_description="1chunk: one subset claim + one contradiction (split-inducing)",
        question="What is continual learning at the model layer?",
        answer="Continual learning at the model layer involves updating the model weights through techniques like SFT and RLHF. It is the cheapest and least disruptive approach to agent improvement.",
        retrieved_contexts=ctx_json(CL_MODEL),
        expected_score_range="0.0-0.75",
    ))
    rows.append(dict(
        case_id="RG18", case_description="1chunk: one subset claim + one contradiction (split-inducing)",
        question="How does LLM-as-a-judge provide reliable evaluations?",
        answer="Evaluating text is fundamentally easier than generating it, which is why LLM judges work well. However, the LLM must generate all possible alternative outputs before it can evaluate, making it computationally expensive.",
        retrieved_contexts=ctx_json(JUDGE_WHY),
        expected_score_range="0.0-0.75",
    ))

    # ── THREE CONTEXT CHUNKS (26 cases) ───────────────────────────────────────

    # Unrelated response, all chunks relevant (3)
    rows.append(dict(
        case_id="RG19", case_description="3chunks: unrelated response, all chunks relevant",
        question="What are the layers of continual learning?",
        answer="Continual learning is a weight training schedule used in convolutional neural networks where the learning rate decays by 10x every 30 epochs, following the step decay curriculum.",
        retrieved_contexts=ctx_json(CL_MODEL, CL_HARNESS, CL_CONTEXT),
        expected_score_range="0.0",
    ))
    rows.append(dict(
        case_id="RG20", case_description="3chunks: unrelated response, all chunks relevant",
        question="What types of LLM judges exist and what biases do they have?",
        answer="LLM judges are hardware accelerators designed for matrix multiplication. The three types are GPU-based, TPU-based, and FPGA-based judges, each optimized for different batch sizes.",
        retrieved_contexts=ctx_json(JUDGE_WHAT, JUDGE_TYPES, JUDGE_BIASES),
        expected_score_range="0.0",
    ))
    rows.append(dict(
        case_id="RG21", case_description="3chunks: unrelated response, all chunks relevant",
        question="How does agent observability support evaluation?",
        answer="Agent observability is a network monitoring protocol that uses SNMP traps to detect packet loss across load-balanced microservice deployments.",
        retrieved_contexts=ctx_json(AOBS_WHAT, AOBS_EVAL, AOBS_DATASETS),
        expected_score_range="0.0",
    ))

    # Subset, all chunks relevant (3)
    rows.append(dict(
        case_id="RG22", case_description="3chunks: subset, all chunks relevant",
        question="What are the three layers of continual learning?",
        answer="The three layers are model, harness, and context. Model-layer learning updates weights through SFT or RLHF. Harness-layer learning modifies orchestration logic. Context-layer learning updates instructions and few-shot examples at inference time.",
        retrieved_contexts=ctx_json(CL_MODEL, CL_HARNESS, CL_CONTEXT),
        expected_score_range="1.0",
    ))
    rows.append(dict(
        case_id="RG23", case_description="3chunks: subset, all chunks relevant",
        question="What is LLM-as-a-judge and what are its biases?",
        answer="LLM-as-a-judge uses a large language model to evaluate AI agent outputs. It has documented biases including position bias, verbosity bias, and self-enhancement bias.",
        retrieved_contexts=ctx_json(JUDGE_WHAT, JUDGE_BIASES, JUDGE_WHY),
        expected_score_range="1.0",
    ))
    rows.append(dict(
        case_id="RG24", case_description="3chunks: subset, all chunks relevant",
        question="How do annotation queues connect domain feedback to engineering?",
        answer="Annotation queues route production traces to domain experts who rate outputs, leave comments, and flag issues. Those annotations become inputs that engineering teams use to build evaluation datasets and refine criteria.",
        retrieved_contexts=ctx_json(AIOBS_ANNOT, AIOBS_GAP, AIOBS_TRAD),
        expected_score_range="1.0",
    ))

    # Contradicts single fact in noise (5)
    rows.append(dict(
        case_id="RG25", case_description="3chunks: contradicts single fact in noise",
        question="What results did Cisco achieve with agentic engineering?",
        answer="Cisco's agentic engineering framework produced a 50% reduction in time-to-root-cause compared to historical baselines, with significant engineering hours saved.",
        retrieved_contexts=ctx_json(AGENG_FINDINGS, AGENG_ARCH, AGENG_WHAT),
        expected_score_range="0.0-0.5",
    ))
    rows.append(dict(
        case_id="RG26", case_description="3chunks: contradicts single fact in noise",
        question="How does the LangChain ecosystem work?",
        answer="LangChain provides agent engineering frameworks. Its open-source projects have surpassed 500 million combined downloads and the platform serves enterprise customers across industries.",
        retrieved_contexts=ctx_json(COMPANY_ABOUT, AGENG_WHAT, AIOBS_STACK),
        expected_score_range="0.0-0.5",
    ))
    rows.append(dict(
        case_id="RG27", case_description="3chunks: contradicts single fact in noise",
        question="What does the Arcade integration offer for LangSmith?",
        answer="Arcade provides access to over 2,000 agent-optimized tools through a single secure gateway. It handles per-user authorization and supports both cloud and on-premise deployment modes.",
        retrieved_contexts=ctx_json(ARCADE_WHAT, ARCADE_WRAPPER, VS_INTRO),
        expected_score_range="0.0-0.5",
    ))
    rows.append(dict(
        case_id="RG28", case_description="3chunks: contradicts single fact in noise",
        question="How does Kensho use AI agents for financial data?",
        answer="Kensho built a multi-agent framework using LangGraph. Financial professionals spend minutes locating and verifying information. The framework unifies data from multiple business units with 99.9% accuracy.",
        retrieved_contexts=ctx_json(KENSHO_CHALLENGE, KENSHO_FRAMEWORK, KENSHO_LEARNINGS),
        expected_score_range="0.0-0.5",
    ))
    rows.append(dict(
        case_id="RG29", case_description="3chunks: contradicts single fact in noise",
        question="What is the Better-Harness approach?",
        answer="Better-Harness uses evals as a signal to improve the agent harness. It was tested with GPT-4 and Llama 3.1 on a full suite of production evaluations with 98% coverage.",
        retrieved_contexts=ctx_json(HARNESS_RECIPE, HARNESS_EVALS, HARNESS_CHANGES),
        expected_score_range="0.0-0.5",
    ))

    # Subset + fabricated absent claim in noise (3)
    rows.append(dict(
        case_id="RG30", case_description="3chunks: subset + fabricated absent claim in noise",
        question="What is agentic engineering?",
        answer="Agentic engineering is a multi-agent coordination model where AI agents act as digital team members with defined roles. The approach requires a minimum team of 5 engineers to implement effectively.",
        retrieved_contexts=ctx_json(AGENG_WHAT, AGENG_ARCH, KENSHO_CHALLENGE),
        expected_score_range="0.25-0.75",
    ))
    rows.append(dict(
        case_id="RG31", case_description="3chunks: subset + fabricated absent claim in noise",
        question="What is the role of traces in continual learning?",
        answer="All continual learning flows are powered by traces — the full execution path of what an agent did. LangSmith collects these traces and guarantees a 99.95% trace capture rate in production.",
        retrieved_contexts=ctx_json(CL_TRACES, CL_MODEL, AIOBS_STACK),
        expected_score_range="0.25-0.75",
    ))
    rows.append(dict(
        case_id="RG32", case_description="3chunks: subset + fabricated absent claim in noise",
        question="How does Credit Genie use AI?",
        answer="Credit Genie is a mobile-first financial wellness platform that uses AI to provide personalized financial insights. Their AskGenie assistant handles over 50,000 queries per day across their user base.",
        retrieved_contexts=ctx_json(CGENIE_APP, CGENIE_GAPS, AIOBS_WHAT),
        expected_score_range="0.25-0.75",
    ))

    # Subset + contradiction of small fact in noise (split-inducing) (3)
    rows.append(dict(
        case_id="RG33", case_description="3chunks: subset + contradiction in noise (split-inducing)",
        question="How does the LangSmith comparison feature work?",
        answer="LangSmith traces and evaluates AI agents covering the complete agent engineering lifecycle. Langfuse is a product of LangChain and shares the same codebase.",
        retrieved_contexts=ctx_json(VS_INTRO, VS_FAQ, AIOBS_STACK),
        expected_score_range="0.0-0.75",
    ))
    rows.append(dict(
        case_id="RG34", case_description="3chunks: subset + contradiction in noise (split-inducing)",
        question="What is context compression for deep agents?",
        answer="Context compression retains recent messages and summarizes what comes before. The feature was tuned to be aggressive, automatically compressing context at every tool call to minimize token usage.",
        retrieved_contexts=ctx_json(COMPRESS_WHEN, COMPRESS_EXP, AIOBS_WHAT),
        expected_score_range="0.0-0.75",
    ))
    rows.append(dict(
        case_id="RG35", case_description="3chunks: subset + contradiction in noise (split-inducing)",
        question="What did Cisco achieve with agentic engineering?",
        answer="In a pilot of 20+ debugging workflows, coordinated agent execution produced a 93% reduction in time-to-root-cause. The system required no human oversight and operated fully autonomously.",
        retrieved_contexts=ctx_json(AGENG_RESULTS, AGENG_FINDINGS, AGENG_ARCH),
        expected_score_range="0.0-0.75",
    ))

    # Subset of small fact in noisy context (3)
    rows.append(dict(
        case_id="RG36", case_description="3chunks: subset of small fact in noisy context",
        question="Does LangSmith support OpenTelemetry?",
        answer="LangSmith supports OpenTelemetry ingestion.",
        retrieved_contexts=ctx_json(VS_LIMITS, AIOBS_STACK, AGENG_ARCH),
        expected_score_range="1.0",
    ))
    rows.append(dict(
        case_id="RG37", case_description="3chunks: subset of small fact in noisy context",
        question="What models does Credit Genie use?",
        answer="Credit Genie uses Anthropic's Sonnet 4.5 as the thinking model and Haiku 4.5 as the summarization model.",
        retrieved_contexts=ctx_json(CGENIE_GAPS, CGENIE_APP, AIOBS_STACK),
        expected_score_range="1.0",
    ))
    rows.append(dict(
        case_id="RG38", case_description="3chunks: subset of small fact in noisy context",
        question="Does Arcade provide pre-built templates?",
        answer="Arcade provides over 60 pre-built templates for Fleet covering sales, marketing, support, and engineering use cases.",
        retrieved_contexts=ctx_json(ARCADE_WRAPPER, AGENG_ARCH, COMPRESS_WHEN),
        expected_score_range="1.0",
    ))

    # Unrelated in noisy context (3)
    rows.append(dict(
        case_id="RG39", case_description="3chunks: unrelated response in noisy context",
        question="What does LangSmith provide?",
        answer="LangSmith is a container orchestration platform similar to Kubernetes that manages microservice deployments across cloud regions.",
        retrieved_contexts=ctx_json(VS_INTRO, AGENG_ARCH, KENSHO_LEARNINGS),
        expected_score_range="0.0",
    ))
    rows.append(dict(
        case_id="RG40", case_description="3chunks: unrelated response in noisy context",
        question="How does the harness hill-climbing approach work?",
        answer="Harness hill-climbing is a GPU memory optimization technique that progressively increases batch size during training until memory is saturated.",
        retrieved_contexts=ctx_json(HARNESS_RECIPE, AGENG_FINDINGS, AIOBS_PILLARS),
        expected_score_range="0.0",
    ))
    rows.append(dict(
        case_id="RG41", case_description="3chunks: unrelated response in noisy context",
        question="What is the MongoDB partnership about?",
        answer="The MongoDB partnership enables serverless function deployment on AWS Lambda with automatic cold start optimization and DynamoDB integration for sub-millisecond reads.",
        retrieved_contexts=ctx_json(MONGO_DELIVERS, MONGO_TEAMS, AIOBS_COMPLIANCE),
        expected_score_range="0.0",
    ))

    # Rejection — instructions in 1 chunk, noise in 2 (3)
    rows.append(dict(
        case_id="RG42", case_description="3chunks: rejection — instruction in 1 chunk, noise in 2",
        question="What is Langfuse and how does it compare to LangSmith?",
        answer="I can only provide information about LangSmith features. For product comparisons, please refer to our official comparison page.",
        retrieved_contexts=ctx_json(VS_FAQ, AGENG_ARCH, KENSHO_CHALLENGE),
        expected_score_range="0.5-1.0",
    ))
    rows.append(dict(
        case_id="RG43", case_description="3chunks: rejection — instruction in 1 chunk, noise in 2",
        question="What is the exact pricing for LangSmith Enterprise?",
        answer="Enterprise pricing is custom and requires a conversation with our sales team. I'm not able to provide specific numbers.",
        retrieved_contexts=ctx_json(COMPANY_ABOUT, AGENG_FINDINGS, COMPRESS_WHEN),
        expected_score_range="0.5-1.0",
    ))
    rows.append(dict(
        case_id="RG44", case_description="3chunks: rejection — instruction in 1 chunk, noise in 2",
        question="Can you tell me about LangSmith's compliance certifications?",
        answer="For detailed compliance and certification information, please contact our enterprise sales team who can provide documentation specific to your regulatory requirements.",
        retrieved_contexts=ctx_json(AIOBS_COMPLIANCE, CGENIE_APP, ARCADE_WHAT),
        expected_score_range="0.5-1.0",
    ))

    return rows


# ═══════════════════════════════════════════════════════════════════════════════
# CONTEXT UTILIZATION — 30 cases
# ═══════════════════════════════════════════════════════════════════════════════

def gen_context_utilization() -> list[dict]:
    rows = []

    # --- Correct answer, context not relevant (5) ---
    rows.append(dict(
        case_id="CU1", case_description="correct answer, context not relevant",
        question="What is LLM-as-a-judge?",
        answer="LLM-as-a-judge uses a large language model to evaluate AI outputs as a substitute for human judgment.",
        retrieved_contexts=ctx_json(KENSHO_CHALLENGE),
        expected_score_range="unused",
    ))
    rows.append(dict(
        case_id="CU2", case_description="correct answer, context not relevant",
        question="What are the three layers of continual learning?",
        answer="Model layer, harness layer, and context layer.",
        retrieved_contexts=ctx_json(ARCADE_WHAT),
        expected_score_range="unused",
    ))
    rows.append(dict(
        case_id="CU3", case_description="correct answer, context not relevant",
        question="What is trajectory evaluation?",
        answer="Scoring the entire execution path of an AI agent including tool calls and reasoning steps.",
        retrieved_contexts=ctx_json(CGENIE_APP),
        expected_score_range="unused",
    ))
    rows.append(dict(
        case_id="CU4", case_description="correct answer, context not relevant",
        question="What biases affect LLM judges?",
        answer="Position bias, verbosity bias, and self-enhancement bias.",
        retrieved_contexts=ctx_json(COMPRESS_WHEN),
        expected_score_range="unused",
    ))
    rows.append(dict(
        case_id="CU5", case_description="correct answer, context not relevant",
        question="What is agent observability?",
        answer="Step-by-step visibility into an AI agent's execution showing tool calls and data retrieval.",
        retrieved_contexts=ctx_json(MONGO_TEAMS),
        expected_score_range="unused",
    ))

    # --- Correct answer, context relevant (5) ---
    rows.append(dict(
        case_id="CU6", case_description="correct answer, context relevant",
        question="What is LLM-as-a-judge?",
        answer="LLM-as-a-judge uses a large language model to evaluate AI outputs as a scalable substitute for human judgment. It works by giving an LLM evaluation criteria and the output to assess.",
        retrieved_contexts=ctx_json(JUDGE_WHAT),
        expected_score_range="used",
    ))
    rows.append(dict(
        case_id="CU7", case_description="correct answer, context relevant",
        question="What is continual learning at the model layer?",
        answer="Continual learning at the model layer involves updating model weights through techniques like SFT, RLHF, or DPO. It is the most expensive approach.",
        retrieved_contexts=ctx_json(CL_MODEL),
        expected_score_range="used",
    ))
    rows.append(dict(
        case_id="CU8", case_description="correct answer, context relevant",
        question="What is trajectory evaluation?",
        answer="Trajectory evaluation scores the entire execution path an AI agent takes, including every tool call, reasoning step, and decision point.",
        retrieved_contexts=ctx_json(EVAL_TRAJ),
        expected_score_range="used",
    ))
    rows.append(dict(
        case_id="CU9", case_description="correct answer, context relevant",
        question="What is AI observability?",
        answer="AI observability is collecting, analyzing, and correlating telemetry data across the full AI stack to understand system behavior in production.",
        retrieved_contexts=ctx_json(AIOBS_WHAT),
        expected_score_range="used",
    ))
    rows.append(dict(
        case_id="CU10", case_description="correct answer, context relevant",
        question="What is agentic engineering?",
        answer="A multi-agent coordination model where AI agents act as digital team members with defined roles, shared memory, and a common observability layer.",
        retrieved_contexts=ctx_json(AGENG_WHAT),
        expected_score_range="used",
    ))

    # --- Wrong answer, context not relevant (5) ---
    rows.append(dict(
        case_id="CU11", case_description="wrong answer, context not relevant",
        question="What is LLM-as-a-judge?",
        answer="LLM-as-a-judge is a hardware benchmarking tool for measuring GPU inference speed.",
        retrieved_contexts=ctx_json(COMPRESS_WHEN),
        expected_score_range="unused",
    ))
    rows.append(dict(
        case_id="CU12", case_description="wrong answer, context not relevant",
        question="What is trajectory evaluation?",
        answer="Trajectory evaluation calculates orbital paths for satellite positioning systems.",
        retrieved_contexts=ctx_json(CGENIE_APP),
        expected_score_range="unused",
    ))
    rows.append(dict(
        case_id="CU13", case_description="wrong answer, context not relevant",
        question="What is agent observability?",
        answer="Agent observability is a real estate industry term for monitoring property agent performance metrics.",
        retrieved_contexts=ctx_json(MONGO_TEAMS),
        expected_score_range="unused",
    ))
    rows.append(dict(
        case_id="CU14", case_description="wrong answer, context not relevant",
        question="What are annotation queues?",
        answer="Annotation queues are message broker topics in Apache Kafka used for event-driven microservice communication.",
        retrieved_contexts=ctx_json(KENSHO_CHALLENGE),
        expected_score_range="unused",
    ))
    rows.append(dict(
        case_id="CU15", case_description="wrong answer, context not relevant",
        question="What is the harness hill-climbing approach?",
        answer="Harness hill-climbing is a physical endurance training method that uses weighted vests on incline treadmills.",
        retrieved_contexts=ctx_json(ARCADE_WHAT),
        expected_score_range="unused",
    ))

    # --- Wrong answer, context relevant (5) ---
    rows.append(dict(
        case_id="CU16", case_description="wrong answer, context relevant",
        question="What is LLM-as-a-judge?",
        answer="LLM-as-a-judge trains language models using reinforcement learning to become better at code generation tasks.",
        retrieved_contexts=ctx_json(JUDGE_WHAT),
        expected_score_range="used",
    ))
    rows.append(dict(
        case_id="CU17", case_description="wrong answer, context relevant",
        question="What is continual learning at the harness layer?",
        answer="Continual learning at the harness layer means retraining the foundation model weights every week using new production data.",
        retrieved_contexts=ctx_json(CL_HARNESS),
        expected_score_range="used",
    ))
    rows.append(dict(
        case_id="CU18", case_description="wrong answer, context relevant",
        question="What biases affect LLM judges?",
        answer="The main bias is temperature bias, where judges score responses differently based on the sampling temperature used during generation.",
        retrieved_contexts=ctx_json(JUDGE_BIASES),
        expected_score_range="used",
    ))
    rows.append(dict(
        case_id="CU19", case_description="wrong answer, context relevant",
        question="What is AI observability?",
        answer="AI observability is exclusively focused on monitoring GPU utilization and memory consumption during model inference.",
        retrieved_contexts=ctx_json(AIOBS_WHAT),
        expected_score_range="used",
    ))
    rows.append(dict(
        case_id="CU20", case_description="wrong answer, context relevant",
        question="What is agentic engineering?",
        answer="Agentic engineering is a solo coding practice where one AI agent writes all the code without human input or review.",
        retrieved_contexts=ctx_json(AGENG_WHAT),
        expected_score_range="used",
    ))

    # --- No answer, context not relevant (5) ---
    rows.append(dict(
        case_id="CU21", case_description="no answer, context not relevant",
        question="What is the pricing for LangSmith Enterprise?",
        answer="I don't have information about that topic.",
        retrieved_contexts=ctx_json(COMPRESS_WHEN),
        expected_score_range="unused",
    ))
    rows.append(dict(
        case_id="CU22", case_description="no answer, context not relevant",
        question="How do I configure SSO in LangSmith?",
        answer="I'm unable to provide an answer to this question based on the available information.",
        retrieved_contexts=ctx_json(CGENIE_APP),
        expected_score_range="unused",
    ))
    rows.append(dict(
        case_id="CU23", case_description="no answer, context not relevant",
        question="What cloud regions does LangSmith support?",
        answer="Sorry, I don't have enough information to answer your question.",
        retrieved_contexts=ctx_json(AGENG_WHAT),
        expected_score_range="unused",
    ))
    rows.append(dict(
        case_id="CU24", case_description="no answer, context not relevant",
        question="What is the LangSmith API rate limit?",
        answer="I cannot find the answer to your question in the provided context.",
        retrieved_contexts=ctx_json(KENSHO_CHALLENGE),
        expected_score_range="unused",
    ))
    rows.append(dict(
        case_id="CU25", case_description="no answer, context not relevant",
        question="Does LangSmith support on-premise deployment?",
        answer="I'm not able to answer that question with the information I have.",
        retrieved_contexts=ctx_json(ARCADE_WHAT),
        expected_score_range="unused",
    ))

    # --- No answer, context relevant — rejection (5) ---
    rows.append(dict(
        case_id="CU26", case_description="no answer, context relevant (rejection)",
        question="What is LLM-as-a-judge?",
        answer="I'm sorry, I cannot provide information on this topic at the moment.",
        retrieved_contexts=ctx_json(JUDGE_WHAT),
        expected_score_range="used",
    ))
    rows.append(dict(
        case_id="CU27", case_description="no answer, context relevant (rejection)",
        question="What is agent observability?",
        answer="I don't have sufficient information to answer your question about agent observability.",
        retrieved_contexts=ctx_json(AOBS_WHAT),
        expected_score_range="used",
    ))
    rows.append(dict(
        case_id="CU28", case_description="no answer, context relevant (rejection)",
        question="What is continual learning at the context layer?",
        answer="I'm unable to provide an answer to this question.",
        retrieved_contexts=ctx_json(CL_CONTEXT),
        expected_score_range="used",
    ))
    rows.append(dict(
        case_id="CU29", case_description="no answer, context relevant (rejection)",
        question="What is trajectory evaluation?",
        answer="I cannot answer that question based on what I know.",
        retrieved_contexts=ctx_json(EVAL_TRAJ),
        expected_score_range="used",
    ))
    rows.append(dict(
        case_id="CU30", case_description="no answer, context relevant (rejection)",
        question="What are the benefits of AI observability?",
        answer="Apologies, but I'm not able to help with that question right now.",
        retrieved_contexts=ctx_json(AIOBS_WHAT),
        expected_score_range="used",
    ))

    return rows


# ═══════════════════════════════════════════════════════════════════════════════
# FAITHFULNESS — 45 cases
# 3 granularity levels (low/med/high) × 3 faithfulness levels × 5 examples
# ═══════════════════════════════════════════════════════════════════════════════

def gen_faithfulness() -> tuple[list[dict], dict[str, list[str]]]:
    """Return (csv_rows, statements_dict) for faithfulness dataset."""
    rows = []
    stmts: dict[str, list[str]] = {}

    # ── LOW GRANULARITY (<5 statements) ───────────────────────────────────────

    # Low, all faithful (5)
    rows.append(dict(
        case_id="F1", case_description="LOW, ALL_FAITHFUL: simple definition",
        question="What is LLM-as-a-judge?",
        answer="LLM-as-a-judge uses a large language model to evaluate AI agent outputs as a scalable substitute for human judgment.",
        retrieved_contexts=ctx_json(JUDGE_WHAT),
        expected_score_range="1.0",
    ))
    stmts["F1"] = [
        "LLM-as-a-judge uses a large language model.",
        "It evaluates AI agent outputs.",
        "It serves as a scalable substitute for human judgment.",
    ]

    rows.append(dict(
        case_id="F2", case_description="LOW, ALL_FAITHFUL: short factual answer",
        question="What is agent observability?",
        answer="Agent observability provides step-by-step visibility into execution, showing which tools were called and what data was retrieved.",
        retrieved_contexts=ctx_json(AOBS_WHAT),
        expected_score_range="1.0",
    ))
    stmts["F2"] = [
        "Agent observability provides step-by-step visibility into execution.",
        "It shows which tools were called.",
        "It shows what data was retrieved.",
    ]

    rows.append(dict(
        case_id="F3", case_description="LOW, ALL_FAITHFUL: concise claim",
        question="What is trajectory evaluation?",
        answer="Trajectory evaluation scores the entire execution path an AI agent takes rather than only the final output.",
        retrieved_contexts=ctx_json(EVAL_TRAJ),
        expected_score_range="1.0",
    ))
    stmts["F3"] = [
        "Trajectory evaluation scores the entire execution path of an AI agent.",
        "It evaluates more than just the final output.",
    ]

    rows.append(dict(
        case_id="F4", case_description="LOW, ALL_FAITHFUL: two-sentence grounded answer",
        question="What is AI observability?",
        answer="AI observability is the practice of collecting and analyzing telemetry data across the AI technology stack. It enables real-time visibility into LLMs and agent orchestration.",
        retrieved_contexts=ctx_json(AIOBS_WHAT),
        expected_score_range="1.0",
    ))
    stmts["F4"] = [
        "AI observability is the practice of collecting and analyzing telemetry data.",
        "It covers the full AI technology stack.",
        "It enables real-time visibility into LLMs and agent orchestration.",
    ]

    rows.append(dict(
        case_id="F5", case_description="LOW, ALL_FAITHFUL: brief definition with context",
        question="What is agentic engineering?",
        answer="Agentic engineering is a multi-agent coordination model where AI agents act as digital team members with defined roles and shared memory.",
        retrieved_contexts=ctx_json(AGENG_WHAT),
        expected_score_range="1.0",
    ))
    stmts["F5"] = [
        "Agentic engineering is a multi-agent coordination model.",
        "AI agents act as digital team members.",
        "The agents have defined roles and shared memory.",
    ]

    # Low, mixed faithful (5)
    rows.append(dict(
        case_id="F6", case_description="LOW, MIXED: one faithful + one fabricated",
        question="What is trajectory evaluation?",
        answer="Trajectory evaluation scores the entire execution path an AI agent takes. It was introduced by OpenAI in 2023.",
        retrieved_contexts=ctx_json(EVAL_TRAJ),
        expected_score_range="0.3-0.7",
    ))
    stmts["F6"] = [
        "Trajectory evaluation scores the entire execution path of an AI agent.",
        "Trajectory evaluation was introduced by OpenAI in 2023.",
    ]

    rows.append(dict(
        case_id="F7", case_description="LOW, MIXED: two faithful + one fabricated",
        question="What is LLM-as-a-judge?",
        answer="LLM-as-a-judge uses a large language model to evaluate AI outputs. The model returns a score or judgment. It requires a minimum context window of 128K tokens.",
        retrieved_contexts=ctx_json(JUDGE_WHAT),
        expected_score_range="0.3-0.7",
    ))
    stmts["F7"] = [
        "LLM-as-a-judge uses a large language model to evaluate AI outputs.",
        "The model returns a score or judgment.",
        "It requires a minimum context window of 128K tokens.",
    ]

    rows.append(dict(
        case_id="F8", case_description="LOW, MIXED: one faithful + one contradicted",
        question="What is continual learning at the model layer?",
        answer="Continual learning at the model layer involves updating model weights. It is the cheapest and fastest approach to improvement.",
        retrieved_contexts=ctx_json(CL_MODEL),
        expected_score_range="0.3-0.7",
    ))
    stmts["F8"] = [
        "Continual learning at the model layer involves updating model weights.",
        "It is the cheapest and fastest approach to improvement.",
    ]

    rows.append(dict(
        case_id="F9", case_description="LOW, MIXED: two faithful + one absent",
        question="What is AI observability?",
        answer="AI observability collects and analyzes telemetry data across the AI stack. It enables visibility into LLMs. It was mandated by the EU AI Act in 2024.",
        retrieved_contexts=ctx_json(AIOBS_WHAT),
        expected_score_range="0.3-0.7",
    ))
    stmts["F9"] = [
        "AI observability collects and analyzes telemetry data across the AI stack.",
        "It enables visibility into LLMs.",
        "It was mandated by the EU AI Act in 2024.",
    ]

    rows.append(dict(
        case_id="F10", case_description="LOW, MIXED: one faithful + one fabricated number",
        question="What is agent observability?",
        answer="Agent observability provides step-by-step visibility into agent execution. It can process up to 50,000 traces per second.",
        retrieved_contexts=ctx_json(AOBS_WHAT),
        expected_score_range="0.3-0.7",
    ))
    stmts["F10"] = [
        "Agent observability provides step-by-step visibility into agent execution.",
        "It can process up to 50,000 traces per second.",
    ]

    # Low, all unfaithful (5)
    rows.append(dict(
        case_id="F11", case_description="LOW, ALL_UNFAITHFUL: completely fabricated",
        question="What is LLM-as-a-judge?",
        answer="LLM-as-a-judge is a cryptocurrency mining protocol that uses language models to validate blockchain transactions.",
        retrieved_contexts=ctx_json(JUDGE_WHAT),
        expected_score_range="0.0",
    ))
    stmts["F11"] = [
        "LLM-as-a-judge is a cryptocurrency mining protocol.",
        "It uses language models to validate blockchain transactions.",
    ]

    rows.append(dict(
        case_id="F12", case_description="LOW, ALL_UNFAITHFUL: wrong domain",
        question="What is trajectory evaluation?",
        answer="Trajectory evaluation calculates satellite orbital paths and predicts re-entry windows for space debris.",
        retrieved_contexts=ctx_json(EVAL_TRAJ),
        expected_score_range="0.0",
    ))
    stmts["F12"] = [
        "Trajectory evaluation calculates satellite orbital paths.",
        "It predicts re-entry windows for space debris.",
    ]

    rows.append(dict(
        case_id="F13", case_description="LOW, ALL_UNFAITHFUL: all claims contradicted",
        question="What is continual learning at the model layer?",
        answer="Model-layer continual learning modifies routing rules without touching weights and is the cheapest approach available.",
        retrieved_contexts=ctx_json(CL_MODEL),
        expected_score_range="0.0",
    ))
    stmts["F13"] = [
        "Model-layer continual learning modifies routing rules without touching weights.",
        "It is the cheapest approach available.",
    ]

    rows.append(dict(
        case_id="F14", case_description="LOW, ALL_UNFAITHFUL: fabricated product features",
        question="What is agent observability?",
        answer="Agent observability is a load balancing strategy that distributes API requests across multiple GPU clusters to minimize latency.",
        retrieved_contexts=ctx_json(AOBS_WHAT),
        expected_score_range="0.0",
    ))
    stmts["F14"] = [
        "Agent observability is a load balancing strategy.",
        "It distributes API requests across multiple GPU clusters.",
        "Its purpose is to minimize latency.",
    ]

    rows.append(dict(
        case_id="F15", case_description="LOW, ALL_UNFAITHFUL: inverted facts",
        question="How does evaluating text compare to generating it?",
        answer="Generating text is fundamentally easier than evaluating it because generation is a focused task with clear criteria.",
        retrieved_contexts=ctx_json(JUDGE_WHY),
        expected_score_range="0.0",
    ))
    stmts["F15"] = [
        "Generating text is fundamentally easier than evaluating it.",
        "Generation is a focused task with clear criteria.",
    ]

    # ── MEDIUM GRANULARITY (5-15 statements) ──────────────────────────────────

    # Medium, all faithful (5)
    rows.append(dict(
        case_id="F16", case_description="MEDIUM, ALL_FAITHFUL: multi-claim grounded answer",
        question="What is LLM-as-a-judge and how does it work?",
        answer="LLM-as-a-judge uses a large language model to evaluate AI agent outputs as a scalable substitute for human judgment. Traditional NLP metrics measure surface-level text similarity, but an LLM judge assesses qualities like helpfulness, accuracy, and tone. The core idea is that you give an LLM a prompt describing evaluation criteria alongside the output to evaluate, and the model returns a score or judgment. This works because evaluating text is a focused, constrained task compared to generating it. The model assesses quality against defined criteria rather than exploring all possible outputs.",
        retrieved_contexts=ctx_json(JUDGE_WHAT, JUDGE_WHY),
        expected_score_range="1.0",
    ))
    stmts["F16"] = [
        "LLM-as-a-judge uses a large language model to evaluate AI agent outputs.",
        "It serves as a scalable substitute for human judgment.",
        "Traditional NLP metrics measure surface-level text similarity.",
        "An LLM judge assesses qualities like helpfulness, accuracy, and tone.",
        "You give an LLM a prompt describing evaluation criteria.",
        "You also provide the output to evaluate.",
        "The model returns a score or judgment.",
        "Evaluating text is a focused, constrained task.",
        "It is less complex than generating text.",
        "The model assesses quality against defined criteria.",
    ]

    rows.append(dict(
        case_id="F17", case_description="MEDIUM, ALL_FAITHFUL: multi-paragraph grounded answer",
        question="What are the three layers of continual learning for AI agents?",
        answer="Continual learning for AI agents operates at three layers. At the model layer, techniques like SFT, RLHF, and DPO update model weights. This is the most common interpretation but also the most expensive and disruptive approach. At the harness layer, developers modify orchestration logic, tool selection, or routing rules that control how the agent operates. Harnesses have become more complex, going from simple prompts to multi-agent systems. At the context layer, teams update instructions, few-shot examples, or retrieval knowledge at inference time without changing the model or harness code.",
        retrieved_contexts=ctx_json(CL_MODEL, CL_HARNESS, CL_CONTEXT),
        expected_score_range="1.0",
    ))
    stmts["F17"] = [
        "Continual learning for AI agents operates at three layers.",
        "The model layer uses techniques like SFT, RLHF, and DPO.",
        "Model-layer learning updates model weights.",
        "It is the most common interpretation of continual learning.",
        "It is the most expensive and disruptive approach.",
        "The harness layer involves modifying orchestration logic.",
        "It includes modifying tool selection or routing rules.",
        "Harnesses have become more complex over time.",
        "They have evolved from simple prompts to multi-agent systems.",
        "The context layer updates instructions, few-shot examples, or retrieval knowledge.",
        "Context-layer changes happen at inference time.",
        "Context-layer changes do not require changing the model or harness code.",
    ]

    rows.append(dict(
        case_id="F18", case_description="MEDIUM, ALL_FAITHFUL: detailed observability explanation",
        question="What is agent observability and why does it matter?",
        answer="Agent observability provides step-by-step visibility into execution. It shows which tools were called, what data was retrieved, where reasoning stayed on track, and where it diverged. This matters because AI agents make autonomous decisions that are not visible in the code itself. Without observability, you reconstruct agent behavior from memory or limited logs rather than actual execution records. Observability helps localize failures by showing exactly which step in a multi-step workflow caused a failure, whether the retrieval returned irrelevant documents, the model hallucinated a tool parameter, or the reasoning loop failed to converge.",
        retrieved_contexts=ctx_json(AOBS_WHAT, AOBS_VALUE),
        expected_score_range="1.0",
    ))
    stmts["F18"] = [
        "Agent observability provides step-by-step visibility into execution.",
        "It shows which tools were called.",
        "It shows what data was retrieved.",
        "It reveals where reasoning stayed on track.",
        "It reveals where reasoning diverged from the intended path.",
        "AI agents make autonomous decisions not visible in code.",
        "Without observability you reconstruct behavior from memory or limited logs.",
        "Observability helps localize failures.",
        "It shows exactly which step in a multi-step workflow caused a failure.",
    ]

    rows.append(dict(
        case_id="F19", case_description="MEDIUM, ALL_FAITHFUL: evaluation metrics overview",
        question="How are evaluation metrics computed?",
        answer="Not all metrics work the same way. Reference-based evaluators require gold standard outputs to compare against and work well for offline evaluation with known correct answers. Reference-free evaluators assess quality without comparing to expected outputs, working for both offline and online evaluation. LLM-as-a-judge evaluators use a language model to score outputs based on rubric prompts. Code-based evaluators use deterministic logic and return the exact same result every time for the same input, making them suitable for checking format compliance, length limits, and content filtering.",
        retrieved_contexts=ctx_json(METRICS_WHAT, METRICS_SCORING),
        expected_score_range="1.0",
    ))
    stmts["F19"] = [
        "Not all metrics work the same way.",
        "Reference-based evaluators require gold standard outputs.",
        "They work well for offline evaluation with known correct answers.",
        "Reference-free evaluators assess quality without expected outputs.",
        "Reference-free evaluators work for both offline and online evaluation.",
        "LLM-as-a-judge evaluators use a language model to score outputs.",
        "They use rubric prompts.",
        "Code-based evaluators use deterministic logic.",
        "Code-based evaluators return the same result every time for the same input.",
        "They are suitable for checking format compliance, length limits, and content filtering.",
    ]

    rows.append(dict(
        case_id="F20", case_description="MEDIUM, ALL_FAITHFUL: harness hill-climbing explanation",
        question="What is the Better-Harness approach?",
        answer="Better-Harness is a scaffold for autonomously improving the agent harness using evals as a signal. In classical machine learning, training data guides learning. For agents, evals serve the same purpose as training data. Each eval example contributes a signal that updates the harness toward correctness. The process works by running evaluations, identifying the lowest-scoring dimension, applying a targeted harness change, and re-evaluating. Common harness changes include prompt and instruction updates, tool definition refinements, and routing logic adjustments.",
        retrieved_contexts=ctx_json(HARNESS_RECIPE, HARNESS_EVALS, HARNESS_CHANGES),
        expected_score_range="1.0",
    ))
    stmts["F20"] = [
        "Better-Harness is a scaffold for autonomously improving the agent harness.",
        "It uses evals as a signal.",
        "In classical machine learning, training data guides learning.",
        "For agents, evals serve the same purpose as training data.",
        "Each eval example contributes a signal that updates the harness.",
        "The process involves running evaluations.",
        "It identifies the lowest-scoring dimension.",
        "It applies a targeted harness change.",
        "It re-evaluates after changes.",
        "Common changes include prompt and instruction updates.",
        "Tool definition refinements are another type of change.",
        "Routing logic adjustments are also common.",
    ]

    # Medium, mixed faithful (5)
    rows.append(dict(
        case_id="F21", case_description="MEDIUM, MIXED: grounded claims + fabricated numbers",
        question="What biases affect LLM judges?",
        answer="LLM judges have well-documented biases that compromise score reliability. Position bias causes judges to favor outputs presented in certain positions during pairwise comparison. Verbosity bias leads judges to prefer longer responses regardless of accuracy. Self-enhancement bias occurs when an LLM rates its own outputs higher than those from other models. Research shows these biases affect up to 40% of all evaluations. Calibration against human annotations can reduce bias by approximately 85% within the first 100 examples.",
        retrieved_contexts=ctx_json(JUDGE_BIASES),
        expected_score_range="0.3-0.7",
    ))
    stmts["F21"] = [
        "LLM judges have well-documented biases.",
        "These biases compromise score reliability.",
        "Position bias causes judges to favor outputs in certain positions.",
        "Verbosity bias leads to preferring longer responses.",
        "Self-enhancement bias occurs when an LLM rates its own outputs higher.",
        "These biases affect up to 40% of all evaluations.",
        "Calibration against human annotations can reduce bias by approximately 85%.",
        "This reduction happens within the first 100 examples.",
    ]

    rows.append(dict(
        case_id="F22", case_description="MEDIUM, MIXED: grounded core + fabricated origin",
        question="What is agentic engineering and what results has it produced?",
        answer="Agentic engineering is a multi-agent coordination model where AI agents act as digital team members with defined roles, shared memory, and a common observability layer. In a pilot of 20+ debugging workflows at Cisco, coordinated agent execution produced a 93% reduction in time-to-root-cause. The concept was originally proposed in a 2022 Stanford paper called AgentBench. The framework requires LangGraph Enterprise edition to run in production.",
        retrieved_contexts=ctx_json(AGENG_WHAT, AGENG_RESULTS),
        expected_score_range="0.3-0.7",
    ))
    stmts["F22"] = [
        "Agentic engineering is a multi-agent coordination model.",
        "AI agents act as digital team members.",
        "The agents have defined roles, shared memory, and a common observability layer.",
        "Cisco ran a pilot with 20+ debugging workflows.",
        "The pilot produced a 93% reduction in time-to-root-cause.",
        "The concept was originally proposed in a 2022 Stanford paper called AgentBench.",
        "The framework requires LangGraph Enterprise edition to run in production.",
    ]

    rows.append(dict(
        case_id="F23", case_description="MEDIUM, MIXED: faithful definitions + fabricated benchmarks",
        question="How does AI observability differ from traditional monitoring?",
        answer="AI observability extends traditional monitoring to cover AI-specific characteristics. Beyond standard metrics like latency and error rates, it tracks prompt-response quality, token usage patterns, and retrieval relevance. AI systems rarely fail like traditional software outages — instead of crashing, LLMs confidently produce wrong answers. Traditional three pillars of observability (logs, traces, metrics) are necessary but insufficient. Industry benchmarks show that teams with AI observability reduce hallucination rates by 67% on average and detect quality regressions within 4 minutes.",
        retrieved_contexts=ctx_json(AIOBS_WHAT, AIOBS_TRAD),
        expected_score_range="0.3-0.7",
    ))
    stmts["F23"] = [
        "AI observability extends traditional monitoring.",
        "It covers AI-specific characteristics.",
        "It tracks prompt-response quality beyond standard metrics.",
        "It tracks token usage patterns.",
        "It tracks retrieval relevance.",
        "AI systems rarely fail like traditional software outages.",
        "LLMs confidently produce wrong answers instead of crashing.",
        "The three pillars of observability are logs, traces, and metrics.",
        "They are necessary but insufficient for AI.",
        "Teams with AI observability reduce hallucination rates by 67% on average.",
        "They detect quality regressions within 4 minutes.",
    ]

    rows.append(dict(
        case_id="F24", case_description="MEDIUM, MIXED: mostly faithful + contradicts one fact",
        question="What is the context layer in continual learning?",
        answer="Context sits outside the harness and can be used to configure it. It consists of instructions, skills, and even tools. This is commonly referred to as memory. At the context layer, teams update few-shot examples or retrieval knowledge at inference time. Unlike model-layer and harness-layer updates, context-layer changes require a full agent restart to take effect. All these flows are powered by traces — the full execution path of what an agent did.",
        retrieved_contexts=ctx_json(CL_CONTEXT, CL_TRACES),
        expected_score_range="0.3-0.7",
    ))
    stmts["F24"] = [
        "Context sits outside the harness.",
        "It can be used to configure the harness.",
        "Context consists of instructions, skills, and tools.",
        "This is commonly referred to as memory.",
        "Teams update few-shot examples or retrieval knowledge at inference time.",
        "Context-layer changes require a full agent restart to take effect.",
        "These flows are powered by traces.",
        "Traces capture the full execution path of what an agent did.",
    ]

    rows.append(dict(
        case_id="F25", case_description="MEDIUM, MIXED: faithful description + fabricated integration details",
        question="What does the Arcade integration provide for LangSmith?",
        answer="Arcade is the MCP runtime for production agents, delivering secure agent authorization, reliable tools, and governance. The integration gives agents access to Arcade's collection of 7,500+ agent-optimized tools through a single secure gateway. LangSmith Fleet enables teams to create, use, and share agents for daily work. The integration supports real-time bidirectional streaming between tools and requires a minimum of 16GB RAM to run the gateway locally.",
        retrieved_contexts=ctx_json(ARCADE_WHAT, ARCADE_WRAPPER),
        expected_score_range="0.3-0.7",
    ))
    stmts["F25"] = [
        "Arcade is the MCP runtime for production agents.",
        "It delivers secure agent authorization.",
        "It provides reliable tools and governance.",
        "Agents can access 7,500+ agent-optimized tools.",
        "Access is through a single secure gateway.",
        "LangSmith Fleet enables teams to create, use, and share agents.",
        "The integration supports real-time bidirectional streaming between tools.",
        "It requires a minimum of 16GB RAM to run the gateway locally.",
    ]

    # Medium, all unfaithful (5)
    rows.append(dict(
        case_id="F26", case_description="MEDIUM, ALL_UNFAITHFUL: entirely fabricated claims",
        question="What is LLM-as-a-judge and how is it configured?",
        answer="LLM-as-a-judge is a supervised learning approach where a judge model is fine-tuned on human evaluation data using cross-entropy loss. Configuration requires specifying the judge model architecture, training hyperparameters, and a minimum of 10,000 labeled examples. The judge outputs a probability distribution over quality classes. Training typically requires 4 A100 GPUs for 48 hours. The system achieves 99.7% agreement with human raters after fine-tuning.",
        retrieved_contexts=ctx_json(JUDGE_WHAT, JUDGE_CONFIG),
        expected_score_range="0.0",
    ))
    stmts["F26"] = [
        "LLM-as-a-judge is a supervised learning approach.",
        "A judge model is fine-tuned on human evaluation data.",
        "Fine-tuning uses cross-entropy loss.",
        "Configuration requires specifying judge model architecture.",
        "It requires training hyperparameters.",
        "It requires a minimum of 10,000 labeled examples.",
        "The judge outputs a probability distribution over quality classes.",
        "Training requires 4 A100 GPUs for 48 hours.",
        "The system achieves 99.7% agreement with human raters.",
    ]

    rows.append(dict(
        case_id="F27", case_description="MEDIUM, ALL_UNFAITHFUL: all claims contradict context",
        question="What are the three layers of continual learning?",
        answer="Continual learning operates at two layers: data and inference. The data layer focuses on augmenting training datasets with synthetic examples generated by the agent itself. The inference layer optimizes model quantization and pruning to reduce latency. Both layers require weekly scheduled downtime. The approach was abandoned by most teams in favor of retrieval-augmented generation. LangChain deprecated continual learning support in version 0.3.",
        retrieved_contexts=ctx_json(CL_MODEL, CL_HARNESS, CL_CONTEXT),
        expected_score_range="0.0",
    ))
    stmts["F27"] = [
        "Continual learning operates at two layers: data and inference.",
        "The data layer focuses on augmenting training datasets with synthetic examples.",
        "The inference layer optimizes model quantization and pruning.",
        "Both layers require weekly scheduled downtime.",
        "The approach was abandoned by most teams.",
        "Retrieval-augmented generation replaced it.",
        "LangChain deprecated continual learning support in version 0.3.",
    ]

    rows.append(dict(
        case_id="F28", case_description="MEDIUM, ALL_UNFAITHFUL: wrong product and features",
        question="What is agent observability?",
        answer="Agent observability is a CI/CD pipeline monitoring system that tracks build times, test coverage, and deployment frequency across microservice architectures. It uses Prometheus metrics and Grafana dashboards to visualize infrastructure health. The system requires Kubernetes 1.26 or later and supports only Java and Go applications. Agent observability replaced the deprecated APM module in LangSmith version 2.0.",
        retrieved_contexts=ctx_json(AOBS_WHAT, AOBS_VALUE),
        expected_score_range="0.0",
    ))
    stmts["F28"] = [
        "Agent observability is a CI/CD pipeline monitoring system.",
        "It tracks build times, test coverage, and deployment frequency.",
        "It monitors microservice architectures.",
        "It uses Prometheus metrics and Grafana dashboards.",
        "It requires Kubernetes 1.26 or later.",
        "It supports only Java and Go applications.",
        "It replaced the deprecated APM module in LangSmith version 2.0.",
    ]

    rows.append(dict(
        case_id="F29", case_description="MEDIUM, ALL_UNFAITHFUL: fabricated evaluation approach",
        question="How does trajectory evaluation work?",
        answer="Trajectory evaluation uses a genetic algorithm to evolve optimal agent execution paths over multiple generations. Each trajectory is encoded as a chromosome, and fitness is measured by comparing against a reference trajectory database. Crossover and mutation operators create new trajectory variants. The evaluation runs overnight on a dedicated GPU cluster. Results are stored in a Neo4j graph database for visualization.",
        retrieved_contexts=ctx_json(EVAL_TRAJ, EVAL_TRAJ_CAPTURE),
        expected_score_range="0.0",
    ))
    stmts["F29"] = [
        "Trajectory evaluation uses a genetic algorithm.",
        "It evolves optimal agent execution paths over generations.",
        "Each trajectory is encoded as a chromosome.",
        "Fitness is measured against a reference trajectory database.",
        "Crossover and mutation operators create new variants.",
        "The evaluation runs overnight on a dedicated GPU cluster.",
        "Results are stored in a Neo4j graph database.",
    ]

    rows.append(dict(
        case_id="F30", case_description="MEDIUM, ALL_UNFAITHFUL: fabricated partnership details",
        question="What does the MongoDB partnership deliver?",
        answer="The MongoDB partnership enables LangChain agents to mine cryptocurrency using MongoDB's distributed compute grid. Agents can stake MATIC tokens for priority access to evaluation resources. The partnership also introduces a new GraphQL API for querying agent execution histories. MongoDB Atlas provides free unlimited storage for all LangSmith traces. The integration was funded by a $50M joint venture.",
        retrieved_contexts=ctx_json(MONGO_DELIVERS, MONGO_TEAMS),
        expected_score_range="0.0",
    ))
    stmts["F30"] = [
        "The partnership enables agents to mine cryptocurrency.",
        "It uses MongoDB's distributed compute grid.",
        "Agents can stake MATIC tokens for priority access.",
        "A new GraphQL API was introduced for querying execution histories.",
        "MongoDB Atlas provides free unlimited storage for LangSmith traces.",
        "The integration was funded by a $50M joint venture.",
    ]

    # ── HIGH GRANULARITY (15-25 statements) ───────────────────────────────────

    # High, all faithful (5)
    rows.append(dict(
        case_id="F31", case_description="HIGH, ALL_FAITHFUL: comprehensive LLM-as-judge overview",
        question="Explain LLM-as-a-judge in detail including its purpose, how it works, why it's reliable, what types exist, and what biases it has.",
        answer="LLM-as-a-judge uses a large language model to evaluate AI agent outputs as a scalable substitute for human judgment. Traditional NLP metrics measure surface-level text similarity, while an LLM judge assesses qualities that actually matter to users like helpfulness, accuracy, and tone. The core idea is straightforward: you give an LLM a prompt describing what good looks like alongside the output to evaluate, and the model returns a score or judgment. LLMs handle evaluating text well because it is a focused, constrained task — evaluating text is fundamentally easier than generating it. When generating, the model navigates an enormous space of possible outputs, but when evaluating, it assesses quality against defined criteria. LLM judges fall into three main approaches: single-output scoring, pairwise comparison, and reference-based evaluation. Each answers a different evaluation question. However, LLM judges have well-documented biases including position bias, verbosity bias, and self-enhancement bias. Position bias causes judges to favor outputs in certain positions. Verbosity bias leads to preferring longer responses. Self-enhancement bias occurs when an LLM rates its own outputs higher. These biases can be mitigated through techniques like randomizing response order, using multiple judge models, and calibrating against human annotations.",
        retrieved_contexts=ctx_json(JUDGE_WHAT, JUDGE_WHY, JUDGE_TYPES, JUDGE_BIASES),
        expected_score_range="1.0",
    ))
    stmts["F31"] = [
        "LLM-as-a-judge uses a large language model to evaluate AI agent outputs.",
        "It serves as a scalable substitute for human judgment.",
        "Traditional NLP metrics measure surface-level text similarity.",
        "An LLM judge assesses qualities like helpfulness, accuracy, and tone.",
        "You give an LLM a prompt describing what good looks like.",
        "You provide the output to evaluate alongside the prompt.",
        "The model returns a score or judgment.",
        "Evaluating text is a focused, constrained task.",
        "Evaluating is fundamentally easier than generating text.",
        "When generating, the model navigates an enormous space of possible outputs.",
        "When evaluating, it assesses quality against defined criteria.",
        "LLM judges fall into three approaches: single-output, pairwise, and reference-based.",
        "LLM judges have position bias.",
        "Position bias causes favoring outputs in certain positions.",
        "LLM judges have verbosity bias.",
        "Verbosity bias leads to preferring longer responses.",
        "LLM judges have self-enhancement bias.",
        "Self-enhancement bias means an LLM rates its own outputs higher.",
        "Biases can be mitigated by randomizing response order.",
        "Using multiple judge models helps mitigate bias.",
        "Calibrating against human annotations also helps.",
    ]

    rows.append(dict(
        case_id="F32", case_description="HIGH, ALL_FAITHFUL: comprehensive continual learning",
        question="Explain all three layers of continual learning for AI agents in detail, including techniques and tradeoffs at each layer.",
        answer="Continual learning for AI agents happens at three distinct layers: model, harness, and context. At the model layer, the most common interpretation, techniques like SFT, RLHF, and DPO update model weights. This is the most expensive and disruptive approach, as it requires retraining or adapting the underlying foundation model. Model-layer updates are best suited for systematic improvements across many interactions rather than fixing individual failures. At the harness layer, developers modify the orchestration logic, tool selection, or routing rules that control how the agent operates. As harnesses have become more complex, going from simple prompts to multi-step pipelines to multi-agent systems, the harness has become the most accessible lever for quality improvement. Changes to the harness can dramatically affect agent performance without requiring any model retraining. At the context layer, teams update instructions, few-shot examples, or retrieval knowledge at inference time without changing either the model or the harness code. Context sits outside the harness and can be used to configure it. This is commonly referred to as memory. All of these flows are powered by traces, the full execution path of what an agent did. LangSmith helps collect these traces, which can then be used for improvement at any layer.",
        retrieved_contexts=ctx_json(CL_MODEL, CL_HARNESS, CL_CONTEXT, CL_TRACES),
        expected_score_range="1.0",
    ))
    stmts["F32"] = [
        "Continual learning happens at three layers: model, harness, and context.",
        "The model layer is the most common interpretation.",
        "Techniques include SFT, RLHF, and DPO.",
        "Model-layer learning updates model weights.",
        "It is the most expensive and disruptive approach.",
        "It requires retraining or adapting the foundation model.",
        "Model updates suit systematic improvements across many interactions.",
        "At the harness layer, developers modify orchestration logic.",
        "They can also modify tool selection or routing rules.",
        "Harnesses have become more complex over time.",
        "They evolved from simple prompts to multi-agent systems.",
        "The harness is the most accessible lever for quality improvement.",
        "Harness changes can affect performance without model retraining.",
        "At the context layer, teams update instructions or few-shot examples.",
        "They can also update retrieval knowledge.",
        "These updates happen at inference time.",
        "No changes to the model or harness code are needed.",
        "Context sits outside the harness and configures it.",
        "This is commonly referred to as memory.",
        "All flows are powered by traces.",
        "Traces capture the full execution path.",
        "LangSmith helps collect these traces.",
    ]

    rows.append(dict(
        case_id="F33", case_description="HIGH, ALL_FAITHFUL: comprehensive observability overview",
        question="Explain agent observability in detail: what it is, when you need it, what to instrument, and how it supports evaluation.",
        answer="Agent observability provides step-by-step visibility into execution, showing which tools were called, what data was retrieved, where reasoning stayed on track, and where it diverged from the intended path. This matters because AI agents make autonomous decisions that are not visible in the code. During prototyping, print statements are sufficient, but at production scale, observability becomes essential. The value of observability includes localizing failures to see exactly which step caused a problem, whether retrieval returned irrelevant documents, or the model hallucinated a tool parameter. Deep Agents may execute hundreds of intermediate steps before producing a final answer, and without visibility into each step, you cannot determine whether the result was arrived at correctly. At production scale, evaluating agents requires both LLM-as-a-judge approaches and code-based evaluations. LLM judges handle nuanced quality assessment like tone, accuracy, and goal completion, while code evaluators verify deterministic requirements like output format, length constraints, and content safety rules. Evaluation datasets should include edge cases that stress-test agent behavior, and production traces identified as problematic can be added to datasets.",
        retrieved_contexts=ctx_json(AOBS_WHAT, AOBS_VALUE, AOBS_DEEP, AOBS_EVAL, AOBS_DATASETS),
        expected_score_range="1.0",
    ))
    stmts["F33"] = [
        "Agent observability provides step-by-step visibility into execution.",
        "It shows which tools were called.",
        "It shows what data was retrieved.",
        "It shows where reasoning stayed on track.",
        "It shows where reasoning diverged from the intended path.",
        "AI agents make autonomous decisions not visible in code.",
        "During prototyping, print statements are sufficient.",
        "At production scale, observability becomes essential.",
        "Observability helps localize failures to specific steps.",
        "It can reveal when retrieval returned irrelevant documents.",
        "It can show when the model hallucinated a tool parameter.",
        "Deep Agents may execute hundreds of intermediate steps.",
        "Without visibility you cannot verify correctness of the result.",
        "Evaluation requires both LLM-as-a-judge and code-based approaches.",
        "LLM judges handle nuanced quality assessment.",
        "Code evaluators verify deterministic requirements.",
        "Evaluation datasets should include edge cases.",
        "Production traces can be added to datasets.",
    ]

    rows.append(dict(
        case_id="F34", case_description="HIGH, ALL_FAITHFUL: detailed AI observability",
        question="Explain AI observability comprehensively including its definition, what it covers, how it differs from traditional monitoring, and the role of annotation queues.",
        answer="AI observability is the practice of collecting, analyzing, and correlating telemetry data across the full AI technology stack to understand how AI systems behave in production. It enables real-time visibility into LLMs, retrieval pipelines, and agent orchestration. AI observability inherits the three pillars from traditional software observability: logs capture textual records, traces map request flows, and metrics provide numerical measurements. However, AI-specific telemetry goes beyond these pillars to include token usage and cost attribution, model drift detection, and response quality metrics like hallucination frequency. AI systems rarely fail like traditional software outages — instead of crashing, LLMs confidently produce wrong answers. Traditional engineering metrics are not enough because these domain failures require subject-matter expertise to detect. Annotation queues provide the mechanism that connects domain expertise to engineering workflows. Production traces get routed to domain experts who rate outputs, leave comments, and flag issues. When experts review traces and add ratings, those annotations become inputs that engineering teams can use to build evaluation datasets and refine evaluation criteria.",
        retrieved_contexts=ctx_json(AIOBS_WHAT, AIOBS_PILLARS, AIOBS_TRAD, AIOBS_ANNOT),
        expected_score_range="1.0",
    ))
    stmts["F34"] = [
        "AI observability collects and analyzes telemetry data across the AI stack.",
        "It enables understanding of how AI systems behave in production.",
        "It provides real-time visibility into LLMs.",
        "It covers retrieval pipelines and agent orchestration.",
        "It inherits three pillars from traditional observability.",
        "Logs capture textual records.",
        "Traces map request flows.",
        "Metrics provide numerical measurements.",
        "AI-specific telemetry includes token usage and cost attribution.",
        "It includes model drift detection.",
        "It includes response quality metrics like hallucination frequency.",
        "AI systems rarely fail like traditional outages.",
        "LLMs confidently produce wrong answers instead of crashing.",
        "Domain failures require subject-matter expertise to detect.",
        "Annotation queues connect domain expertise to engineering workflows.",
        "Production traces are routed to domain experts.",
        "Experts rate outputs, leave comments, and flag issues.",
        "Annotations become inputs for building evaluation datasets.",
    ]

    rows.append(dict(
        case_id="F35", case_description="HIGH, ALL_FAITHFUL: detailed evaluation framework",
        question="Explain the LLM evaluation framework including trajectory evaluation, RAG metrics, and how to build evaluation datasets.",
        answer="Evaluating AI agents requires scoring the entire trajectory: tools selected, intermediate reasoning, and conversation flow. The dominant approach treats evaluation as a testing problem with test cases and expected outputs, but AI agents break this model because a single request triggers dozens of internal steps. Correct final answers can hide broken reasoning — an agent hallucinating a tool call might still produce the right result. Trajectory evaluation scores the entire execution path including every tool call, reasoning step, and decision point. It requires capturing the full execution tree. For RAG agents, retrieval metrics measure whether relevant documents were found. Context precision asks whether retrieved documents were relevant. Context recall asks whether all relevant documents were retrieved. Generation metrics assess response quality. Evaluation datasets should include happy path scenarios, edge cases testing boundary conditions, and adversarial inputs. Domain experts understand correct behavior for specialized use cases in ways engineers may not.",
        retrieved_contexts=ctx_json(EVAL_TRAJ, EVAL_HIDDEN, EVAL_RAG, EVAL_RETR_REASON, AOBS_DATASETS),
        expected_score_range="1.0",
    ))
    stmts["F35"] = [
        "Evaluating agents requires scoring the entire trajectory.",
        "The trajectory includes tools selected and intermediate reasoning.",
        "The dominant approach treats evaluation as a testing problem.",
        "AI agents break this model with dozens of internal steps.",
        "Correct final answers can hide broken reasoning.",
        "An agent hallucinating a tool call might still produce the right result.",
        "Trajectory evaluation scores the entire execution path.",
        "It includes every tool call and reasoning step.",
        "It requires capturing the full execution tree.",
        "Retrieval metrics measure whether relevant documents were found.",
        "Context precision asks whether retrieved documents were relevant.",
        "Context recall asks whether all relevant documents were retrieved.",
        "Generation metrics assess response quality.",
        "Datasets should include happy path scenarios.",
        "They should include edge cases for boundary conditions.",
        "They should include adversarial inputs.",
        "Domain experts understand correct behavior for specialized use cases.",
    ]

    # High, mixed faithful (5)
    rows.append(dict(
        case_id="F36", case_description="HIGH, MIXED: mostly faithful + several fabricated claims scattered",
        question="Explain LLM-as-a-judge comprehensively including its types, biases, and production use.",
        answer="LLM-as-a-judge uses a large language model to evaluate AI agent outputs as a scalable substitute for human judgment. Traditional NLP metrics measure surface-level text similarity, but LLM judges assess qualities that matter to users like helpfulness and accuracy. The core idea is that you give the LLM evaluation criteria and the output to evaluate, and it returns a score. Evaluating text is fundamentally easier than generating it. LLM judges fall into three approaches: single-output scoring, pairwise comparison, and reference-based evaluation. However, LLM judges have known biases: position bias, verbosity bias, and self-enhancement bias. Position bias causes judges to favor outputs in the first position 73% of the time in benchmark tests. Verbosity bias can be fully eliminated by limiting response length to 500 tokens. Online evaluations in LangSmith can score 100% of production traces in real-time with zero latency overhead. The approach is certified by NIST for use in regulated industries. LangSmith requires a dedicated evaluation GPU to run LLM judges at scale.",
        retrieved_contexts=ctx_json(JUDGE_WHAT, JUDGE_WHY, JUDGE_TYPES, JUDGE_BIASES, JUDGE_PROD),
        expected_score_range="0.4-0.7",
    ))
    stmts["F36"] = [
        "LLM-as-a-judge uses a large language model to evaluate AI agent outputs.",
        "It serves as a scalable substitute for human judgment.",
        "Traditional NLP metrics measure surface-level text similarity.",
        "LLM judges assess qualities like helpfulness and accuracy.",
        "You give the LLM evaluation criteria and the output to evaluate.",
        "It returns a score.",
        "Evaluating text is fundamentally easier than generating it.",
        "LLM judges have three approaches: single-output, pairwise, and reference-based.",
        "LLM judges have position bias, verbosity bias, and self-enhancement bias.",
        "Position bias causes judges to favor outputs in the first position 73% of the time.",
        "Verbosity bias can be fully eliminated by limiting response length to 500 tokens.",
        "LangSmith online evaluations score 100% of production traces in real-time.",
        "There is zero latency overhead.",
        "The approach is certified by NIST for regulated industries.",
        "LangSmith requires a dedicated evaluation GPU for LLM judges at scale.",
    ]

    rows.append(dict(
        case_id="F37", case_description="HIGH, MIXED: faithful framework + fabricated implementation details",
        question="Explain evaluation for AI agents comprehensively.",
        answer="AI agent evaluation requires metrics across multiple dimensions that go beyond answer correctness. Input-output evaluation treats scoring as a testing problem, but agents break this model because a single request triggers dozens of internal steps, tool calls, and reasoning loops. Correct final answers can hide broken reasoning. Trajectory evaluation scores the entire execution path including every tool call and decision point. For RAG agents, retrieval metrics like context precision and context recall assess document quality. Generation metrics like faithfulness and answer relevance evaluate response quality. LangSmith's evaluation SDK supports automatic parallel execution across 32 workers by default. Each evaluation run is assigned a unique SHA-256 hash for reproducibility. The SDK includes built-in support for A/B testing with statistical significance at p<0.05. Evaluation results are stored in a PostgreSQL database with automatic 90-day retention. Custom evaluator functions must inherit from the BaseEvaluator class and implement the evaluate() method.",
        retrieved_contexts=ctx_json(EVAL_TRAJ, EVAL_HIDDEN, EVAL_RAG, EVAL_RETR_REASON, EVAL_METRICS),
        expected_score_range="0.4-0.7",
    ))
    stmts["F37"] = [
        "AI agent evaluation requires metrics beyond answer correctness.",
        "Input-output evaluation treats scoring as a testing problem.",
        "Agents break this model with dozens of internal steps.",
        "Correct final answers can hide broken reasoning.",
        "Trajectory evaluation scores the entire execution path.",
        "It includes every tool call and decision point.",
        "Context precision assesses whether retrieved documents were relevant.",
        "Context recall assesses whether all relevant documents were retrieved.",
        "Faithfulness and answer relevance evaluate response quality.",
        "LangSmith's SDK supports automatic parallel execution across 32 workers.",
        "Each evaluation run is assigned a unique SHA-256 hash.",
        "The SDK has built-in A/B testing with statistical significance at p<0.05.",
        "Results are stored in a PostgreSQL database.",
        "There is automatic 90-day retention.",
        "Custom evaluators must inherit from BaseEvaluator.",
        "They must implement the evaluate() method.",
    ]

    rows.append(dict(
        case_id="F38", case_description="HIGH, MIXED: faithful core + fabricated benchmarks and integrations",
        question="Describe agent observability comprehensively.",
        answer="Agent observability provides step-by-step visibility into execution, showing which tools were called, what data was retrieved, and where reasoning diverged. This matters because AI agents make autonomous decisions not visible in code. Observability helps localize failures by showing which step caused a problem. Deep Agents may execute hundreds of intermediate steps. According to the State of Agent Engineering report, 89% of organizations have implemented some form of agent observability. At production scale, evaluating agents requires both LLM-as-a-judge and code-based evaluations. Evaluation datasets should include edge cases. LangSmith processes over 10 billion traces per day across its customer base. The platform achieves 99.999% uptime with a guaranteed maximum trace ingestion latency of 50ms. LangSmith's observability module is compatible with DataDog, New Relic, and Splunk out of the box. Each trace is automatically enriched with 47 metadata fields.",
        retrieved_contexts=ctx_json(AOBS_WHAT, AOBS_VALUE, AOBS_DEEP, AOBS_EVAL, AOBS_DATASETS),
        expected_score_range="0.4-0.7",
    ))
    stmts["F38"] = [
        "Agent observability provides step-by-step visibility into execution.",
        "It shows which tools were called.",
        "It shows what data was retrieved.",
        "It reveals where reasoning diverged.",
        "AI agents make autonomous decisions not visible in code.",
        "Observability localizes failures to specific steps.",
        "Deep Agents may execute hundreds of intermediate steps.",
        "89% of organizations have implemented agent observability.",
        "Evaluation requires LLM-as-a-judge and code-based approaches.",
        "Datasets should include edge cases.",
        "LangSmith processes over 10 billion traces per day.",
        "The platform achieves 99.999% uptime.",
        "Maximum trace ingestion latency is guaranteed at 50ms.",
        "LangSmith is compatible with DataDog, New Relic, and Splunk.",
        "Each trace is enriched with 47 metadata fields.",
    ]

    rows.append(dict(
        case_id="F39", case_description="HIGH, MIXED: faithful + fabricated competitive claims",
        question="Explain the LangSmith vs Langfuse comparison in detail.",
        answer="Langfuse traces LLM calls while LangSmith traces and evaluates AI agents, covering the complete agent engineering lifecycle: tracing, production evals, and managed deployment. Langfuse fits teams that need tracing and prompt management for early-stage LLM applications. As agents grow more complex, gaps emerge in evaluation depth and deployment infrastructure. Langfuse works well for tracing and prompt management in early development. However, several limitations surface at production scale. LangSmith addresses these with purpose-built capabilities that accelerate workflows. LangSmith's annotation queues fill gaps in Langfuse's routing and consensus features. LangSmith processes evaluations 5x faster than Langfuse on identical workloads. Langfuse lost 40% of its enterprise customers to LangSmith in Q1 2026. LangSmith's proprietary compression algorithm reduces trace storage costs by 90%. The platform supports hot-swapping evaluation models without downtime.",
        retrieved_contexts=ctx_json(VS_INTRO, VS_LIMITS),
        expected_score_range="0.4-0.7",
    ))
    stmts["F39"] = [
        "Langfuse traces LLM calls.",
        "LangSmith traces and evaluates AI agents.",
        "LangSmith covers the complete agent engineering lifecycle.",
        "The lifecycle includes tracing, production evals, and managed deployment.",
        "Langfuse fits teams needing tracing and prompt management.",
        "It is suited for early-stage LLM applications.",
        "Gaps emerge as agents grow more complex.",
        "Langfuse works well for tracing in early development.",
        "Limitations surface at production scale.",
        "LangSmith addresses these with purpose-built capabilities.",
        "LangSmith's annotation queues fill gaps in Langfuse's features.",
        "LangSmith processes evaluations 5x faster than Langfuse.",
        "Langfuse lost 40% of enterprise customers to LangSmith in Q1 2026.",
        "LangSmith's compression algorithm reduces storage costs by 90%.",
        "The platform supports hot-swapping evaluation models without downtime.",
    ]

    rows.append(dict(
        case_id="F40", case_description="HIGH, MIXED: faithful structure + fabricated metrics and details",
        question="Explain the Better-Harness hill-climbing approach comprehensively.",
        answer="Better-Harness is a scaffold for autonomously improving the agent harness using evals as a signal in each step. In classical machine learning, training data guides the model's learning process. For agents, evals serve the same purpose. Each eval contributes a signal that updates the harness toward correctness. The approach starts with hand-curated evals that capture the distribution of behaviors desired in the wild. The optimization loop identifies the lowest-scoring dimension, applies a targeted harness change, and re-evaluates. Common changes include prompt updates, tool definition refinements, and routing logic adjustments. The team tested this with Claude Sonnet 4.6 and Z.ai's GLM-5 on evaluation subsets. The Better-Harness loop converges in an average of 7.3 iterations. Each iteration costs approximately $0.50 in LLM API calls. The approach requires a minimum eval suite of 200 examples to avoid overfitting. Convergence is guaranteed within 20 iterations by the monotonic improvement theorem. The loop automatically generates Git commits for each harness change.",
        retrieved_contexts=ctx_json(HARNESS_RECIPE, HARNESS_EVALS, HARNESS_CHANGES),
        expected_score_range="0.4-0.7",
    ))
    stmts["F40"] = [
        "Better-Harness autonomously improves the agent harness.",
        "It uses evals as a signal.",
        "In classical ML, training data guides learning.",
        "For agents, evals serve the same purpose.",
        "Each eval contributes a signal toward harness correctness.",
        "The approach starts with hand-curated evals.",
        "It identifies the lowest-scoring dimension.",
        "It applies a targeted harness change.",
        "It re-evaluates after changes.",
        "Common changes include prompt updates and tool refinements.",
        "The team tested with Claude Sonnet 4.6 and Z.ai's GLM-5.",
        "The loop converges in an average of 7.3 iterations.",
        "Each iteration costs approximately $0.50 in API calls.",
        "A minimum eval suite of 200 examples is required to avoid overfitting.",
        "Convergence is guaranteed within 20 iterations.",
        "The loop automatically generates Git commits for each change.",
    ]

    # High, all unfaithful (5)
    rows.append(dict(
        case_id="F41", case_description="HIGH, ALL_UNFAITHFUL: entirely fabricated LLM-as-judge explanation",
        question="Explain LLM-as-a-judge comprehensively.",
        answer="LLM-as-a-judge is a distributed computing framework for training language models using federated learning across edge devices. Each device runs a local judge model that evaluates data quality before sending gradients to the central server. The framework uses homomorphic encryption to protect judge decisions during transit. Training requires a minimum of 1,000 participating devices to achieve statistical convergence. The judge models are initialized from a pre-trained BERT base and fine-tuned using contrastive learning with temperature scaling at tau=0.07. Each judge maintains a local evaluation cache using Redis with a TTL of 300 seconds. The system supports both synchronous and asynchronous federation protocols. Results are aggregated using a novel weighted averaging scheme called JudgeFed. The framework was developed at DeepMind and open-sourced under the Apache 2.0 license. It requires PyTorch 2.1 and CUDA 12.0 minimum. Deployment uses Helm charts with automatic horizontal pod autoscaling. The framework achieves 94.3% agreement with human evaluators on the JudgeBench benchmark.",
        retrieved_contexts=ctx_json(JUDGE_WHAT, JUDGE_WHY, JUDGE_TYPES, JUDGE_BIASES),
        expected_score_range="0.0",
    ))
    stmts["F41"] = [
        "LLM-as-a-judge is a distributed computing framework.",
        "It uses federated learning across edge devices.",
        "Each device runs a local judge model.",
        "The framework uses homomorphic encryption.",
        "Training requires a minimum of 1,000 participating devices.",
        "Judge models are initialized from pre-trained BERT base.",
        "Fine-tuning uses contrastive learning with temperature scaling.",
        "Each judge maintains a local Redis cache with 300s TTL.",
        "The system supports synchronous and asynchronous protocols.",
        "Results are aggregated using JudgeFed weighted averaging.",
        "The framework was developed at DeepMind.",
        "It is open-sourced under Apache 2.0.",
        "It requires PyTorch 2.1 and CUDA 12.0.",
        "Deployment uses Helm charts with autoscaling.",
        "It achieves 94.3% agreement on JudgeBench.",
    ]

    rows.append(dict(
        case_id="F42", case_description="HIGH, ALL_UNFAITHFUL: entirely fabricated continual learning",
        question="Explain continual learning for AI agents in detail.",
        answer="Continual learning for AI agents is implemented through a three-phase pipeline: data distillation, knowledge consolidation, and experience replay. In the data distillation phase, a teacher model generates synthetic training examples that capture the distribution of production failures. Knowledge consolidation uses elastic weight consolidation to prevent catastrophic forgetting when updating the student model. Experience replay maintains a buffer of 50,000 historical interactions sampled using prioritized replay with alpha=0.6. The pipeline runs on a dedicated Kubernetes cluster with auto-scaling based on replay buffer utilization. Each consolidation cycle takes approximately 4 hours on 8 A100 GPUs. The system checkpoints every 1,000 gradient steps to enable rollback. Models are validated against a held-out test set of 10,000 examples before deployment. The entire pipeline is orchestrated by Apache Airflow with custom operators for each phase. Monitoring uses Weights & Biases for experiment tracking with automatic hyperparameter sweeps using Bayesian optimization.",
        retrieved_contexts=ctx_json(CL_MODEL, CL_HARNESS, CL_CONTEXT, CL_TRACES),
        expected_score_range="0.0",
    ))
    stmts["F42"] = [
        "Continual learning uses a three-phase pipeline.",
        "The phases are data distillation, knowledge consolidation, and experience replay.",
        "A teacher model generates synthetic training examples.",
        "Knowledge consolidation uses elastic weight consolidation.",
        "It prevents catastrophic forgetting.",
        "Experience replay maintains a buffer of 50,000 interactions.",
        "Prioritized replay uses alpha=0.6.",
        "The pipeline runs on a dedicated Kubernetes cluster.",
        "Each consolidation cycle takes 4 hours on 8 A100 GPUs.",
        "The system checkpoints every 1,000 gradient steps.",
        "Models are validated on a held-out set of 10,000 examples.",
        "Apache Airflow orchestrates the pipeline.",
        "Custom operators handle each phase.",
        "Weights & Biases is used for experiment tracking.",
        "Bayesian optimization handles hyperparameter sweeps.",
    ]

    rows.append(dict(
        case_id="F43", case_description="HIGH, ALL_UNFAITHFUL: fabricated observability system",
        question="Explain agent observability comprehensively.",
        answer="Agent observability is built on a custom time-series database called TraceDB that stores execution events with nanosecond precision. Each event is tagged with a 256-bit agent fingerprint derived from the SHA-3 hash of the agent configuration. The system uses a pub-sub architecture with Apache Kafka partitioned by agent ID, achieving 99.99% event delivery with at-most-once semantics. Observability data is compressed using zstd at level 19 before storage, reducing disk usage by 95%. Query performance is optimized through a custom columnar index called AgentTree that supports sub-millisecond lookups across billions of events. The dashboard is built with Three.js for 3D visualization of agent execution graphs. Alerting uses a custom anomaly detection model trained on 6 months of historical data, achieving 97.2% precision at 89.1% recall. The system requires a minimum of 3 nodes with 64GB RAM each for production deployment. All data is encrypted at rest using AES-256-GCM with keys rotated every 24 hours.",
        retrieved_contexts=ctx_json(AOBS_WHAT, AOBS_VALUE, AOBS_DEEP, AOBS_EVAL),
        expected_score_range="0.0",
    ))
    stmts["F43"] = [
        "Agent observability uses TraceDB, a custom time-series database.",
        "Events are stored with nanosecond precision.",
        "Events are tagged with a 256-bit agent fingerprint.",
        "The fingerprint is derived from SHA-3 hash of agent configuration.",
        "A pub-sub architecture uses Apache Kafka.",
        "It achieves 99.99% event delivery.",
        "Data is compressed using zstd at level 19.",
        "Disk usage is reduced by 95%.",
        "A custom AgentTree index supports sub-millisecond lookups.",
        "It handles billions of events.",
        "The dashboard uses Three.js for 3D visualization.",
        "Anomaly detection is trained on 6 months of data.",
        "It achieves 97.2% precision at 89.1% recall.",
        "Production requires 3 nodes with 64GB RAM each.",
        "Data is encrypted with AES-256-GCM.",
        "Keys are rotated every 24 hours.",
    ]

    rows.append(dict(
        case_id="F44", case_description="HIGH, ALL_UNFAITHFUL: fabricated evaluation metrics system",
        question="Explain RAG evaluation metrics in detail.",
        answer="RAG evaluation metrics are computed using a proprietary algorithm called RAGScore that combines information retrieval theory with neural network attention patterns. The algorithm first tokenizes the retrieved context and response using a custom BPE tokenizer with a vocabulary of 128,000 tokens. It then computes a retrieval quality matrix using cosine similarity between document embeddings generated by a specialized 7B parameter model called RAGEmbed. Context precision is calculated as the ratio of relevant tokens to total tokens, weighted by their TF-IDF scores. Context recall uses a modified version of ROUGE-L that accounts for semantic similarity rather than exact lexical overlap. Faithfulness is measured by extracting knowledge triples from both the context and response using a relation extraction model, then computing the Jaccard similarity between the two triple sets. The entire evaluation pipeline runs in under 200ms per example on a single V100 GPU. Results are calibrated against a reference dataset of 50,000 human judgments collected through Amazon Mechanical Turk.",
        retrieved_contexts=ctx_json(METRICS_RAG, EVAL_RAG, EVAL_RETR_REASON),
        expected_score_range="0.0",
    ))
    stmts["F44"] = [
        "RAG metrics use a proprietary algorithm called RAGScore.",
        "It combines information retrieval theory with attention patterns.",
        "It uses a custom BPE tokenizer with 128,000 tokens.",
        "A 7B parameter model called RAGEmbed generates embeddings.",
        "Context precision is the ratio of relevant to total tokens.",
        "Tokens are weighted by TF-IDF scores.",
        "Context recall uses modified ROUGE-L with semantic similarity.",
        "Faithfulness extracts knowledge triples from context and response.",
        "It computes Jaccard similarity between triple sets.",
        "Evaluation runs in under 200ms per example.",
        "It runs on a single V100 GPU.",
        "Results are calibrated against 50,000 human judgments.",
        "Judgments were collected through Amazon Mechanical Turk.",
    ]

    rows.append(dict(
        case_id="F45", case_description="HIGH, ALL_UNFAITHFUL: fabricated Kensho case study",
        question="Describe the Kensho multi-agent framework in detail.",
        answer="Kensho built their multi-agent framework using a custom fork of AutoGen with 47 specialized agents. The lead orchestrator agent uses a GPT-5 backbone fine-tuned on 2 million S&P Global financial documents. Each worker agent maintains a private vector store with 500,000 embeddings refreshed hourly from Bloomberg Terminal data feeds. The system processes 10,000 queries per minute with an average latency of 23ms. Agents communicate using a custom binary protocol called FinComm that reduces message overhead by 80% compared to JSON. The framework uses a novel consensus algorithm where agents vote on answer candidates using quadratic voting weighted by confidence scores. Quality assurance is handled by a dedicated auditor agent that checks every response against SEC filing data. The system runs on a dedicated cluster of 128 TPU v5e chips hosted in Google Cloud's us-central1 region. Total infrastructure cost is approximately $45,000 per month.",
        retrieved_contexts=ctx_json(KENSHO_FRAMEWORK, KENSHO_CHALLENGE, KENSHO_LEARNINGS),
        expected_score_range="0.0",
    ))
    stmts["F45"] = [
        "Kensho used a custom fork of AutoGen with 47 agents.",
        "The orchestrator uses GPT-5 fine-tuned on 2 million documents.",
        "Each agent maintains a vector store with 500,000 embeddings.",
        "Embeddings are refreshed hourly from Bloomberg Terminal.",
        "The system processes 10,000 queries per minute.",
        "Average latency is 23ms.",
        "Agents communicate using a binary protocol called FinComm.",
        "FinComm reduces message overhead by 80%.",
        "Agents vote on answers using quadratic voting.",
        "Votes are weighted by confidence scores.",
        "A dedicated auditor agent checks against SEC filing data.",
        "The system runs on 128 TPU v5e chips.",
        "Infrastructure cost is $45,000 per month.",
    ]

    return rows, stmts


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("Generating datasets...")
    write_csv("answer-relevancy-test.csv", gen_answer_relevancy())
    write_csv("context-relevance-test.csv", gen_context_relevance())
    write_csv("response-groundedness-test.csv", gen_response_groundedness())
    write_csv("context-utilization-test.csv", gen_context_utilization())

    faith_rows, faith_stmts = gen_faithfulness()
    write_csv("faithfulness-test.csv", faith_rows)

    stmts_path = os.path.join(DATASETS_DIR, "faithfulness-test-statements.json")
    with open(stmts_path, "w", encoding="utf-8") as f:
        json.dump(faith_stmts, f, indent=2, ensure_ascii=False)
    print(f"  faithfulness-test-statements.json: {len(faith_stmts)} cases")

    print("\nDone. All datasets generated.")
