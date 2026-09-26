# Mini Agent Runtime — Part 2: Real LLM & Tool Calling

## 1. Goal of This Stage

Upgrade the runtime from a fixed `FakeLLMProvider` to a real LLM-driven Agent.

The key change is:

```text
Before:
Goal → Fake LLM → fixed tools

Now:
Goal → DeepSeek → choose tool → execute tool → observe result → continue
```

The user goal now actually affects the Agent's behavior.

## 2. Tool Schema

A real LLM must know:

- what tools exist
- what each tool does
- what arguments each tool expects

Each tool now has both:

```text
Tool Schema   → shown to the LLM
Tool Function → executed by the Runtime
```

Example:

```python
Tool(
    name="read_file",
    description="Read text content from a file.",
    parameters={
        "type": "object",
        "properties": {
            "path": {"type": "string"}
        },
        "required": ["path"],
    },
)
```

`Tool.to_openai_schema()` converts the internal representation into the OpenAI-compatible format used by DeepSeek.

## 3. Tool Registry Upgrade

`ToolRegistry` now stores both functions and schemas:

```text
tools   → executable Python functions
schemas → descriptions sent to the LLM
```

Important interfaces:

```python
execute(name, arguments)
```

executes a real tool.

```python
get_openai_schemas()
```

returns tool definitions that can be sent to DeepSeek.

This keeps internal Runtime design separate from external LLM API format.

## 4. DeepSeek Provider

`DeepSeekProvider` replaced the fake provider.

The Agent now sends:

```text
messages + tool schemas
```

to DeepSeek.

DeepSeek can return either:

```text
final answer
```

or:

```text
tool call
```

When a tool call is returned, the provider extracts:

```text
tool_call_id
tool_name
arguments
```

The `arguments` field arrives as JSON text and is parsed into a Python dictionary before execution.

## 5. Real Tool Selection

The Agent can now choose tools based on the goal.

Example:

```text
Goal:
Read README.md and summarize it.
```

Flow:

```text
DeepSeek
→ read_file
→ Runtime reads README.md
→ tool result returned
→ DeepSeek summarizes content
→ Final Answer
```

Another example:

```text
Goal:
Create test_agent.py that prints Hello Agent.
```

Flow:

```text
DeepSeek
→ write_file
→ Runtime creates the file
→ tool result returned
→ DeepSeek confirms completion
```

This is the first point where the project becomes a real LLM-driven Agent rather than a fixed simulation.

## 6. Standard Tool Call History

The earlier Fake Provider used simplified history:

```text
assistant: "tool_call: read_file"
user: "tool_result: ..."
```

For real Tool Calling, the history must be structured.

### Assistant Tool Call

```python
{
    "role": "assistant",
    "content": None,
    "tool_calls": [
        {
            "id": tool_call_id,
            "type": "function",
            "function": {
                "name": tool_name,
                "arguments": json.dumps(arguments),
            },
        }
    ],
}
```

### Tool Result

```python
{
    "role": "tool",
    "tool_call_id": tool_call_id,
    "content": tool_result,
}
```

### Why `tool_call_id` Matters

`tool_call_id` links one tool request to its corresponding result.

```text
call_123 → read_file("README.md")
             ↓
tool result with call_123
```

This becomes essential when an Agent performs multiple tool calls.

The important idea is:

> Tool history is not plain text logging. It is structured state that preserves the relationship between actions and observations.

## 7. Current Agent Flow

The runtime now supports:

```text
User Goal
 ↓
CLI
 ↓
Core
 ↓
AgentLoop
 ↓
DeepSeek + Tool Schemas
 ↓
Tool Call
 ↓
ToolRegistry
 ↓
Tool Execution
 ↓
Structured Tool Result
 ↓
DeepSeek
 ↓
Final Answer
```

## 8. What Was Learned

The most important ideas from this stage:

- A real LLM needs Tool Schemas before it can use tools.
- The LLM proposes actions; the Runtime executes them.
- Tool calls and tool results must be represented as structured messages.
- `tool_call_id` connects an action with its observation.
- The Agent loop stays mostly unchanged even when replacing a fake provider with a real model.
- Separating Provider, Tool Registry, and AgentLoop makes the system easier to extend.

## 9. Current Status

Completed:

- Tool Schema
- OpenAI-compatible schema conversion
- DeepSeek Provider
- Real tool selection
- `read_file`
- `write_file`
- Structured Tool Call history
- Multi-step decision → action → observation → final-answer loop

## 10. Next Stage

Next engineering improvements:

- Workspace sandbox
- Safer filesystem access
- Permission control
- Better error handling
- Session / context management
- More tools