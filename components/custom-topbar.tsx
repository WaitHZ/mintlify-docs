import React, { useState, useEffect } from 'react';

interface TopbarProps {
  currentPath?: string;
}

export default function CustomTopbar({ currentPath }: TopbarProps) {
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  useEffect(() => {
    // Check for dark mode preference
    const checkDarkMode = () => {
      setIsDarkMode(document.documentElement.classList.contains('dark') || 
                   window.matchMedia('(prefers-color-scheme: dark)').matches);
    };
    
    checkDarkMode();
    
    // Listen for theme changes
    const observer = new MutationObserver(checkDarkMode);
    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ['class']
    });
    
    return () => observer.disconnect();
  }, []);

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  const isActive = (path: string) => {
    return currentPath?.startsWith(path) ? 'active' : '';
  };

  return (
    <>
      <div className={`custom-topbar ${isDarkMode ? 'dark' : ''}`}>
        <div className="topbar-left">
          <a href="/" className={`topbar-logo ${isDarkMode ? 'dark' : ''}`}>
            <img src="/logo-light.svg" alt="MCPBench" />
            MCPBench
          </a>
          
          <nav className="topbar-nav">
            <div className="topbar-nav-item">
              <a 
                href="/docs" 
                className={`topbar-nav-link ${isActive('/docs')} ${isDarkMode ? 'dark' : ''}`}
              >
                Docs
              </a>
            </div>
            
            <div className="topbar-nav-item">
              <a 
                href="/leaderboard" 
                className={`topbar-nav-link ${isActive('/leaderboard')} ${isDarkMode ? 'dark' : ''}`}
              >
                Leaderboard
              </a>
            </div>
            
            <div className="topbar-nav-item">
              <a 
                href="/tasks" 
                className={`topbar-nav-link ${isActive('/tasks')} ${isDarkMode ? 'dark' : ''}`}
              >
                Tasks
              </a>
              <div className={`topbar-dropdown ${isDarkMode ? 'dark' : ''}`}>
                <a href="/tasks/system-administration" className={`dropdown-item ${isDarkMode ? 'dark' : ''}`}>
                  System Administration
                </a>
                <a href="/tasks/security" className={`dropdown-item ${isDarkMode ? 'dark' : ''}`}>
                  Security
                </a>
                <a href="/tasks/data-science" className={`dropdown-item ${isDarkMode ? 'dark' : ''}`}>
                  Data Science
                </a>
                <div className={`dropdown-divider ${isDarkMode ? 'dark' : ''}`}></div>
                <a href="/tasks/overview" className={`dropdown-item ${isDarkMode ? 'dark' : ''}`}>
                  All Tasks
                </a>
              </div>
            </div>
            
            <div className="topbar-nav-item">
              <a 
                href="/registry" 
                className={`topbar-nav-link ${isActive('/registry')} ${isDarkMode ? 'dark' : ''}`}
              >
                Registry
              </a>
            </div>
            
            <div className="topbar-nav-item">
              <a 
                href="/contributors" 
                className={`topbar-nav-link ${isActive('/contributors')} ${isDarkMode ? 'dark' : ''}`}
              >
                Contributors
              </a>
            </div>
            
            <div className="topbar-nav-item">
              <a 
                href="/news" 
                className={`topbar-nav-link ${isActive('/news')} ${isDarkMode ? 'dark' : ''}`}
              >
                News
              </a>
            </div>
          </nav>
        </div>
        
        <div className="topbar-right">
          <a 
            href="https://github.com/mcpbench" 
            className={`topbar-button secondary ${isDarkMode ? 'dark' : ''}`}
            target="_blank"
            rel="noopener noreferrer"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
            </svg>
            GitHub
          </a>
          
          <a 
            href="https://discord.gg/mcpbench" 
            className={`topbar-button primary ${isDarkMode ? 'dark' : ''}`}
            target="_blank"
            rel="noopener noreferrer"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
              <path d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515.074.074 0 0 0-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0 12.64 12.64 0 0 0-.617-1.25.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 0 0 .031.057 19.9 19.9 0 0 0 5.993 3.03.078.078 0 0 0 .084-.028c.462-.63.874-1.295 1.226-1.994a.076.076 0 0 0-.041-.106 13.107 13.107 0 0 1-1.872-.892.077.077 0 0 1-.008-.128 10.2 10.2 0 0 0 .372-.292.074.074 0 0 1 .077-.01c3.928 1.793 8.18 1.793 12.062 0a.074.074 0 0 1 .078.01c.12.098.246.198.373.292a.077.077 0 0 1-.006.127 12.299 12.299 0 0 1-1.873.892.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028 19.839 19.839 0 0 0 6.002-3.03.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 0 0-.031-.03zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.956-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.955-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.946 2.418-2.157 2.418z"/>
            </svg>
            Discord
          </a>
          
          <button 
            className={`mobile-menu-toggle ${isDarkMode ? 'dark' : ''}`}
            onClick={toggleMobileMenu}
            aria-label="Toggle mobile menu"
          >
            ☰
          </button>
        </div>
      </div>
      
      {/* Mobile Navigation */}
      <div className={`mobile-nav ${isMobileMenuOpen ? 'open' : ''} ${isDarkMode ? 'dark' : ''}`}>
        <div className="mobile-nav-item">
          <a href="/docs" className={`mobile-nav-link ${isDarkMode ? 'dark' : ''}`}>
            Docs
          </a>
        </div>
        <div className="mobile-nav-item">
          <a href="/leaderboard" className={`mobile-nav-link ${isDarkMode ? 'dark' : ''}`}>
            Leaderboard
          </a>
        </div>
        <div className="mobile-nav-item">
          <a href="/tasks" className={`mobile-nav-link ${isDarkMode ? 'dark' : ''}`}>
            Tasks
          </a>
        </div>
        <div className="mobile-nav-item">
          <a href="/registry" className={`mobile-nav-link ${isDarkMode ? 'dark' : ''}`}>
            Registry
          </a>
        </div>
        <div className="mobile-nav-item">
          <a href="/contributors" className={`mobile-nav-link ${isDarkMode ? 'dark' : ''}`}>
            Contributors
          </a>
        </div>
        <div className="mobile-nav-item">
          <a href="/news" className={`mobile-nav-link ${isDarkMode ? 'dark' : ''}`}>
            News
          </a>
        </div>
      </div>
    </>
  );
}
