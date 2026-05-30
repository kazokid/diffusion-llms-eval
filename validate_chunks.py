import json
import csv
import sys

csv.field_size_limit(sys.maxsize)

CHUNK_LIBRARY = "datasets/final_datasets/chunk_library.json"
CSV_FILES = [
    "datasets/final_datasets/context-relevance-test.csv",
    "datasets/final_datasets/faithfulness-test.csv",
    "datasets/final_datasets/answer-relevancy-test.csv",
    "datasets/final_datasets/context-utilization-test.csv",
    "datasets/final_datasets/response-groundedness-test.csv",
]

with open(CHUNK_LIBRARY) as f:
    chunks = json.load(f)

chunk_texts = set(c["text"] for c in chunks)
print(f"Chunk library: {len(chunks)} chunks\n")

total_contexts = 0
matched = 0
mismatched = 0
errors = []

for path in CSV_FILES:
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        file_total = 0
        file_matched = 0
        file_mismatched = 0
        for row in reader:
            case_id = row["case_id"]
            try:
                contexts = json.loads(row["retrieved_contexts"])
            except json.JSONDecodeError as e:
                errors.append(f"{path} {case_id}: JSON parse error: {e}")
                continue

            for i, ctx in enumerate(contexts):
                text = ctx.get("text", "")
                file_total += 1
                total_contexts += 1
                if text in chunk_texts:
                    file_matched += 1
                    matched += 1
                else:
                    file_mismatched += 1
                    mismatched += 1
                    snippet = text[:80].replace("\n", " ")
                    ctx_file = ctx.get("filename", "unknown")
                    errors.append(
                        f"{path} | {case_id} chunk[{i}] | file={ctx_file} | "
                        f'NOT FOUND | starts with: "{snippet}..."'
                    )

        status = "ALL MATCH" if file_mismatched == 0 else f"{file_mismatched} MISSING"
        print(
            f"{path}: {file_total} chunks, "
            f"{file_matched} matched, {file_mismatched} missing -> {status}"
        )

print(f"\n--- SUMMARY ---")
print(f"Total chunks checked: {total_contexts}")
print(f"Matched in library:   {matched}")
print(f"Not found:            {mismatched}")

if errors:
    print(f"\n--- ISSUES ({len(errors)}) ---")
    for e in errors:
        print(f"  {e}")
else:
    print("\nAll retrieved contexts are present in chunk_library.json!")
