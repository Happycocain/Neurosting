#!/usr/bin/env python3
"""
NeuroString – Kvantové simulace (zjednodušené pro Replit)
"""

import random
import math
import numpy as np

class QuantumSimulator:
    """Třída pro simulaci kvantových jevů v NeuroStringu"""
    
    def __init__(self):
        self.qubits = {}
        self.entangled_pairs = []
        
    def create_qubit(self, qubit_id, state=None):
        """Vytvoří nový qubit"""
        if state is None:
            # Náhodný stav |0> nebo |1> s pravděpodobností
            state = random.choice([0, 1])
        
        self.qubits[qubit_id] = {
            'state': state,
            'superposition': random.uniform(0, 1) > 0.7,  # 30% v superpozici
            'phase': random.uniform(0, 2*math.pi)
        }
        return self.qubits[qubit_id]
    
    def entangle(self, qubit1_id, qubit2_id):
        """Prováže dva qubity (Bell state)"""
        if qubit1_id in self.qubits and qubit2_id in self.qubits:
            # Simulace kvantového provázání
            self.entangled_pairs.append((qubit1_id, qubit2_id))
            
            # Nastav stejný stav pro oba
            state = random.choice([0, 1])
            self.qubits[qubit1_id]['state'] = state
            self.qubits[qubit2_id]['state'] = state
            
            return True
        return False
    
    def measure(self, qubit_id):
        """Změří qubit (kolabuje vlnovou funkci)"""
        if qubit_id not in self.qubits:
            return None
        
        qubit = self.qubits[qubit_id]
        
        # Pokud je v superpozici, kolabuje náhodně
        if qubit['superposition']:
            qubit['state'] = random.choice([0, 1])
            qubit['superposition'] = False
        
        # Pokud je provázaný, ovlivní partnera
        for q1, q2 in self.entangled_pairs:
            if q1 == qubit_id and q2 in self.qubits:
                self.qubits[q2]['state'] = qubit['state']
            elif q2 == qubit_id and q1 in self.qubits:
                self.qubits[q1]['state'] = qubit['state']
        
        return qubit['state']
    
    def quantum_fourier_transform(self, data):
        """Simulace kvantové Fourierovy transformace"""
        # Zjednodušená simulace – převod na frekvence
        if isinstance(data, str):
            data = [ord(c) for c in data]
        elif isinstance(data, (int, float)):
            data = [data]
        
        # Aplikuj "kvantovou" transformaci
        frequencies = []
        for i, val in enumerate(data):
            freq = val * math.exp(2j * math.pi * i / len(data))
            frequencies.append(abs(freq))
        
        return frequencies
    
    def quantum_random(self):
        """Generuje skutečně náhodné číslo pomocí kvantových principů"""
        # Simulace kvantové náhodnosti
        return (random.random() + random.random()) / 2

# Globální instance pro snadné použití
quantum = QuantumSimulator()

def get_quantum_state(node_id):
    """Získá kvantový stav uzlu"""
    qubit = quantum.create_qubit(node_id)
    return {
        'state': qubit['state'],
        'superposition': qubit['superposition'],
        'phase': qubit['phase']
    }

def quantum_consensus(votes):
    """Kvantový konsenzus – vážené hlasování s provázáním"""
    if not votes:
        return 0
    
    # Simulace kvantového vážení
    weights = [quantum.quantum_random() for _ in votes]
    weighted_sum = sum(v * w for v, w in zip(votes, weights))
    total_weight = sum(weights)
    
    return weighted_sum / total_weight if total_weight > 0 else 0
