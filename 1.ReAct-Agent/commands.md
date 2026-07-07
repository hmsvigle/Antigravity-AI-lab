uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
.venv/bin/python agent.py

# Or run with a question directly as a command-line argument:
.venv/bin/python agent.py "If a farmer has 150 sheep and 4 run away, then he buys 10 more, how many sheep does he have?"

.venv/bin/python agent.py "If a baker has 120 cookies and sells 50 in the morning and 30 in the afternoon, then bakes 20 more, how many does he have?"

Using model : llama3.2
Backend URL : http://localhost:11434/v1

--- Model Response ---
Thought: The baker starts with 120. He sells 50 in the morning, so we subtract 50 (120 - 50). Then, he sells 30 more in the afternoon, so we subtract that as well (120 - 50 - 30). After selling those cookies and baking new ones, we still need to add the 20 he just baked.

Action: calculate[120 - 50 - 30 + 20]
----------------------

Observation (Calculated Result): 60
Final Answer: 60