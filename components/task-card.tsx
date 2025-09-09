import React from 'react';

interface TaskCardProps {
  title: string;
  description: string;
  difficulty: 'easy' | 'medium' | 'hard';
  category: string;
  estimatedTime: string;
  href: string;
  tags?: string[];
  author?: string;
  githubUrl?: string;
}

export default function TaskCard({ 
  title, 
  description, 
  difficulty, 
  category, 
  estimatedTime, 
  href, 
  tags,
  author,
  githubUrl
}: TaskCardProps) {
  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'easy': return 'success';
      case 'medium': return 'warning';
      case 'hard': return 'destructive';
      default: return 'secondary';
    }
  };

  const getCategoryIcon = (category: string) => {
    switch (category.toLowerCase()) {
      case 'system administration':
      case 'system-administration':
        return '🖥️';
      case 'security':
        return '🛡️';
      case 'data science':
      case 'data-science':
        return '🧠';
      case 'research':
        return '🔬';
      case 'development':
        return '💻';
      default:
        return '📋';
    }
  };

  return (
    <div className="task-card">
      <div className="task-header">
        <div className="task-title-section">
          <h3 className="task-title">{title}</h3>
          <div className="task-category">
            <span className="category-icon">{getCategoryIcon(category)}</span>
            <span className="category-name">{category}</span>
          </div>
        </div>
        <div className="task-badges">
          <span className={`badge badge-${getDifficultyColor(difficulty)}`}>
            {difficulty}
          </span>
        </div>
      </div>
      
      <p className="task-description">{description}</p>
      
      <div className="task-meta">
        <div className="task-time">
          <span className="time-icon">⏱️</span>
          <span>{estimatedTime}</span>
        </div>
        {author && (
          <div className="task-author">
            <span className="author-icon">👤</span>
            <span>{author}</span>
          </div>
        )}
      </div>
      
      {tags && tags.length > 0 && (
        <div className="task-tags">
          {tags.map((tag, index) => (
            <span key={index} className="task-tag">#{tag}</span>
          ))}
        </div>
      )}
      
      <div className="task-footer">
        <div className="task-actions">
          <a href={href} className="task-link">
            View Task →
          </a>
          {githubUrl && (
            <a 
              href={githubUrl} 
              className="task-github-link"
              target="_blank"
              rel="noopener noreferrer"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
              </svg>
              GitHub
            </a>
          )}
        </div>
      </div>
    </div>
  );
}
