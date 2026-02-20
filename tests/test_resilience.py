#!/usr/bin/env python3
"""
Resilience tests for Neurosting.

Tests included
--------------
1. Node crash scenarios and network recovery.
2. Error handling for invalid transactions and spontaneous node shutdowns.
"""

import pytest

from node import NeuroNode
from network import NeuroNetwork
from tests.conftest import build_network


# ---------------------------------------------------------------------------
# 1. Node crash scenarios and network recovery
# ---------------------------------------------------------------------------

class TestNodeCrashAndRecovery:
    """Simulate node crashes and verify the network recovers gracefully."""

    def test_remove_single_node_leaves_network_functional(self, small_network):
        """Removing one node must not break transaction processing."""
        node_id = next(iter(small_network.nodes))
        small_network.remove_node(node_id)
        assert node_id not in small_network.nodes
        # Network should still process transactions with remaining nodes
        result = small_network.process_transaction("post_crash_tx")
        assert result is not None

    def test_remove_all_but_one_node(self):
        """Removing all but one node should leave the last node operational."""
        net = build_network(5)
        node_ids = list(net.nodes.keys())
        for nid in node_ids[:-1]:
            net.remove_node(nid)
        assert len(net.nodes) == 1
        # Single remaining node can still attempt processing
        result = net.process_transaction("last_node_tx")
        # Result may be None if activation threshold not met; no crash is the goal
        # (no exception means success)

    def test_remove_node_cleans_up_synapses(self, small_network):
        """After removing a node, no other node should reference it."""
        victim_id = next(iter(small_network.nodes))
        small_network.remove_node(victim_id)
        for node in small_network.nodes.values():
            assert victim_id not in node.synapses, (
                f"Stale synapse to removed node {victim_id} in {node.node_id}"
            )

    def test_network_state_reflects_node_removal(self, small_network):
        """get_network_state() must report the updated node count after removal."""
        before = small_network.get_network_state()["nodes"]
        node_id = next(iter(small_network.nodes))
        small_network.remove_node(node_id)
        after = small_network.get_network_state()["nodes"]
        assert after == before - 1

    def test_mass_node_removal_then_readd(self):
        """Network should recover after mass removal and re-addition of nodes."""
        net = build_network(10)
        node_ids = list(net.nodes.keys())
        # Remove 8 out of 10
        for nid in node_ids[:8]:
            net.remove_node(nid)
        assert len(net.nodes) == 2
        # Re-add nodes
        for i in range(8):
            net.add_node(NeuroNode(node_id=f"recovered_{i}"))
        assert len(net.nodes) == 10
        result = net.process_transaction("recovery_tx")
        assert result is not None

    def test_remove_nonexistent_node_is_safe(self, small_network):
        """Removing a node that does not exist must not raise an exception."""
        small_network.remove_node("ghost_node_that_does_not_exist")

    def test_entanglement_recomputed_after_node_removal(self, small_network):
        """Entanglement should still be in [0, 1] after node removal."""
        node_id = next(iter(small_network.nodes))
        small_network.remove_node(node_id)
        small_network.activate_quantum_entanglement()
        assert 0.0 <= small_network.entanglement_level <= 1.0


# ---------------------------------------------------------------------------
# 2. Error handling for invalid transactions and spontaneous shutdowns
# ---------------------------------------------------------------------------

class TestInvalidTransactionHandling:
    """Verify robustness against malformed or edge-case inputs."""

    def test_empty_string_transaction(self, small_network):
        """An empty-string transaction must not crash the network."""
        result = small_network.process_transaction("")
        # Result may be None or a string; either is acceptable as long as no
        # exception is raised.

    def test_none_transaction(self, small_network):
        """A None payload must not crash the network."""
        small_network.process_transaction(None)

    def test_very_long_payload(self, small_network):
        """An extremely long payload (1 MB) must not crash the network."""
        payload = "x" * (1024 * 1024)
        small_network.process_transaction(payload)

    def test_bytes_payload(self, small_network):
        """A bytes payload must be handled without error."""
        small_network.process_transaction(b"\x00\xff\xab\x12")

    def test_integer_payload(self, small_network):
        """An integer payload must be handled without error."""
        small_network.process_transaction(42)

    def test_dict_payload(self, small_network):
        """A dict payload must be handled without error."""
        small_network.process_transaction({"key": "value", "amount": 100})

    def test_transaction_on_empty_network(self):
        """Processing a transaction on an empty network must return an error message."""
        net = NeuroNetwork()
        result = net.process_transaction("tx_on_empty")
        assert result is not None, "Expected a non-None response for empty network"

    def test_repeated_identical_transactions(self, small_network):
        """Sending the same payload many times must not cause errors."""
        for _ in range(50):
            small_network.process_transaction("duplicate_payload")

    def test_consensus_on_empty_network_returns_none(self):
        """get_consensus on an empty network must return None gracefully."""
        net = NeuroNetwork()
        result = net.get_consensus("some_data")
        assert result is None

    def test_consensus_on_populated_network(self, small_network):
        """get_consensus on a populated network must return a boolean."""
        result = small_network.get_consensus("vote_data")
        assert isinstance(result, bool)


class TestSpontaneousNodeShutdown:
    """Simulate spontaneous / mid-stream node shutdown scenarios."""

    def test_node_removed_during_transaction_stream(self):
        """
        Removing a node in the middle of a transaction stream must not
        interrupt subsequent transactions.
        """
        net = build_network(10)
        node_ids = list(net.nodes.keys())

        for i in range(5):
            net.process_transaction(f"pre_shutdown_{i}")

        # Simulate spontaneous shutdown of half the nodes
        for nid in node_ids[:5]:
            net.remove_node(nid)

        for i in range(5):
            net.process_transaction(f"post_shutdown_{i}")

    def test_single_node_shutdown_then_transaction(self):
        """After a single node is removed the network must still accept TXs."""
        net = build_network(3)
        first_id = next(iter(net.nodes))
        net.remove_node(first_id)
        result = net.process_transaction("after_shutdown")
        assert result is not None

    def test_node_state_reports_correctly_after_shutdown(self):
        """After removal, the deleted node must not appear in network state."""
        net = build_network(5)
        victim = next(iter(net.nodes))
        net.remove_node(victim)
        state = net.get_network_state()
        assert state["nodes"] == 4
        assert victim not in net.nodes
