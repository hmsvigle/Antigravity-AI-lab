import os
import re
from dotenv import load_dotenv
import ollama

# 1. Load env variables from .env file
load_dotenv()

MODEL = os.getenv("OLLAMA_MODEL")
if not MODEL:
    raise ValueError("OLLAMA_MODEL is not defined in the environment or .env file.")

BASE_URL = os.getenv("OLLAMA_BASE_URL")
client = ollama.Client(host=BASE_URL)

# 2. Basic math calculator tool
def calculate(expression: str):
    # Basic math execution using eval
    return eval(expression)

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
    
    # Call Ollama once
    try:
        response = client.chat(
            model=MODEL,
            messages=messages
        )
        text = response['message']['content'].strip()
    except Exception as e:
        print(f"Error calling Ollama: {e}")
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
