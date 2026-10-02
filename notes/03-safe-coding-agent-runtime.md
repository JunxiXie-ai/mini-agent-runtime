# Mini Agent Runtime — Part 3: Safe Coding Agent Runtime

## 1. Goal of This Stage

Upgrade the Agent from basic tool calling to a safer coding workflow that can:

- inspect the workspace
- execute Python code
- observe failures
- recover from tool errors
- fix code and verify the result

The Agent now supports:

```text
Code
→ Execute
→ Observe
→ Fix
→ Verify
```

## 2. Workspace Sandbox

File tools are restricted to the `workspace/` directory.

```
WORKSPACE_ROOT = Path("workspace").resolve()
```

Every filesystem path is resolved before use:

```
target = (WORKSPACE_ROOT / path).resolve()
```

If the resolved path is outside the workspace, the operation is rejected.

```
workspace/hello.py
→ allowed

workspace/../README.md
→ resolves outside workspace
→ rejected
```

Key idea:

> Sandbox controls where the Agent is allowed to operate.

## 3. Tool Error Handling

Tool failures should not crash the entire Agent Runtime.

`ToolRegistry.execute()` catches tool exceptions:

```
try:    return tool(**arguments)except Exception as exc:    return f"Tool error: {exc}"
```

A failure such as:

```
Path escapes workspace
```

becomes an Observation:

```
Tool error: Path escapes workspace
```

The LLM can then decide what to do next.

Key idea:

> Failure is also an Observation.

## 4. Directory Inspection

A new `list_dir` tool lets the Agent inspect files and directories inside the workspace.

```
list_dir(".")
→ hello.py
→ add.py
→ tests/
```

This gives the Agent environment discovery capability before deciding which file to read or modify.

Adding this tool does not require changing `AgentLoop`.

```
AgentLoop
→ ToolRegistry
→ read_file
→ write_file
→ list_dir
→ run_python
```

This demonstrates that the tool system is extensible.

## 5. Python Execution

The `run_python` tool allows the Agent to execute Python files inside the workspace.

```
subprocess.run(    ["python", str(target)],    cwd=WORKSPACE_ROOT,    capture_output=True,    text=True,    timeout=10,)
```

Important design choices:

```
capture_output
→ capture stdout and stderr

timeout
→ prevent infinite execution

no shell=True
→ avoid unnecessary shell execution capability
```

The execution result becomes another Observation for the LLM.

## 6. System Prompt

The Agent now has a system-level coding policy.

The System Prompt tells the LLM to:

- use tools instead of pretending actions succeeded
- inspect execution errors
- fix failed code
- rerun and verify before finishing

Important distinction:

```
Tool
→ what the Agent can do

System Prompt
→ how the Agent should behave

AgentLoop
→ allows repeated decisions and actions
```

## 7. Self-Correction Loop

Self-correction is not a separate tool.

It emerges from:

```
AgentLoop
+
Tools
+
Observations
+
System Prompt
```

Example:

```
write_file
↓
run_python
↓
ZeroDivisionError
↓
Observation returned to LLM
↓
write_file again
↓
run_python again
↓
successful verification
↓
Final Answer
```

The Agent can now use real execution results to revise its own work.

## 8. Current Architecture

```
User Goal
 ↓
AgentLoop
 ↓
LLM Provider
 ↓
DeepSeek Decision
 ↓
Tool Call
 ↓
ToolRegistry
 ↓
Sandboxed Tool Execution
 ↓
Observation
 ↓
LLM Re-evaluation
 ↓
Fix / Retry / Final
```

## 9. Key Mental Model

```
LLM
= decision maker

Provider
= model adapter

AgentLoop
= control loop

ToolRegistry
= tool dispatcher

Tool
= action

Sandbox
= permission boundary

Observation
= environment feedback

System Prompt
= behavior policy
```

## 10. Current Status

The Agent can now:

- inspect files and directories
- read and write files safely
- run Python code
- capture stdout and stderr
- handle tool failures without crashing Core
- recover from execution errors
- modify code and verify fixes

The runtime is now moving from a basic tool-calling Agent toward a practical local coding Agent.