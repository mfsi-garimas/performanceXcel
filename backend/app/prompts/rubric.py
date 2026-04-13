def build_prompt(rubric_data, rubric_html):
    return f"""
You are an expert at reading and structuring rubrics from OCR text fragments.

Given this list of text fragments extracted from a rubric:

{rubric_data}

HTML structure to understand the rubric:

{rubric_html}

Task:
1. Automatically detect all rubric categories/criteria (e.g., "Restate", "Answer", "Cite", "Explain", "Conventions").
2. Detect all rubric levels (e.g., Level 4, Level 3, Level 2, Level 1) available in provided text fragments.
3. For each criterion, map the description of each level.
4. Output a **valid JSON** with the following structure:

{{
  "rubric_title": "Generated Rubric",
  "levels": ["Level 4", "Level 3", "Level 2", "Level 1"],
  "criteria": {{
    "Criterion Name": {{
      "Level 4": "...",
      "Level 3": "...",
      "Level 2": "...",
      "Level 1": "..."
    }},
    "...": {{
      "...": "..."
    }}
  }},
  "comments": ""
}}
5. Detect the name of the rubric from the text fragments and HTML structure.

Make sure the JSON is valid and includes all detected categories and level descriptions.
Return ONLY valid JSON. No extra text.
Ensure all brackets are closed.

If you cannot finish JSON, output {} only.
"""