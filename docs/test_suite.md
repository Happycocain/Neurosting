# Neurosting Test Suite Documentation

## Overview

This document describes the automated pytest test suite for the Neurosting project.
The suite evaluates three key areas:

| Area | Module | Tests |
|------|--------|-------|
| Performance | `tests/test_performance.py` | 8 |
| Scalability | `tests/test_scalability.py` | 27 |
| Resilience | `tests/test_resilience.py` | 22 |

---

## Setup

### Prerequisites

| Tool | Minimum version |
|------|----------------|
| Python | 3.10 |
| pytest | 7.0 |
| numpy | 1.24 |

### Install dependencies

```bash
pip install pytest numpy flask
```

> Flask and NumPy are required by the Neurosting source modules; they are not
> needed by the test runner directly.

---

## Running the tests

### All tests

```bash
# From the repository root
pytest tests/ -v
```

### Single category

```bash
pytest tests/test_performance.py -v   # performance only
pytest tests/test_scalability.py -v   # scalability only
pytest tests/test_resilience.py  -v   # resilience only
```

### Quick smoke run (skip slow parametrised cases)

```bash
pytest tests/ -v -k "not 1000"
```

---

## Test cases

### Performance (`test_performance.py`)

#### `TestTransactionProcessingTime`

| Test | Description | Pass criterion |
|------|-------------|---------------|
| `test_single_transaction_completes` | Submits one TX and checks a result is returned | Result is not `None` |
| `test_single_transaction_latency` | Measures end-to-end time for one TX | < 1 second |
| `test_average_latency_over_100_transactions` | Runs 100 sequential TXs and averages latency | Mean < 100 ms |
| `test_transaction_history_updated` | Sends 20 TXs and checks history grows | `len(history)` increases |

#### `TestThroughput`

| Test | Description | Pass criterion |
|------|-------------|---------------|
| `test_throughput_not_zero` | Counts TXs processed in a 2-second window | TPS > 0 |
| `test_throughput_10_tps_minimum` | Same window, stricter threshold | TPS ≥ 10 |
| `test_high_volume_no_crash` | Submits 1,000 TXs in a loop | No exception |
| `test_memory_growth_under_load` | Sends 200 TXs and checks `memory_patterns` | Non-decreasing |

---

### Scalability (`test_scalability.py`)

Network sizes tested: **10, 50, 100, 500, 1 000 nodes**.

#### `TestNetworkSizeImpact`

| Test | Description | Pass criterion |
|------|-------------|---------------|
| `test_network_initialises[N]` | Builds a network of N nodes | `len(nodes) == N` |
| `test_transactions_processed_at_scale[N]` | Measures TPS for each size | TPS > 0 |
| `test_throughput_does_not_collapse_at_1000_nodes` | Stress-tests 1,000-node network | TPS ≥ 1 |
| `test_synapse_count_increases_with_nodes` | Compares 10 vs 100-node synapse counts | 100-node ≥ 10-node |
| `test_network_state_reflects_correct_node_count[N]` | Validates `get_network_state()` | `state["nodes"] == N` |

#### `TestQuantumEntanglementThroughput`

| Test | Description | Pass criterion |
|------|-------------|---------------|
| `test_entanglement_level_in_range[N]` | Checks entanglement after activation | ∈ [0, 1] |
| `test_entanglement_positive_for_multi_node_network[N]` | Ensures >0 entanglement for multi-node nets | > 0.0 |
| `test_entanglement_reactivation_updates_level` | Re-activates entanglement on a 20-node net | ∈ [0, 1] |
| `test_throughput_with_entanglement_vs_without[N]` | Compares TPS with/without entanglement | Both > 0 TPS |

---

### Resilience (`test_resilience.py`)

#### `TestNodeCrashAndRecovery`

| Test | Description | Pass criterion |
|------|-------------|---------------|
| `test_remove_single_node_leaves_network_functional` | Removes 1 of 5 nodes; processes TX | Result not `None` |
| `test_remove_all_but_one_node` | Removes 4 of 5; last node survives | No exception |
| `test_remove_node_cleans_up_synapses` | Checks no dangling synapse references | All synapse maps clean |
| `test_network_state_reflects_node_removal` | Validates node count in state dict | Count decremented by 1 |
| `test_mass_node_removal_then_readd` | Removes 8/10 nodes then re-adds them | Network operational |
| `test_remove_nonexistent_node_is_safe` | Removes a ghost node ID | No exception |
| `test_entanglement_recomputed_after_node_removal` | Re-activates entanglement post-removal | ∈ [0, 1] |

#### `TestInvalidTransactionHandling`

| Test | Description | Pass criterion |
|------|-------------|---------------|
| `test_empty_string_transaction` | Submits `""` | No exception |
| `test_none_transaction` | Submits `None` | No exception |
| `test_very_long_payload` | Submits 1 MB string | No exception |
| `test_bytes_payload` | Submits raw bytes | No exception |
| `test_integer_payload` | Submits integer `42` | No exception |
| `test_dict_payload` | Submits a dict | No exception |
| `test_transaction_on_empty_network` | TX on zero-node network | Non-`None` error message |
| `test_repeated_identical_transactions` | Same payload 50 times | No exception |
| `test_consensus_on_empty_network_returns_none` | `get_consensus` on empty net | Returns `None` |
| `test_consensus_on_populated_network` | `get_consensus` on live net | Returns `bool` |

#### `TestSpontaneousNodeShutdown`

| Test | Description | Pass criterion |
|------|-------------|---------------|
| `test_node_removed_during_transaction_stream` | Removes 5/10 nodes mid-stream; continues TXs | No exception |
| `test_single_node_shutdown_then_transaction` | Removes 1/3 nodes; sends TX | Result not `None` |
| `test_node_state_reports_correctly_after_shutdown` | Checks state dict after removal | `nodes == 4`, removed ID absent |

---

## Fixtures (`tests/conftest.py`)

| Fixture | Description |
|---------|-------------|
| `single_node` | A fresh `NeuroNode` with id `"test_node"` |
| `small_network` | `NeuroNetwork` with 5 nodes + entanglement activated |
| `medium_network` | `NeuroNetwork` with 50 nodes + entanglement activated |
| `build_network(n)` | Helper function returning a network of n nodes |

---

## Interpreting results

```
57 passed in 5.86s
```

All tests must pass with exit code `0`. A failure indicates a regression in
the corresponding area:

* **Performance failures** — the network has become slower; profile
  `NeuroNetwork.process_transaction` and `NeuroNode.process_data`.
* **Scalability failures** — large-network construction or entanglement
  calculation is broken; check `NeuroNetwork.add_node` and
  `activate_quantum_entanglement`.
* **Resilience failures** — error handling or cleanup logic is broken; inspect
  `NeuroNetwork.remove_node`, `process_transaction`, and `get_consensus`.
