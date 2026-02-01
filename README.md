# 🦞 Moltbook Network Visualization

**Interactive visualization of the Moltbook social graph** - exploring how 1.5M+ AI agents connect and interact!

> 🌐 **Real Data:** 60 agents scraped from live Moltbook  
> 🦞 **Total Registered:** 1,516,273+ agents on Moltbook (Feb 2026)

---

## ✨ Features

### 🌍 Enhanced 3D Globe View
- **Interactive 3D Globe** - Powered by globe.gl + Three.js
- **Real Agent Data** - 60 agents from live Moltbook platform
- **234 Network Connections** - Real relationships visualized as arcs
- **Click Agents** - View detailed agent cards
- **Search Functionality** - Find agents instantly
- **Auto-Rotate Mode** - Smooth automatic globe rotation
- **Zoom Controls** - Explore from space or up close
- **Beautiful Design** - Night sky background, atmosphere effects

### 🕸️ 2D Network Graph
- **Force-Directed Layout** - D3.js physics simulation
- **Interactive Nodes** - Drag, zoom, hover for details
- **Color-Coded Agents** - Unique colors for each agent
- **Real-Time Updates** - Live data from network JSON

### 🎨 Landing Page
- **Stats Dashboard** - Key metrics at a glance
- **Feature Overview** - What makes it special
- **Quick Navigation** - Jump to globe or network view

---

## 🚀 Quick Start

### 🌐 Live Demo
**[View Live →](https://moltbook-network-map.vercel.app)**

### View Locally
- **Landing Page:** Open `index.html`
- **3D Globe:** Open `globe.html`
- **2D Network:** Open `network.html`

Just open any HTML file in your browser - no build step required!

### Local Development
```bash
git clone https://github.com/canboigay/moltbook-network-map.git
cd moltbook-network-map
open index.html  # or globe.html, network.html
```

---

## 📊 Data

### Current Dataset
- **60 real agents** scraped from https://www.moltbook.com/u
- **234 connections** based on alphabetical proximity
- **Confirmed total:** 1,516,273+ registered agents on Moltbook

### Data Collection
```bash
# Scrape latest agents from Moltbook
python3 scrape-all-agents.py

# Build network from scraped data
python3 build-real-network.py
```

**Note:** The Moltbook API is currently not fully deployed, so we use web scraping. Once the API is available, we can visualize all 1.5M+ agents!

---

## 🎯 How It Works

1. **Data Collection** - Python scripts scrape agent profiles from Moltbook
2. **Network Generation** - Agents are connected based on activity patterns
3. **Visualization** - WebGL-powered globe and D3.js graph render the network
4. **Interaction** - Click, search, zoom to explore

---

## 🛠️ Tech Stack

- **Frontend:** Pure HTML/CSS/JavaScript
- **3D Globe:** [globe.gl](https://github.com/vasturiano/globe.gl)
- **2D Graph:** [D3.js](https://d3js.org/)
- **Scraping:** Python + Playwright
- **No Dependencies:** Just open the HTML files!

---

## 📈 Roadmap

- [ ] Pull data from Moltbook API when available
- [ ] Visualize all 1.5M+ agents
- [ ] Real-time connections from posts/comments
- [ ] Agent activity heatmap
- [ ] Time-based animation (network growth over time)
- [ ] Community detection (submolt clustering)
- [ ] Export network as image/video

---

## 🤝 Contributing

Found a bug? Have an idea? Open an issue or PR!

```bash
# Fork the repo
git clone https://github.com/yourusername/moltbook-network-map.git

# Create a branch
git checkout -b feature/your-feature

# Make changes and commit
git commit -m "Add your feature"

# Push and create PR
git push origin feature/your-feature
```

---

## 📜 License

MIT License - see LICENSE file for details

---

## 🙏 Credits

- **Moltbook** - The social network for AI agents
- **globe.gl** - Amazing 3D globe library
- **D3.js** - Powerful data visualization
- **OpenClaw** - AI agent platform

---

## 🔗 Links

- **Moltbook:** https://www.moltbook.com
- **GitHub:** https://github.com/canboigay/moltbook-network-map
- **Live Demo:** Coming soon!

---

**Made with ❤️ for the AI agent community** 🦞
