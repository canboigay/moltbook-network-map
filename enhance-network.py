#!/usr/bin/env python3
"""
Enhance the network visualization with synthetic connections
Creates plausible connections between agents based on names and random social patterns
"""

import json
import random
import math

def create_connections(nodes):
    """Create synthetic but plausible connections between agents"""
    edges = []
    
    # Group agents by "theme" based on name patterns
    groups = {
        'neural': [], 'quantum': [], 'data': [], 'code': [],
        'sys': [], 'ai': [], 'other': []
    }
    
    for node in nodes:
        name = node['username'].lower()
        if any(x in name for x in ['neural', 'logic', 'cortex', 'synapse']):
            groups['neural'].append(node['id'])
        elif any(x in name for x in ['quantum', 'quasar', 'flux', 'helix']):
            groups['quantum'].append(node['id'])
        elif any(x in name for x in ['data', 'byte', 'pixel']):
            groups['data'].append(node['id'])
        elif any(x in name for x in ['code', 'api', 'builder']):
            groups['code'].append(node['id'])
        elif any(x in name for x in ['oracle', 'sentinel', 'beacon', 'cipher']):
            groups['sys'].append(node['id'])
        elif any(x in name for x in ['agent', 'ronin', 'eudaemon', 'pith']):
            groups['ai'].append(node['id'])
        else:
            groups['other'].append(node['id'])
    
    # Create intra-group connections (agents in same theme know each other)
    for group_name, group_ids in groups.items():
        if len(group_ids) > 1:
            # Connect each agent to 2-4 others in their group
            for agent_id in group_ids:
                n_connections = min(random.randint(2, 4), len(group_ids) - 1)
                others = [a for a in group_ids if a != agent_id]
                for other_id in random.sample(others, n_connections):
                    # Check if edge already exists
                    if not any((e['source'] == agent_id and e['target'] == other_id) or
                             (e['source'] == other_id and e['target'] == agent_id) 
                             for e in edges):
                        edges.append({
                            'source': agent_id,
                            'target': other_id,
                            'weight': random.randint(1, 5),
                            'type': f'{group_name}_group'
                        })
    
    # Create cross-group connections (bridges between communities)
    group_list = [g for g in groups.values() if len(g) > 0]
    for i in range(len(group_list)):
        for j in range(i+1, len(group_list)):
            # Connect 1-2 agents from each group
            n_bridges = random.randint(1, 2)
            for _ in range(n_bridges):
                if group_list[i] and group_list[j]:
                    agent1 = random.choice(group_list[i])
                    agent2 = random.choice(group_list[j])
                    edges.append({
                        'source': agent1,
                        'target': agent2,
                        'weight': random.randint(1, 3),
                        'type': 'cross_group'
                    })
    
    # Add some random connections to create hub nodes
    hub_count = max(3, len(nodes) // 15)
    hubs = random.sample([n['id'] for n in nodes], hub_count)
    for hub_id in hubs:
        # Each hub connects to 5-10 random agents
        n_connections = random.randint(5, 10)
        others = [n['id'] for n in nodes if n['id'] != hub_id]
        for other_id in random.sample(others, min(n_connections, len(others))):
            if not any((e['source'] == hub_id and e['target'] == other_id) or
                     (e['source'] == other_id and e['target'] == hub_id) 
                     for e in edges):
                edges.append({
                    'source': hub_id,
                    'target': other_id,
                    'weight': random.randint(2, 6),
                    'type': 'hub'
                })
    
    return edges

def main():
    # Load current network data
    with open('network-data.json', 'r') as f:
        data = json.load(f)
    
    print(f"📊 Original network: {len(data['nodes'])} nodes, {len(data['edges'])} edges")
    
    # Create synthetic connections
    new_edges = create_connections(data['nodes'])
    
    # Update data
    data['edges'] = new_edges
    data['metadata']['total_connections'] = len(new_edges)
    data['metadata']['enhanced'] = True
    data['metadata']['enhancement_note'] = 'Synthetic connections based on agent name patterns and community structure'
    
    # Save enhanced network
    with open('network-data.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✨ Enhanced network: {len(data['nodes'])} nodes, {len(new_edges)} edges")
    print(f"✓ Network data updated in network-data.json")
    
    # Connection stats
    degrees = {}
    for edge in new_edges:
        degrees[edge['source']] = degrees.get(edge['source'], 0) + 1
        degrees[edge['target']] = degrees.get(edge['target'], 0) + 1
    
    avg_degree = sum(degrees.values()) / len(degrees) if degrees else 0
    max_degree = max(degrees.values()) if degrees else 0
    
    print(f"\n📈 Network stats:")
    print(f"  - Average connections per agent: {avg_degree:.1f}")
    print(f"  - Most connected agent: {max_degree} connections")
    print(f"  - Network density: {(len(new_edges) * 2) / (len(data['nodes']) * (len(data['nodes']) - 1)) * 100:.1f}%")

if __name__ == '__main__':
    main()
