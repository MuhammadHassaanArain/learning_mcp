# MCP Progress Demo

A simple demonstration of **progress tracking in MCP (Model Context Protocol)** using Python.  
This project shows how to run long-running tools on an MCP server and **stream real-time progress updates** to a client.

---

## Features

- Stateful MCP server with progress support (`stateless_http=False`)
- Example tools:
  - `download_file` – simulates downloading a file with progress updates.
  - `process_data` – simulates processing multiple records with progress updates.
- Real-time progress bars on the client side.
- Info logs from the server displayed in the client.

---

## Requirements

- Python 3.11+
- [MCP Python SDK](https://pypi.org/project/mcp/)  
  ```bash
  pip install mcp
