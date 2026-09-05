import streamlit as st
import streamlit.components.v1 as components
import tempfile
import os
from datetime import datetime

from src.core.styles import get_theme_css, THEMES
from src.core.llm_client import LLMClient
from src.rag.document_store import DocumentStore
from src.engine.feynman_evaluator import FeynmanEvaluator
from src.engine.socratic_tutor import SocraticTutor
from src.engine.voice_handler import VoiceHandler
from src.engine.flashcard_generator import FlashcardGenerator
from src.engine.interactive_graph import InteractiveGraphBuilder
from src.engine.remediator import ConceptRemediator

# --- IMPORT NEW ENGINES ---
from src.engine.semantic_scanner import SemanticScanner
from src.engine.stress_tester import CounterfactualStressTester
from src.engine.flaw_hunter import ReverseTuringHunter

st.set_page_config(page_title="CogniFlow AI | Socratic Studio", page_icon="⚡", layout="wide", initial_sidebar_state="collapsed")

if "active_theme" not in st.session_state:
    st.session_state.active_theme = "Cyber Indigo (Dark)"
st.markdown(get_theme_css(st.session_state.active_theme), unsafe_allow_html=True)

# Cache & Instantiate Services
@st.cache_resource
def load_services():
    llm = LLMClient()
    return (
        DocumentStore(),
        FeynmanEvaluator(llm),
        SocraticTutor(llm),
        VoiceHandler(llm),
        FlashcardGenerator(llm),
        InteractiveGraphBuilder(llm),
        ConceptRemediator(llm),
        SemanticScanner(llm),
        CounterfactualStressTester(llm),
        ReverseTuringHunter(llm)
    )

(doc_store, evaluator, tutor, voice_handler, flashcards, 
 graph_builder, remediator, scanner, stress_tester, flaw_hunter) = load_services()

# Session State Initializations
for key, default in [
    ("chat_history", []), ("eval_result", None), ("topic_input", ""), 
    ("explanation_input", ""), ("remediation_text", None), ("current_cards", []),
    ("scan_results", None), ("active_scenario", None), ("stress_critique", None),
    ("active_flawed_case", None), ("flaw_verdict", None)
]:
    if key not in st.session_state:
        st.session_state[key] = default

# Presets Library
PRESETS = {
    "🧠 Backprop in Neural Nets": {
        "topic": "Backpropagation",
        "explanation": "Backpropagation is how neural networks learn. When an error is computed at the output, the network passes the gradient backward through each layer using calculus and the chain rule to update weights."
    },
    "⚛️ Quantum Superposition": {
        "topic": "Quantum Superposition",
        "explanation": "A quantum particle exists in a linear combination of all possible states simultaneously until measurement, which forces the state vector to project into a single eigenvalue."
    },
    "🌐 TCP 3-Way Handshake": {
        "topic": "TCP Handshake",
        "explanation": "A client sends a SYN packet, the server answers with SYN-ACK, and the client replies with ACK to confirm the socket connection is open for bidirectional transmission."
    },
    "📦 Raft Distributed Consensus": {
        "topic": "Raft Consensus Algorithm",
        "explanation": "Nodes use randomized election timers to pick a single leader. The leader receives client entries, replicates them across a quorum, and commits the state."
    }
}

# Top Theme Navigation Bar
col_th_label, col_th_btns = st.columns([1.2, 2.8])
with col_th_label:
    st.markdown(f"<span style='font-size:0.85rem; font-weight:700; color:var(--text-sub); text-transform:uppercase;'>🎨 Theme: <b>{st.session_state.active_theme}</b></span>", unsafe_allow_html=True)
with col_th_btns:
    t_cols = st.columns(len(THEMES))
    emojis = {"Cyber Indigo (Dark)": "🌌 Indigo", "Emerald Matrix (Dark)": "🟩 Matrix", "Solar Flare (Dark)": "🔥 Solar", "Frost Quantum (Light)": "❄️ Frost"}
    for idx, t_name in enumerate(THEMES.keys()):
        if t_cols[idx].button(emojis.get(t_name, t_name), key=f"btn_{t_name}", use_container_width=True):
            st.session_state.active_theme = t_name
            st.rerun()

st.markdown("<hr style='border:none; border-top:1px solid var(--card-border); margin:0.4rem 0 1.2rem 0;'>", unsafe_allow_html=True)

