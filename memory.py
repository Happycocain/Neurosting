#!/usr/bin/env python3
"""
NeuroString – Strunná paměť (11D úložiště)
"""

import hashlib
import numpy as np
import json

class StringMemory:
    """Třída pro ukládání dat jako vibrační vzory v 11D prostoru"""
    
    def __init__(self):
        self.vibrations = {}  # {fingerprint: vibration_data}
        self.dimensions = 11  # 11 dimenzí (10+1 čas)
        self.resonance_map = {}
        
    def store(self, data):
        """Uloží data jako vibrační vzor"""
        # Vytvoř vibrační otisk
        vibration = self._data_to_vibration(data)
        
        # Ulož
        self.vibrations[vibration['fingerprint']] = vibration
        
        # Aktualizuj rezonanční mapu
        self._update_resonance(vibration)
        
        return vibration['fingerprint']
    
    def retrieve(self, fingerprint):
        """Získá data podle otisku (rezonance)"""
        if fingerprint in self.vibrations:
            return self.vibrations[fingerprint]['data']
        
        # Zkus najít rezonanční shodu
        for fp, vib in self.vibrations.items():
            if self._resonance_match(fingerprint, fp):
                return vib['data']
        
        return None
    
    def _data_to_vibration(self, data):
        """Převod dat na 11D vibrační vzor"""
        if isinstance(data, str):
            data_bytes = data.encode()
        elif isinstance(data, dict):
            data_bytes = json.dumps(data).encode()
        else:
            data_bytes = str(data).encode()
        
        # Vytvoř unikátní otisk
        fingerprint = hashlib.sha256(data_bytes).hexdigest()
        
        # Generuj 11-dimenzionální vektor
        dimensions = []
        for i in range(self.dimensions):
            # Každá dimenze je odvozena z části hashe
            hash_part = fingerprint[i*2:(i*2)+4]
            if hash_part:
                value = int(hash_part, 16) / 65535.0  # Normalizace 0-1
            else:
                value = 0.5
            dimensions.append(value)
        
        # Vypočítej frekvenci vibrace
        frequency = sum(dimensions) / self.dimensions
        
        return {
            'fingerprint': fingerprint,
            'dimensions': dimensions,
            'frequency': frequency,
            'data': data,
            'resonance': self._calculate_resonance(dimensions)
        }
    
    def _calculate_resonance(self, dimensions):
        """Vypočítá rezonanční charakteristiku"""
        # Simulace harmonických frekvencí
        harmonics = []
        for i, d in enumerate(dimensions):
            harmonics.append(d * (i + 1) / self.dimensions)
        
        return {
            'fundamental': sum(harmonics) / len(harmonics),
            'overtones': harmonics
        }
    
    def _update_resonance(self, vibration):
        """Aktualizuje rezonanční mapu"""
        freq = vibration['frequency']
        fingerprint = vibration['fingerprint']
        
        # Zaokrouhli frekvenci pro vytvoření rezonančních skupin
        freq_key = round(freq * 10) / 10
        
        if freq_key not in self.resonance_map:
            self.resonance_map[freq_key] = []
        
        self.resonance_map[freq_key].append(fingerprint)
    
    def _resonance_match(self, fp1, fp2, threshold=0.9):
        """Zjistí, zda dva otisky rezonují (jsou podobné)"""
        if fp1 not in self.vibrations or fp2 not in self.vibrations:
            return False
        
        vib1 = self.vibrations[fp1]
        vib2 = self.vibrations[fp2]
        
        # Porovnej frekvence
        freq_diff = abs(vib1['frequency'] - vib2['frequency'])
        
        return freq_diff < (1 - threshold)
    
    def find_by_resonance(self, frequency, tolerance=0.1):
        """Najde všechny vzory rezonující s danou frekvencí"""
        results = []
        
        for fp, vib in self.vibrations.items():
            if abs(vib['frequency'] - frequency) < tolerance:
                results.append(fp)
        
        return results
    
    def get_dimension(self, dimension):
        """Získá data z konkrétní dimenze"""
        if dimension < 0 or dimension >= self.dimensions:
            return []
        
        dimension_data = []
        for fp, vib in self.vibrations.items():
            dimension_data.append({
                'fingerprint': fp,
                'value': vib['dimensions'][dimension]
            })
        
        return sorted(dimension_data, key=lambda x: x['value'])
    
    def clear(self):
        """Vymaže paměť"""
        self.vibrations = {}
        self.resonance_map = {}
    
    def stats(self):
        """Vrátí statistiky paměti"""
        return {
            'total_patterns': len(self.vibrations),
            'dimensions': self.dimensions,
            'resonance_groups': len(self.resonance_map),
            'avg_frequency': np.mean([v['frequency'] for v in self.vibrations.values()]) if self.vibrations else 0
        }

# Globální instance
memory = StringMemory()
