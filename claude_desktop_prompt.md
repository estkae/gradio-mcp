# Claude Desktop MCP Integration

## Setup-Anleitung

1. Die MCP-Konfiguration zu Claude Desktop hinzufügen:
   - Öffnen Sie Claude Desktop Einstellungen
   - Navigieren Sie zu "MCP Servers"
   - Fügen Sie einen neuen Server hinzu

2. Konfiguration einfügen:
```json
{
  "gradio-projectile": {
    "command": "python",
    "args": ["C:/Users/kae/source/repos/gradio-mcp/app1_hybrid.py"],
    "env": {}
  }
}
```

Alternativ können Sie den absoluten Pfad zur Python-Executable verwenden:
```json
{
  "gradio-projectile": {
    "command": "C:/Users/kae/AppData/Local/Programs/Python/Python310/python.exe",
    "args": ["C:/Users/kae/source/repos/gradio-mcp/app1_hybrid.py"],
    "env": {}
  }
}
```

## Verwendung in Claude Desktop

Nach der Konfiguration können Sie das Tool in Claude Desktop verwenden:

```
Berechne die Flugweite eines Projektils mit einer Anfangsgeschwindigkeit von 50 m/s und einem Abwurfwinkel von 45 Grad.
```

Claude wird automatisch das MCP-Tool `calculate_projectile` aufrufen.

## Test-Prompts

1. **Einfache Berechnung:**
   "Wie weit fliegt ein Projektil bei 30 m/s und 45 Grad?"

2. **Optimaler Winkel:**
   "Bei welchem Winkel fliegt ein Projektil mit 40 m/s am weitesten?"

3. **Vergleich:**
   "Vergleiche die Flugweiten bei 50 m/s für die Winkel 30°, 45° und 60°"

## Fehlerbehebung

Falls die Integration nicht funktioniert:

1. Prüfen Sie den Python-Pfad
2. Stellen Sie sicher, dass Gradio installiert ist: `pip install gradio`
3. Testen Sie das Script manuell: `python app1_hybrid.py`
4. Überprüfen Sie die Claude Desktop Logs