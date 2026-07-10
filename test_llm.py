from utils.llm import ask_llm

print("Testing Azure GPT-5.4...")

response = ask_llm(
    "What is Root Cause Analysis?",
    "No plant data available."
)

print("\nAI Response:\n")
print(response)