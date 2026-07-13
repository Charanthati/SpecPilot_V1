import json

from backend.ai import ask_llm


def generate_csv_documentation(document_text, user_prompt):

    prompt = f"""
You are a Senior CSV Consultant.

Return ONLY valid JSON.

NO markdown.

NO explanation.

NO text.

Return exactly this structure.

{{
"project_name":"",
"user_stories":[],
"risk_assessment":[],
"test_cases":[]
}}

Uploaded Module

{document_text}

User Request

{user_prompt}

Generate

1.User Stories

2.Risk Assessment

3.Validation Test Cases

Professional CSV language.

Return JSON ONLY.
"""

    answer = ask_llm(prompt)

    print("========== RAW ANSWER ==========")
    print(answer)


    answer = answer.replace("```json", "")
    answer = answer.replace("```", "")

    print("========== CLEAN ANSWER ==========")
    print(answer)

    try:
        data = json.loads(answer)
        print("========== JSON TYPE ==========")
        print(type(data))
        return data

    except Exception as e:
        print("JSON ERROR:", e)
        print(answer)
        raise
