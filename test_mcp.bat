@echo off
REM MCP Test-Script für Windows
REM Testet die MCP-Funktionalität der Hybrid-App

echo MCP-Test: Initialisierung...
echo {"jsonrpc": "2.0", "method": "initialize", "id": 1} | python app1_hybrid.py

echo.
echo MCP-Test: Tools auflisten...
echo {"jsonrpc": "2.0", "method": "tools/list", "id": 2} | python app1_hybrid.py

echo.
echo MCP-Test: Projektil-Berechnung (50 m/s, 45 Grad)...
echo {"jsonrpc": "2.0", "method": "tools/call", "params": {"name": "calculate_projectile", "arguments": {"initial_speed": 50, "angle": 45}}, "id": 3} | python app1_hybrid.py

echo.
pause