# main.py

from typing import List
from ollama import Message
import prompts

import llm_client
from color import Color

def main_loop() -> None:
    running: bool = True
    iteration: int = 0
    msgs: List[Message] = []

    inp: str = input("Use autonomous mode? [Y/n]: ").strip().lower()
    auto_mode: bool = not inp or inp[0] == 'y'

    while running:
        print(f"\n=-=-=-=-=\n{Color.BG_GREEN}iteration:{Color.RESET} {iteration}\n=-=-=-=-=-\n")

        # generate LLM output based on the current conversation
        result = llm_client.generate_response(messages=msgs)

        # append the result to the conversation
        append_result(result, msgs)

        if auto_mode:
            # Build a fresh, compact supervisor context and get its feedback
            supervisor_messages = build_supervisor_messages(msgs, iteration)
            input()
            supervisor_result = llm_client.generate_response(
                messages=supervisor_messages,
                auto_mode=True,
            )

            # Feed supervisor feedback back into the main agent as a "user" message
            append_auto_message(supervisor_result, msgs)
        else:
            # let the user prompt the LLM or terminate the chat
            running = append_user_message(msgs)

        iteration += 1

def append_result(results: llm_client.ParsedStreamResult, msgs: List[Message]) -> None:
    """
    Appends the LLM's response to the conversation history.
    
    Processes the thinking, content, and tool calls from the LLM response
    and creates corresponding msgs for the conversation history.
    
    Args:
        results: Dictionary containing the LLM's response components
        msgs: List of Message objects representing the conversation history
    
    Returns:
        None
    """
    thinking: str = results["thinking"]
    content: str = results["content"]
    tool_calls: List[Message.ToolCall] = results["tool_calls"]

    if thinking or content or tool_calls:
        assistant_msg = Message(
            role="assistant",
            thinking=thinking or None,
            content=content or None,
            tool_calls=tool_calls or None
        )
        msgs.append(assistant_msg)

    for call in tool_calls:

        result = "Not implemented."
        tool_msg = Message(
            role="tool",
            tool_name=call.function.name,
            content=result
        )
        msgs.append(tool_msg)

def append_user_message(msgs: List[Message]) -> bool:
    """
    Processes user input and appends it to the conversation history.
    """
    raw = input("\n\nEnter a message or 'q' to quit: ").strip()
    running = not raw.lower().startswith("q")
    msgs.append(
        Message(
            role="user",
            content=raw if raw else "You are an autonomous agent. Please decide how to proceed and continue."
        )
    )
    return running

def append_auto_message(result: llm_client.ParsedStreamResult, msgs: List[Message]) -> None:
    msgs.append(
        Message(
            role="user",
            content=result["content"]
        )
    )

def _last_message_with_role(msgs: List[Message], role: str):
    """
    Return the last message in `msgs` with the given role, or None.
    """
    for msg in reversed(msgs):
        if msg.role == role:
            return msg
    return None

def build_supervisor_messages(msgs: List[Message], iteration: int) -> List[Message]:
    """
    Build a compact, high-signal context for the supervisor.

    It includes:
    - The high-level trading-bot task
    - The last 'user' message
    - The last 'assistant' message (thinking + content)
    """
    system_msg = Message(
        role="system",
        content=prompts.get_full_supervisor_prompt()
    )

    last_user = _last_message_with_role(msgs, "user")
    last_assistant = _last_message_with_role(msgs, "assistant")

    parts: List[str] = [
        f"You are evaluating iteration {iteration} of an autonomous agent that is "
        f"building a Python trading bot using the Alpaca API.\n",
        "High-level task for the agent:\n",
        (prompts.get_full_prompt().strip() or "(no extra task description provided)"),
    ]

    if last_user is not None:
        parts += [
            "\n\nLatest user message the agent responded to:\n",
            last_user.content or "(empty message)",
        ]

    if last_assistant is not None:
        if getattr(last_assistant, "thinking", None):
            parts += [
                "\n\nAgent internal thinking (may be partial):\n",
                last_assistant.thinking,
            ]
        if last_assistant.content:
            parts += [
                "\n\nAgent final answer to critique:\n",
                last_assistant.content,
            ]

    parts += [
        "\n\nNow perform your supervisor role from the system prompt: "
        "judge the LAST answer only, point out concrete issues, and give numbered "
        "actionable suggestions for the agent's next step."
    ]

    user_msg = Message(
        role="user",
        content="".join(parts)
    )

    return [system_msg, user_msg]

if __name__ == "__main__":
    main_loop()
