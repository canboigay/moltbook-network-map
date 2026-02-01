#!/usr/bin/env python3
"""
Build network visualization from real Moltbook agents
"""

import json
import random

# Load scraped agents
with open('moltbook-agents-full.json') as f:
    data = json.load(f)

agents = data['agents']

print(f"Building network from {len(agents)} real Moltbook agents")

# Create nodes - all agents positioned randomly on globe
nodes = []
for agent in agents:
    nodes.append({
        'id': agent,
        'username': agent,
        'posts_count': 0,  # Unknown without API
        'karma': 0,  # Unknown without API
        'verified': False
    })

# Create some edges based on alphabetical proximity
# (agents with similar names might be related)
edges = []

for i, agent1 in enumerate(agents):
    # Connect to nearby agents alphabetically
    for j in range(max(0, i-2), min(len(agents), i+3)):
        if i != j:
            agent2 = agents[j]
            edges.append({
                'source': agent1,
                'target': agent2,
                'weight': 1,
                'type': 'alphabetical_proximity'
            })

network = {
    'nodes': nodes,
    'edges': edges,
    'metadata': {
        'total_agents': len(nodes),
        'total_registered_on_moltbook': '1,516,273',
        'total_connections': len(edges),
        'data_source': 'real_moltbook_website_scrape',
        'note': 'Showing first 60 agents. Connections are synthetic (alphabetical) since API unavailable.'
    }
}

with open('network-data.json', 'w') as f:
    json.dump(network, f, indent=2)

print(f"✓ Created network with {len(nodes)} nodes and {len(edges)} edges")
print(f"✓ Saved to network-data.json")
print(f"\n📊 Network includes real agents from Moltbook!")
print(f"Total registered on Moltbook: 1,516,273")
print(f"Showing in visualization: {len(nodes)}")
