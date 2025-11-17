# llm_client.py

from typing import Any, Dict, Iterator, List, TypedDict
from ollama import chat, ChatResponse, Message# type: ignore

import prompts
from color import Color

MODEL: str = "qwen3:8b"

class ParsedStreamResult(TypedDict):
    thinking: str
    content: str
    tool_calls: List[Message.ToolCall]

def generate_response(
    messages: List[Message],
    auto_mode: bool = False
) -> ParsedStreamResult:
    """
    Generates a response from the LLM using the provided conversation history.
    
    This function streams the LLM's response (using Ollama's `chat` API), processes
    the streaming output, and returns a structured dictionary containing:
    - The LLM's internal thinking process
    - The final response content
    - Any tool calls made by the LLM
    
    Args:
        messages: A list of `Message` objects representing the conversation history.
    
    Returns:
        A dictionary containing:
        - 'thinking': The LLM's internal reasoning process.
        - 'content': The final response content.
        - 'tool_calls': A list of tool calls made by the LLM.
    """
    if len(messages) == 0:
        messages = _build_initial_message(auto_mode)
    return _parse_stream(
        chat(
            model=MODEL,
            messages=messages,
            think=True,
            stream=True
        ),
        auto_mode=auto_mode
    )

def _build_initial_message(auto_mode: bool) -> List[Message]:
    """
    Builds the initial system message for the LLM.
    
    This function creates a system message containing the combined prompts
    (from `prompts.get_full_prompt()`) to initialize the conversation context.
    
    Args:
        prompt: A string containing the combined system prompt for the LLM.
    
    Returns:
        A list containing a single `Message` object with the system prompt.
    """
    if auto_mode:
        prompt=prompts.get_full_supervisor_prompt()
    else:
        prompt=prompts.get_full_prompt()
    msg = Message(
        role="system",
        content=prompt
    )
    return [msg]

def _parse_stream(stream: Iterator[ChatResponse], auto_mode: bool = False) -> ParsedStreamResult:
    """
    Parses the stream of LLM response chunks and extracts relevant information.
    
    This function processes each chunk in the stream to extract the thinking,
    content, and tool calls from the LLM's response, then aggregates them into
    a dictionary for further processing.
    
    Args:
        stream: An iterator that yields chunks of the LLM's response.
    
    Returns:
        A dictionary containing the extracted information, with keys:
        - 'thinking': The LLM's internal reasoning process.
        - 'content': The final response content.
        - 'tool_calls': A list of tool calls made by the LLM.
    """
    in_thinking: bool = False
    content: str = ''
    thinking: str = ''
    tool_calls: List[Message.ToolCall] = []

    if auto_mode:
        color = Color.BG_BLUE
    else:
        color = Color.BG_RED

    for chunk in stream:
        if chunk.message.thinking:
            if not in_thinking:
                in_thinking = True
                print('Thinking:\n', end='', flush=True)
            print(f"{color}{chunk.message.thinking}{Color.RESET}", end='', flush=True)
            thinking += chunk.message.thinking
        elif chunk.message.content:
            if in_thinking:
                in_thinking = False
                print('\n\nAnswer:\n', end='', flush=True)
            print(f"{color}{chunk.message.content}{Color.RESET}", end='', flush=True)
            content += chunk.message.content
        elif chunk.message.tool_calls:
            tool_calls.extend(chunk.message.tool_calls)
            print(f"{color}{chunk.message.tool_calls}{Color.RESET}")

    return {"thinking": thinking, "content": content, "tool_calls": tool_calls}
