# knowledge_graph_generation

# Code Structure
```
src/
│
├── agents/                        # AI agents handling specific tasks in the pipeline
│   ├── __init__.py
│   ├── _agent_registry.py        # Registry to manage agent instances
│   ├── _base.py                  # Base LLM model for all agents
│   ├── doc_parser_agent.py       # Agent for document parsing
│   ├── dynamic_relation_extractor_agent.py  # Agent for extracting relations dynamically
│   ├── section_distiller_agent.py  # Agent for distilling document sections
│   └── single_distiller_agent.py   # Single Agent distillation system
│
├── config/                        # Configuration ollama setting
│   ├── __init__.py
│
├── models/                        # Data models, enums, and schema definitions
│   ├── __init__.py
│   ├── enum.py                    # Custom enums used across the project
│   ├── schema.py                  # Pydantic or custom schema definitions
│   └── state.py                   # State management models
│
├── nodes/                         # Modular processing nodes used by agents or pipelines
│   ├── __init__.py
│   ├── doc_parser.py              # Node logic for document parsing
│   ├── section_distiller.py       # Node logic for section distillation
│   └── single_distiller.py        # Node logic for single agent distillation
│
├── prompts/                       # Prompt templates used by LLM agents
│   ├── __init__.py
│   ├── doc_parser_prompt.py       # Prompts for document parser agent
│   ├── dynamic_relation_extractor_prompt.py # Prompts for relation extractor
│   ├── section_distiller_prompt.py # Prompts for section distiller
│   └── single_distiller_agent.py  # Prompts for single agent (first approach)
│
├── __init__.py
├── _utils.py                      # Utility functions
└── distill.py                     # Main script or entry point to run distillation pipeline
```

# Installation
```bash
conda install pydantic -c conda-forge

pip install pydantic-ai
# or
pip install "pydantic-ai-slim[openai]"

pip install pydantic-graph

pip install pyvis
```

To use Open-AI models, visit https://platform.openai.com and generate API key, and set this to
```bash
export OPENAI_API_KEY='your-api-key'
```

To use free Ollama locally using Pydantic, 
```bash
sudo snap install ollama
# Open serve
ollama serve
# Check running
curl http://127.0.0.1:11434 # 'Ollama is running(react)' if running

# Run llama3.1:8b model, need to change model name in agents/_base.py
ollama run llama3.1:8b

# Run qwen3:8b model, need to change model name in agents/_base.py
ollama run qwen3:8b
```

# References
- https://jupyter2607.medium.com/part-2a-update-implementing-a-graph-builder-agent-for-document-based-knowledge-graphs-with-c372497ecc24
- https://medium.com/the-muse-junction/how-to-build-knowledge-graphs-using-llms-on-local-machines-5926261c04eb