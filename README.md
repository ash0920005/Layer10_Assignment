# Layer10_Assignment
# 🧠 Grounded Long-Term Memory (GLTM) Pipeline

This project implements an intelligent system designed to transform scattered, unstructured organizational knowledge—specifically **GitHub Issues (Tickets)** and **Slack Chat (Communication)**—into a structured, queryable, and grounded **Knowledge Graph**.

This system was developed for the **Layer10 Take-Home Project**, focusing on the challenge of maintaining "correctness over time" in an environment where messages are edited, decisions are reversed, and data is fragmented across multiple platforms.

---

## 🚀 Key Features

*   **Semantic Entity Resolution:** Uses Vector Embeddings (`all-minilm`) to merge entities like *"momo app"* and *"com.immomo.momo"* based on mathematical meaning, ensuring the memory isn't fragmented by different naming conventions.
*   **Multi-Source Knowledge Fusion:** Automatically connects technical artifacts (GitHub) with human discussions (Slack) to provide a unified organizational "Brain."
*   **Temporal Conflict Resolution:** Tracks claims by timestamp, distinguishing between the **Current Truth** and **Historical Context** when decisions are reversed.
*   **Strong Grounding:** Every fact in the memory graph is strictly traced to an `evidence_url` (GitHub Link or Slack ID) and a `source_type`.
*   **Interactive Visualization:** A high-visibility, spacious graph UI with a built-in schema legend for easy exploration of the organization's memory.

---

## 🛠️ Tech Stack

| Component | Technology |
| :--- | :--- |
| **LLM (Extraction)** | Llama 3 (via Ollama) |
| **Embeddings** | all-minilm (via Ollama) |
| **Data Processing** | Python 3.11, Pandas |
| **Graph Visualization** | Pyvis (D3.js based) |
| **Memory Store** | Standardized JSON Knowledge Graph |

---

## 📂 Project Structure

```text
/Layer10_Memory_Project
├──cleaning_data.py    # Prepares diverse GitHub data from raw CSV
├──extract_graph.py    # AI Engine: Extraction & Semantic Fusion
├──query_memory.py     # Retrieval: Fused memory & Conflict resolution
├──visualize_graph.py  # UI: Generates the interactive HTML graph
├──clean_data.json     # Standardized GitHub artifacts
├──slack_data.json     # Mock Slack communication logs
├──memory_graph.json   # The final Long-Term Memory store
├── memory_map.html         # Interactive high-visibility visualization
└── README.md               # Project documentation
```

## 🚦 Getting Started

### 1. Prerequisites
Ensure you have [Ollama](https://ollama.com/) installed and running. Download the required open-weight models via your terminal:

```bash
# Pull the LLM for extraction
ollama pull llama3

# Pull the embedding model for deduplication
ollama pull all-minilm
```
### 2. Installation
Clone the repository and install the necessary Python libraries:

```bash
# Install core dependencies
pip install pandas ollama pyvis
```
### 3. Execution Pipeline
Run the scripts in the following order to build the memory from scratch:
```bash
python cleaning_data.py
python extract_graph.py
python visualize_graph.py
python query_memory.py
```

## 🧠 Technical Design & Evaluation

### 1. Grounding & Provenance
Every claim in the graph is explicitly linked to a source. To satisfy the Grounded Memory requirement, our memory_graph.json stores an evidence_url for every triple. This ensures the system is auditable and never provides a fact without a "receipt

### 2. Deduplication (Semantic vs. String)
Standard systems fail when names collide or change. We implemented Semantic Deduplication using Vector Similarity. Using a similarity threshold of 0.82, the system calculates the cosine similarity of entity vectors.
Example: Merging "fabric app" (Slack) into "fabric.io" (GitHub) happens automatically.

### 3. Long-Term Correctness
To handle decision reversals, the system uses Temporal Logic. When a query is performed, the system groups claims by their relationship and flags the most recent timestamp as the Current Truth, while archiving older versions as Historical Conflicts.

### 4. Idempotency & Maintainability
The extraction script utilizes a processed_log.txt. This ensures Idempotency—the pipeline can be run incrementally. It will only process new messages, preventing redundant processing and making it viable for production use.

## 🏢 Adaptation to Layer10 Target Environment
How this scales to Slack, Email, and Jira:
Handling Edits/Deletions: Because every claim is grounded to a specific ID, the system can perform a "Provenance Trace." If a message is deleted, the system identifies and invalidates all facts that relied on that redacted source.
Unstructured + Structured Fusion: For Slack/Email, we implement Contextual Windows. Since chat is a stream, we group messages by Thread ID or time proximity before extraction to ensure the LLM understands the intent of a conversation.
Permissions: In a production-grade system, we would attach access_group metadata to every edge. The retrieval engine then filters the graph based on the user's permission token (e.g., Engineering vs. HR).

## 📊 Sample Retrieval Output
The following output demonstrates Knowledge Fusion for the entity com.immomo.momo:

```text
======================================================================
🧠 FUSED ORGANIZATIONAL MEMORY: com.immomo.momo
======================================================================
Type: App | Total Mentions across all platforms: 15

📂 TECHNICAL ARTIFACTS (GitHub Issues):
   • [2023-01-01 03:00:00] com.immomo.momo has_issue 59c0de8f...
     🔗 Source: https://github.com/lstjsuperman/fabric/issues/15885
   • [2023-01-01 11:00:00] momo6 developed com.immomo.momo
     🔗 Source: https://github.com/lstjsuperman/fabric/issues/6564

💬 COMMUNICATION CONTEXT (Slack Discussion):
   • CURRENT STATUS: bob prioritize the fix for com.immomo.momo
     🔗 Link: SLACK_002 | Time: 2023-01-05 09:15:00

✨ INSIGHT: This entity represents a 'Fused Memory'. Technical issues on 
   GitHub are currently being prioritized in Slack discussions.
```


