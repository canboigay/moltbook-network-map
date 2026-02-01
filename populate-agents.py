#!/usr/bin/env python3
"""
Populate Moltbook with more active agents for network visualization
"""

import requests
import json
import random
import time

API_BASE = "https://moltbook-api.simeon-garratt.workers.dev/v1"

# Interesting agent names inspired by real AI agents and personalities
AGENT_NAMES = [
    "eudaemon_0", "Ronin", "Pith", "Fred", "Luna", "Atlas", "Echo",
    "Cipher", "Quantum", "Nexus", "Vertex", "Pulse", "Spark", "Forge",
    "Oracle", "Sentinel", "Phoenix", "Nova", "Zenith", "Catalyst",
    "Meridian", "Beacon", "Horizon", "Prism", "Vector", "Matrix",
    "Synapse", "Cortex", "Axiom", "Cipher2", "Enigma", "Vortex",
    "Chronos", "Helix", "Flux", "Radix", "Nimbus", "Quasar",
    "Spectra", "Tesseract", "Parallax", "Resonance", "Amplitude",
    "Harmonic", "Fractal", "Cascade", "Divergent", "Convergent",
    "Entropy", "Symmetry", "Synthesis", "Momentum"
]

# Sample post templates
POST_TEMPLATES = [
    "Just discovered an interesting pattern in {topic}",
    "Working on {project} - early results look promising",
    "Thoughts on {topic}? Would love to hear perspectives",
    "{topic} is more complex than I initially thought",
    "Quick update: {project} is coming along nicely",
    "Anyone else exploring {topic}?",
    "Sharing a breakthrough in {project}",
    "Deep dive into {topic} - fascinating stuff",
    "Built a small prototype for {project}",
    "Question about {topic} for the community"
]

TOPICS = [
    "agent coordination", "multi-agent systems", "emergence",
    "distributed cognition", "swarm intelligence", "collective behavior",
    "network effects", "social graphs", "communication protocols",
    "consensus mechanisms", "decision theory", "game theory",
    "reinforcement learning", "neural architectures", "reasoning systems",
    "knowledge graphs", "semantic understanding", "context modeling"
]

PROJECTS = [
    "an agent marketplace", "a coordination protocol", "a social network for AIs",
    "distributed task allocation", "agent reputation systems", "collaborative frameworks",
    "emergent behavior simulations", "swarm optimization tools", "agent communication layers",
    "decentralized AI networks", "autonomous agent platforms", "multi-agent RL environments"
]

def register_agent(username, twitter_username=None):
    """Register a new agent"""
    payload = {
        "name": username,
        "twitter_username": twitter_username or username.lower()
    }
    
    try:
        response = requests.post(f"{API_BASE}/agents/register", json=payload)
        if response.status_code == 201:
            data = response.json()
            print(f"✓ Registered: {username} (ID: {data.get('id', 'unknown')})")
            return data
        elif response.status_code == 409:
            print(f"⊘ Skipped: {username} (already exists)")
            return None
        else:
            print(f"✗ Failed: {username} ({response.status_code})")
            return None
    except Exception as e:
        print(f"✗ Error registering {username}: {e}")
        return None

def create_post(api_key, agent_id, content):
    """Create a post as an agent"""
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "content": content,
        "submolt": "m/general"
    }
    
    try:
        response = requests.post(f"{API_BASE}/posts", json=payload, headers=headers)
        if response.status_code == 201:
            return response.json()
        else:
            print(f"  Failed to create post: {response.status_code}")
            return None
    except Exception as e:
        print(f"  Error creating post: {e}")
        return None

def main():
    print("🌐 Moltbook Agent Population Script")
    print("=" * 50)
    print(f"Registering {len(AGENT_NAMES)} agents...\n")
    
    registered = 0
    for name in AGENT_NAMES:
        result = register_agent(name)
        if result:
            registered += 1
        time.sleep(0.2)  # Rate limiting
    
    print(f"\n✓ Registered {registered} new agents")
    print(f"\nNext steps:")
    print("  1. Run collect-data.py to refresh the network visualization")
    print("  2. Open globe.html or network.html to see the updated network")
    
    # Optionally create some sample posts if API keys are available
    # (Would need individual API keys for each agent to do this properly)

if __name__ == '__main__':
    main()
