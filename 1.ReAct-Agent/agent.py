import os
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

# 3. Simple ReAct Prompt
SYSTEM_PROMPT = """You solve math word problems using ReAct.
For each step, you must output either:
Thought: <your thought>
Action: calculate[<math expression>]

When you get the observation, you do the next step.
Once you have the answer, output:
Thought: I have the final answer.
Answer: <final answer>

Example:
Question: What is 2 plus 2?
Thought: I need to calculate 2 + 2.
Action: calculate[2+2]
Observation: 4
Thought: I have the final answer.
Answer: 4
"""

def run_agent(question: str):
    # Build initial prompt text
    prompt = f"{SYSTEM_PROMPT}\nQuestion: {question}\n"
    
    print(f"Starting agent for question: {question}\n")
    
    # Run a simple loop for up to 5 steps
    for turn in range(1, 6):
        print(f"--- Turn {turn} ---")
        
        # Call Ollama locally using raw completion
        response = client.generate(
            model=MODEL,
            prompt=prompt,
            options={"stop": ["Observation:"]}
        )
        text = response['response'].strip()
        
        # Truncate text after the first action to prevent generating multiple steps at once
        action_idx = text.find("Action: calculate[")
        if action_idx != -1:
            end_idx = text.find("]", action_idx)
            if end_idx != -1:
                text = text[:end_idx + 1]
                
        print(text)
        
        # Append assistant's response to the prompt
        prompt += text + "\n"
        
        # Check if model wants to calculate something
        if "Action: calculate[" in text:
            # Parse the expression between calculate[ and ]
            start_idx = text.find("Action: calculate[") + len("Action: calculate[")
            end_idx = text.find("]", start_idx)
            expression = text[start_idx:end_idx]
            
            # Execute calculation
            result = calculate(expression)
            print(f"Observation: {result}\n")
            
            # Append observation to the prompt
            prompt += f"Observation: {result}\n"
        elif "Answer:" in text:
            print("\nFinal Answer reached!")
            break

if __name__ == "__main__":
    run_agent("If a farmer has 15 sheep and 4 run away, then he buys 10 more, how many sheep does he have?")
