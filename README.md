# lightrag-tutorial

LightRAG tutorial

# Install

```bash
pip install -r requirements.txt

git clone https://github.com/HKUDS/LightRAG.git
cd LightRAG
pip install -e .
```

# Experiment result

1. GraphRAG vs LightRAG
   - Question: `What is the difference between GraphRAG vs LightRAG? Answer in Korean.`
   - Code: `playground/paper_demo.py`
   - Input:
     - `data/graph-1, result-1`: GraphRAG paper
     - `data/graph-2, result-2`: LightRAG paper
     - `data/graph-12, result-12`: GraphRAG paper + LightRAG paper
