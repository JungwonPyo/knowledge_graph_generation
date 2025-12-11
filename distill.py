import asyncio
import json
import csv
from dataclasses import is_dataclass, asdict
from pathlib import Path

from pydantic_graph import Graph

from src.nodes import SectionDistillerNode, DocParserNode
from src.models import MyUsage, DistilledUnit, Section, Mention, Relation
from src.nodes.single_distiller import SingleDistillerNode

import networkx as nx
from pyvis.network import Network

def build_and_save_knowledge_graph(distilled: DistilledUnit, html_path: str = "kg.html"):
    G = nx.DiGraph()

    unit_id = "unit"
    G.add_node(unit_id, label=distilled.title, type="unit")
    # Add section nodes
    for si, section in enumerate(distilled.sections):
        section_id = f"section-{si}"
        G.add_node(section_id, label=section.title, type="section")
        G.add_edge(unit_id, section_id, label="HAS_SECTION")

        # Add mention nodes
        mention_ids = []
        for mi, m in enumerate(section.mentions):
            if not m.string.strip():
                continue
            mid = f"{section_id}-m-{mi}"
            G.add_node(mid, label=m.string, type=m.type)
            G.add_edge(section_id, mid, label="MENTION")
            mention_ids.append((mid, m))

        # Add relation edges
        if section.relations:
            for rel in section.relations:
                if not rel.head.strip() or not rel.tail.strip():
                    continue
                head_id = next((mid for mid, m in mention_ids if m.string == rel.head), None)
                tail_id = next((mid for mid, m in mention_ids if m.string == rel.tail), None)
                if head_id and tail_id:
                    G.add_edge(head_id, tail_id, label=rel.relation_description)

    # Visualize with pyvis
    net = Network(height="750px", width="100%", notebook=False, directed=True)
    net.from_nx(G)

    # Write HTML without trying to auto-detect notebook environment
    net.write_html(html_path, open_browser=False)
    print(f"Saved knowledge graph to {html_path}")
    
def to_plain(obj):
    # Pydantic model
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    # dataclass
    if is_dataclass(obj):
        return {k: to_plain(v) for k, v in asdict(obj).items()}
    # list / tuple
    if isinstance(obj, (list, tuple)):
        return [to_plain(v) for v in obj]
    # dict
    if isinstance(obj, dict):
        return {k: to_plain(v) for k, v in obj.items()}
    # primitive
    return obj
    
def save_distilled_to_json(distilled, path: str = "kg_structured.json"):
    # handle both BaseModel and dataclass
    if hasattr(distilled, "model_dump"):
        data = distilled.model_dump()
    else:
        # data = asdict(distilled)
        data = to_plain(distilled)
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved structured KG to {path}")

def export_kg_to_csv(distilled: DistilledUnit,
                     nodes_path: str = "kg_nodes.csv",
                     edges_path: str = "kg_edges.csv"):
    nodes = []
    edges = []

    # Unit node
    unit_id = "unit"
    nodes.append({"id": unit_id, "label": distilled.title, "type": "unit"})

    for si, section in enumerate(distilled.sections):
        section_id = f"section-{si}"
        nodes.append({"id": section_id, "label": section.title, "type": "section"})
        edges.append({"source": unit_id, "target": section_id, "label": "HAS_SECTION"})

        mention_ids = []
        for mi, m in enumerate(section.mentions):
            if not m.string.strip():
                continue
            mid = f"{section_id}-m-{mi}"
            nodes.append({"id": mid, "label": m.string, "type": m.type})
            edges.append({"source": section_id, "target": mid, "label": "MENTION"})
            mention_ids.append((mid, m))

        for rel in section.relations or []:
            if not rel.head.strip() or not rel.tail.strip():
                continue
            head_id = next((mid for mid, m in mention_ids if m.string == rel.head), None)
            tail_id = next((mid for mid, m in mention_ids if m.string == rel.tail), None)
            if head_id and tail_id:
                edges.append({
                    "source": head_id,
                    "target": tail_id,
                    "label": rel.relation_description,
                })

    # write nodes
    with open(nodes_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "label", "type"])
        writer.writeheader()
        writer.writerows(nodes)

    # write edges
    with open(edges_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["source", "target", "label"])
        writer.writeheader()
        writer.writerows(edges)

    print(f"Saved nodes to {nodes_path}, edges to {edges_path}")


sample = "temp_doc_1.txt"

with open(sample, "r", encoding="utf-8") as f:
    sample = f.read()

print(sample)

# graph = Graph(nodes=[DocParserNode, SectionDistillerNode])
graph: Graph[MyUsage, None, DistilledUnit] = Graph(
    nodes=[DocParserNode, SectionDistillerNode]
)

state = MyUsage()
# # For single shot
# state = MyUsage(requests=1, request_tokens=2803, response_tokens=3276, total_tokens=6079)
# # For multi stage
# state = MyUsage(requests=11, request_tokens=17836, response_tokens=24076, total_tokens=41912)

async def main():
    import time
    s = time.perf_counter()
    result = await graph.run(DocParserNode(sample), state=state)
    
    distilled: DistilledUnit = result.output
    final_state = result.state

    print(distilled)
    print("=========")
    print(final_state)
    print("Runtime:", time.perf_counter() - s)
    
    # After you have `distilled`, build & save a knowledge graph
    build_and_save_knowledge_graph(distilled)
    
    save_distilled_to_json(distilled)
    export_kg_to_csv(distilled)
    
asyncio.run(main())
