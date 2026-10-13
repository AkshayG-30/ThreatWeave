import React, { useEffect, useState } from 'react';
import { 
  Shield, 
  FlaskConical, 
  Cpu, 
  Network, 
  Target, 
  GitFork, 
  Layers, 
  FileText, 
  BookOpen, 
  Activity, 
  Wifi, 
  WifiOff,
  Menu,
  X
} from 'lucide-react';
import { PAGES, type PageId } from '../types/navigation';
import { ApiService } from '../services/api';
import { useIncident } from '../context/IncidentContext';

interface AppLayoutProps {
  currentPage: PageId;
  onNavigate: (page: PageId) => void;
  children: React.ReactNode;
}

export const AppLayout: React.FC<AppLayoutProps> = ({
  currentPage,
  onNavigate,
  children,
}) => {
  const [backendStatus, setBackendStatus] = useState<'checking' | 'online' | 'offline'>('checking');
  const [mobileMenuOpen, setMobileMenuOpen] = useState<boolean>(false);
  const { selectedScenarioId, incident } = useIncident();

  useEffect(() => {
    let mounted = true;
    const check = async () => {
      const res = await ApiService.checkHealth();
      if (mounted) {
        setBackendStatus(res.status === 'ok' ? 'online' : 'offline');
      }
    };
    check();
    const interval = setInterval(check, 10000);
    return () => {
      mounted = false;
      clearInterval(interval);
    };
  }, []);

  const getIcon = (iconName: string) => {
    switch (iconName) {
      case 'Shield': return <Shield size={14} />;
      case 'FlaskConical': return <FlaskConical size={14} />;
      case 'Cpu': return <Cpu size={14} />;
      case 'Network': return <Network size={14} />;
      case 'Target': return <Target size={14} />;
      case 'GitFork': return <GitFork size={14} />;
      case 'Layers': return <Layers size={14} />;
      case 'FileText': return <FileText size={14} />;
      case 'BookOpen': return <BookOpen size={14} />;
      default: return <Activity size={14} />;
    }
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Top SOC Navbar */}
      <header className="soc-navbar">
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div className="soc-brand" onClick={() => onNavigate('overview')}>
            <div className="soc-brand-icon">
              <Shield size={18} />
            </div>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.45rem' }}>
                <span className="soc-brand-text">THREATWEAVE</span>
                <span className="soc-brand-badge font-mono">SOC</span>
              </div>
            </div>
          </div>

          {/* Active Scenario Quick Badge */}
          <div 
            onClick={() => onNavigate('scenarios')}
            style={{ 
              display: 'flex', 
              alignItems: 'center', 
              gap: '0.4rem', 
              cursor: 'pointer',
              background: 'rgba(6, 182, 212, 0.08)',
              border: '1px solid rgba(6, 182, 212, 0.25)',
              padding: '0.2rem 0.55rem',
              borderRadius: 'var(--tw-radius-sm)',
              fontSize: '0.72rem'
            }}
            title="Click to change scenario in Scenario Lab"
          >
            <span style={{ color: 'var(--tw-text-muted)' }}>Target:</span>
            <strong className="font-mono" style={{ color: 'var(--tw-accent-cyan)' }}>{selectedScenarioId}</strong>
            <span className="soc-badge soc-badge-emerald" style={{ padding: '0.05rem 0.35rem', fontSize: '0.65rem' }}>
              REPLAY
            </span>
            {incident && (
              <span className="font-mono" style={{ color: 'var(--tw-text-secondary)', fontSize: '0.68rem' }}>
                ({incident.event_count} ev)
              </span>
            )}
          </div>
        </div>

        {/* Desktop Navigation Bar (No horizontal clipping) */}
        <nav className="soc-nav-pills desktop-nav" aria-label="Main Navigation">
          {PAGES.map((page) => {
            const isActive = currentPage === page.id;
            return (
              <button
                key={page.id}
                onClick={() => onNavigate(page.id)}
                className={`soc-nav-pill ${isActive ? 'active' : ''}`}
                title={page.description}
              >
                {getIcon(page.iconName)}
                <span>{page.shortLabel}</span>
              </button>
            );
          })}
        </nav>

        {/* Right Status Actions */}
        <div className="soc-header-actions">
          <div 
            className="soc-system-status" 
            style={{ 
              borderColor: backendStatus === 'online' ? 'rgba(16, 185, 129, 0.3)' : 'rgba(239, 68, 68, 0.3)',
              backgroundColor: backendStatus === 'online' ? 'rgba(16, 185, 129, 0.08)' : 'rgba(239, 68, 68, 0.08)',
              color: backendStatus === 'online' ? 'var(--tw-accent-emerald)' : 'var(--tw-accent-rose)'
            }}
          >
            {backendStatus === 'online' ? (
              <>
                <div className="soc-status-pulse" />
                <Wifi size={11} />
                <span>API ONLINE</span>
              </>
            ) : backendStatus === 'checking' ? (
              <>
                <Activity size={11} />
                <span>CONNECTING...</span>
              </>
            ) : (
              <>
                <WifiOff size={11} />
                <span>API OFFLINE (CACHE MODE)</span>
              </>
            )}
          </div>

          {/* Mobile Menu Toggle Button */}
          <button 
            className="soc-btn soc-btn-secondary mobile-menu-toggle"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            style={{ padding: '0.35rem', display: 'none' }}
          >
            {mobileMenuOpen ? <X size={16} /> : <Menu size={16} />}
          </button>
        </div>
      </header>

      {/* Mobile Navigation Drawer */}
      {mobileMenuOpen && (
        <div style={{
          background: 'var(--tw-bg-card)',
          borderBottom: '1px solid var(--tw-border-subtle)',
          padding: '0.75rem 1rem',
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(130px, 1fr))',
          gap: '0.4rem',
          zIndex: 99
        }}>
          {PAGES.map((page) => (
            <button
              key={page.id}
              onClick={() => {
                onNavigate(page.id);
                setMobileMenuOpen(false);
              }}
              className={`soc-nav-pill ${currentPage === page.id ? 'active' : ''}`}
              style={{ justifyContent: 'flex-start', width: '100%' }}
            >
              {getIcon(page.iconName)}
              <span>{page.shortLabel}</span>
            </button>
          ))}
        </div>
      )}

      {/* Main Workspace */}
      <main className="soc-workspace">
        {children}
      </main>

      {/* Footer System Breadcrumbs */}
      <footer style={{
        padding: '0.65rem 1.5rem',
        borderTop: '1px solid var(--tw-border-subtle)',
        fontSize: '0.75rem',
        color: 'var(--tw-text-muted)',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        background: 'var(--tw-bg-base)',
        flexWrap: 'wrap',
        gap: '0.5rem'
      }}>
        <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center' }}>
          <span>ThreatWeave Enterprise SOC</span>
          <span>•</span>
          <span>NF-UNSW-NB15-v2 Pipeline</span>
          <span>•</span>
          <span className="font-mono">Controlled Incident INC_1 (TC-10)</span>
        </div>
        <div>
          <span>Phase 12B.1 • Standalone React Workspace</span>
        </div>
      </footer>
    </div>
  );
};
