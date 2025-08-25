# System Architecture & Patterns

## Overall Architecture
Moonshot AI follows a modular, service-oriented architecture:

```
Frontend (React UI) ←→ Web API (FastAPI) ←→ Core Engine ←→ Data Repository
     ↓                       ↓                    ↓              ↓
moonshot-ui-aisi    moonshot/integrations/  moonshot/src/  moonshot-data-aisi
                         web_api/
```

## Key Design Patterns

### 1. Runner Pattern
- **Core Concept**: All test execution goes through "Runners" 
- **Types**: `BENCHMARK`, `REDTEAM`, `AGENTIC` (enum in `runner_type.py`)
- **Implementation**: Async execution with progress tracking
- **Location**: `moonshot/src/runners/`

### 2. Module Processing Pattern
- **Runner Processing**: `-l agentic` specifies runner processing module
- **Result Processing**: `-o result_proc_module` handles output formatting
- **Location**: `moonshot-data-aisi/runners-modules/` and `results-modules/`

### 3. API Layer Pattern
**CLI Integration**: `moonshot/integrations/cli/`
- Commands parsed and routed to appropriate handlers
- Structured argument parsing with `cmd2.Cmd2ArgumentParser`

**Web API Integration**: `moonshot/integrations/web_api/`
- FastAPI routes in `/routes/` directory
- Services layer in `/services/` for business logic
- DTOs/schemas in `/schemas/` for data validation

### 4. Data Management Pattern
**Environment-based Configuration**:
```
COOKBOOKS="./moonshot-data-aisi/cookbooks"
RECIPES="./moonshot-data-aisi/recipes"  
DATASETS="./moonshot-data-aisi/datasets"
ENDPOINTS="./moonshot-data-aisi/connectors-endpoints"
```

**Storage Pattern**:
- JSON-based configuration files
- Generated outputs in `generated-outputs/`
- Modular plugin system for connectors, metrics, etc.

## Component Relationships

### Cookbook → Recipe → Dataset Flow
1. **Cookbook**: Collection of recipes (`run_cookbook` command)
2. **Recipe**: Test definition with datasets, metrics, prompt templates
3. **Dataset**: Actual test data (prompts and expected responses)
4. **Metrics**: Evaluation criteria for responses

### Missing Agentic Integration Points
1. **Web API Routes**: No `agentic.py` in `/routes/` (benchmarking and redteam exist)
2. **Frontend Components**: UI needs agentic section matching benchmarking flow
3. **Service Layer**: Missing agentic service class in `/services/`

## Critical Implementation Paths

### Benchmarking Flow (Template to Follow)
1. **Frontend**: User selects cookbooks/endpoints → configuration form
2. **API**: `POST /api/v1/benchmarks` → validation → runner creation
3. **Backend**: Async cookbook execution → progress updates → results
4. **Results**: Formatted output display in UI

### Required Agentic Flow (To Implement)
1. **Frontend**: New agentic section with cookbook selection
2. **API**: New `POST /api/v1/agentic` endpoint  
3. **Backend**: Use existing agentic runner with `-l agentic` flag
4. **Results**: Compatible results display

## Technical Constraints
- **Async Execution**: All test runs must be non-blocking
- **Progress Tracking**: Real-time updates via WebSocket or polling
- **Error Handling**: Graceful failure with detailed error messages
- **Resource Management**: Proper cleanup of runners and connections
