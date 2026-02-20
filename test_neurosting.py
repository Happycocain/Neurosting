#!/usr/bin/env python3
"""
NeuroString – Komplexní sada testů (pytest)
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))


# ---------------------------------------------------------------------------
# NeuroNode tests
# ---------------------------------------------------------------------------

class TestNeuroNode:
    def test_default_id(self):
        from node import NeuroNode
        node = NeuroNode()
        assert node.node_id.startswith("node_")

    def test_custom_id(self):
        from node import NeuroNode
        node = NeuroNode(node_id="test_node")
        assert node.node_id == "test_node"

    def test_initial_state(self):
        from node import NeuroNode
        node = NeuroNode(node_id="n1")
        assert isinstance(node.synapses, dict)
        assert isinstance(node.memory, dict)
        assert 0.1 <= node.activation_potential <= 1.0
        assert node.spike_count == 0

    def test_add_synapse(self):
        from node import NeuroNode
        node = NeuroNode(node_id="n1")
        node.add_synapse("n2")
        assert "n2" in node.synapses
        assert 0.3 <= node.synapses["n2"] <= 0.7

    def test_remove_synapse(self):
        from node import NeuroNode
        node = NeuroNode(node_id="n1")
        node.add_synapse("n2")
        node.remove_synapse("n2")
        assert "n2" not in node.synapses

    def test_remove_nonexistent_synapse(self):
        from node import NeuroNode
        node = NeuroNode(node_id="n1")
        # Should not raise an exception
        node.remove_synapse("nonexistent")

    def test_learn_strengthen(self):
        from node import NeuroNode
        node = NeuroNode(node_id="n1")
        node.add_synapse("n2")
        initial = node.synapses["n2"]
        node.learn("n2", True)
        assert node.synapses["n2"] >= initial

    def test_learn_weaken(self):
        from node import NeuroNode
        node = NeuroNode(node_id="n1")
        node.add_synapse("n2")
        initial = node.synapses["n2"]
        node.learn("n2", False)
        assert node.synapses["n2"] <= initial

    def test_learn_caps_at_one(self):
        from node import NeuroNode
        node = NeuroNode(node_id="n1")
        node.synapses["n2"] = 0.99
        for _ in range(20):
            node.learn("n2", True)
        assert node.synapses["n2"] <= 1.0

    def test_learn_floor_at_zero(self):
        from node import NeuroNode
        node = NeuroNode(node_id="n1")
        node.synapses["n2"] = 0.01
        for _ in range(20):
            node.learn("n2", False)
        assert node.synapses["n2"] >= 0.0

    def test_process_data_increments_spike_count(self):
        from node import NeuroNode
        node = NeuroNode(node_id="n1")
        node.activation_potential = 1.0  # ensure spike
        node.process_data("hello")
        assert node.spike_count == 1

    def test_process_data_returns_spike_or_none(self):
        from node import NeuroNode
        node = NeuroNode(node_id="n1")
        node.activation_potential = 1.0
        result = node.process_data("test data")
        # Either a dict (spike fired) or None (potential too low)
        assert result is None or isinstance(result, dict)

    def test_spike_contains_required_keys(self):
        from node import NeuroNode
        node = NeuroNode(node_id="n1")
        node.activation_potential = 1.0
        result = node.process_data("trigger")
        if result is not None:
            assert "from" in result
            assert "vibration" in result
            assert "timestamp" in result
            assert "strength" in result

    def test_get_state_keys(self):
        from node import NeuroNode
        node = NeuroNode(node_id="n1")
        state = node.get_state()
        for key in ("id", "age", "synapses", "spike_count", "activation", "quantum_state"):
            assert key in state

    def test_str_representation(self):
        from node import NeuroNode
        node = NeuroNode(node_id="n1")
        assert "n1" in str(node)

    def test_quantum_state_keys(self):
        from node import NeuroNode
        node = NeuroNode(node_id="n1")
        qs = node.quantum_state
        assert "superposition" in qs
        assert "entanglement" in qs
        assert "vibration_freq" in qs


# ---------------------------------------------------------------------------
# NeuroNetwork tests
# ---------------------------------------------------------------------------

class TestNeuroNetwork:
    def test_initial_state(self):
        from network import NeuroNetwork
        net = NeuroNetwork()
        assert net.nodes == {}
        assert net.transaction_history == []
        assert net.entanglement_level == 0.0
        assert net.memory_patterns == 0

    def test_add_node(self):
        from network import NeuroNetwork
        from node import NeuroNode
        net = NeuroNetwork()
        node = NeuroNode(node_id="n1")
        net.add_node(node)
        assert "n1" in net.nodes

    def test_add_multiple_nodes(self):
        from network import NeuroNetwork
        from node import NeuroNode
        net = NeuroNetwork()
        for i in range(3):
            net.add_node(NeuroNode(node_id=f"n{i}"))
        assert len(net.nodes) == 3

    def test_remove_node(self):
        from network import NeuroNetwork
        from node import NeuroNode
        net = NeuroNetwork()
        node = NeuroNode(node_id="n1")
        net.add_node(node)
        net.remove_node("n1")
        assert "n1" not in net.nodes

    def test_remove_node_cleans_synapses(self):
        from network import NeuroNetwork
        from node import NeuroNode
        net = NeuroNetwork()
        n1 = NeuroNode(node_id="n1")
        n2 = NeuroNode(node_id="n2")
        net.add_node(n1)
        net.add_node(n2)
        n1.add_synapse("n2")
        net.remove_node("n2")
        assert "n2" not in n1.synapses

    def test_remove_nonexistent_node(self):
        from network import NeuroNetwork
        net = NeuroNetwork()
        # Should not raise
        net.remove_node("ghost")

    def test_activate_quantum_entanglement_single_node(self):
        from network import NeuroNetwork
        from node import NeuroNode
        net = NeuroNetwork()
        net.add_node(NeuroNode(node_id="n1"))
        net.activate_quantum_entanglement()
        assert net.entanglement_level == 0.0

    def test_activate_quantum_entanglement_multiple_nodes(self):
        from network import NeuroNetwork
        from node import NeuroNode
        net = NeuroNetwork()
        for i in range(4):
            net.add_node(NeuroNode(node_id=f"n{i}"))
        net.activate_quantum_entanglement()
        assert 0.0 <= net.entanglement_level <= 1.0

    def test_process_transaction_no_nodes(self):
        from network import NeuroNetwork
        net = NeuroNetwork()
        result = net.process_transaction("data")
        # No nodes available – should return a non-empty string error message
        assert isinstance(result, str) and len(result) > 0

    def test_process_transaction_with_nodes(self):
        from network import NeuroNetwork
        from node import NeuroNode
        net = NeuroNetwork()
        for i in range(3):
            net.add_node(NeuroNode(node_id=f"n{i}"))
        result = net.process_transaction("test_data")
        assert isinstance(result, str)

    def test_total_synapses(self):
        from network import NeuroNetwork
        from node import NeuroNode
        net = NeuroNetwork()
        n1 = NeuroNode(node_id="n1")
        n2 = NeuroNode(node_id="n2")
        net.add_node(n1)
        net.add_node(n2)
        total = net.total_synapses()
        assert total >= 0

    def test_get_network_state_keys(self):
        from network import NeuroNetwork
        net = NeuroNetwork()
        state = net.get_network_state()
        for key in ("nodes", "synapses", "transactions", "entanglement", "memory_patterns"):
            assert key in state

    def test_get_consensus_empty(self):
        from network import NeuroNetwork
        net = NeuroNetwork()
        assert net.get_consensus("data") is None

    def test_get_consensus_with_nodes(self):
        from network import NeuroNetwork
        from node import NeuroNode
        net = NeuroNetwork()
        for i in range(5):
            net.add_node(NeuroNode(node_id=f"n{i}"))
        result = net.get_consensus("data")
        assert result in (True, False)


# ---------------------------------------------------------------------------
# StringMemory tests
# ---------------------------------------------------------------------------

class TestStringMemory:
    def test_store_returns_fingerprint(self):
        from memory import StringMemory
        mem = StringMemory()
        fp = mem.store("hello")
        assert isinstance(fp, str)
        assert len(fp) == 64  # SHA-256 hex digest

    def test_store_and_retrieve(self):
        from memory import StringMemory
        mem = StringMemory()
        fp = mem.store("neurostring")
        retrieved = mem.retrieve(fp)
        assert retrieved == "neurostring"

    def test_retrieve_nonexistent(self):
        from memory import StringMemory
        mem = StringMemory()
        assert mem.retrieve("deadbeef" * 8) is None

    def test_store_dict(self):
        from memory import StringMemory
        mem = StringMemory()
        data = {"key": "value", "num": 42}
        fp = mem.store(data)
        assert fp is not None

    def test_stats_empty(self):
        from memory import StringMemory
        mem = StringMemory()
        stats = mem.stats()
        assert stats["total_patterns"] == 0

    def test_stats_after_store(self):
        from memory import StringMemory
        mem = StringMemory()
        mem.store("a")
        mem.store("b")
        stats = mem.stats()
        assert stats["total_patterns"] == 2

    def test_clear(self):
        from memory import StringMemory
        mem = StringMemory()
        mem.store("data")
        mem.clear()
        assert mem.stats()["total_patterns"] == 0
        assert mem.resonance_map == {}

    def test_find_by_resonance(self):
        from memory import StringMemory
        mem = StringMemory()
        fp = mem.store("resonance test")
        vib = mem.vibrations[fp]
        results = mem.find_by_resonance(vib["frequency"], tolerance=0.05)
        assert fp in results

    def test_get_dimension_valid(self):
        from memory import StringMemory
        mem = StringMemory()
        mem.store("dim test")
        result = mem.get_dimension(0)
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_dimension_out_of_range(self):
        from memory import StringMemory
        mem = StringMemory()
        mem.store("dim test")
        assert mem.get_dimension(-1) == []
        assert mem.get_dimension(11) == []

    def test_dimensions_count(self):
        from memory import StringMemory
        mem = StringMemory()
        fp = mem.store("test")
        assert len(mem.vibrations[fp]["dimensions"]) == mem.dimensions


# ---------------------------------------------------------------------------
# QuantumSimulator tests
# ---------------------------------------------------------------------------

class TestQuantumSimulator:
    def test_create_qubit_default(self):
        from quantum import QuantumSimulator
        qs = QuantumSimulator()
        qubit = qs.create_qubit("q1")
        assert qubit["state"] in (0, 1)
        assert isinstance(qubit["superposition"], bool)

    def test_create_qubit_forced_state(self):
        from quantum import QuantumSimulator
        qs = QuantumSimulator()
        qubit = qs.create_qubit("q1", state=0)
        assert qubit["state"] == 0

    def test_entangle_existing_qubits(self):
        from quantum import QuantumSimulator
        qs = QuantumSimulator()
        qs.create_qubit("q1")
        qs.create_qubit("q2")
        result = qs.entangle("q1", "q2")
        assert result is True
        assert qs.qubits["q1"]["state"] == qs.qubits["q2"]["state"]

    def test_entangle_nonexistent_qubits(self):
        from quantum import QuantumSimulator
        qs = QuantumSimulator()
        result = qs.entangle("ghost1", "ghost2")
        assert result is False

    def test_measure_returns_state(self):
        from quantum import QuantumSimulator
        qs = QuantumSimulator()
        qs.create_qubit("q1", state=1)
        qs.qubits["q1"]["superposition"] = False
        result = qs.measure("q1")
        assert result == 1

    def test_measure_nonexistent(self):
        from quantum import QuantumSimulator
        qs = QuantumSimulator()
        assert qs.measure("ghost") is None

    def test_measure_collapses_superposition(self):
        from quantum import QuantumSimulator
        qs = QuantumSimulator()
        qs.create_qubit("q1")
        qs.qubits["q1"]["superposition"] = True
        result = qs.measure("q1")
        assert result in (0, 1)
        assert qs.qubits["q1"]["superposition"] is False

    def test_entangled_partner_updates_on_measure(self):
        from quantum import QuantumSimulator
        qs = QuantumSimulator()
        qs.create_qubit("q1")
        qs.create_qubit("q2")
        qs.entangle("q1", "q2")
        qs.qubits["q1"]["superposition"] = False
        measured = qs.measure("q1")
        assert qs.qubits["q2"]["state"] == measured

    def test_quantum_fourier_transform_string(self):
        from quantum import QuantumSimulator
        qs = QuantumSimulator()
        result = qs.quantum_fourier_transform("ABC")
        assert len(result) == 3
        assert all(isinstance(f, float) for f in result)

    def test_quantum_fourier_transform_number(self):
        from quantum import QuantumSimulator
        qs = QuantumSimulator()
        result = qs.quantum_fourier_transform(42)
        assert len(result) == 1

    def test_quantum_random_range(self):
        from quantum import QuantumSimulator
        qs = QuantumSimulator()
        for _ in range(20):
            val = qs.quantum_random()
            assert 0.0 <= val <= 1.0

    def test_quantum_consensus_empty(self):
        from quantum import quantum_consensus
        assert quantum_consensus([]) == 0

    def test_quantum_consensus_returns_float(self):
        from quantum import quantum_consensus
        result = quantum_consensus([0.8, 0.9, 0.7])
        assert isinstance(result, float)
        assert 0.0 <= result <= 1.0


# ---------------------------------------------------------------------------
# Web API tests (Flask test client)
# ---------------------------------------------------------------------------

class TestWebAPI:
    @pytest.fixture
    def client(self):
        from web import app
        app.config["TESTING"] = True
        with app.test_client() as client:
            yield client

    def test_index_returns_200(self, client):
        response = client.get("/")
        assert response.status_code == 200

    def test_index_contains_neurostring(self, client):
        response = client.get("/")
        assert b"NEUROSTRING" in response.data or b"NeuroString" in response.data

    def test_api_stats_returns_200(self, client):
        response = client.get("/api/stats")
        assert response.status_code == 200

    def test_api_stats_json_keys(self, client):
        import json
        response = client.get("/api/stats")
        data = json.loads(response.data)
        for key in ("nodes", "synapses", "entanglement", "memory_patterns"):
            assert key in data

    def test_api_transaction_post(self, client):
        import json
        response = client.post(
            "/api/transaction",
            data=json.dumps({"data": "test_tx"}),
            content_type="application/json"
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "success" in data
        assert "message" in data

    def test_api_add_node_post(self, client):
        import json
        response = client.post("/api/add_node")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "success" in data
        assert "message" in data
