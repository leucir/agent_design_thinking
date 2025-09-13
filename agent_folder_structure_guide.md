# Agent Folder Structure Guide

This guide outlines a standardized folder structure for building AI agents using LangGraph and related frameworks. This structure promotes modularity, maintainability, and clear separation of concerns.

## Folder Structure Overview

```
agent_name/
├── main.py                    # Entry point and usage examples
├── agent_name_agent.py        # Main agent class and workflow logic
├── models.py                  # LLM model configurations
├── state.py                   # State management and TypedDict definitions
├── prompts.py                 # Prompt templates and formatting functions
├── tools.py                   # External tool integrations (APIs, search, etc.)
├── structured_outputs.py      # Pydantic models for structured outputs (STANDARDIZED NAME)
├── config.py                  # Configuration settings and parameters
├── state_helper.py            # Helper functions for state manipulation
├── utils.py                   # General utility functions
├── tests/                     # NEW: Test files
│   ├── test_agent.py
│   ├── test_tools.py
│   └── test_state.py
├── examples/                  # NEW: Usage examples
│   ├── basic_usage.py
│   └── advanced_usage.py
├── docs/                      # NEW: Additional documentation
│   ├── workflow.md
│   └── api_reference.md
├── README.md                  # Documentation and workflow diagrams
└── __pycache__/              # Python cache (auto-generated)
```

## File Descriptions and Purposes

### Core Agent Files

#### `main.py`
**Purpose**: Entry point and usage examples
- Contains the main execution function
- Demonstrates how to initialize and use the agent
- Provides example usage patterns
- Handles result formatting and display
- **Key responsibilities**: Agent instantiation, example problems, result presentation

#### `agent_name_agent.py`
**Purpose**: Main agent class and workflow logic
- Defines the primary agent class
- Implements the LangGraph workflow with nodes and edges
- Contains all node functions (entry, processing, validation, etc.)
- Handles routing logic between nodes
- Manages the overall agent execution flow
- **Key responsibilities**: Workflow definition, node implementation, routing decisions

### Configuration and Models

#### `models.py`
**Purpose**: LLM model configurations
- Defines available language models (OpenAI, local models, etc.)
- Configures model parameters (temperature, max_tokens, etc.)
- Sets up embedding models for vector operations
- Manages API keys and endpoints
- **Key responsibilities**: Model instantiation, configuration management, API setup

#### `config.py`
**Purpose**: Configuration settings and parameters
- Contains agent-specific configuration
- Defines tool settings (web search, API limits, etc.)
- Sets graph parameters (recursion limits, timeouts)
- Manages debug and logging settings
- **Key responsibilities**: Centralized configuration, environment-specific settings

### State Management

#### `state.py`
**Purpose**: State management and TypedDict definitions
- Defines the agent's state structure using TypedDict
- Specifies all state variables and their types
- Documents state transitions and data flow
- Ensures type safety across the workflow
- **Key responsibilities**: State schema definition, type safety, data structure

#### `state_helper.py`
**Purpose**: Helper functions for state manipulation
- Provides utility functions for state operations
- Implements state validation and transformation logic
- Contains decision-making helpers (should_continue, etc.)
- Manages state updates and iterations
- **Key responsibilities**: State manipulation, validation logic, decision helpers

### Prompting and Output

#### `prompts.py`
**Purpose**: Prompt templates and formatting functions
- Contains all system prompts and templates
- Implements prompt formatting functions
- Manages context injection and variable substitution
- Organizes prompts by workflow stage
- **Key responsibilities**: Prompt management, template formatting, context handling

#### `structure_outputs.py`
**Purpose**: Pydantic models for structured outputs
- Defines Pydantic models for each node's output
- Ensures consistent data structure across the workflow
- Provides validation for LLM responses
- Documents expected output formats
- **Key responsibilities**: Output validation, data structure enforcement, type safety

### External Integrations

#### `tools.py`
**Purpose**: External tool integrations
- Implements external API integrations (web search, databases, etc.)
- Handles tool-specific configuration and error handling
- Provides data processing and filtering functions
- Manages tool-specific output formatting
- **Key responsibilities**: External integrations, API management, data processing

### Utilities

#### `utils.py`
**Purpose**: General utility functions
- Contains reusable utility functions
- Implements common operations (text processing, visualization, etc.)
- Provides helper functions for data manipulation
- Manages external library integrations
- **Key responsibilities**: Common utilities, data processing, visualization helpers

### Documentation

#### `README.md`
**Purpose**: Documentation and workflow diagrams
- Provides agent overview and usage instructions
- Contains workflow diagrams (Mermaid or ASCII art)
- Documents configuration requirements
- Explains the agent's purpose and capabilities
- **Key responsibilities**: Documentation, workflow visualization, usage guidance

## Best Practices

### 1. Separation of Concerns
- Keep business logic in the main agent file
- Separate configuration from implementation
- Isolate external integrations in tools
- Maintain clear boundaries between components

### 2. Type Safety
- Use TypedDict for state definitions
- Implement Pydantic models for structured outputs
- Add type hints throughout the codebase
- Validate inputs and outputs consistently

### 3. Configuration Management
- Centralize all configuration in `config.py`
- Use environment variables for sensitive data
- Provide sensible defaults for all settings
- Document configuration options clearly

### 4. Error Handling
- Implement comprehensive error handling in each node
- Provide meaningful error messages
- Include retry logic where appropriate
- Log errors for debugging purposes

### 5. Testing and Validation
- Include validation logic in state helpers
- Implement quality checks for outputs
- Provide debugging and monitoring capabilities
- Document expected behaviors and edge cases

### 6. Documentation
- Maintain clear README with usage examples
- Document workflow diagrams
- Explain configuration requirements
- Provide troubleshooting guidance

## Implementation Guidelines

### Starting a New Agent
1. Create the folder structure
2. Define the state schema in `state.py`
3. Implement basic prompts in `prompts.py`
4. Create structured output models
5. Build the main agent workflow
6. Add configuration and tools
7. Implement utilities and helpers
8. Create documentation and examples

### Maintenance
- Keep prompts updated and well-documented
- Monitor and update configuration as needed
- Regularly review and optimize tool integrations
- Maintain comprehensive error handling
- Update documentation with changes

This structure provides a solid foundation for building maintainable, scalable AI agents while promoting code reusability and clear separation of concerns.

