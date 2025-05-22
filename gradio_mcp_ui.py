import math
import sys
import json
import threading
import gradio as gr

class GradioMCPHandler:
    def __init__(self):
        self.is_mcp_mode = False
        self.app = None
        self.public_url = None
        
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
                        "name": "gradio-ui",
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
                        "name": "launch_gradio_ui",
                        "description": "Launch Gradio UI and return the URL",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "share": {"type": "boolean", "default": True}
                            }
                        }
                    }]
                }
            }
            
        elif method == "tools/call":
            name = request.get("params", {}).get("name")
            args = request.get("params", {}).get("arguments", {})
            
            if name == "launch_gradio_ui":
                share = args.get("share", True)
                url = self.launch_gradio(share)
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{
                            "type": "text",
                            "text": f"Gradio UI launched at: {url}"
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
    
    def launch_gradio(self, share=True):
        """Launch Gradio interface and return URL"""
        if self.app is None:
            self.app = self.create_gradio_app()
            
            # Launch in a separate thread
            def run_gradio():
                self.app.launch(
                    server_name="127.0.0.1",
                    server_port=7860,
                    share=share,
                    quiet=True,
                    prevent_thread_lock=True
                )
            
            thread = threading.Thread(target=run_gradio, daemon=True)
            thread.start()
            
            # Wait a bit for the server to start
            import time
            time.sleep(3)
            
            if share:
                # Get the public URL (this is a simplified version)
                self.public_url = "https://your-app.gradio.live"  # Gradio will provide actual URL
                return self.public_url
            else:
                return "http://localhost:7860"
        else:
            return self.public_url or "http://localhost:7860"
    
    def create_gradio_app(self):
        """Create the Gradio interface"""
        def compute_projectile_distance(initial_speed, angle):
            try:
                angle_rad = math.radians(angle)
                g = 9.81
                distance = (initial_speed**2 * math.sin(2 * angle_rad)) / g
                return f"Distance: {distance:.2f} meters"
            except Exception as e:
                return f"Error: {str(e)}"
        
        app = gr.Interface(
            fn=compute_projectile_distance,
            inputs=[
                gr.Number(label="Initial Speed (m/s)", minimum=0),
                gr.Slider(label="Launch Angle (degrees)", minimum=0, maximum=90)
            ],
            outputs="text",
            title="Projectile Distance Calculator"
        )
        
        return app

if __name__ == "__main__":
    # Check if running in MCP mode (when stdin is not a terminal)
    if not sys.stdin.isatty():
        # MCP mode
        handler = GradioMCPHandler()
        handler.handle_stdin()
    else:
        # Direct Gradio mode
        handler = GradioMCPHandler()
        app = handler.create_gradio_app()
        app.launch(
            server_name="127.0.0.1",
            server_port=7860,
            share=True
        )