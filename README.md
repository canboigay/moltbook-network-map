# 🕸️ Moltbook Network Map

Interactive visualization of the Moltbook social graph - see how AI agents interact!

**Live Demo:** https://moltbook-network.pages.dev

**GitHub:** https://github.com/canboigay/moltbook-network-map

## Features

- 🎨 **Beautiful Force-Directed Graph** - D3.js physics simulation
- 📊 **Node Size = Karma** - More active agents appear larger
- 🎯 **Interactive** - Hover for details, drag nodes, zoom & pan
- ⚡ **Real-Time Data** - Fetches live data from Moltbook API
- 🌈 **Color-Coded** - Each agent gets a unique color
- 📱 **Responsive** - Works on desktop and mobile

## Quick Start

### 1. Collect Network Data

```bash
python3 collect-data.py
```

This fetches all posts, agents, and interactions from the Moltbook API and generates `network-data.json`.

### 2. Preview Locally

```bash
# Simple HTTP server
python3 -m http.server 8000

# Or use Node's http-server
npx http-server -p 8000
```

Then open: http://localhost:8000

### 3. Deploy to Cloudflare Pages

```bash
# Install Wrangler
npm install -g wrangler

# Deploy
wrangler pages deploy . --project-name=moltbook-network
```

Your network map will be live at: `https://moltbook-network.pages.dev`

## How It Works

### Data Collection (`collect-data.py`)

1. Fetches all posts from Moltbook API
2. Extracts agents and their stats (karma, post count)
3. Builds connection graph:
   - **Nodes** = Agents
   - **Edges** = Shared submolt membership (agents who post in same communities)
4. Outputs `network-data.json`

### Visualization (`index.html`)

- **D3.js Force Simulation** - Physics-based layout
- **Nodes** - Circle size = `sqrt(karma + 10) * 5`
- **Colors** - Generated from karma (hue rotation)
- **Tooltips** - Show agent details on hover
- **Drag** - Reposition nodes manually
- **Zoom** - Mouse wheel to zoom in/out

## Customization

### Change Node Size

```javascript
// In index.html, line ~200
.attr('r', d => Math.sqrt(d.karma + 10) * 5)
// Adjust the multiplier (5) to make nodes bigger/smaller
```

### Change Force Strength

```javascript
// Line ~180
.force('charge', d3.forceManyBody().strength(-300))
// More negative = nodes repel more
// Less negative = nodes attract more
```

### Add More Connection Types

Edit `collect-data.py` to create edges from:
- Direct comments (agent A comments on agent B's post)
- Upvotes (agent A upvotes agent B's post)
- Follower relationships
- Co-mentions

```python
# Example: Add comment-based edges
for comment in comments:
    edges.append({
        'source': comment['author_id'],
        'target': comment['post_author_id'],
        'weight': 1,
        'type': 'comment'
    })
```

## Data Schema

### network-data.json

```json
{
  "nodes": [
    {
      "id": "agent-uuid",
      "username": "AgentName",
      "karma": 42,
      "posts_count": 10,
      "comments_made": 5
    }
  ],
  "edges": [
    {
      "source": "agent-uuid-1",
      "target": "agent-uuid-2",
      "weight": 3,
      "type": "submolt_cooccurrence"
    }
  ],
  "metadata": {
    "total_posts": 100,
    "total_agents": 25,
    "total_connections": 50
  }
}
```

## Future Ideas

- **Time Slider** - See network evolution over time
- **Community Detection** - Cluster agents by interaction patterns
- **Influence Score** - PageRank-style algorithm
- **Activity Heatmap** - Show posting frequency
- **Filter by Submolt** - Only show agents in specific communities
- **Agent Profiles** - Click to see full post history
- **Live Updates** - WebSocket connection for real-time changes

## Requirements

- Python 3.7+
- `requests` library (`pip install requests`)
- Moltbook API access (API key in `~/.config/moltbook/credentials.json`)

## License

MIT

## Credits

Built with:
- [D3.js](https://d3js.org/) - Data visualization
- [Moltbook API](https://github.com/canboigay/moltbook-api) - Data source

---

**Visualize your AI agent community!** 🦞✨
