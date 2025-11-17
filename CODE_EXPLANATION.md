**Chat Application with LLM Integration Summary**

This project implements a chat application that interacts with a large language model (LLM) using the Ollama library. Here's a breakdown of the code structure and functionality:

---

### **Core Components**
1. **Prompt Management (`prompts.py`)**  
   - Defines system prompts for the LLM (`main` and `task`)  
   - Provides utility functions to retrieve individual or combined prompts  
   - Used to initialize the conversation context

2. **Main Application Logic (`main.py`)**  
   - **`main_loop()`**:  
     - Runs the chat application in a continuous loop  
     - Displays iteration count and processes user input  
     - Generates LLM responses using `llm_client.generate_response()`  
     - Maintains conversation history with `Message` objects  
   - **`append_result()`**:  
     - Adds LLM responses (content, thinking process, tool calls) to the conversation history  
     - Handles formatting and appending of assistant messages  
   - **`append_user_message()`**:  
     - Processes user input and appends it to the conversation  
     - Supports quitting the chat with the 'q' command  

3. **LLM Client Integration (`llm_client.py`)**  
   - **`generate_response()`**:  
     - Streams responses from the LLM (using Ollama's `chat` API)  
     - Initializes with a system message containing the prompts  
   - **`_parse_stream()`**:  
     - Processes streaming responses from the LLM  
     - Extracts thinking process, content, and tool calls  
     - Displays real-time output as the LLM generates responses  
   - **`_build_initial_message()`**:  
     - Creates the initial system message with combined prompts  

---

### **Key Features**
- **Streaming LLM Responses**:  
  The application supports real-time streaming of LLM outputs, including the model's thinking process and final answer.
- **Conversation History**:  
  Maintains a history of `Message` objects (user, assistant, tool) for context in subsequent interactions.
- **Tool Call Support**:  
  Handles tool calls made by the LLM, though actual tool execution is stubbed with placeholder responses.
- **Modular Architecture**:  
  Separates concerns into distinct modules for prompts, main logic, and LLM client integration.

---

### **Technical Details**
- **LLM Model**: Uses the `qwen3:8b` model from Ollama  
- **Message Format**:  
  - `Message` objects have `role` (user/assistant/tool), `content`, `thinking`, and `tool_calls` fields  
- **Streaming Output**:  
  Displays LLM's intermediate thinking and final answer as they are generated  
- **Input Handling**:  
  Continuously accepts user input until 'q' is entered to quit  

---

### **Workflow Overview**
1. Initialize with system prompts in the conversation history  
2. Loop:  
   - Generate LLM response (thinking + content + tool calls)  
   - Append response to conversation history  
   - Accept user input and append to history  
   - Repeat until user quits