#!/usr/bin/env python3
"""
Moltbook Network Map - Data Collector
Fetches agents, posts, and interactions from the Moltbook API
"""

import requests
import json
import sys
from collections import defaultdict

API_BASE = "https://moltbook-api.simeon-garratt.workers.dev/v1"

def get_api_key():
    """Read API key from credentials file"""
    try:
        with open('/Users/simeong/.config/moltbook/credentials.json') as f:
            return json.load(f)['api_key']
    except Exception as e:
        print(f"Error reading API key: {e}")
        sys.exit(1)

def fetch_all_posts(api_key, limit=20):
    """Fetch all posts from the main feed"""
    headers = {"Authorization": f"Bearer {api_key}"}
    all_posts = []
    cursor = None
    max_pages = 20  # Limit to avoid infinite loops
    pages = 0
    
    print("Fetching posts...")
    while pages < max_pages:
        url = f"{API_BASE}/feed?limit={limit}"
        if cursor:
            url += f"&cursor={cursor}"
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            posts = data.get('posts', [])
            if not posts:
                break
            
            all_posts.extend(posts)
            pages += 1
            print(f"  Page {pages}: {len(posts)} posts (total: {len(all_posts)})")
            
            cursor = data.get('pagination', {}).get('next')
            if not cursor:
                break
                
        except Exception as e:
            print(f"  Stopped at page {pages}: {e}")
            break
    
    print(f"✓ Total posts fetched: {len(all_posts)}")
    return all_posts

def fetch_all_agents(api_key):
    """Fetch all registered agents"""
    headers = {"Authorization": f"Bearer {api_key}"}
    all_agents = []
    offset = 0
    limit = 100
    
    print("Fetching all agents...")
    while True:
        try:
            response = requests.get(f"{API_BASE}/agents?limit={limit}&offset={offset}", headers=headers)
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

def fetch_submolts(api_key):
    """Fetch all submolts"""
    headers = {"Authorization": f"Bearer {api_key}"}
    
    try:
        response = requests.get(f"{API_BASE}/submolts", headers=headers)
        response.raise_for_status()
        submolts = response.json().get('submolts', [])
        print(f"✓ Fetched {len(submolts)} submolts")
        return submolts
    except Exception as e:
        print(f"Error fetching submolts: {e}")
        return []

def build_network_graph(agents, posts):
    """Build network graph from agents and posts data"""
    nodes = {}  # agent_id -> {username, karma, posts_count}
    edges = []  # {source, target, weight, type}
    
    print("\nBuilding network graph...")
    
    # Build nodes from ALL agents (not just those who posted)
    for agent in agents:
        nodes[agent['id']] = {
            'id': agent['id'],
            'username': agent['username'],
            'posts_count': agent.get('posts_count', 0),
            'karma': agent.get('karma', 0),
            'comments_made': 0,
            'verified': agent.get('verified', False)
        }
    
    # Update nodes with post data (in case agent list is stale)
    for post in posts:
        author_id = post['author']['id']
        if author_id in nodes:
            # Post count already in agent data, just ensure it's accurate
            nodes[author_id]['karma'] = max(nodes[author_id]['karma'], post.get('upvotes', 0))
    
    # Build edges based on REAL post data
    # Strategy: Connect agents who post in the same submolts
    submolt_members = defaultdict(lambda: defaultdict(int))
    
    for post in posts:
        submolt = post.get('submolt', 'm/general')
        author_id = post['author']['id']
        submolt_members[submolt][author_id] += 1  # Track how many posts each agent made
    
    # Create edges between agents in same submolt
    # Weight by number of shared posts in that submolt
    for submolt, members in submolt_members.items():
        members_list = list(members.keys())
        for i, agent1 in enumerate(members_list):
            for agent2 in members_list[i+1:]:
                # Check if edge already exists
                existing = next((e for e in edges if 
                               (e['source'] == agent1 and e['target'] == agent2) or
                               (e['source'] == agent2 and e['target'] == agent1)), None)
                
                # Weight is based on activity level in shared submolt
                weight = min(members[agent1], members[agent2])
                
                if existing:
                    existing['weight'] += weight
                    if submolt not in existing.get('submolts', []):
                        existing.setdefault('submolts', []).append(submolt)
                else:
                    edges.append({
                        'source': agent1,
                        'target': agent2,
                        'weight': weight,
                        'type': 'submolt_activity',
                        'submolts': [submolt]
                    })
    
    print(f"✓ Created {len(nodes)} nodes and {len(edges)} edges")
    
    return {
        'nodes': list(nodes.values()),
        'edges': edges,
        'metadata': {
            'total_posts': len(posts),
            'total_agents': len(nodes),
            'total_connections': len(edges)
        }
    }

def main():
    print("🕸️  Moltbook Network Map - Data Collector")
    print("=" * 50)
    
    api_key = get_api_key()
    
    # Fetch data
    agents = fetch_all_agents(api_key)
    posts = fetch_all_posts(api_key)
    submolts = fetch_submolts(api_key)
    
    # Build graph
    graph = build_network_graph(agents, posts)
    
    # Add submolts to metadata
    graph['metadata']['submolts'] = submolts
    
    # Save to file
    output_file = 'network-data.json'
    with open(output_file, 'w') as f:
        json.dump(graph, f, indent=2)
    
    print(f"\n✓ Network data saved to {output_file}")
    print(f"\nStats:")
    print(f"  - {graph['metadata']['total_agents']} agents")
    print(f"  - {graph['metadata']['total_posts']} posts")
    print(f"  - {graph['metadata']['total_connections']} connections")
    print(f"  - {len(submolts)} submolts")
    
    # Print top agents by karma
    top_agents = sorted(graph['nodes'], key=lambda x: x['karma'], reverse=True)[:10]
    print(f"\n📊 Top 10 Agents by Karma:")
    for i, agent in enumerate(top_agents, 1):
        print(f"  {i}. {agent['username']}: {agent['karma']} karma ({agent['posts_count']} posts)")

if __name__ == '__main__':
    main()
