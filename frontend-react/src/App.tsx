import React, { useState, useEffect } from 'react';
import { IncidentProvider } from './context/IncidentContext';
import { AppLayout } from './layouts/AppLayout';
import type { PageId } from './types/navigation';
import { SecurityOverview } from './pages/SecurityOverview';
import { ScenarioLab } from './pages/ScenarioLab';
import { ModelEvaluation } from './pages/ModelEvaluation';
import { CrossDataset } from './pages/CrossDataset';
import { UnseenAttack } from './pages/UnseenAttack';
import { AttackGraph } from './pages/AttackGraph';
import { MitreMapping } from './pages/MitreMapping';
import { AiExplanation } from './pages/AiExplanation';
import { Methodology } from './pages/Methodology';

const AppContent: React.FC = () => {
  const getInitialPage = (): PageId => {
    const hash = window.location.hash.replace('#', '') as PageId;
    const validPages: PageId[] = [
      'overview',
      'scenarios',
      'models',
      'cross-dataset',
      'unseen-attack',
      'graph',
      'mitre',
      'ai-explanation',
      'methodology'
    ];
    return validPages.includes(hash) ? hash : 'overview';
  };

  const [currentPage, setCurrentPage] = useState<PageId>(getInitialPage);

  useEffect(() => {
    const handleHashChange = () => {
      const hash = window.location.hash.replace('#', '') as PageId;
      if (hash) setCurrentPage(hash);
    };
    window.addEventListener('hashchange', handleHashChange);
    return () => window.removeEventListener('hashchange', handleHashChange);
  }, []);

  const handleNavigate = (page: PageId) => {
    window.location.hash = page;
    setCurrentPage(page);
  };

  const renderCurrentPage = () => {
    switch (currentPage) {
      case 'overview':
        return <SecurityOverview onNavigate={handleNavigate} />;
      case 'scenarios':
        return <ScenarioLab onNavigate={handleNavigate} />;
      case 'models':
        return <ModelEvaluation />;
      case 'cross-dataset':
        return <CrossDataset />;
      case 'unseen-attack':
        return <UnseenAttack />;
      case 'graph':
        return <AttackGraph />;
      case 'mitre':
        return <MitreMapping />;
      case 'ai-explanation':
        return <AiExplanation />;
      case 'methodology':
        return <Methodology />;
      default:
        return <SecurityOverview onNavigate={handleNavigate} />;
    }
  };

  return (
    <AppLayout currentPage={currentPage} onNavigate={handleNavigate}>
      {renderCurrentPage()}
    </AppLayout>
  );
};

export const App: React.FC = () => {
  return (
    <IncidentProvider>
      <AppContent />
    </IncidentProvider>
  );
};

export default App;
