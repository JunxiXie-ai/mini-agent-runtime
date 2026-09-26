# Mini Agent Runtime — Part 1: Minimal Agent Loop

## 1. Project Goal

Build a local AI Agent Runtime from scratch to understand the core mechanics behind modern coding agents:

- Agent Loop
- LLM Provider
- Tool Calling
- Tool Registry
- Context / Observation
- Future Session, Permission, and Memory systems

The goal is not just to build a chatbot, but to understand how an Agent **decides, acts, observes, and continues**.

## 2. Architecture

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

### Module Responsibilities

- `cli.py` — receives the user goal and sends requests to Core.
- `protocol.py` — defines the JSON request/response format.
- `core/server.py` — runs the Core daemon and handles requests.
- `agent/runner.py` — entry point for one Agent run.
- `agent/loop.py` — controls the Agent decision loop.
- `llm/fake_provider.py` — simulates LLM decisions for testing.
- `tools/registry.py` — registers and executes tools.
- `read_file.py` / `write_file.py` — perform real filesystem actions.

## 3. Core Concepts

### LLM ≠ Agent

The LLM is mainly the **decision maker**.

The Agent Runtime is responsible for:

- controlling the loop
- executing tools
- maintaining context
- managing state and future permissions

### Agent Loop

```text
Goal
→ LLM Decision
→ Tool Call
→ Tool Execution
→ Observation
→ LLM Decision
→ ...
→ Final Answer
```

A simple way to remember it:

```text
Think → Act → Observe → Repeat
```

### Tool Calling

The LLM does not directly modify files.

Instead, it returns a structured request:

```python
{
    "tool_name": "write_file",
    "arguments": {
        "path": "hello.py",
        "content": "..."
    }
}
```

The Runtime then executes the actual Python function.

### Tool Registry

Instead of writing tool-specific logic inside `AgentLoop`, tools are managed in one place:

```python
self.tools.execute(
    name=tool_name,
    arguments=arguments,
)
```

This keeps the Agent loop simple and makes new tools easier to add.

### Observation

After a tool runs, its result is added back into the Agent context.

This lets the next LLM decision depend on what actually happened.

## 4. Minimal Agent Loop Completed

The first working loop was:

```text
Goal
→ Fake LLM
→ write_file
→ Tool Result
→ read_file
→ Tool Result
→ Final Answer
```

`FakeLLMProvider` used fixed logic, so it did not understand the user's goal.

Its purpose was to verify that the Agent Runtime itself worked before connecting a real model.

## 5. Mental Model

```text
CLI       = interface
Core      = execution service
AgentLoop = control logic
LLM       = decision maker
Tool      = action
```

## 6. Next Stage

- Define Tool Schemas
- Connect DeepSeek
- Implement real Tool Calling
- Add structured Tool Call history
- Add workspace sandboxing
- Add permission, session, and context management