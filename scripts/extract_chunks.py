"""Extract clean text chunks from annotated docx files into a JSON chunk library."""

import json
import os
import re

import docx

ANNOTATED_DIR = os.path.join(os.path.dirname(__file__), "..", "baby_langchain_annotated")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "datasets", "chunk_library.json")

TOPIC_MAP = {
    "_about_annotated.docx": "langchain_company",
    "_articles_agent-observability_annotated.docx": "agent_observability",
    "_articles_ai-observability_annotated.docx": "ai_observability",
    "_articles_langsmith-vs-langfuse_annotated.docx": "langsmith_vs_langfuse",
    "_articles_llm-as-a-judge_annotated.docx": "llm_as_judge",
    "_articles_llm-evaluation-framework_annotated.docx": "evaluation_framework",
    "_articles_llm-evaluation-metrics_annotated.docx": "evaluation_metrics",
    "_blog_agent-evaluation-readiness-checklist_annotated.docx": "evaluation_readiness",
    "_blog_agent-observability-powers-agent-evaluation_annotated.docx": "observability_evaluation",
    "_blog_agentic-engineering-redefining-software-engineering_annotated.docx": "agentic_engineering",
    "_blog_announcing-the-langchain-mongodb-partnership-the-ai-agent-stack-that-runs-on-the-database-you-already-trust_annotated.docx": "mongodb_partnership",
    "_blog_arcade-dev-tools-now-in-langsmith-fleet_annotated.docx": "arcade_fleet",
    "_blog_autonomous-context-compression_annotated.docx": "context_compression",
    "_blog_better-harness-a-recipe-for-harness-hill-climbing-with-evals_annotated.docx": "harness_hill_climbing",
    "_blog_continual-learning-for-ai-agents_annotated.docx": "continual_learning",
    "_blog_credit-genie-insights-agent-financial-assistant_annotated.docx": "credit_genie",
    "_blog_customers-kensho_annotated.docx": "kensho",
}


def clean_text(text: str) -> str:
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\*+", "", text)
    text = re.sub(r"#{1,6}\s*", "", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"<!metadata>", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_chunks_from_docx(filepath: str) -> list[str]:
    doc = docx.Document(filepath)
    raw = " ".join(p.text.strip() for p in doc.paragraphs if p.text.strip())
    sections = re.split(r"<node>", raw)
    chunks = []
    for section in sections:
        cleaned = clean_text(section)
        if len(cleaned) > 100 and not cleaned.startswith("Try LangSmith"):
            chunks.append(cleaned)
    return chunks


def main():
    files = sorted(
        f for f in os.listdir(ANNOTATED_DIR)
        if f.endswith(".docx") and not f.startswith("~")
    )

    library = []
    for fname in files:
        filepath = os.path.join(ANNOTATED_DIR, fname)
        topic = TOPIC_MAP.get(fname, "unknown")
        chunks = extract_chunks_from_docx(filepath)

        for i, chunk_text in enumerate(chunks):
            library.append({
                "id": f"{fname}:{i}",
                "text": chunk_text,
                "filename": fname,
                "topic": topic,
                "char_count": len(chunk_text),
            })

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(library, f, indent=2, ensure_ascii=False)

    print(f"Extracted {len(library)} chunks from {len(files)} files")
    print(f"Output: {OUTPUT_PATH}")

    by_topic = {}
    for c in library:
        by_topic.setdefault(c["topic"], []).append(c)
    for topic, chunks in sorted(by_topic.items()):
        print(f"  {topic}: {len(chunks)} chunks")


if __name__ == "__main__":
    main()
