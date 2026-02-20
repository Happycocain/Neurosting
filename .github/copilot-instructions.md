# GitHub Copilot Instructions for NeuroString

## Project Overview

NeuroString is an experimental decentralized network that combines neural networks, quantum physics, and string theory concepts into a self-organizing alternative to blockchain technology. The project is written in Czech and implements a conceptual "thinking network" with bio-inspired neuronal architecture.

## Technology Stack

- **Language**: Python 3.8+
- **Web Framework**: Flask 2.3.3
- **Dependencies**: NumPy 1.24.3
- **Architecture**: Neural network simulation with quantum-inspired consensus

## Code Style & Conventions

### Language & Comments
- All code comments and docstrings must be in **Czech** (česky)
- Variable and function names should be in Czech where appropriate
- User-facing messages must be in Czech
- Example: `vytvoř_uzel()` instead of `create_node()`

### Python Style
- Follow PEP 8 conventions
- Use descriptive variable names that match the domain concepts
- Use type hints where it improves clarity
- Prefer class-based organization for major components

### Naming Patterns
- Classes: `PascalCase` (e.g., `NeuroNode`, `NeuroNetwork`)
- Functions/methods: `snake_case` (e.g., `process_data`, `add_synapse`)
- Constants: `UPPER_SNAKE_CASE`
- Private methods: prefix with `_` (e.g., `_spike`, `_data_to_vibration`)

## Architecture & Key Concepts

### Core Components

1. **NeuroNode** (`node.py`): Individual neuron in the network
   - Manages synaptic connections
   - Processes data through activation potentials
   - Implements Hebbian learning
   - Maintains quantum state

2. **NeuroNetwork** (`network.py`): Network orchestrator
   - Manages collection of nodes
   - Handles transaction processing
   - Implements quantum entanglement simulation
   - Provides consensus mechanisms

3. **StringMemory** (`memory.py`): 11-dimensional storage
   - Stores data as vibrational patterns
   - Uses frequency-based resonance matching
   - Simulates multi-dimensional data storage

4. **QuantumSimulator** (`quantum.py`): Quantum mechanics simulation
   - Simulates qubits and superposition
   - Implements quantum entanglement
   - Provides quantum random number generation

5. **Web Interface** (`web.py`): Flask-based UI
   - Provides REST API endpoints
   - Real-time network visualization
   - Interactive controls for the network

### Domain-Specific Terminology

- **Synapse** (`synapse`): Connection between nodes with strength value (0.0-1.0)
- **Vibrační vzor** (vibration pattern): How data is represented in 11D space
- **Kvantové provázání** (quantum entanglement): Network interconnectedness metric
- **Aktivační potenciál** (activation potential): Node's readiness to fire
- **Spike**: Neural impulse/signal transmitted between nodes
- **Rezonance** (resonance): Similarity metric between data patterns

## Development Guidelines

### Adding New Features

1. **Maintain the metaphor**: Keep the bio-inspired, quantum, and string theory metaphors consistent
2. **Czech-first**: All new functionality should have Czech comments and messages
3. **Simulation over accuracy**: This is a conceptual project; prioritize interesting behavior over scientific accuracy

### Testing
- Currently no formal test suite exists
- Manual testing through the web interface and CLI
- Test new features by running `python main.py` and using the interactive commands

### Running the Application

```bash
# Install dependencies (note: file is named "Requirements" not "requirements.txt")
pip install -r Requirements

# Run the application
python main.py
```

The application provides:
- CLI interface with commands: T (Transaction), S (Status), I (Info), Q (Quit)
- Web interface on port 5000

### Code Organization

- Keep files focused on single responsibilities
- Neural concepts go in `node.py` and `network.py`
- Memory/storage concepts go in `memory.py`
- Quantum mechanics simulation in `quantum.py`
- Web/API endpoints in `web.py`
- Main entry point in `main.py`

## Common Patterns

### Data Processing Flow
1. Data enters through transaction
2. Random node selected as entry point
3. Node converts data to vibrational pattern (11D hash)
4. Node processes data, potentially fires spike
5. Spike propagates through synaptic connections
6. Network learns via Hebbian learning

### Adding a New Node
```python
node = NeuroNode(node_id="custom_id")  # or auto-generated
network.add_node(node)  # automatically creates synapses
```

### Processing Data
```python
result = network.process_transaction(data)
# Returns status string in Czech
```

## Error Handling

- Use descriptive Czech error messages
- Return user-friendly status messages
- Fail gracefully with informative feedback
- Example: `"❌ Žádné uzly v síti"` instead of raising exceptions for user actions

## Dependencies Management

- Keep dependencies minimal
- Only Flask and NumPy are currently required
- Document any new dependencies in `Requirements` file
- Prefer standard library when possible

## Performance Considerations

- This is a simulation/proof-of-concept, not production code
- Optimize for clarity and interesting behavior over raw performance
- Network size is expected to be small (< 100 nodes)
- Web interface should update within reasonable time (~5 seconds)

## Security Notes

- This is an experimental project, not for production use
- No real cryptography or security is implemented
- Quantum and neural concepts are simplified simulations
- Not suitable for actual data storage or financial transactions

## Future Directions

When adding features, consider:
- More sophisticated neural learning algorithms
- Better visualization of network state
- Persistent storage of network state
- More realistic quantum simulations
- Multi-node distributed operation

## Questions or Issues?

When unsure about implementation details:
1. Follow existing patterns in the codebase
2. Maintain Czech language for user-facing content
3. Keep the bio-inspired metaphor consistent
4. Prioritize code clarity and interesting behavior
