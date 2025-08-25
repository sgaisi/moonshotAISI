# Technical Context

## Core Technologies
- **Backend Language**: Python 3.11+
- **Web Framework**: FastAPI with Uvicorn server
- **CLI Framework**: cmd2 for command-line interface
- **Frontend**: React (separate repository: moonshot-ui-aisi)
- **Build System**: Poetry for dependency management
- **Data Format**: JSON for configuration and results

## Key Dependencies
```python
# Core dependencies from pyproject.toml
"fastapi>=0.100.0"
"uvicorn>=0.22.0" 
"pydantic>=2.0"
"datasets>=2.21.0"
"pandas>=2.2.2"
"rich>=13.0.0"  # CLI formatting
"cmd2>=2.4.0"   # CLI framework
"slugify>=0.0.1"  # ID generation
```

## Development Setup
1. **Backend Setup**:
   ```bash
   poetry install
   poetry shell
   ```

2. **Data Repository**:
   ```bash
   git clone https://github.com/sgaisi/moonshot-data-aisi.git
   ```

3. **UI Setup** (separate repo):
   ```bash
   git clone https://github.com/sgaisi/moonshot-ui-aisi.git
   cd moonshot-ui-aisi
   npm install
   npm run build
   ```

4. **Running Services**:
   ```bash
   # Backend API
   python -m moonshot web
   
   # CLI interface  
   python -m moonshot cli
   ```

## Environment Configuration
Environment variables defined in `.env`:
```bash
COOKBOOKS="./moonshot-data-aisi/cookbooks"
RECIPES="./moonshot-data-aisi/recipes"
DATASETS="./moonshot-data-aisi/datasets"
CONNECTORS_ENDPOINTS="./moonshot-data-aisi/connectors-endpoints"
RUNNERS_MODULES="./moonshot-data-aisi/runners-modules"
RESULTS_MODULES="./moonshot-data-aisi/results-modules"
TOOLS="./moonshot-data-aisi/tools"
```

## Technical Constraints
- **Python Version**: 3.11+ required for modern async features
- **Memory**: LLM operations can be memory-intensive
- **Network**: External API calls to LLM providers
- **Storage**: JSON files for persistence (no database required)
- **CORS**: Configured in FastAPI for cross-origin requests

## Testing Infrastructure
- **Unit Tests**: pytest with asyncio support
- **Integration Tests**: API endpoint testing
- **CLI Tests**: Command validation and execution
- **Coverage**: pytest-cov for test coverage reporting

## API Architecture
- **Base URL**: `http://127.0.0.1:5000/api/v1/`
- **Authentication**: Token-based for LLM endpoints
- **Error Handling**: Structured JSON error responses
- **Validation**: Pydantic schemas for request/response validation
- **Documentation**: Auto-generated OpenAPI/Swagger docs

## Frontend Integration
- **Communication**: REST API calls from React to FastAPI
- **State Management**: React hooks for state management
- **Build Process**: npm build creates static files served by backend
- **Styling**: Component-based styling (likely CSS modules or styled-components)

## Current Tool Usage Patterns
From the CLI command analysis:
- `-l agentic`: Specifies runner processing module
- `-r 1`: Random seed for reproducibility  
- Cookbook lists: `['jt3-tl-cookbook-gpt41']`
- Dataset lists: `['AISI-JT3-tl']`
- Endpoint lists: `['openai-gpt41']`
