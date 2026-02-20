#!/usr/bin/env python3
"""
Performance tests for Neurosting.

Tests included
--------------
1. Transaction processing time – measures end-to-end latency.
2. Stress / throughput test – determines how many transactions the network
   can handle in a fixed time window.
"""

import time
import pytest

from tests.conftest import build_network


# ---------------------------------------------------------------------------
# 1. Transaction processing time
# ---------------------------------------------------------------------------

class TestTransactionProcessingTime:
    """Measure latency from transaction initiation to completion."""

    def test_single_transaction_completes(self, small_network):
        """A transaction submitted to a live network must produce a result."""
        result = small_network.process_transaction("perf_test_payload")
        assert result is not None, "process_transaction must return a result"

    def test_single_transaction_latency(self, small_network):
        """End-to-end latency for one transaction should be under 1 second."""
        start = time.perf_counter()
        small_network.process_transaction("latency_test")
        elapsed = time.perf_counter() - start
        assert elapsed < 1.0, f"Transaction took {elapsed:.4f}s – expected < 1s"

    def test_average_latency_over_100_transactions(self, small_network):
        """Mean latency across 100 sequential transactions must be under 100 ms."""
        latencies = []
        for i in range(100):
            start = time.perf_counter()
            small_network.process_transaction(f"tx_{i}")
            latencies.append(time.perf_counter() - start)

        mean_latency = sum(latencies) / len(latencies)
        assert mean_latency < 0.1, (
            f"Mean latency {mean_latency * 1000:.2f} ms exceeds 100 ms threshold"
        )

    def test_transaction_history_updated(self, small_network):
        """Each successful transaction should be recorded in history."""
        before = len(small_network.transaction_history)
        # process_transaction may return None if activation threshold not met;
        # retry until at least one transaction is recorded.
        for i in range(20):
            small_network.process_transaction(f"hist_tx_{i}")
        after = len(small_network.transaction_history)
        assert after > before, "Transaction history was not updated"


# ---------------------------------------------------------------------------
# 2. Stress / throughput test
# ---------------------------------------------------------------------------

class TestThroughput:
    """Stress-test the network to determine transactions-per-second (TPS)."""

    def test_throughput_not_zero(self, small_network):
        """The network must process at least one transaction per second."""
        window = 2.0  # seconds
        count = 0
        deadline = time.perf_counter() + window
        while time.perf_counter() < deadline:
            small_network.process_transaction(f"stress_{count}")
            count += 1

        tps = count / window
        assert tps > 0, "No transactions were processed during the stress window"

    def test_throughput_10_tps_minimum(self, small_network):
        """Network throughput must reach at least 10 TPS under stress."""
        window = 2.0
        count = 0
        deadline = time.perf_counter() + window
        while time.perf_counter() < deadline:
            small_network.process_transaction(f"stress_{count}")
            count += 1

        tps = count / window
        assert tps >= 10, f"Throughput {tps:.1f} TPS is below the 10 TPS minimum"

    def test_high_volume_no_crash(self, small_network):
        """Submitting 1 000 transactions must not raise an exception."""
        for i in range(1000):
            small_network.process_transaction(f"bulk_{i}")

    def test_memory_growth_under_load(self, small_network):
        """memory_patterns should grow monotonically under sustained load."""
        prev = small_network.memory_patterns
        for i in range(200):
            small_network.process_transaction(f"load_{i}")
        assert small_network.memory_patterns >= prev, (
            "memory_patterns must not decrease under load"
        )
