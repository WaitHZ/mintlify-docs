# MCPBench - AI Agent Terminal Benchmark

A comprehensive benchmark for evaluating AI agents' capabilities in terminal environments, built with Mintlify.

## 🚀 Features

- **Custom Top Navigation**: Terminal Bench inspired navigation bar
- **Full-Screen Leaderboard**: Application-style leaderboard without sidebar
- **Task Registry**: Comprehensive task browsing with filtering
- **Responsive Design**: Mobile-friendly interface
- **Dark Mode Support**: Automatic theme switching
- **Component-Based**: Reusable React components

## 📁 Project Structure

```
mintlify-docs/
├── components/           # Custom React components
│   ├── custom-topbar.tsx # Main navigation component
│   ├── task-card.tsx     # Task display component
│   └── task-filter.tsx   # Task filtering component
├── styles/
│   └── custom.css        # Custom styles and themes
├── leaderboard/
│   └── models.mdx        # Full-screen leaderboard page
├── tasks/
│   └── overview.mdx      # Task registry page
├── get-started/          # Documentation pages
├── docs.json             # Mintlify configuration
└── index.mdx             # Homepage
```

## 🎨 Key Components

### Custom Topbar
- Terminal Bench inspired navigation
- Dropdown menus for task categories
- Mobile responsive with hamburger menu
- Dark mode support

### Leaderboard
- Full-screen layout (no sidebar)
- Real-time model rankings
- Category performance breakdown
- Methodology explanation

### Task Registry
- Advanced filtering and search
- Task cards with metadata
- Category and difficulty badges
- GitHub integration

## 🛠️ Development

### Prerequisites
- Node.js 16+
- Mintlify CLI

### Setup
```bash
# Install Mintlify CLI
npm install -g mintlify

# Start development server
mintlify dev
```

### Customization

#### Adding New Pages
1. Create `.mdx` file in appropriate directory
2. Update `docs.json` navigation structure
3. Use `sidebar: false` for full-screen pages

#### Styling
- Edit `styles/custom.css` for global styles
- Use CSS modules or styled-jsx for component-specific styles
- Follow existing design patterns for consistency

#### Components
- Create React components in `components/` directory
- Import and use in MDX files
- Follow TypeScript best practices

## 📱 Responsive Design

The site is fully responsive with:
- Mobile-first approach
- Collapsible navigation on mobile
- Adaptive grid layouts
- Touch-friendly interactions

## 🌙 Dark Mode

Automatic dark mode support:
- Detects system preference
- Smooth theme transitions
- Consistent color scheme
- Accessible contrast ratios

## 🚀 Deployment

### Vercel (Recommended)
```bash
# Connect to Vercel
vercel

# Deploy
vercel --prod
```

### Other Platforms
- Netlify
- GitHub Pages
- Any static hosting service

## 📄 License

MIT License - see LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

- GitHub Issues: [Report bugs](https://github.com/mcpbench/mcpbench/issues)
- Discord: [Join community](https://discord.gg/mcpbench)
- Documentation: [Read docs](https://docs.mcpbench.ai)

---

Built with ❤️ using [Mintlify](https://mintlify.com)