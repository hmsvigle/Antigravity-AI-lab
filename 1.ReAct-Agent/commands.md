uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
.venv/bin/python agent.py

# Or run with a question directly as a command-line argument:
.venv/bin/python agent.py "If a farmer has 15 sheep and 4 run away, then he buys 10 more, how many sheep does he have?"
