#!/usr/bin/env python3
"""
Shared pytest fixtures for the Neurosting test suite.
"""

import sys
import os
import pytest

# Ensure the project root is on the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from node import NeuroNode
from network import NeuroNetwork


@pytest.fixture
def single_node():
    """Return a fresh NeuroNode."""
    return NeuroNode(node_id="test_node")


@pytest.fixture
def small_network():
    """Return a NeuroNetwork with 5 nodes and quantum entanglement activated."""
    net = NeuroNetwork()
    for i in range(5):
        net.add_node(NeuroNode(node_id=f"node_{i}"))
    net.activate_quantum_entanglement()
    return net


@pytest.fixture
def medium_network():
    """Return a NeuroNetwork with 50 nodes and quantum entanglement activated."""
    net = NeuroNetwork()
    for i in range(50):
        net.add_node(NeuroNode(node_id=f"node_{i}"))
    net.activate_quantum_entanglement()
    return net


def build_network(n_nodes: int) -> NeuroNetwork:
    """Helper: build a fresh NeuroNetwork with *n_nodes* nodes."""
    net = NeuroNetwork()
    for i in range(n_nodes):
        net.add_node(NeuroNode(node_id=f"node_{i}"))
    net.activate_quantum_entanglement()
    return net
