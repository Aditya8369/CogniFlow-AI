from pyvis.network import Network
import tempfile
from src.core.llm_client import LLMClient

class InteractiveGraphBuilder:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def generate_graph_html(self, topic: str, gaps: list[str]) -> str:
        gaps_str = ", ".join(gaps) if gaps else "None"
        prompt = f"""
        Topic: {topic}
        Identified Gaps / Misconceptions: {gaps_str}

        Deconstruct this topic into a 6 to 10 node concept dependency graph.
        Label which nodes represent the student's weak points (status: "gap") vs understood concepts (status: "mastered").
        
        Output strictly JSON:
        {{
            "nodes": [
                {{"id": "1", "label": "Concept Name", "status": "mastered"}},
                {{"id": "2", "label": "Confused Concept", "status": "gap"}}
            ],
            "edges": [
                {{"from": "1", "to": "2", "label": "leads to"}}
            ]
        }}
        """
        graph_data = self.llm.generate_json(prompt, schema={})
        
        net = Network(height="450px", width="100%", bgcolor="#0E1117", font_color="white", directed=True)
        net.force_atlas_2based()

        nodes = graph_data.get("nodes", [])
        edges = graph_data.get("edges", [])

        for node in nodes:
            is_gap = node.get("status") == "gap"
            color = "#FF4B4B" if is_gap else "#00CC96"
            title_text = "Needs Review" if is_gap else "Mastered / Understood"
            net.add_node(
                node["id"],
                label=node.get("label", node["id"]),
                color=color,
                title=title_text,
                size=22
            )

        for edge in edges:
            net.add_edge(edge["from"], edge["to"], title=edge.get("label", ""), color="#888888")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode="w", encoding="utf-8") as f:
            net.save_graph(f.name)
            temp_path = f.name

        with open(temp_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        return html_content