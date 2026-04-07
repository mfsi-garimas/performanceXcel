import json

def generate_grading_template(rubric_dict: dict) -> str:
    """
    Generate a grading template JSON string based on rubric.
    """
    # Assume rubric_dict has 'criteria' dict with subcriteria levels
    categories = list(rubric_dict.get("criteria", {}).keys())

    # Use number of levels as max score per category
    first_category_levels = list(rubric_dict.get("criteria", {}).get(categories[0], {}).keys()) if categories else []
    max_score_per_category = len(first_category_levels)
    total_max_score = len(categories) * max_score_per_category

    # Build category feedback
    aligned_feedback = '    "AlignedToRubric": {\n'
    for cat in categories:
        aligned_feedback += f'      "{cat}": "Explain score based on provided rubric",\n'
    aligned_feedback = aligned_feedback.rstrip(',\n') + '\n'
    aligned_feedback += '    }'

    # Build template
    template = "{\n"
    for cat in categories:
        template += f'  "{cat}": "Out of {max_score_per_category}",\n'
    template += f'  "TotalScore": "total out of {total_max_score}",\n'
    template += '  "Percentage": "percent score",\n'
    template += '  "Grade": "letter grade (A, B, C, D, F)",\n'
    template += '  "OverallGrade": "Exceeds / Meets / Developing / Beginning",\n'
    template += '  "Feedback": {\n'
    template += f'{aligned_feedback},\n'
    template += '    "Strengths": ["list at least 2 strengths"],\n'
    template += '    "AreasForImprovement": ["list at least 2 areas"],\n'
    template += '    "SuggestionsForRevision": ["list at least 2 actionable improvements"]\n'
    template += '  }\n'
    template += '}'
    return template

def build_prompt(rubric_dict: dict, submission_text: str) -> str:
    """
    Build a prompt for the LLM using the rubric and student submission.
    """
    grading_template = generate_grading_template(rubric_dict)
    prompt = f"""
You are an assignment grader. Use the following rubric JSON to evaluate the student response below.

Rubric JSON:
{json.dumps(rubric_dict, indent=2)}

Return ONLY valid JSON in this format:

{grading_template}

Student response:
\"\"\"{submission_text}\"\"\"
"""
    return prompt