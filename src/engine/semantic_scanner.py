import re
import numpy as np
from src.core.llm_client import LLMClient

class SemanticScanner:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def split_sentences(self, text: str) -> list[str]:
        # Split by periods, question marks, and exclamation points while ignoring decimals
        sentences = re.split(r'(?<=[.?!])\s+', text.strip())
        return [s.strip() for s in sentences if len(s.strip()) > 6]

    def scan_explanation(self, explanation: str, reference_text: str) -> list[dict]:
        sentences = self.split_sentences(explanation)
        if not sentences:
            return []

        # If no custom PDF uploaded, generate ground-truth consensus context
        if not reference_text or len(reference_text.strip()) < 30:
            prompt = f"Provide a dense, rigorous, factually complete summary of the core principles of: '{sentences[0]}'."
            reference_text = self.llm.generate(prompt)

        ref_emb = np.array(self.llm.get_embedding(reference_text))
        ref_norm = np.linalg.norm(ref_emb)

        results = []
        for s in sentences:
            s_emb = np.array(self.llm.get_embedding(s))
            s_norm = np.linalg.norm(s_emb)
            similarity = float(np.dot(s_emb, ref_emb) / (s_norm * ref_norm)) if (s_norm * ref_norm) > 0 else 0.0

            # Categorize based on cosine similarity
            if similarity >= 0.65:
                status = "grounded"
                label = "High Factual Density"
                bg = "rgba(16, 185, 129, 0.18)"
                border = "#10B981"
            elif similarity >= 0.48:
                status = "shallow"
                label = "Abstract / Vague"
                bg = "rgba(245, 158, 11, 0.18)"
                border = "#F59E0B"
            else:
                status = "drift"
                label = "Potential Misconception / Drift"
                bg = "rgba(239, 68, 68, 0.20)"
                border = "#EF4444"

            results.append({
                "sentence": s,
                "similarity": round(similarity, 3),
                "status": status,
                "label": label,
                "bg": bg,
                "border": border
            })
        return results

    def render_heatmap_html(self, scan_results: list[dict]) -> str:
        spans = []
        for item in scan_results:
            span = (
                f"<span style='background:{item['bg']}; border-bottom: 2px solid {item['border']}; "
                f"padding: 2px 6px; margin: 2px; border-radius: 4px; display: inline; "
                f"title='Score: {item['similarity']} - {item['label']}'>"
                f"{item['sentence']}</span>"
            )
            spans.append(span)

        legend = """
        <div style='display: flex; gap: 1rem; margin-top: 1rem; font-size: 0.78rem; font-weight: 600;'>
            <span><span style='background:#10B981; width:10px; height:10px; display:inline-block; border-radius:50%; margin-right:4px;'></span>Grounded</span>
            <span><span style='background:#F59E0B; width:10px; height:10px; display:inline-block; border-radius:50%; margin-right:4px;'></span>Shallow/Generic</span>
            <span><span style='background:#EF4444; width:10px; height:10px; display:inline-block; border-radius:50%; margin-right:4px;'></span>Drift/Flagged</span>
        </div>
        """
        container = (
            f"<div style='line-height: 2.1; font-size: 0.95rem; padding: 1.2rem; background: rgba(0,0,0,0.3); "
            f"border-radius: 14px; border: 1px solid rgba(255,255,255,0.06);'>"
            f"{' '.join(spans)}{legend}</div>"
        )
        return container