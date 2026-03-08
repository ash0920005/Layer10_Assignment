import json
import os

def redact_evidence(evidence_url):
    if not os.path.exists('memory_graph.json'):
        return

    with open('memory_graph.json', 'r') as f:
        graph = json.load(f)

    # Count before
    initial_count = len(graph['claims'])

    # Filter out any claim grounded by this URL
    graph['claims'] = [c for c in graph['claims'] if c['evidence_url'] != evidence_url]

    # Clean up entities that no longer have any claim
    active_subjects = {c['subject'] for c in graph['claims']}
    active_objects = {c['object'] for c in graph['claims']}
    active_entities = active_subjects.union(active_objects)
    

    removed = initial_count - len(graph['claims'])
    
    with open('memory_graph.json', 'w') as f:
        json.dump(graph, f, indent=2)

    print(f"🛑 REDACTION COMPLETE: Removed {removed} facts tied to {evidence_url}")

redact_evidence("https://github.com/lstjsuperman/fabric/issues/22014")