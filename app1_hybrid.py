import math
import sys
import json
import threading
import gradio as gr

class MCPHandler:
    def __init__(self):
        self.is_mcp_mode = False
        
    def handle_stdin(self):
        """Handle MCP protocol over stdin/stdout"""
        self.is_mcp_mode = True
        while True:
            try:
                line = sys.stdin.readline()
                if not line:
                    break
                    
                request = json.loads(line.strip())
                response = self.process_mcp_request(request)
                
                # Only send response if there is one (notifications don't get responses)
                if response is not None:
                    sys.stdout.write(json.dumps(response) + "\n")
                    sys.stdout.flush()
                
            except Exception as e:
                sys.stderr.write(f"MCP Error: {e}\n")
                sys.stderr.flush()
    
    def process_mcp_request(self, request):
        method = request.get("method")
        req_id = request.get("id")
        
        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "serverInfo": {
                        "name": "gradio-projectile",
                        "version": "1.0.0"
                    },
                    "capabilities": {}
                }
            }
            
        elif method == "notifications/initialized":
            # This is a notification, not a request - no response needed
            return None
            
        elif method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "tools": [{
                        "name": "calculate_projectile",
                        "description": "Calculate projectile distance",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "initial_speed": {"type": "number"},
                                "angle": {"type": "number"}
                            },
                            "required": ["initial_speed", "angle"]
                        }
                    }]
                }
            }
            
        elif method == "tools/call":
            name = request.get("params", {}).get("name")
            args = request.get("params", {}).get("arguments", {})
            
            if name == "calculate_projectile":
                distance = self.calculate_distance(
                    args.get("initial_speed", 0),
                    args.get("angle", 45)
                )
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{
                            "type": "text",
                            "text": f"Distance: {distance:.2f} meters"
                        }]
                    }
                }
                
        elif method in ["resources/list", "prompts/list"]:
            # Return empty lists for unsupported methods
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    method.split('/')[0]: []
                }
            }
                
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {
                "code": -32601,
                "message": f"Method not found: {method}"
            }
        }
    
    def calculate_distance(self, initial_speed, angle):
        angle_rad = math.radians(angle)
        g = 9.81
        distance = (initial_speed**2 * math.sin(2 * angle_rad)) / g
        return distance

def compute_projectile_distance(initial_speed, angle):
    """Calculate the horizontal distance traveled by a projectile."""
    try:
        angle_rad = math.radians(angle)
        g = 9.81
        distance = (initial_speed**2 * math.sin(2 * angle_rad)) / g
        return f"Distance: {distance:.2f} meters"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    # Check if running in MCP mode (when stdin is not a terminal)
    if not sys.stdin.isatty():
        # MCP mode
        handler = MCPHandler()
        handler.handle_stdin()
    else:
        # Gradio mode
        app = gr.Interface(
            fn=compute_projectile_distance,
            inputs=[
                gr.Number(label="Initial Speed (m/s)", minimum=0),
                gr.Slider(label="Launch Angle (degrees)", minimum=0, maximum=90)
            ],
            outputs="text",
            title="Projectile Distance Calculator"
        )
        
        app.launch(
            server_name="127.0.0.1",
            server_port=7860,
            quiet=True
        )