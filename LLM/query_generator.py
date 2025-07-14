import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

client = OpenAI(
          base_url = "https://openrouter.ai/api/v1",
          api_key=api_key)

INPUT_FILE = "generated_narration_sequences.json"
OUTPUT_FILE = "generated_queries.json"

def build_prompt(narrations):
    narrs = "\n".join(narrations)
    return f"""Given the following narrations describing a person's actions, generate a simple natural language query that could be answered by watching the corresponding video segment:

{narrs}

Query:"""

with open("narrationV8.json", "r", encoding="utf-8") as f:
    for line in f:
        sequences = json.loads(line)
        for item in tqdm(sequences, desc="Generating queries"):
            prompt = build_prompt(item["clips"]["annotations"]["language_query"]["description"])

            try:
                response = client.chat.completions.create(
                    model="cognitivecomputations/dolphin3.0-r1-mistral-24b:free",
                    messages=[{"role": "user", "content": prompt}],
                )

                generated_text = response.choices[0].message.content.strip()

                item["clips"]["annotations"]["language_query"]["query"] = generated_text

            except Exception as e:
                print(f" Error: {e}")
                continue