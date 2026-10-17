# Framework-Specific Configurations

## Claude Code

```json
{
  "permissions": {
    "allow": [
      "Read(**)",
      "Edit(**)",
      "Bash(git *)",
      "Bash(npm test)",
      "Bash(npm run build)"
    ],
    "deny": [
      "Bash(curl *)",
      "Bash(wget *)",
      "Bash(rm -rf *)",
      "Bash(chmod *)",
      "Bash(* > /etc/*)"
    ]
  },
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/workspace"],
      "env": {}
    }
  }
}
```

## Cursor

Cursor's agent sandbox and terminal allowlist are configured in two files, `sandbox.json` and `permissions.json`, rather than in the editor's `settings.json`. Each file can sit in `~/.cursor/` (every workspace) or in `.cursor/` at the workspace root (that workspace only). The keys below follow Cursor's [sandbox reference](https://cursor.com/docs/reference/sandbox) and [permissions reference](https://cursor.com/docs/reference/permissions) as of October 2026. Longer versions of both files are in [`examples/cursor-sandbox.json`](../examples/cursor-sandbox.json) and [`examples/cursor-permissions.json`](../examples/cursor-permissions.json).

`.cursor/sandbox.json` controls what sandboxed terminal commands can read, write and reach on the network:

```json
{
  "type": "workspace_readwrite",
  "readBoundary": "workspace",
  "networkPolicy": {
    "default": "deny",
    "allow": ["registry.npmjs.org"]
  }
}
```

- `type`: `workspace_readwrite` gives read/write access in the workspace, `workspace_readonly` restricts it to read-only, and `insecure_none` disables the sandbox. `additionalReadonlyPaths` lists extra paths the agent can read; `additionalReadwritePaths` lists extra paths it can read and write, and applies only with `workspace_readwrite`.
- `readBoundary`: `workspace` asks before the agent reads files outside the workspace and limits what sandboxed commands can read. It requires Cursor 3.23 or later; the default is `system`.
- `networkPolicy`: `default` applies when no rule matches. `allow` and `deny` take exact domains, wildcards such as `*.example.com`, or CIDR ranges, and a host that matches `deny` is blocked even if it also matches `allow`.
- `disableTmpWrite`: set it to `true` to remove the default write access to `/tmp` and the system temp directories.

`.cursor/permissions.json` lists the terminal commands the agent can run without asking for approval:

```json
{
  "terminalAllowlist": [
    "git status",
    "git diff",
    "npm test",
    "npm run lint"
  ]
}
```

Entries match by case-sensitive prefix, so `git status` also matches `git status --short`. A `terminalAllowlist` in this file replaces the allowlist set in the app under Settings > Agents > Approvals & Execution, and Cursor applies the file only when a Run Mode is enabled. Cursor's documentation states that allowlists "are not a security guarantee", so use the allowlist together with the sandbox file, not in place of it. The Cursor CLI has its own permissions system.

Controls that Cursor does not document a setting for:

- **Command deny patterns** (for example blocking `rm -rf` or `curl ... | bash`): Cursor's permissions reference defines no command deny list. `autoRun.block_instructions` in `permissions.json` gives guidance to the Auto-review classifier and is steering, not enforcement. Keep `terminalAllowlist` narrow instead.
- **Limiting writes to one directory** such as `./src/`: the sandbox reference has no key that narrows writes below the whole workspace.
- **Blocking secret files**: `.cursorignore` (gitignore syntax) blocks Agent, Tab, Inline Edit and @-mention access to matching files, but Cursor's documentation states that the terminal and MCP tools used by Agent cannot block access to them. Keep credentials out of the workspace.

## LangChain

```python
from langchain.agents import AgentExecutor
from langchain.tools import StructuredTool

# Define tools with explicit input validation
def search_docs(query: str) -> str:
    """Search documentation. Query must be under 200 characters."""
    if len(query) > 200:
        raise ValueError("Query too long")
    if any(c in query for c in [';', '|', '`', '$']):
        raise ValueError("Invalid characters in query")
    # ... actual search logic
    return results

search_tool = StructuredTool.from_function(
    func=search_docs,
    name="search_docs",
    description="Search project documentation",
)

# Configure agent with safety limits
agent_executor = AgentExecutor(
    agent=agent,
    tools=[search_tool],
    max_iterations=10,           # prevent infinite loops
    max_execution_time=60,       # timeout in seconds
    handle_parsing_errors=True,  # graceful error handling
    return_intermediate_steps=True,  # for audit logging
)
```
