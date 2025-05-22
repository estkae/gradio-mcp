# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Gradio-MCP integration project that creates interfaces compatible with both Gradio UI and Model Context Protocol (MCP) communication. The project demonstrates two approaches:

1. **app1.py**: Basic Gradio app with MCP-compatible JSON endpoints
2. **app1_hybrid.py**: Hybrid approach that can run as either a Gradio server or MCP tool

## Build and Run Commands

### Running the Applications

```bash
# Run basic Gradio app with MCP endpoint
python3 app1.py

# Run hybrid app (auto-detects MCP mode vs Gradio mode)
python3 app1_hybrid.py
```

### MCP Mode Testing

```bash
# Test MCP protocol with stdin/stdout
echo '{"jsonrpc": "2.0", "method": "initialize", "id": 1}' | python3 app1_hybrid.py
```

## Architecture

### app1.py Architecture
- Creates a tabbed Gradio interface with two tabs:
  - UI Calculator: Direct user interface for projectile distance calculation
  - MCP Endpoint: JSON API endpoint for MCP integration
- Functions handle both standard returns and MCP-compatible JSON responses
- Runs on localhost:7860 with quiet mode enabled

### app1_hybrid.py Architecture
- Implements full MCP protocol handler with stdin/stdout communication
- Auto-detects running mode:
  - If stdin is not a terminal: Operates in MCP mode
  - If stdin is a terminal: Launches Gradio interface
- Supports MCP methods:
  - `initialize`: Protocol handshake
  - `tools/list`: Lists available tools
  - `tools/call`: Executes projectile calculation
  - `resources/list` and `prompts/list`: Returns empty lists (unsupported)
- MCP tool exposed: `calculate_projectile` with initial_speed and angle parameters

## Key Technical Details

- Python 3.10.12 environment
- Gradio 5.29.0 dependency
- Default server settings: localhost:7860
- MCP protocol version: "2024-11-05"
- Calculation uses standard projectile motion formula with g=9.81 m/s²