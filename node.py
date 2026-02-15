#!/usr/bin/env python3
"""
NeuroString – Třída NeuroNode (neuronový uzel)
"""

import uuid
import random
import hashlib
import numpy as np
from datetime import datetime

class NeuroNode:
    """Třída reprezentující jeden neuronový uzel v síti NeuroString"""
    
    def __init__(self, node_id=None):
        """Inicializace uzlu"""
        self.node_id = node_id or f"node_{uuid.uuid4().hex[:8]}"
        self.created_at = datetime.now()
        self.synapses = {}  # Spojení na jiné uzly {node_id: strength}
        self.memory = {}    # Lokální paměť (vibrační vzory)
        self.activation_potential = random.uniform(0.1, 1.0)
        self.learning_rate = 0.1
        self.spike_count = 0
        self.quantum_state = self._init_quantum_state()
        
    def _init_quantum_state(self):
        """Inicializuje kvantový stav uzlu"""
        return {
            'superposition': random.choice([0, 1]),
            'entanglement': {},
            'vibration_freq': random.uniform(0.1, 10.0)
        }
    
    def process_data(self, data):
        """Zpracuje příchozí data (vytvoří nervový impuls)"""
        # Konvertuj data na hash (vibrační otisk)
        vibration = self._data_to_vibration(data)
        
        # Zvýší aktivační potenciál
        self.activation_potential *= 1.1
        self.spike_count += 1
        
        # Pokud je potenciál vysoký, pošli dál
        if self.activation_potential > 0.8:
            return self._spike(vibration)
        
        return None
    
    def _data_to_vibration(self, data):
        """Převod dat na vibrační otisk (simulace 11D)"""
        if isinstance(data, str):
            data = data.encode()
        elif not isinstance(data, bytes):
            data = str(data).encode()
        
        # Vytvoř unikátní otisk
        hash_obj = hashlib.sha256(data).hexdigest()
        
        # Simulace vícerozměrnosti
        return {
            'fingerprint': hash_obj,
            'dimensions': np.random.rand(11).tolist(),  # 11 dimenzí
            'frequency': float(int(hash_obj[:8], 16)) / 10**10
        }
    
    def _spike(self, vibration):
        """Vyšle impuls přes synapse"""
        self.activation_potential = 0.1  # Reset
        return {
            'from': self.node_id,
            'vibration': vibration,
            'timestamp': datetime.now().isoformat(),
            'strength': len(self.synapses) * 0.1
        }
    
    def learn(self, from_node, success):
        """Učení – posílení/zeslabení synapsí (Hebbian learning)"""
        if from_node in self.synapses:
            if success:
                # Posílit spojení
                self.synapses[from_node] = min(1.0, self.synapses[from_node] + self.learning_rate)
            else:
                # Oslabit spojení
                self.synapses[from_node] = max(0.0, self.synapses[from_node] - self.learning_rate/2)
    
    def add_synapse(self, other_node):
        """Přidá spojení na jiný uzel"""
        strength = random.uniform(0.3, 0.7)  # Náhodná počáteční síla
        self.synapses[other_node] = strength
        
    def remove_synapse(self, other_node):
        """Odstraní spojení (zapomínání)"""
        if other_node in self.synapses:
            del self.synapses[other_node]
    
    def get_state(self):
        """Vrátí aktuální stav uzlu"""
        return {
            'id': self.node_id,
            'age': (datetime.now() - self.created_at).total_seconds(),
            'synapses': len(self.synapses),
            'spike_count': self.spike_count,
            'activation': self.activation_potential,
            'quantum_state': self.quantum_state
        }
    
    def __str__(self):
        return f"<NeuroNode {self.node_id} | syn: {len(self.synapses)} | spikes: {self.spike_count}>"
