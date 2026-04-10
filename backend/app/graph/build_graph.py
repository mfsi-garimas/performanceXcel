from langgraph.graph import StateGraph, END
from app.graph.state import EvalState
from app.graph.nodes import (
    ocr_node,
    merge_input_node,
    grading_node,
    evaluation_node
)

def build_graph():
    workflow = StateGraph(EvalState)

    workflow.add_node("ocr", ocr_node)
    workflow.add_node("merge", merge_input_node)
    workflow.add_node("grade", grading_node)
    workflow.add_node("evaluate", evaluation_node)

    workflow.set_entry_point("ocr")

    workflow.add_edge("ocr", "merge")
    workflow.add_edge("merge", "grade")
    workflow.add_edge("grade", "evaluate")
    workflow.add_edge("evaluate", END)

    return workflow.compile()