"""
- Reference: https://python.langchain.com/docs/integrations/document_loaders/source_code/
"""

import os
import random
from os.path import abspath, join, dirname

import networkx as nx
from pyvis.network import Network
from lightrag import LightRAG, QueryParam
from lightrag.llm import gpt_4o_mini_complete

from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser

# from langchain_text_splitters import Language

from pathlib import Path


def insert_repositories(rag, code_paths: list[str]) -> None:
    """Insert repository files into the graph."""

    def extract_text(doc, base_path: str) -> str:
        clean_path = lambda path: Path(path).relative_to(base_path).as_posix()
        metadata = "# " + "\n# ".join(
            [
                f"{k}: {clean_path(v) if k == 'source' else v}"
                for k, v in doc.metadata.items()
            ]
        )
        return f"{metadata}\n\n{doc.page_content}"

    texts = []
    for path in code_paths:
        loader = GenericLoader.from_filesystem(
            path,
            glob="*/**/*",
            suffixes=[".py"],
            parser=LanguageParser(),
        )
        docs = loader.load()
        texts.extend([extract_text(doc, dirname(path)) for doc in docs])
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


CODE_PATHS = [join(dirname(dirname(abspath(__file__))), "LightRAG", "lightrag")]
ROOT_DIR = join(dirname(dirname(abspath(__file__))), "data")
GRAPH_DIR = join(ROOT_DIR, "graph")
RESULT_DIR = join(ROOT_DIR, "result")

os.makedirs(GRAPH_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)


rag = LightRAG(
    working_dir=GRAPH_DIR,
    llm_model_func=gpt_4o_mini_complete,
)
insert_repositories(rag, CODE_PATHS)
visualize_graph(GRAPH_DIR)


query = "LightRAG가 어떻게 동작해?"


# Perform naive search
for mode in ("naive", "local", "global", "hybrid"):
    result = rag.query(query, param=QueryParam(mode=mode))
    with open(join(RESULT_DIR, f"result_{mode}.txt"), "w", encoding="utf-8") as f:
        f.write(result)
        print(f"Result of '{mode}' mode has been successfully saved.")
