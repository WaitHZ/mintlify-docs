import React from 'react';

interface HeroSectionProps {
  title: string;
  subtitle: string;
  image?: string;
  buttons?: Array<{
    title: string;
    href: string;
    variant?: 'primary' | 'secondary';
  }>;
}

export default function HeroSection({ title, subtitle, image, buttons }: HeroSectionProps) {
  return (
    <div className="hero-section">
      <div className="hero-content">
        <h1 className="hero-title">{title}</h1>
        <p className="hero-subtitle">{subtitle}</p>
        {buttons && (
          <div className="hero-buttons">
            {buttons.map((button, index) => (
              <a
                key={index}
                href={button.href}
                className={`hero-button ${button.variant || 'primary'}`}
              >
                {button.title}
              </a>
            ))}
          </div>
        )}
      </div>
      {image && (
        <div className="hero-image">
          <img src={image} alt="Hero" />
        </div>
      )}
    </div>
  );
}
