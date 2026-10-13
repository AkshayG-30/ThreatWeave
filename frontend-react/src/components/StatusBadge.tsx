import React from 'react';
import type { ScenarioStatus } from '../types/scenario';

interface StatusBadgeProps {
  status: ScenarioStatus | 'ONLINE' | 'OFFLINE' | 'CRITICAL' | 'ELEVATED' | 'BENIGN';
  className?: string;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status, className = '' }) => {
  let badgeClass = 'soc-badge-muted';
  let label = status;

  switch (status) {
    case 'VERIFIED':
    case 'ONLINE':
    case 'BENIGN':
      badgeClass = 'soc-badge-emerald';
      break;
    case 'IMPLEMENTATION REQUIRED':
    case 'ELEVATED':
      badgeClass = 'soc-badge-amber';
      break;
    case 'EXPERIMENTAL ARTIFACT PRESENT':
      badgeClass = 'soc-badge-purple';
      break;
    case 'BLOCKED':
    case 'CRITICAL':
    case 'OFFLINE':
      badgeClass = 'soc-badge-rose';
      break;
    case 'REQUIRES DATA':
      badgeClass = 'soc-badge-cyan';
      break;
    default:
      badgeClass = 'soc-badge-muted';
  }

  return (
    <span className={`soc-badge ${badgeClass} ${className}`}>
      {label}
    </span>
  );
};
