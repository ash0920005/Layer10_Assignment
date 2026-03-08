from pyvis.network import Network
import json
import os

# Load the Memory Graph
if not os.path.exists('memory_graph.json'):
    print("Error: memory_graph.json not found!")
    exit()

with open('memory_graph.json', 'r', encoding='utf-8') as f:
    graph = json.load(f)

# Initialize the Network with refined UI settings
net = Network(
    height="900px", 
    width="100%", 
    bgcolor="#0b0e14", # Deeper charcoal/navy
    font_color="#cee221", 
    notebook=False, 
    directed=True
)

# Define the Design Palette
PALETTE = {
    "person": {"color": "#FF9F43", "label": "Human (Slack)"},      # Vibrant Orange
    "app": {"color": "#FF5252", "label": "Application/Service"},   # Soft Red
    "file": {"color": "#00D2FF", "label": "Source Code File"},     # Cyan
    "method": {"color": "#28C76F", "label": "Method/Function"},    # Emerald Green
    "ghost": {"color": "#555555", "label": "External Entity"}      # Gray
}

# Add Nodes with BIG, crisp labels
for name, info in graph['entities'].items():
    mentions = info.get('mentions', 1)
    type_key = info['type'].lower()
    
    node_color = PALETTE.get(type_key, {"color": "#4da6ff"})["color"]
    node_size = 35 + (mentions * 5)
    
    net.add_node(
        name, 
        label=name, 
        size=node_size, 
        color=node_color,
        title=f"CATEGORY: {type_key.upper()}\nTOTAL MENTIONS: {mentions}",
        font={
            'size': 42 + (mentions * 2), 
            'face': 'Verdana',
            'strokeWidth': 4,
            'strokeColor': '#000000'
        },
        borderWidth=2,
        borderWidthSelected=5
    )

# Add Edges with Source-Aware Styling
for claim in graph['claims']:
    subj, obj = claim['subject'], claim['object']
    source = claim.get('source_type', 'unknown')
    
    edge_color = "#FFFEFE" # Subtle for GitHub
    edge_width = 1
    if source == 'slack_message':
        edge_color = "#FF9F43" # Match the 'Person' color for Slack
        edge_width = 3        # Make human conversation lines stand out

    # Ghost Node Protection
    for node_id in [subj, obj]:
        if node_id not in net.get_nodes():
            net.add_node(node_id, label=node_id, size=20, color=PALETTE["ghost"]["color"], 
                         font={'size': 30, 'color': 'white', 'strokeWidth': 3, 'strokeColor': 'black'})

    net.add_edge(subj, obj, title=f"Fact: {claim['predicate']}\nSource: {source.upper()}", 
                 color=edge_color, width=edge_width, arrowStrikethrough=False)

# Advanced Physics and Interaction UI
net.set_options("""
{
  "physics": {
    "forceAtlas2Based": {
      "gravitationalConstant": -150,
      "centralGravity": 0.005,
      "springLength": 356,
      "springConstant": 0.18
    },
    "maxVelocity": 146,
    "solver": "forceAtlas2Based",
    "timestep": 0.35,
    "stabilization": {"iterations": 150}
  },
  "interaction": {
    "navigationButtons": true,
    "hover": true,
    "keyboard": true
  }
}
""")

# INJECT CUSTOM CSS LEGEND (The 'Designer' Touch)
legend_html = f"""
<div id="graph-legend" style="position: absolute; top: 20px; left: 20px; padding: 15px; 
     background: rgba(255,255,255,0.05); color: white; border-radius: 10px; 
     border: 1px solid rgba(255,255,255,0.1); backdrop-filter: blur(5px); font-family: sans-serif; z-index: 1000;">
    <h3 style="margin: 0 0 10px 0; font-size: 16px; color: #00D2FF;">Organizational Memory Map</h3>
    <div style="font-size: 13px;">
        <div style="margin-bottom: 5px;"><span style="display:inline-block; width:12px; height:12px; background:#FF9F43; border-radius:50%;"></span> {PALETTE['person']['label']}</div>
        <div style="margin-bottom: 5px;"><span style="display:inline-block; width:12px; height:12px; background:#FF5252; border-radius:50%;"></span> {PALETTE['app']['label']}</div>
        <div style="margin-bottom: 5px;"><span style="display:inline-block; width:12px; height:12px; background:#00D2FF; border-radius:50%;"></span> {PALETTE['file']['label']}</div>
        <div style="margin-bottom: 5px;"><span style="display:inline-block; width:12px; height:12px; background:#28C76F; border-radius:50%;"></span> {PALETTE['method']['label']}</div>
        <div style="margin-bottom: 10px;"><span style="display:inline-block; width:12px; height:12px; background:#555555; border-radius:50%;"></span> {PALETTE['ghost']['label']}</div>
        <hr style="border: 0; border-top: 1px solid rgba(255,255,255,0.1);">
        <div style="margin-top: 5px;"><span style="display:inline-block; width:20px; height:2px; background:#FF9F43;"></span> Slack Fusion Path</div>
        <div style="margin-top: 5px;"><span style="display:inline-block; width:20px; height:2px; background:#555555;"></span> GitHub Trace</div>
    </div>
</div>
"""

# Save and Inject
output_file = "memory_map.html"
net.save_graph(output_file)

# We manually append the legend to the generated HTML
with open(output_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

html_content = html_content.replace('<body>', f'<body>{legend_html}')

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"DESIGNER SUCCESS! Open '{output_file}' to see the high-visibility legend and navigation.")