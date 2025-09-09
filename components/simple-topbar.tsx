import React from 'react';

export default function SimpleTopbar() {
  return (
    <div className="custom-topbar">
      <div className="topbar-left">
        <a href="/" className="topbar-logo">
          <span>MCPBench</span>
        </a>
        
        <nav className="topbar-nav">
          <a href="/docs" className="topbar-nav-link">Docs</a>
          <a href="/leaderboard" className="topbar-nav-link">Leaderboard</a>
          <a href="/tasks" className="topbar-nav-link">Tasks</a>
          <a href="/registry" className="topbar-nav-link">Registry</a>
          <a href="/contributors" className="topbar-nav-link">Contributors</a>
          <a href="/news" className="topbar-nav-link">News</a>
        </nav>
      </div>
      
      <div className="topbar-right">
        <a href="https://github.com/mcpbench" className="topbar-button secondary">
          GitHub
        </a>
        <a href="https://discord.gg/mcpbench" className="topbar-button primary">
          Discord
        </a>
      </div>
    </div>
  );
}
