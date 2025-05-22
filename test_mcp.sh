#!/bin/bash

# MCP Test-Script
# Testet die MCP-Funktionalität der Hybrid-App

echo "MCP-Test: Initialisierung..."
echo '{"jsonrpc": "2.0", "method": "initialize", "id": 1}' | python3 app1_hybrid.py

echo -e "\nMCP-Test: Tools auflisten..."
echo '{"jsonrpc": "2.0", "method": "tools/list", "id": 2}' | python3 app1_hybrid.py

echo -e "\nMCP-Test: Projektil-Berechnung (50 m/s, 45°)..."
echo '{"jsonrpc": "2.0", "method": "tools/call", "params": {"name": "calculate_projectile", "arguments": {"initial_speed": 50, "angle": 45}}, "id": 3}' | python3 app1_hybrid.py