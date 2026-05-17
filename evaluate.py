from rag import generate_answer
import pandas as pd

test_cases = [
    {
        "question": "What is required for privileged access?",
        "expected_source": "security-policy.txt.txt"
    },
    {
        "question": "What must AI systems be evaluated for?",
        "expected_source": "ai-governance-policy.txt.txt"
    },
    {
        "question": "Who must use multi-factor authentication?",
        "expected_source": "security-policy.txt.txt"
    }
]

results = []

for test in test_cases:
    answer, docs = generate_answer(test["question"])

    retrieved_sources = [doc["source"] for doc in docs]
    passed = test["expected_source"] in retrieved_sources

    results.append({
        "question": test["question"],
        "expected_source": test["expected_source"],
        "retrieved_sources": ", ".join(retrieved_sources),
        "passed": passed,
        "answer": answer
    })

df = pd.DataFrame(results)

df.to_csv("evaluation_results.csv", index=False)

print(df)
print("\nSaved results to evaluation_results.csv")