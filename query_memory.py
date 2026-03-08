import json
import os

with open('memory_graph.json', 'r') as f:
    graph = json.load(f)

def query_fused_memory(query_entity):
    query_entity = query_entity.lower().strip()
    print(f"\n" + "="*70)
    print(f"🧠 FUSED ORGANIZATIONAL MEMORY: {query_entity}")
    print("="*70)

    if query_entity not in graph['entities']:
        print(f"❌ '{query_entity}' not found in memory.")
        return

    # Identify Entity Info
    info = graph['entities'][query_entity]
    print(f"Type: {info['type']} | Total Mentions across all platforms: {info['mentions']}")

    # Get Related Claims
    related = [c for c in graph['claims'] if c['subject'] == query_entity or c['object'] == query_entity]
    
    # Separate by Source
    github_claims = [c for c in related if c.get('source_type') == 'github_issue']
    slack_claims = [c for c in related if c.get('source_type') == 'slack_message']

    # Show Technical Evidence (GitHub)
    print(f"\n📂 TECHNICAL ARTIFACTS (GitHub Issues):")
    if not github_claims:
        print("   No technical tickets found.")
    else:
        for c in github_claims:
            print(f"   • [{c['timestamp']}] {c['subject']} {c['predicate']} {c['object']}")
            print(f"     🔗 Source: {c['evidence_url']}")

    # Show Human Context (Slack)
    print(f"\n💬 COMMUNICATION CONTEXT (Slack Discussion):")
    if not slack_claims:
        print("   No chat discussions found.")
    else:
        # Conflict Resolution: Sort Slack by newest first
        sorted_slack = sorted(slack_claims, key=lambda x: x['timestamp'], reverse=True)
        current_discussion = sorted_slack[0]
        
        print(f"   • CURRENT STATUS: {current_discussion['subject']} {current_discussion['predicate']} {current_discussion['object']}")
        print(f"     🔗 Link: {current_discussion['evidence_url']} | Time: {current_discussion['timestamp']}")
        
        if len(sorted_slack) > 1:
            print(f"   • HISTORICAL CONTEXT: Found {len(sorted_slack)-1} previous mentions in chat.")

    if github_claims and slack_claims:
        print(f"\n✨ INSIGHT: This entity represents a 'Fused Memory'. It is currently being discussed")
        print(f"   by humans on Slack while having active technical issues on GitHub.")

# (like 'com.immomo.momo' or 'statusbarheightutil')
query_fused_memory("com.immomo.momo")