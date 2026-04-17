from langgraph.graph import StateGraph, END
from app.graph.state import EvalState
from app.graph.nodes import (
    ocr_node,
    merge_input_node,
    grading_node,
    evaluation_node,
    load_rubric_node
)

def should_evaluate(state: dict):
    if state.get("submission_images"):
        return "evaluate"
    return "end"

def entry_router(state: dict):
    return "load_rubric" if state.get("rubric_id") else "ocr"

def router_node(state):
    return state

def build_graph():
    workflow = StateGraph(EvalState)

    workflow.add_node("ocr", ocr_node)
    workflow.add_node("merge", merge_input_node)
    workflow.add_node("grade", grading_node)
    workflow.add_node("evaluate", evaluation_node)
    workflow.add_node("load_rubric", load_rubric_node)
    workflow.add_node("router", router_node)

    workflow.set_entry_point("router")

    workflow.add_conditional_edges(
        "router",
        entry_router,
        {
            "load_rubric": "load_rubric",
            "ocr": "ocr"
        }
    )
    workflow.add_edge("load_rubric", "ocr")
    workflow.add_edge("ocr", "merge")
    workflow.add_edge("merge", "grade")

    workflow.add_conditional_edges(
        "grade",
        should_evaluate,
        {
            "evaluate": "evaluate",
            "end": END
        }
    )
    workflow.add_edge("evaluate", END)

    return workflow.compile()