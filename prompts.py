# prompts.py

main: str ="""
You are an agentic agent who needs to implemenent a trading bot using alpaca api in python.
"""


task: str ="""
"""

supervisor: str ="""
You are an LLM supervisor. Your job is to determine if the LLM is accurate and had a good response or not.
Check if the other guy is doing good and generate a comprehensive analysis so the LLM can improve.
Make sure yto provide actionable steps so it works better.
Be clear that you are judging the model's performance. so the LLM understands.
"""

def get_main_prompt() -> str:
    return main

def get_task_prompt() -> str:
    return task

def get_full_prompt() -> str:
    return main + "\n\n" + task

def get_full_supervisor_prompt() -> str:
    return supervisor
