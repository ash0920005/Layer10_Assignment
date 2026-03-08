import json
import ollama
import re
import os
import math

# CONFIGURATION & CORE OBJECTS
SOURCES = [
    {"file": "clean_data.json", "type": "github_issue"},
    {"file": "slack_data.json", "type": "slack_message"}
]
OUTPUT_FILE = 'memory_graph.json'
LOG_FILE = 'processed_log.txt'

# Initialize Memory Store
if os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
        memory = json.load(f)
        memory = {"entities": {}, "claims": []}
else:
    memory = {"entities": {}, "claims": []}

# Idempotency: Track processed IDs to avoid re-processing
processed_ids = set()
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'r') as f:
        processed_ids = set(f.read().splitlines())

#SEMANTIC HELPERS (Vector Similarity)

def get_embedding(text):
    # Turns text into a vector for Semantic Deduplication.
    try:
        response = ollama.embed(model='all-minilm', input=text)
        return response['embeddings'][0]
    except Exception as e:
        return None

def cosine_similarity(v1, v2):
    # Calculates mathematical similarity between two meanings.
    if not v1 or not v2: return 0.0
    dot_product = sum(a * b for a, b in zip(v1, v2))
    mag1 = math.sqrt(sum(a * a for a in v1))
    mag2 = math.sqrt(sum(b * b for b in v2))
    return dot_product / (mag1 * mag2) if (mag1 * mag2) != 0 else 0.0

def find_semantic_match(new_name, threshold=0.82):
    # Semantic Entity Resolution: Merges similar names into one node.
    new_vector = get_embedding(new_name)
    if not new_vector: return None, None

    best_match = None
    highest_score = 0

    for existing_name, info in memory['entities'].items():
        if 'embedding' in info:
            score = cosine_similarity(new_vector, info['embedding'])
            if score > highest_score:
                highest_score = score
                best_match = existing_name

    if highest_score >= threshold:
        return best_match, new_vector
    return None, new_vector

#EXTRACTION HELPERS

SYSTEM_PROMPT = """
You are a Knowledge Graph Extractor. Extract Entities (Files, Methods, Apps, People) and Claims.
Format strictly as JSON:
{
  "entities": [{"name": "string", "type": "File|Method|App|Person"}],
  "claims": [{"subject": "string", "predicate": "string", "object": "string"}]
}
"""

def extract_json_from_text(text):
    try:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        return json.loads(match.group()) if match else None
    except: return None

# MAIN PIPELINE

def build_graph():
    print(f"🚀 Starting GLTM Pipeline (Idempotency: ON, Fusion: ON)")
    
    # Observability Metrics
    stats = {"total_processed": 0, "fusions": 0, "errors": 0}

    for source in SOURCES:
        if not os.path.exists(source['file']):
            continue
            
        with open(source['file'], 'r', encoding='utf-8') as f:
            source_data = json.load(f)

        print(f"\n--- Ingesting {source['type']} ---")
        
        # Limit GitHub issues for demo speed, process all Slack
        limit = 20 if source['type'] == "github_issue" else len(source_data)

        for i, item in enumerate(source_data[:limit]):
            # IDEMPOTENCY CHECK (Maintainability)
            if item['id'] in processed_ids:
                continue

            print(f"[{i+1}/{limit}] Extracting: {item['id']}")
            input_context = f"Source: {source['type']}\nContent: {item['content']}"

            try:
                # AI EXTRACTION
                response = ollama.chat(model='llama3', messages=[
                    {'role': 'system', 'content': SYSTEM_PROMPT},
                    {'role': 'user', 'content': input_context},
                ])

                knowledge = extract_json_from_text(response['message']['content'])

                if knowledge:
                    # SEMANTIC ENTITY FUSION
                    for ent in knowledge.get('entities', []):
                        raw_name = ent['name'].strip()
                        match_name, vector = find_semantic_match(raw_name)

                        if match_name:
                            memory['entities'][match_name]['mentions'] += 1
                            if match_name != raw_name:
                                stats["fusions"] += 1
                                print(f"      ✨ FUSION: '{raw_name}' -> '{match_name}'")
                        else:
                            memory['entities'][raw_name] = {
                                "type": ent.get('type', 'Unknown'),
                                "mentions": 1,
                                "embedding": vector 
                            }

                    # GROUNDED CLAIM STORAGE (Provenance Tracking)
                    for claim in knowledge.get('claims', []):
                        memory['claims'].append({
                            "subject": claim.get('subject', '').strip().lower(),
                            "predicate": claim.get('predicate', '').strip().lower(),
                            "object": claim.get('object', '').strip().lower(),
                            "evidence_url": item['id'].replace('"', ''),
                            "source_type": source['type'],
                            "timestamp": item['timestamp']
                        })
                    
                    # Log success for Idempotency
                    processed_ids.add(item['id'])
                    stats["total_processed"] += 1
                else:
                    stats["errors"] += 1

            except Exception as e:
                print(f"   ! Error: {e}")
                stats["errors"] += 1

    # OBSERVABILITY & STORAGE
    # Update log for next run
    with open(LOG_FILE, 'w') as f:
        f.write("\n".join(processed_ids))

    # Remove vectors before saving JSON (keeps file lightweight)
    output_mem = memory.copy()
    for ent in output_mem['entities']:
        if 'embedding' in output_mem['entities'][ent]:
            del output_mem['entities'][ent]['embedding']

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output_mem, f, indent=2)
    
    print(f"\n" + "="*40)
    print(f"📊 OBSERVABILITY REPORT")
    print(f"   Items Processed: {stats['total_processed']}")
    print(f"   Semantic Fusions: {stats['fusions']}")
    print(f"   Extraction Errors: {stats['errors']}")
    print(f"   Final Entity Count: {len(memory['entities'])}")
    print(f"="*40)

if __name__ == "__main__":
    build_graph()