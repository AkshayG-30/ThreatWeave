import './style.css';
import { ApiService } from './services/api';
import { Dashboard } from './components/Dashboard';

async function init() {
    const appDiv = document.getElementById('app');
    if (!appDiv) return;

    // Get scenario from URL
    const urlParams = new URLSearchParams(window.location.search);
    const scenarioId = urlParams.get('scenario') || 'TC-10';

    const dashboard = new Dashboard(appDiv, () => refresh(true));
    
    async function refresh(fetchAiExplanation = false) {
        dashboard.renderLoading();
        try {
            const incident = await ApiService.getIncident(scenarioId);
            let explanation = null;
            if (fetchAiExplanation) {
                explanation = await ApiService.getExplanation();
            }
            
            if (incident) {
                dashboard.updateData(incident, explanation);
                setupScenarioSelector(scenarioId);
            } else {
                dashboard.renderError('Failed to fetch demo incident data for ' + scenarioId);
            }
        } catch (error: any) {
            dashboard.renderError(error.message || 'Unknown error occurred.');
        }
    }

    async function setupScenarioSelector(currentId: string) {
        const scenarios = await ApiService.getScenarios();
        const headerNav = document.querySelector('.header-nav');
        if (!headerNav || scenarios.length === 0) return;

        let options = scenarios.map(s => 
            `<option value="${s.id}" ${s.id === currentId ? 'selected' : ''}>${s.id} — ${s.name}</option>`
        ).join('');

        const selectorHtml = `
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-right: 1rem;">
                <select id="scenario-select" style="padding: 0.3rem; background: var(--bg-card); color: var(--text-primary); border: 1px solid var(--border-color); border-radius: 4px;">
                    ${options}
                </select>
                <button id="run-scenario-btn" class="btn-refresh">RUN SCENARIO</button>
            </div>
        `;
        
        const container = document.createElement('div');
        container.innerHTML = selectorHtml;
        headerNav.prepend(container.firstElementChild as HTMLElement);

        document.getElementById('run-scenario-btn')?.addEventListener('click', () => {
            const sel = document.getElementById('scenario-select') as HTMLSelectElement;
            if (sel) {
                window.location.search = '?scenario=' + sel.value;
            }
        });
    }

    // Initial load
    await refresh();
}

document.addEventListener('DOMContentLoaded', init);
