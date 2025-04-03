"""
Finish tool for completing tasks
"""

from crewai.tools import tool

@tool("finish")
def finish(answer:str) -> str:
    """Finish the task and give your final answer.
    
    Args:
        answer: Your answer for the task
    """
    return answer