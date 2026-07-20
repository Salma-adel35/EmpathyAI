from rag import retrieve_relevant_context


query = "I feel very stressed about my exam."


results = retrieve_relevant_context(
    query=query,
    top_k=3
)


print("Query:")
print(query)


print("\nRetrieved Context:\n")


for i, result in enumerate(results, start=1):

    print(f"Result {i}")
    print("Score:", result["score"])
    print("Text:", result["text"])
    print("-" * 50)