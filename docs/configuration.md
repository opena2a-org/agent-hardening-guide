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

```json
{
  "cursor.ai.security": {
    "sandboxMode": "strict",
    "allowedCommands": [
      "git status",
      "git diff",
      "npm test",
      "npm run lint"
    ],
    "blockedPatterns": [
      "rm -rf",
      "curl.*|.*bash",
      "eval(",
      "exec("
    ],
    "fileAccessScope": "./src/**",
    "networkAccess": "none"
  }
}
```

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