# Hero Header
st.markdown("""
<div class="hero-wrapper">
    <div class="hero-tag">⚡ Multi-Agent Cognitive Studio</div>
    <h1 class="hero-title">CogniFlow AI: First-Principles Mastery</h1>
    <p class="hero-subtitle">
        Vector-grounded semantic drift heatmaps, counterfactual stress-testing, and dialectic sparring.
    </p>
</div>
""", unsafe_allow_html=True)

# Presets Quick-Bar
p_cols = st.columns(4)
for idx, (p_title, p_data) in enumerate(PRESETS.items()):
    if p_cols[idx].button(p_title, use_container_width=True):
        st.session_state.topic_input = p_data["topic"]
        st.session_state.explanation_input = p_data["explanation"]
        st.session_state.eval_result = None
        st.session_state.scan_results = None
        st.session_state.chat_history = []
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns([1.05, 1], gap="large")

# LEFT COLUMN: INPUT & DIAGNOSTIC SCANNER
with col1:
    st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
    st.markdown("### 🧪 Step 1: Concept Deconstruction")
    topic_val = st.text_input("Concept Title", value=st.session_state.topic_input, placeholder="e.g. Backpropagation, Paxos, Entropy")
    
    explanation_val = st.text_area(
        "Explain it simply in your own words",
        value=st.session_state.explanation_input,
        height=190,
        placeholder="Explain what physically/computationally occurs step-by-step..."
    )

    if st.button("🚀 Analyze with Feynman & Vector Engine", type="primary", use_container_width=True):
        if not topic_val.strip() or not explanation_val.strip():
            st.warning("Please enter both the topic and your explanation.")
        else:
            with st.spinner("Executing dense vector scan and semantic drift evaluation..."):
                ref_context = doc_store.retrieve_context(topic_val)
                st.session_state.eval_result = evaluator.evaluate_explanation(topic_val, explanation_val, ref_context)
                st.session_state.scan_results = scanner.scan_explanation(explanation_val, ref_context)
                
                # Start Socratic dialectic
                first_prompt = tutor.get_scaffolding_response(
                    topic=topic_val,
                    gaps=st.session_state.eval_result.get("misconceptions", []),
                    conversation_history=[{"role": "user", "content": explanation_val}]
                )
                st.session_state.chat_history = [
                    {"role": "user", "content": explanation_val},
                    {"role": "assistant", "content": first_prompt}
                ]
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # Telemetry Pod & Semantic Heatmap
    if st.session_state.eval_result:
        res = st.session_state.eval_result
        st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
        st.markdown("### 📊 Diagnostic Telemetry")
        st.markdown(f"*{res.get('verdict', '')}*")

        c_score = res.get('clarity_score', 0)
        a_score = res.get('accuracy_score', 0)
        st.markdown(f"""
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:1rem; margin:1rem 0;">
            <div class="gauge-box"><div class="gauge-score">{c_score}/10</div><div class="gauge-label">Clarity</div></div>
            <div class="gauge-box"><div class="gauge-score">{a_score}/10</div><div class="gauge-label">Rigor</div></div>
        </div>
        """, unsafe_allow_html=True)

        # Feature 1: Render Semantic Heatmap
        if st.session_state.scan_results:
            st.markdown("<b style='color:var(--accent-cyan);'>🧬 Sentence-Level Grounding Heatmap:</b>", unsafe_allow_html=True)
            heatmap_html = scanner.render_heatmap_html(st.session_state.scan_results)
            st.markdown(heatmap_html, unsafe_allow_html=True)

        gaps = res.get("misconceptions", [])
        if gaps:
            st.markdown("<br><b style='color:#F87171;'>⚠️ Identified Blindspots:</b>", unsafe_allow_html=True)
            pills = "".join([f"<span class='pill-tag pill-gap'>{g}</span>" for g in gaps])
            st.markdown(f"<div style='margin-top:6px;'>{pills}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# RIGHT COLUMN: MULTI-MODAL MASTERY LAB
with col2:
    st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
    st.markdown("### 💡 Step 2: Dialectic & Stress-Testing Suite")

    tab_chat, tab_stress, tab_hunt, tab_graph = st.tabs([
        "💬 Socratic Sparring",
        "🌪️ 'What-If' Stress-Test",
        "🕵️ Reverse Turing Flaw Hunt",
        "🕸️ Interactive Graph"
    ])

    # Tab 1: Socratic Dialogue
    with tab_chat:
        chat_box = st.container(height=340)
        with chat_box:
            for msg in st.session_state.chat_history:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])
        user_reply = st.chat_input("Challenge Socrates or defend your reasoning...")
        if user_reply:
            st.session_state.chat_history.append({"role": "user", "content": user_reply})
            with st.spinner("Socrates is formulating a counter-argument..."):
                gaps = st.session_state.eval_result.get("misconceptions", []) if st.session_state.eval_result else []
                next_q = tutor.get_scaffolding_response(topic_val, gaps, st.session_state.chat_history)
                st.session_state.chat_history.append({"role": "assistant", "content": next_q})
            st.rerun()

    # Tab 2: Feature 2 - Counterfactual Stress-Testing
    with tab_stress:
        st.caption("Alters reality parameters to test if you can extrapolate from first principles.")
        if st.button("Generate Counterfactual Scenario", use_container_width=True):
            if topic_val.strip() and explanation_val.strip():
                with st.spinner("Injecting impossible boundary constraint..."):
                    st.session_state.active_scenario = stress_tester.generate_scenario(topic_val, explanation_val)
                    st.session_state.stress_critique = None
            else:
                st.info("Input a topic and explanation first.")

        if st.session_state.active_scenario:
            sc = st.session_state.active_scenario
            st.markdown(f"#### ⚡ Scenario: *{sc.get('altered_premise')}*")
            st.info(sc.get('scenario_setup'))

            stress_answer = st.text_area("What is the direct consequence?", placeholder="Derive what happens under this altered condition...", height=100)
            if st.button("Submit Derivation"):
                if stress_answer.strip():
                    with st.spinner("Evaluating logical extrapolation..."):
                        critique = stress_tester.evaluate_response(topic_val, sc, stress_answer)
                        st.session_state.stress_critique = critique

            if st.session_state.stress_critique:
                st.markdown("### 🔍 Evaluation of Your Reasoning:")
                st.markdown(st.session_state.stress_critique)

    # Tab 3: Feature 3 - Reverse Turing Flaw Hunter
    with tab_hunt:
        st.caption("Spot the deliberate flaw in this 90%-accurate explanation.")
        if st.button("Generate Flawed Concept Case", use_container_width=True):
            if topic_val.strip():
                with st.spinner("Crafting adversarial explanation with a subtle flaw..."):
                    st.session_state.active_flawed_case = flaw_hunter.generate_flawed_concept(topic_val)
                    st.session_state.flaw_verdict = None
            else:
                st.info("Input a topic first.")

        if st.session_state.active_flawed_case:
            fc = st.session_state.active_flawed_case
            st.markdown("<div style='background:rgba(255,255,255,0.03); padding:1rem; border-radius:12px; border:1px solid var(--card-border);'>", unsafe_allow_html=True)
            st.markdown(f"**Explanation:**\n\n> {fc.get('flawed_explanation')}")
            st.markdown("</div><br>", unsafe_allow_html=True)

            hunt_input = st.text_input("Identify the misconception or error:")
            if st.button("Verify Diagnosis"):
                if hunt_input.strip():
                    with st.spinner("Checking your diagnosis against the hidden flaw..."):
                        verdict = flaw_hunter.verify_hunt(hunt_input, fc.get("the_hidden_flaw"))
                        st.session_state.flaw_verdict = (verdict, fc)

            if st.session_state.flaw_verdict:
                v, original = st.session_state.flaw_verdict
                if v.get("found_flaw"):
                    st.success(f"🎯 **Flaw Spotted!** {v.get('feedback')}")
                else:
                    st.error(f"❌ **Missed:** {v.get('feedback')}")
                with st.expander("Reveal Full Flaw & Correct Mental Model"):
                    st.markdown(f"**Hidden Flaw:** {original.get('the_hidden_flaw')}")
                    st.markdown(f"**Proper Correction:** {original.get('correction')}")

    # Tab 4: Interactive Graph
    with tab_graph:
        if st.button("Render Knowledge Graph", use_container_width=True):
            if topic_val.strip():
                with st.spinner("Generating dependency graph..."):
                    gaps = st.session_state.eval_result.get("misconceptions", []) if st.session_state.eval_result else []
                    html_graph = graph_builder.generate_graph_html(topic_val, gaps)
                    components.html(html_graph, height=440, scrolling=False)
    st.markdown("</div>", unsafe_allow_html=True)