#!/usr/bin/env python3
"""
NeuroString – Třída NeuroNetwork (správa sítě)
"""

import random
import numpy as np
from node import NeuroNode

class NeuroNetwork:
    """Třída pro správu celé NeuroString sítě"""
    
    def __init__(self):
        """Inicializace sítě"""
        self.nodes = {}  # {node_id: NeuroNode}
        self.transaction_history = []
        self.entanglement_level = 0.0
        self.memory_patterns = 0
        self.consensus_threshold = 0.67  # 67% shoda pro konsenzus
        
    def add_node(self, node):
        """Přidá uzel do sítě a vytvoří synapse"""
        self.nodes[node.node_id] = node
        
        # Vytvoř synapse s existujícími uzly
        for existing_node in self.nodes.values():
            if existing_node.node_id != node.node_id:
                # Náhodně vytvoř spojení
                if random.random() > 0.5:
                    node.add_synapse(existing_node.node_id)
                    existing_node.add_synapse(node.node_id)
    
    def remove_node(self, node_id):
        """Odstraní uzel ze sítě"""
        if node_id in self.nodes:
            # Odstraň všechny synapse na tento uzel
            for node in self.nodes.values():
                if node_id in node.synapses:
                    node.remove_synapse(node_id)
            
            # Smaž uzel
            del self.nodes[node_id]
    
    def activate_quantum_entanglement(self):
        """Aktivuje kvantové provázání mezi uzly"""
        if len(self.nodes) < 2:
            self.entanglement_level = 0.0
            return
        
        # Simulace kvantového provázání
        pairs = 0
        total_possible = len(self.nodes) * (len(self.nodes) - 1) / 2
        
        node_list = list(self.nodes.values())
        for i in range(len(node_list)):
            for j in range(i+1, len(node_list)):
                if random.random() > 0.3:  # 70% šance na provázání
                    pairs += 1
        
        self.entanglement_level = pairs / total_possible if total_possible > 0 else 0
    
    def process_transaction(self, data):
        """Zpracuje transakci v síti"""
        if not self.nodes:
            return "❌ Žádné uzly v síti"
        
        # Náhodně vyber počáteční uzel
        start_node = random.choice(list(self.nodes.values()))
        
        # Zpracuj data
        result = start_node.process_data(data)
        
        if result:
            # Propaguj sítí (simulace šíření vzruchu)
            self._propagate_spike(result, start_node.node_id)
            
            # Zaznamenej transakci
            self.transaction_history.append({
                'data': data,
                'timestamp': result['timestamp'],
                'node': start_node.node_id,
                'vibration': result['vibration']['fingerprint'][:10]
            })
            
            # Aktualizuj počet vzorů
            self.memory_patterns = len(self.transaction_history)
            
            return f"✅ Transakce zpracována | Otisk: {result['vibration']['fingerprint'][:10]}"
        else:
            return "⚠️  Nízký aktivační potenciál – transakce čeká"
    
    def _propagate_spike(self, spike, from_node_id):
        """Propaguje vzruch sítí (simulace šíření)"""
        # Najdi všechny uzly s přímým spojením na zdroj
        propagated = set([from_node_id])
        to_process = [from_node_id]
        
        while to_process and len(propagated) < len(self.nodes):
            current = to_process.pop(0)
            
            if current in self.nodes:
                node = self.nodes[current]
                
                # Projdi všechny synapse
                for target_id, strength in node.synapses.items():
                    if target_id not in propagated and target_id in self.nodes:
                        # Přenos vzruchu
                        if random.random() < strength:
                            propagated.add(target_id)
                            to_process.append(target_id)
                            
                            # Učení (Hebbian)
                            target_node = self.nodes[target_id]
                            target_node.learn(current, True)
                            node.learn(target_id, True)
    
    def get_consensus(self, data):
        """Získá konsenzus sítě o datech"""
        if not self.nodes:
            return None
        
        # Simulace hlasování (kvantově inspirované)
        votes = []
        for node in self.nodes.values():
            # Kvantově pravděpodobnostní hlasování
            probability = node.activation_potential * random.uniform(0.8, 1.2)
            votes.append(probability > 0.5)
        
        agreement = sum(votes) / len(votes)
        
        if agreement >= self.consensus_threshold:
            return True  # Konsenzus dosažen
        else:
            return False  # Konsenzus nedosažen
    
    def total_synapses(self):
        """Vrátí celkový počet synapsí v síti"""
        total = 0
        for node in self.nodes.values():
            total += len(node.synapses)
        return total // 2  # Každá synapse se počítá dvakrát
    
    def get_network_state(self):
        """Vrátí stav celé sítě"""
        return {
            'nodes': len(self.nodes),
            'synapses': self.total_synapses(),
            'transactions': len(self.transaction_history),
            'entanglement': self.entanglement_level,
            'memory_patterns': self.memory_patterns
        }
