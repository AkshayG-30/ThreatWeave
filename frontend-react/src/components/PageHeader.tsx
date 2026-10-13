import React from 'react';

interface PageHeaderProps {
  title: string;
  subtitle: string;
  milestoneTag?: string;
  actions?: React.ReactNode;
}

export const PageHeader: React.FC<PageHeaderProps> = ({
  title,
  subtitle,
  milestoneTag,
  actions,
}) => {
  return (
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.75rem', gap: '1rem', flexWrap: 'wrap' }}>
      <div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
          <h1 style={{ fontSize: '1.45rem', fontWeight: 700 }}>{title}</h1>
          {milestoneTag && (
            <span className="soc-badge soc-badge-cyan font-mono" style={{ fontSize: '0.7rem' }}>
              {milestoneTag}
            </span>
          )}
        </div>
        <p style={{ color: 'var(--tw-text-secondary)', fontSize: '0.85rem', marginTop: '0.2rem' }}>
          {subtitle}
        </p>
      </div>
      {actions && <div>{actions}</div>}
    </div>
  );
};
