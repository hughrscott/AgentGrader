import json
from pathlib import Path

class AnswerGraderAgent:
    def __init__(self, model):
        self.model = model
        self.system_prompt = Path("prompts/system_prompt.txt").read_text()

    def format_prompt(self, input):
        return f"""
{self.system_prompt}

Question: {input["question"]}
Context: {input.get("context", "N/A")}
LLM Answer: {input["answer"]}
Reference Answer: {input.get("reference_answer", "N/A")}
"""

    def parse_response(self, output):
        try:
            return json.loads(output)
        except Exception:
            return {"error": "Could not parse output", "raw_output": output}

    def run(self, input):
        prompt = self.format_prompt(input)
        response = self.model(prompt)
        return self.parse_response(response)
