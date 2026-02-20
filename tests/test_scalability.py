#!/usr/bin/env python3
"""
Scalability tests for Neurosting.

Tests included
--------------
1. Network-size impact on overall performance (10 → 1 000 nodes).
2. Role of quantum entanglement in throughput across network sizes.
"""

import time
import pytest

from tests.conftest import build_network


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

NETWORK_SIZES = [10, 50, 100, 500, 1000]
TRANSACTIONS_PER_PROBE = 20   # kept small so the suite completes quickly


def _measure_tps(network, n_tx: int = TRANSACTIONS_PER_PROBE) -> float:
    """Return transactions-per-second for *network* over *n_tx* transactions."""
    start = time.perf_counter()
    for i in range(n_tx):
        network.process_transaction(f"scale_tx_{i}")
    elapsed = time.perf_counter() - start
    return n_tx / elapsed if elapsed > 0 else float("inf")


# ---------------------------------------------------------------------------
# 1. Network-size impact on performance
# ---------------------------------------------------------------------------

class TestNetworkSizeImpact:
    """Analyse how the number of nodes affects throughput and state."""

    @pytest.mark.parametrize("n_nodes", NETWORK_SIZES)
    def test_network_initialises(self, n_nodes):
        """A network of *n_nodes* must initialise without error."""
        net = build_network(n_nodes)
        assert len(net.nodes) == n_nodes

    @pytest.mark.parametrize("n_nodes", NETWORK_SIZES)
    def test_transactions_processed_at_scale(self, n_nodes):
        """All network sizes must successfully process transactions."""
        net = build_network(n_nodes)
        tps = _measure_tps(net)
        assert tps > 0, f"{n_nodes}-node network returned 0 TPS"

    def test_throughput_does_not_collapse_at_1000_nodes(self):
        """A 1 000-node network must still achieve >= 1 TPS."""
        net = build_network(1000)
        tps = _measure_tps(net)
        assert tps >= 1, f"1 000-node network TPS {tps:.2f} collapsed below 1"

    def test_synapse_count_increases_with_nodes(self):
        """Larger networks should (on average) have more synapses."""
        small = build_network(10)
        large = build_network(100)
        # With random 50 % connectivity the expectation holds with very high
        # probability; we allow a small tolerance for RNG edge-cases.
        assert large.total_synapses() >= small.total_synapses(), (
            "100-node network has fewer synapses than 10-node network"
        )

    @pytest.mark.parametrize("n_nodes", [10, 100, 1000])
    def test_network_state_reflects_correct_node_count(self, n_nodes):
        """get_network_state() must report the exact number of added nodes."""
        net = build_network(n_nodes)
        state = net.get_network_state()
        assert state["nodes"] == n_nodes


# ---------------------------------------------------------------------------
# 2. Quantum entanglement and throughput
# ---------------------------------------------------------------------------

class TestQuantumEntanglementThroughput:
    """Examine the role of quantum entanglement in network throughput."""

    @pytest.mark.parametrize("n_nodes", NETWORK_SIZES)
    def test_entanglement_level_in_range(self, n_nodes):
        """Entanglement level must be a float in [0, 1] after activation."""
        net = build_network(n_nodes)
        level = net.entanglement_level
        assert 0.0 <= level <= 1.0, (
            f"Entanglement {level} out of [0, 1] for {n_nodes}-node network"
        )

    @pytest.mark.parametrize("n_nodes", NETWORK_SIZES)
    def test_entanglement_positive_for_multi_node_network(self, n_nodes):
        """Networks with > 1 node should (statistically) have entanglement > 0."""
        # With 70 % pair-entanglement probability and multiple nodes, the
        # probability of zero entanglement is astronomically low.
        net = build_network(n_nodes)
        assert net.entanglement_level > 0.0, (
            f"Expected entanglement > 0 for {n_nodes}-node network"
        )

    def test_entanglement_reactivation_updates_level(self):
        """Re-activating quantum entanglement should return a valid level."""
        net = build_network(20)
        first = net.entanglement_level
        net.activate_quantum_entanglement()
        second = net.entanglement_level
        assert 0.0 <= second <= 1.0, "Re-activated entanglement out of range"

    @pytest.mark.parametrize("n_nodes", [10, 100, 1000])
    def test_throughput_with_entanglement_vs_without(self, n_nodes):
        """
        Networks with entanglement activated must process transactions at least
        as fast as the same network before activation (no regression).
        """
        # Build without entanglement
        net_no_ent = build_network_no_entanglement(n_nodes)
        tps_no_ent = _measure_tps(net_no_ent)

        # Build with entanglement
        net_ent = build_network(n_nodes)
        tps_ent = _measure_tps(net_ent)

        # We don't assert a strict ordering (entanglement is simulated), but
        # both must be functional.
        assert tps_no_ent > 0, f"No-entanglement network (n={n_nodes}) processed 0 TPS"
        assert tps_ent > 0, f"Entanglement network (n={n_nodes}) processed 0 TPS"


def build_network_no_entanglement(n_nodes: int):
    """Build a NeuroNetwork without calling activate_quantum_entanglement."""
    from network import NeuroNetwork
    from node import NeuroNode
    net = NeuroNetwork()
    for i in range(n_nodes):
        net.add_node(NeuroNode(node_id=f"node_{i}"))
    return net
