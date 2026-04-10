import json

def generate_grading_template(rubric_dict: dict) -> str:
    """
    Generate a grading template JSON string based on rubric.
    """
    criteria = rubric_dict.get("criteria", {})
    categories = list(criteria.keys())

    levels = rubric_dict.get("levels", [])
    max_score_per_category = len(levels)
    total_max_score = len(categories) * max_score_per_category

    aligned_feedback = '    "AlignedToRubric": {\n'

    for cat in categories:
        aligned_feedback += f'      "{cat}": "Explain score based on provided rubric",\n'

    aligned_feedback = aligned_feedback.rstrip(',\n') + '\n'
    aligned_feedback += '    }'

    template = "{\n"
    for cat in categories:
        template += f'  "{cat}": "Out of {max_score_per_category}",\n'
    template += f'  "TotalScore": "total out of {total_max_score} Example: 2/10",\n'
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
    print(template)
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