from typing import TypedDict, Optional, Dict, Any, List

class EvalState(TypedDict):
    rubric_text: Optional[str]
    submission_text: Optional[str]

    rubric_file: Optional[str]
    submission_file: Optional[str]

    rubric_images: Optional[List[str]]
    submission_images: Optional[List[str]]

    rubric_tokens: Optional[list]
    rubric_json: Optional[Dict[str, Any]]

    llm_output: Optional[Dict[str, Any]]
    final_output: Optional[Dict[str, Any]]