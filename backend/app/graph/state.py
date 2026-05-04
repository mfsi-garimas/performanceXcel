from typing import TypedDict, Optional, Dict, Any, List

class EvalState(TypedDict):
    rubric_text: Optional[str]
    rubric_html: Optional[str]
    submission_text: Optional[str]

    rubric_file: Optional[str]
    submission_file: Optional[str]

    rubric_id: Optional[int]

    evaluation_id: Optional[int]

    rubric_images: Optional[List[str]]
    submission_images: Optional[List[str]]

    rubric_tokens: Optional[list]
    rubric_json: Optional[Dict[str, Any]]

    llm_output: Optional[Dict[str, Any]]
    final_output: Optional[Dict[str, Any]]

    events: Optional[List[str]]