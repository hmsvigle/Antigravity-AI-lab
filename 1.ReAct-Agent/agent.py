import os
import re
from openai import OpenAI
from dotenv import load_dotenv

# 1. Load env variables from .env file
load_dotenv()

# ---------------------------------------------------------------------------
# Generic LLM client configuration
# ---------------------------------------------------------------------------
# These env vars work with ANY OpenAI-compatible backend:
#   - Ollama    → LLM_BASE_URL=http://localhost:11434/v1, LLM_API_KEY=ollama
#   - OpenAI    → LLM_BASE_URL=https://api.openai.com/v1, LLM_API_KEY=sk-...
#   - Groq      → LLM_BASE_URL=https://api.groq.com/openai/v1, LLM_API_KEY=gsk_...
#   - Together  → LLM_BASE_URL=https://api.together.xyz/v1, LLM_API_KEY=...
#   - LM Studio → LLM_BASE_URL=http://localhost:1234/v1, LLM_API_KEY=lm-studio
# ---------------------------------------------------------------------------

MODEL = os.getenv("LLM_MODEL")
if not MODEL:
    raise ValueError("LLM_MODEL is not defined in the environment or .env file.")

BASE_URL = os.getenv("LLM_BASE_URL", "http://localhost:11434/v1")
API_KEY = os.getenv("LLM_API_KEY", "ollama")  # Many local servers accept any non-empty key

client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY,
)

# 2. Basic math calculator tool
def calculate(expression: str):
    """Safely evaluate a mathematical expression."""
    return eval(expression)  # noqa: S307

# 3. Prompt instructing the model to generate the calculation in 1 turn
SYSTEM_PROMPT = """You solve math word problems by translating them into a single mathematical expression.
Output your reasoning and the mathematical expression using the following format:

Thought: <your step-by-step reasoning>
Action: calculate[<mathematical expression>]

Example:
Question: If a farmer has 15 sheep and 4 run away, then he buys 10 more, how many sheep does he have?
Thought: The farmer starts with 15. 4 run away means we subtract 4 (15 - 4). Then he buys 10 more, so we add 10 (15 - 4 + 10).
Action: calculate[15 - 4 + 10]
"""

def run_agent(question: str):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Question: {question}"}
    ]

    print(f"Starting agent for question: {question}\n")
    print(f"Using model : {MODEL}")
    print(f"Backend URL : {BASE_URL}\n")

    # Call LLM via generic OpenAI-compatible client
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
        )
        text = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error calling LLM: {e}")
        return

    print("--- Model Response ---")
    print(text)
    print("----------------------\n")

    # Parse the calculation expression
    action_match = re.search(r'Action:\s*calculate\s*[\[\(](.*?)[\]\)]', text, re.IGNORECASE)

    if action_match:
        expression = action_match.group(1)
        result = calculate(expression)
        print(f"Observation (Calculated Result): {result}")
        print(f"Final Answer: {result}")
    else:
        print("Could not find a valid calculate Action in the model response.")

if __name__ == "__main__":
    import sys

    # Check if a question was passed as command line arguments
    if len(sys.argv) > 1:
        question_arg = " ".join(sys.argv[1:])
    else:
        # Prompt user dynamically for the math problem
        question_arg = input("Enter your math word problem: ").strip()

    if question_arg:
        run_agent(question_arg)
    else:
        print("No question provided. Exiting.")
