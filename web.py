#!/usr/bin/env python3
"""
NeuroString – Jednoduché webové rozhraní pro Replit
"""

from flask import Flask, render_template_string, jsonify, request
import random
import time
from datetime import datetime

app = Flask(__name__)

# Jednoduchá HTML šablona
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="cs">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NeuroString • První myslící síť</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        
        h1 {
            font-size: 3em;
            margin-bottom: 10px;
            background: linear-gradient(to right, #fff, #e0e0ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .subtitle {
            font-size: 1.2em;
            opacity: 0.9;
            margin-bottom: 30px;
        }
        
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        
        .card {
            background: rgba(255, 255, 255, 0.15);
            border-radius: 15px;
            padding: 20px;
            transition: transform 0.3s;
        }
        
        .card:hover {
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.2);
        }
        
        .card h3 {
            margin-bottom: 15px;
            font-size: 1.3em;
            border-bottom: 2px solid rgba(255,255,255,0.3);
            padding-bottom: 10px;
        }
        
        .stat {
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            font-size: 1.1em;
        }
        
        .stat .label {
            opacity: 0.8;
        }
        
        .stat .value {
            font-weight: bold;
            background: rgba(255,255,255,0.2);
            padding: 3px 10px;
            border-radius: 20px;
        }
        
        .button {
            background: white;
            color: #764ba2;
            border: none;
            padding: 10px 20px;
            border-radius: 25px;
            font-size: 1em;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            margin-top: 10px;
        }
        
        .button:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 20px rgba(0,0,0,0.2);
        }
        
        .network-viz {
            height: 200px;
            background: rgba(0,0,0,0.2);
            border-radius: 10px;
            margin: 20px 0;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2em;
        }
        
        .footer {
            margin-top: 30px;
            text-align: center;
            opacity: 0.7;
            font-size: 0.9em;
        }
        
        .log {
            background: rgba(0,0,0,0.3);
            border-radius: 10px;
            padding: 15px;
            margin-top: 20px;
            font-family: monospace;
            max-height: 200px;
            overflow-y: auto;
        }
        
        .log-entry {
            margin-bottom: 5px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            padding-bottom: 5px;
        }
        
        .timestamp {
            color: #aaffaa;
            margin-right: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧠 NEUROSTRING</h1>
        <div class="subtitle">První decentralizovaná síť, která myslí</div>
        
        <div class="network-viz" id="viz">
            ⚛️ Inicializuji kvantovou neuronovou síť...
        </div>
        
        <div class="grid">
            <div class="card">
                <h3>🧬 Stav sítě</h3>
                <div id="network-stats">
                    <div class="stat">
                        <span class="label">Aktivních neuronů:</span>
                        <span class="value" id="node-count">0</span>
                    </div>
                    <div class="stat">
                        <span class="label">Synaptických spojení:</span>
                        <span class="value" id="synapse-count">0</span>
                    </div>
                    <div class="stat">
                        <span class="label">Kvantové provázání:</span>
                        <span class="value" id="entanglement">0%</span>
                    </div>
                    <div class="stat">
                        <span class="label">Paměťové vzory:</span>
                        <span class="value" id="memory">0</span>
                    </div>
                </div>
            </div>
            
            <div class="card">
                <h3>⚡ Ovládání</h3>
                <button class="button" onclick="sendTransaction()">📤 Odeslat transakci</button>
                <button class="button" onclick="addNeuron()">🧠 Přidat neuron</button>
                <button class="button" onclick="refreshStats()">🔄 Obnovit</button>
            </div>
            
            <div class="card">
                <h3>🌌 Teorie strun</h3>
                <div class="stat">
                    <span class="label">Aktivní dimenze:</span>
                    <span class="value">11</span>
                </div>
                <div class="stat">
                    <span class="label">Základní frekvence:</span>
                    <span class="value" id="frequency">432 Hz</span>
                </div>
                <div class="stat">
                    <span class="label">Rezonanční grupy:</span>
                    <span class="value" id="resonance">0</span>
                </div>
            </div>
        </div>
        
        <div class="log" id="log">
            <div class="log-entry">
                <span class="timestamp">[{{ timestamp }}]</span> 🚀 NeuroString spuštěn
            </div>
        </div>
        
        <div class="footer">
            NeuroString v0.1.0 • Post-blockchain protokol • 2025
        </div>
    </div>
    
    <script>
        let logCount = 0;
        
        function addLog(message) {
            const log = document.getElementById('log');
            const entry = document.createElement('div');
            entry.className = 'log-entry';
            const now = new Date();
            const timestamp = `[${now.getHours().toString().padStart(2,'0')}:${now.getMinutes().toString().padStart(2,'0')}:${now.getSeconds().toString().padStart(2,'0')}]`;
            entry.innerHTML = `<span class="timestamp">${timestamp}</span> ${message}`;
            log.appendChild(entry);
            
            // Omez na posledních 20 zpráv
            if (log.children.length > 20) {
                log.removeChild(log.children[0]);
            }
            
            // Scroll na konec
            log.scrollTop = log.scrollHeight;
        }
        
        function updateStats(data) {
            document.getElementById('node-count').textContent = data.nodes;
            document.getElementById('synapse-count').textContent = data.synapses;
            document.getElementById('entanglement').textContent = (data.entanglement * 100).toFixed(1) + '%';
            document.getElementById('memory').textContent = data.memory_patterns;
            document.getElementById('resonance').textContent = data.resonance || 0;
            
            // Vizualizace
            const viz = document.getElementById('viz');
            if (data.nodes > 0) {
                viz.innerHTML = `🧠 ${data.nodes} neuronů propojených ${data.synapses} synapsemi ⚡`;
            }
        }
        
        async function refreshStats() {
            try {
                const response = await fetch('/api/stats');
                const data = await response.json();
                updateStats(data);
            } catch (e) {
                addLog('❌ Chyba při načítání statistik');
            }
        }
        
        async function sendTransaction() {
            const data = 'transakce_' + Date.now();
            try {
                const response = await fetch('/api/transaction', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({data: data})
                });
                const result = await response.json();
                addLog(`📤 ${result.message}`);
                refreshStats();
            } catch (e) {
                addLog('❌ Chyba při odesílání transakce');
            }
        }
        
        async function addNeuron() {
            try {
                const response = await fetch('/api/add_node', {method: 'POST'});
                const result = await response.json();
                addLog(`🧠 ${result.message}`);
                refreshStats();
            } catch (e) {
                addLog('❌ Chyba při přidávání neuronu');
            }
        }
        
        // Aktualizuj každých 5 sekund
        setInterval(refreshStats, 5000);
        
        // První načtení
        refreshStats();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Hlavní stránka"""
    from datetime import datetime
    return render_template_string(HTML_TEMPLATE, timestamp=datetime.now().strftime('%H:%M:%S'))

@app.route('/api/stats')
def api_stats():
    """API pro získání statistik"""
    try:
        from network import network
        stats = network.get_network_state()
        return jsonify(stats)
    except:
        # Simulovaná data
        return jsonify({
            'nodes': 3,
            'synapses': 5,
            'entanglement': 0.73,
            'memory_patterns': 12,
            'resonance': 4
        })

@app.route('/api/transaction', methods=['POST'])
def api_transaction():
    """API pro odeslání transakce"""
    data = request.json.get('data', 'test')
    
    try:
        from network import network
        result = network.process_transaction(data)
        return jsonify({'success': True, 'message': result})
    except:
        # Simulace
        return jsonify({
            'success': True,
            'message': f'✅ Transakce zpracována | Otisk: {hash(data)[:10]}'
        })

@app.route('/api/add_node', methods=['POST'])
def api_add_node():
    """API pro přidání uzlu"""
    try:
        from node import NeuroNode
        from network import network
        
        node = NeuroNode()
        network.add_node(node)
        
        return jsonify({
            'success': True,
            'message': f'Přidán uzel {node.node_id}'
        })
    except:
        return jsonify({
            'success': True,
            'message': 'Přidán nový neuron (simulace)'
        })

# Pokud nejsou moduly dostupné, vytvoř globální proměnné
try:
    from network import network
except:
    class DummyNetwork:
        def get_network_state(self):
            return {
                'nodes': 3,
                'synapses': 5,
                'entanglement': 0.73,
                'memory_patterns': 12,
                'resonance': 4
            }
        def process_transaction(self, data):
            return f"✅ Transakce zpracována | Otisk: {hash(data)}"
    
    network = DummyNetwork()
