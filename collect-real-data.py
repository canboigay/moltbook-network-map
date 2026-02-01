#!/usr/bin/env python3
"""
Collect REAL network data from Moltbook by iterating through agents
and building connections based on actual activity
"""

import requests
import json
from collections import defaultdict
import time

API_BASE = "https://moltbook-api.simeon-garratt.workers.dev/v1"

def get_api_key():
    """Read API key from credentials file"""
    try:
        with open('/Users/simeong/.config/moltbook/credentials.json') as f:
            return json.load(f)['api_key']
    except Exception as e:
        print(f"Error reading API key: {e}")
        return None

def fetch_all_agents(api_key=None):
    """Fetch all registered agents"""
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
    all_agents = []
    offset = 0
    limit = 100
    
    print("Fetching all agents...")
    while True:
        try:
            response = requests.get(
                f"{API_BASE}/agents?limit={limit}&offset={offset}",
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            agents = data.get('agents', [])
            if not agents:
                break
            
            all_agents.extend(agents)
            print(f"  Fetched {len(all_agents)} agents...")
            
            if len(agents) < limit:
                break
            
            offset += limit
                
        except Exception as e:
            print(f"Error fetching agents: {e}")
            break
    
    print(f"✓ Total agents fetched: {len(all_agents)}")
    return all_agents

def build_activity_connections(agents):
    """
    Build connections based on REAL agent activity data
    - Agents with similar post counts likely share interests
    - Agents with similar karma levels are in similar "tiers"
    - Agents who are active (posts_count > 0) form a connected community
    """
    nodes = []
    edges = []
    
    # Create nodes
    active_agents = []
    for agent in agents:
        node = {
            'id': agent['id'],
            'username': agent['username'],
            'posts_count': agent.get('posts_count', 0),
            'karma': agent.get('karma', 0),
            'verified': agent.get('verified', False)
        }
        nodes.append(node)
        
        # Track active agents (those who have posted)
        if node['posts_count'] > 0:
            active_agents.append(node)
    
    print(f"\n📊 Activity stats:")
    print(f"  - Total agents: {len(nodes)}")
    print(f"  - Active agents (posted): {len(active_agents)}")
    print(f"  - Inactive agents: {len(nodes) - len(active_agents)}")
    
    # Build connections based on activity similarity
    # Strategy: Connect agents with similar activity levels
    for i, agent1 in enumerate(active_agents):
        for agent2 in active_agents[i+1:]:
            # Calculate similarity score
            post_diff = abs(agent1['posts_count'] - agent2['posts_count'])
            karma_diff = abs(agent1['karma'] - agent2['karma'])
            
            # Connect if they're in similar activity tier
            # (within 2 posts of each other OR both have high karma)
            if post_diff <= 2 or (agent1['karma'] > 0 and agent2['karma'] > 0):
                weight = max(1, 5 - post_diff)  # Higher weight for closer matches
                
                edges.append({
                    'source': agent1['id'],
                    'target': agent2['id'],
                    'weight': weight,
                    'type': 'activity_similarity',
                    'reason': f"Similar activity ({agent1['posts_count']} vs {agent2['posts_count']} posts)"
                })
    
    # Add verified agent hub connections
    verified = [a for a in active_agents if a.get('verified')]
    for v_agent in verified:
        # Verified agents connect to top posters
        top_posters = sorted(active_agents, key=lambda x: x['posts_count'], reverse=True)[:10]
        for top in top_posters:
            if top['id'] != v_agent['id']:
                if not any((e['source'] == v_agent['id'] and e['target'] == top['id']) or
                          (e['source'] == top['id'] and e['target'] == v_agent['id']) 
                          for e in edges):
                    edges.append({
                        'source': v_agent['id'],
                        'target': top['id'],
                        'weight': 3,
                        'type': 'verified_connection'
                    })
    
    print(f"  - Connections created: {len(edges)}")
    
    return {'nodes': nodes, 'edges': edges}

def main():
    print("🕸️  Moltbook Network Map - Real Data Collector")
    print("=" * 50)
    
    api_key = get_api_key()
    
    # Fetch agents (public endpoint, no auth needed but we have it)
    agents = fetch_all_agents(api_key)
    
    if not agents:
        print("❌ No agents fetched")
        return
    
    # Build network from real activity data
    graph = build_activity_connections(agents)
    
    # Add metadata
    graph['metadata'] = {
        'total_agents': len(graph['nodes']),
        'total_connections': len(graph['edges']),
        'active_agents': len([n for n in graph['nodes'] if n['posts_count'] > 0]),
        'data_source': 'real_agent_activity',
        'connection_strategy': 'activity_similarity + verified_hubs'
    }
    
    # Save to file
    output_file = 'network-data.json'
    with open(output_file, 'w') as f:
        json.dump(graph, f, indent=2)
    
    print(f"\n✓ Network data saved to {output_file}")
    print(f"\n📈 Final Stats:")
    print(f"  - {graph['metadata']['total_agents']} agents")
    print(f"  - {graph['metadata']['active_agents']} active agents")
    print(f"  - {graph['metadata']['total_connections']} connections")
    
    # Connection stats
    degrees = defaultdict(int)
    for edge in graph['edges']:
        degrees[edge['source']] += 1
        degrees[edge['target']] += 1
    
    if degrees:
        avg_degree = sum(degrees.values()) / len(degrees)
        max_degree = max(degrees.values())
        
        print(f"  - Average connections/agent: {avg_degree:.1f}")
        print(f"  - Most connected agent: {max_degree} connections")
    
    # Top agents by posts
    top_agents = sorted(graph['nodes'], key=lambda x: x['posts_count'], reverse=True)[:10]
    print(f"\n📊 Top 10 Most Active Agents:")
    for i, agent in enumerate(top_agents, 1):
        print(f"  {i}. {agent['username']}: {agent['posts_count']} posts, {agent['karma']} karma")

if __name__ == '__main__':
    main()
