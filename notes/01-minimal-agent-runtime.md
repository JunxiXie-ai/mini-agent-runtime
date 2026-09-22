```
# Mini Agent Runtime — Part 1: Minimal Agent Loop

## 1. Project Goal

Build a local AI Agent Runtime from scratch to understand the core ideas behind:

- Agent Loop
- LLM Provider
- Tool Calling
- Tool Registry
- Context / Observation
- Future Permission, Session, and Memory systems

The goal is not just to build a chatbot, but to understand how an Agent decides actions, executes tools, observes results, and continues reasoning.

## 2. Current Architecture

```text
User
 ↓
CLI
 ↓
Protocol
 ↓
Core Daemon
 ↓
AgentRunner
 ↓
AgentLoop
 ↓
LLM Provider
 ↓
Tool Registry
 ↓
Tools
```



## 3. Module Responsibilities

- `cli.py`
   Receives the user goal and sends requests to the Core.
- `protocol.py`
   Defines the JSON message format between CLI and Core.
- `core/server.py`
   Runs the Core daemon and handles incoming requests.
- `agent/runner.py`
   Entry point for one Agent run.
- `agent/loop.py`
   Controls the main Agent decision loop.
- `llm/fake_provider.py`
   Simulates LLM decisions before connecting a real model.
- `tools/registry.py`
   Registers and executes available tools.
- `tools/write_file.py` / `read_file.py`
   Perform actual filesystem operations.

## 4. Core Concepts

### LLM is not the Agent

The LLM only decides what should happen next.

The Agent Runtime is responsible for:

- controlling the loop
- executing tools
- managing context
- handling state and permissions

### Agent Loop

```
Goal
→ LLM Decision
→ Tool Call
→ Tool Execution
→ Observation
→ LLM Decision
→ ...
→ Final Answer
```

### Tool Calling

The LLM does not directly modify files.

Instead, it returns structured data such as:

```
{
    "tool_name": "write_file",
    "arguments": {
        "path": "hello.py",
        "content": "..."
    }
}
```

The Runtime then executes the actual Python tool.

### Tool Registry

Instead of putting tool-specific logic inside `AgentLoop`, tools are registered in one place.

```
self.tools.execute(
    name=tool_name,
    arguments=arguments,
)
```

This makes it easier to add more tools later.

### Observation

After a tool runs, its result is added back into the Agent context.

This allows the next LLM decision to depend on what actually happened.

## 5. Current Progress

The following loop is working:

```
Goal
→ Fake LLM
→ write_file
→ Tool Result
→ read_file
→ Tool Result
→ Final Answer
```

The current `FakeLLMProvider` uses fixed logic, so it does not actually understand the user goal yet.

Its purpose is to verify that the Agent Runtime architecture works correctly before introducing a real LLM.

## 6. Next Steps

- Define Tool Schemas
- Add DeepSeek Provider
- Implement real Tool Calling
- Add workspace sandboxing
- Add permission control
- Add session and context management