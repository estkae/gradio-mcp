import math
import gradio as gr
import sys
import json

def compute_projectile_distance(initial_speed, angle):
    """
    Calculate the horizontal distance traveled by a projectile.
    Returns JSON for MCP compatibility.
    """
    try:
        angle_rad = math.radians(angle)
        g = 9.81
        distance = (initial_speed**2 * math.sin(2 * angle_rad)) / g
        
        # Return as JSON-compatible dictionary
        return  json.dumps({
            "status": "success",
            "result": distance,
            "units": "meters"
        })
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": {str(e)}
        })

# MCP-compatible interface
def handle_mcp_request(params):
    try:
        data = json.loads(params)
        result = compute_projectile_distance(
            data.get("initial_speed", 0),
            data.get("angle", 45)
        )
        return json.dumps(result)
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"Invalid request: {str(e)}"
        })

# Standard Gradio UI for testing
if __name__ == "__main__":
    # Print initialization message to stderr for MCP logging
    # print("Initializing Projectile Distance Calculator...", file=sys.stderr)
    
    # Create both interfaces
    mcp_interface = gr.Interface(
        fn=handle_mcp_request,
        inputs="text",
        outputs="text",
        title="MCP Endpoint",
        description="JSON API endpoint for MCP integration"
    )
    
    ui_interface = gr.Interface(
        fn=compute_projectile_distance,
        inputs=[
            gr.Number(label="Initial Speed (m/s)", minimum=0),
            gr.Slider(label="Launch Angle (degrees)", minimum=0, maximum=90)
        ],
        outputs=gr.JSON(label="Result"),
        title="Projectile Distance Calculator"
    )
    
    # Combine interfaces
    app = gr.TabbedInterface(
        [ui_interface, mcp_interface],
        ["UI Calculator", "MCP Endpoint"]
    )
    
    # Launch with MCP-compatible settings
    app.launch(
        server_name="127.0.0.1",
        server_port=7860,
        show_error=True,
        share=False,
        quiet=True  # Reduces console output
        #enable_queue=False
    )