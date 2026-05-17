from rag import generate_answer

question = "Who must use multi-factor authentication?"

answer, docs = generate_answer(question)

print("QUESTION:", question)
print("\nANSWER:", answer)
print("\nSOURCES:")

for doc in docs:
    print("-", doc["source"])