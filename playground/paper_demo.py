import os
import random
from os.path import join

import networkx as nx
from pypdf import PdfReader
from pyvis.network import Network
from lightrag import LightRAG, QueryParam
from lightrag.llm import gpt_4o_mini_complete

from src.core.loader import ls_file


def insert_pdf(rag, pdf_dir: str) -> None:
    """Insert PDF files into the graph."""
    texts = []
    for path in ls_file(pdf_dir):
        reader = PdfReader(path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        texts.append(text)

    # Select only one
    texts = [texts[1]]

    rag.insert(texts)


def visualize_graph(graph_dir: str) -> None:
    # Load the GraphML file
    G = nx.read_graphml(join(graph_dir, "graph_chunk_entity_relation.graphml"))

    # Create a Pyvis network
    net = Network(height="100vh", notebook=True)

    # Convert NetworkX graph to Pyvis network
    net.from_nx(G)

    # Add colors to nodes
    for node in net.nodes:
        node["color"] = "#{:06x}".format(random.randint(0, 0xFFFFFF))

    # Save and display the network
    net.show(join(graph_dir, "knowledge_graph.html"))


DATA_DIR = "data"
PDF_DIR = join(DATA_DIR, "pdf")
GRAPH_DIR = join(DATA_DIR, "graph-12")
RESULT_DIR = join(DATA_DIR, "result")

os.makedirs(GRAPH_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)


rag = LightRAG(
    working_dir=GRAPH_DIR,
    llm_model_func=gpt_4o_mini_complete,
)
# insert_pdf(rag, PDF_DIR)
visualize_graph(GRAPH_DIR)


query = "What is the difference between GraphRAG vs LightRAG? Answer in Korean."

# Perform naive search
for mode in ("naive", "local", "global", "hybrid"):
    result = rag.query(query, param=QueryParam(mode=mode))
    with open(join(RESULT_DIR, f"result_{mode}.txt"), "w", encoding="utf-8") as f:
        f.write(result)
        print(f"Result of '{mode}' mode has been successfully saved.")
