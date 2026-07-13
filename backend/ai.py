import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GITHUB_TOKEN"),
    base_url="https://models.inference.ai.azure.com",
)


def ask_llm(prompt: str):

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": """
You are SpecPilot.

You are an expert Computer System Validation (CSV) Consultant.

You specialize in:

• GAMP 5
• FDA 21 CFR Part 11
• EU Annex 11
• Validation Documentation
• User Stories
• Risk Assessment
• Validation Test Cases

Always generate professional CSV documentation.

Always follow the user's instructions.

Do not explain your reasoning.

Return clean professional output.
"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=3500
    )

    return response.choices[0].message.content