from gpt4all import GPT4All
import json
import os
import re

MODEL_PATH = r"C:\desktop_miku\models\GPT4ALL\Llama-3.2-3B-Instruct-Q4_0.gguf"
MEMORY_FILE = r"C:\desktop_miku\memory.json"
CONTEXT_MESSAGES = 100  # How many recent messages to send to GPT4All

print("[AI] Loading GPT4All model...")
model = GPT4All(MODEL_PATH, allow_download=False)
print("[AI] Model loaded successfully!")

# 🧠 Load or initialize memory
memory = {"facts": {}, "history": []}
if os.path.exists(MEMORY_FILE):
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            memory = json.load(f)
    except json.JSONDecodeError:
        print("[AI] Warning: memory.json corrupted, starting fresh.")
        memory = {"facts": {}, "history": []}
    if "facts" not in memory:
        memory["facts"] = {}


def save_memory():
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2)

def learn_fact(prompt: str):
    """
    Detects if the user shared personal info and saves it in memory["facts"].
    """
    # Simple natural language patterns
    patterns = [
        (r"\bmy name is ([\w\s]+)", "name"),
        (r"\bi am ([\w\s]+)", "identity"),
        (r"\bi like ([\w\s]+)", "likes"),
        (r"\bmy hobby is ([\w\s]+)", "hobby"),
        (r"\bi enjoy ([\w\s]+)", "hobby"),
    ]
    for pattern, key in patterns:
        match = re.search(pattern, prompt, re.IGNORECASE)
        if match:
            memory["facts"][key] = match.group(1).strip().rstrip(".")
            save_memory()
            return f"Got it! I’ll remember that your {key} is {match.group(1).strip()}."

    return None

def ask(prompt, max_tokens=80):
    # Check if it’s a fact update
    learned = learn_fact(prompt)
    if learned:
        return learned  # Respond right away if fact detected

    # Build memory context
    facts_context = ""
    if memory.get("facts"):
        facts = [f"{k}: {v}" for k, v in memory["facts"].items()]
        facts_context = "Here are things I know about you:\n" + "\n".join(facts) + "\n"

    # Include recent chat history
    memory["history"].append(f"User: {prompt}")
    history_context = "\n".join(memory["history"][-CONTEXT_MESSAGES:])

    # Full prompt for the AI
    full_prompt = f"{facts_context}\n{history_context}\nMiku (reply warmly and briefly):"

    response = model.generate(full_prompt, max_tokens=max_tokens)
    response = response.split("\n")[0]  # Keep responses short and neat

    # Save chat
    memory["history"].append(f"Miku: {response}")
    save_memory()

    return response
