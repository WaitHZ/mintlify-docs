import React from 'react';

interface TaskCardProps {
  title: string;
  description: string;
  difficulty: 'easy' | 'medium' | 'hard';
  category: string;
  estimatedTime: string;
  href: string;
  tags?: string[];
}

export default function TaskCard({ 
  title, 
  description, 
  difficulty, 
  category, 
  estimatedTime, 
  href, 
  tags 
}: TaskCardProps) {
  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'easy': return 'success';
      case 'medium': return 'warning';
      case 'hard': return 'destructive';
      default: return 'secondary';
    }
  };

  return (
    <div className="task-card">
      <div className="task-header">
        <h3 className="task-title">{title}</h3>
        <div className="task-badges">
          <span className={`badge badge-${getDifficultyColor(difficulty)}`}>
            {difficulty}
          </span>
          <span className="badge badge-secondary">{category}</span>
        </div>
      </div>
      
      <p className="task-description">{description}</p>
      
      <div className="task-meta">
        <span className="task-time">⏱️ {estimatedTime}</span>
        {tags && (
          <div className="task-tags">
            {tags.map((tag, index) => (
              <span key={index} className="task-tag">#{tag}</span>
            ))}
          </div>
        )}
      </div>
      
      <div className="task-footer">
        <a href={href} className="task-link">
          View Task →
        </a>
      </div>
    </div>
  );
}
