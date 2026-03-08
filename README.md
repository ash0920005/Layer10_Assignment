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
├── scripts/
│   ├── cleaning_data.py    # Prepares diverse GitHub data from raw CSV
│   ├── extract_graph.py    # AI Engine: Extraction & Semantic Fusion
│   ├── query_memory.py     # Retrieval: Fused memory & Conflict resolution
│   └── visualize_graph.py  # UI: Generates the interactive HTML graph
├── data/
│   ├── clean_data.json     # Standardized GitHub artifacts
│   ├── slack_data.json     # Mock Slack communication logs
│   └── memory_graph.json   # The final Long-Term Memory store
├── memory_map.html         # Interactive high-visibility visualization
└── README.md               # Project documentation
