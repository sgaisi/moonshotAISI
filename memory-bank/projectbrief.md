# Moonshot AI Project Brief

## Project Overview
Moonshot AI is a comprehensive LLM testing and evaluation platform with three main operational modes:
1. **Benchmarking** - Model performance evaluation against standard datasets
2. **Red Teaming** - Security and safety testing through adversarial prompting  
3. **Agentic** - Testing of agentic AI capabilities (partially implemented)

## Current Task
Add a new "Agentic" section to the UI that follows the same styling and flow as the existing "Benchmarking" section. The agentic functionality already exists in the backend but needs to be fully integrated into the web interface.

## Architecture
- **Backend**: Python-based with CLI and Web API (FastAPI)
- **Frontend**: React-based UI in separate repository (`moonshot-ui-aisi`)
- **Data**: External data repository (`moonshot-data-aisi`) containing cookbooks, recipes, datasets
- **Structure**: Modular design with separate integrations for CLI and Web API

## Key Requirements
1. Follow existing benchmarking section patterns
2. Integrate existing agentic CLI functionality into UI
3. Support dynamic cookbook and LLM selection
4. No hard-coding of cookbooks - they should be discovered from data folder
5. Maintain consistent styling and user experience

## Target Command Integration
The CLI command that needs UI integration:
```bash
python -m moonshot cli "run_cookbook -l agentic -r 1 ['jt3-tl-cookbook-gpt41'] ['AISI-JT3-tl'] ['openai-gpt41']"
```

## Success Criteria
- Agentic section available in UI navigation
- Can select from available agentic cookbooks dynamically
- Can select from available LLM endpoints
- Can configure and run agentic tests through UI
- Results displayed similar to benchmarking results
