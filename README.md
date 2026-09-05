<div align="center">

# ⚡ CogniFlow AI
### *Adaptive Feynman Knowledge Engine & Multi-Modal Socratic Dialectic Studio*

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Google GenAI](https://img.shields.io/badge/Model-Gemini%202.5%20Flash-8E75C2?logo=google&logoColor=white)](https://ai.google.dev/)
[![Vector Store](https://img.shields.io/badge/RAG-ChromaDB-purple)](https://www.trychroma.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

*Move beyond passive Q&A chatbots. CogniFlow AI forces active mental deconstruction, detects conceptual drift at the sentence level, and guides learners to first-principles mastery.*

---

</div>

## 📌 Executive Summary

Most educational AI interfaces act as passive query machines—spoon-feeding summaries that induce an **illusion of competence**. 

**CogniFlow AI** inverses this dynamic using the **Feynman Technique** and **Socratic Dialectic Dialogue**:
1. **Active Concept Deconstruction:** The learner must explain complex mechanisms in plain English without notes or jargon.
2. **Dense Vector Grounding & Semantic Drift Detection:** Deconstructs the explanation sentence-by-sentence and calculates cosine similarity against ground-truth consensus or uploaded textbooks to flag hallucinations, weak definitions, and logical gaps.
3. **Adaptive Socratic Scaffolding:** Engages in targeted dialectic inquiry, challenging the student's premise rather than providing direct answers.
4. **Boundary Stress-Testing & Flaw Hunting:** Evaluates conceptual transferability by altering fundamental rules ("What-If") and challenging learners to debug subtly flawed mental models.

---

## 🚀 Key Features

### 1. 🧪 Feynman Diagnostic Engine
- Evaluates student input across **Clarity & Simplicity (0-10)** and **Technical Depth (0-10)**.
- **Jargon Trap Scanner:** Detects and flags buzzwords used to conceal a lack of understanding.
- Generates structured, actionable diagnostic cards highlighting specific misconceptions.

### 2. 🧬 Semantic Drift & Grounding Heatmap
- Tokenizes input into discrete semantic claims.
- Generates dense vector embeddings using Google's `text-embedding-004`.
- Inlines a color-coded factual density heatmap:
  - 🟢 **Grounded ($\ge 0.65$ similarity):** Core principles verified.
  - 🟡 **Shallow / Generic ($0.48 - 0.64$):** Vague assertions lacking rigor.
  - 🔴 **Semantic Drift ($< 0.48$):** Detected hallucination or misconception.

### 3. 💬 Socratic Dialectic Sparring
- Dynamic tutor persona that never spoon-feeds solutions.
- Analyzes previous turn states and knowledge gaps to formulate targeted counter-questions, analogies, or thought experiments.

### 4. 🌪️ Counterfactual "What-If" Stress-Tester
- Automatically alters boundary conditions (e.g., *infinite network latency*, *strictly linear activation functions*, *frictionless surfaces*).
- Forces students to extrapolate principles outside typical memorized patterns.

### 5. 🕵️ Reverse Turing Flaw Hunt
- Inverts the assessment: the model drafts an explanation that is 90% technically accurate but embeds a single common, subtle misconception.
- The student must identify, diagnose, and rectify the flaw.

### 6. 🕸️ Interactive Knowledge Graph & Spaced Repetition
- Generates dynamic, draggable force-directed dependency graphs using PyVis (🟢 Mastered concepts vs. 🔴 Flagged gaps).
- Exports one-click **Anki-compatible flashcard decks (`.tsv`)** targeting identified weaknesses.
- Generates a complete **Markdown Study Dossier** for offline review.

### 7. 🎨 Cyber-Academic UI & Multi-Theming
- Glassmorphic panels with hardware-accelerated SVG cyber-reticle cursors.
- Real-time theme toggle: **Cyber Indigo**, **Emerald Matrix**, **Solar Flare**, and **Frost Quantum**.
- Built-in **Concept Arcade** presets (*Backpropagation*, *TCP Handshake*, *Quantum Superposition*, *Raft Consensus*).

---

## 🛠️ Architecture & Tech Stack

```text
┌────────────────────────────────────────────────────────────────────────┐
│                          Streamlit Frontend UI                         │
│  (Custom Glassmorphic CSS, Dynamic Cursor Engine, Theme Token Manager)  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                            Core Engines                                │
│  ┌─────────────────────────┐              ┌─────────────────────────┐  │
│  │    Feynman Evaluator    │              │    Semantic Scanner     │  │
│  │ (Gap & Jargon Detection)│              │(Vector Cosine Heatmap)  │  │
│  └─────────────────────────┘              └─────────────────────────┘  │
│  ┌─────────────────────────┐              ┌─────────────────────────┐  │
│  │   Socratic Scaffolder   │              │  Counterfactual Engine  │  │
│  │ (Adaptive Dialectic)    │              │  (Stress-Test Scenarios)│  │
│  └─────────────────────────┘              └─────────────────────────┘  │
│  ┌─────────────────────────┐              ┌─────────────────────────┐  │
│  │   PyVis Graph Engine    │              │  Anki Flashcard Export  │  │
│  │ (Dependency Visualizer) │              │  (Spaced Repetition)    │  │
│  └─────────────────────────┘              └─────────────────────────┘  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                  ┌─────────────────┴─────────────────┐
                  ▼                                   ▼
┌───────────────────────────────────┐ ┌──────────────────────────────────┐
│        LLM & Embeddings API       │ │        Local Vector Engine       │
│  • Google Gemini 2.5 Flash        │ │  • ChromaDB Persistence Store   │
│  • text-embedding-004             │ │  • PyPDF Document Chunking       │
└───────────────────────────────────┘ └──────────────────────────────────┘
