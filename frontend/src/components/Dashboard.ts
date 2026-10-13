import type { StructuredIncident, IncidentEvent } from '../types/incident';
import type { LLMExplanation } from '../types/explanation';
import cytoscape from 'cytoscape';

export class Dashboard {
    private incident: StructuredIncident | null = null;
    private explanation: LLMExplanation | null = null;
    private cy: cytoscape.Core | null = null;
    
    private rootElement: HTMLElement;
    private onRefresh: () => void;
    
    constructor(rootElement: HTMLElement, onRefresh: () => void) {
        this.rootElement = rootElement;
        this.onRefresh = onRefresh;
    }
    
    public renderLoading() {
        this.rootElement.innerHTML = `
            <div class="header">
                <div class="header-brand">
                    <h1>THREATWEAVE</h1>
                    <div class="subtitle">AI-Driven Advanced Threat Detection & Attack Reconstruction</div>
                </div>
                <div class="header-nav">
                    <span class="nav-item">Connecting to backend...</span>
                </div>
            </div>
            <div class="state-container">
                <div class="text-muted">Loading incident data...</div>
            </div>
        `;
    }

    public renderError(message: string) {
        this.rootElement.innerHTML = `
            <div class="header">
                <div class="header-brand">
                    <h1>THREATWEAVE</h1>
                    <div class="subtitle">AI-Driven Advanced Threat Detection & Attack Reconstruction</div>
                </div>
                <div class="header-nav">
                    <div class="status-indicator offline">
                        <div class="status-dot"></div> SYSTEM OFFLINE
                    </div>
                </div>
            </div>
            <div class="state-container">
                <div class="error-text">ThreatWeave backend unavailable</div>
                <div class="text-muted">${message}</div>
                <div class="text-muted">Ensure the FastAPI service is running on the correct port.</div>
                <button class="btn-refresh" style="margin-top: 1rem" id="refresh-btn">Retry Connection</button>
            </div>
        `;
        document.getElementById('refresh-btn')?.addEventListener('click', this.onRefresh);
    }

    public updateData(incident: StructuredIncident, explanation: LLMExplanation | null) {
        this.incident = incident;
        this.explanation = explanation;
        this.render();
    }

    private render() {
        if (!this.incident) return;
        
        const threatLevel = this.incident.event_count > 0 ? 'CRITICAL' : 'SAFE';
        
        this.rootElement.innerHTML = `
            <div class="header">
                <div class="header-brand">
                    <h1>THREATWEAVE</h1>
                    <div class="subtitle">AI-Driven Advanced Threat Detection & Attack Reconstruction</div>
                </div>
                <div class="header-nav">
                    <span class="nav-item">Demo Incident</span>
                    <span class="nav-item">MITRE ATT&CK</span>
                    <span class="nav-item">AI Analysis</span>
                    <button class="btn-refresh" id="refresh-btn">Refresh Analysis</button>
                    <div class="status-indicator">
                        <div class="status-dot"></div> SYSTEM ONLINE
                    </div>
                </div>
            </div>
            <div class="dashboard-content">
                <div class="metrics-row">
                    <div class="metric-card">
                        <div class="metric-title">Threat Level</div>
                        <div class="metric-value ${threatLevel === 'CRITICAL' ? 'threat-high' : ''}">${threatLevel}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-title">Events in Chain</div>
                        <div class="metric-value">${this.incident.event_count}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-title">Correlation Score</div>
                        <div class="metric-value">${this.incident.correlation_score.toFixed(1)}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-title">MITRE Techniques</div>
                        <div class="metric-value">${this.incident.mitre_mappings.filter(m => m.technique_id).length}</div>
                    </div>
                </div>

                <!-- Left Column -->
                <div style="display: flex; flex-direction: column; gap: 1rem; overflow-y: auto;">
                    <div class="panel">
                        <div class="panel-header">Detection & Anomaly</div>
                        <div class="panel-body detail-list">
                            <div class="detail-item">
                                <span class="detail-label">Supervised Avg</span>
                                <span class="detail-value">${this.incident.detection_summary.supervised_avg?.toFixed(2) || 'Not available'}</span>
                            </div>
                            <div class="detail-item">
                                <span class="detail-label">Anomaly Avg</span>
                                <span class="detail-value">${this.incident.detection_summary.anomaly_avg?.toFixed(2) || 'Not available'}</span>
                            </div>
                            <div class="detail-item">
                                <span class="detail-label">Timestamp Source</span>
                                <span class="detail-value">${this.incident.timestamp_source || 'Not available'}</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="panel" style="flex: 1">
                        <div class="panel-header">Event Details <span class="badge" id="event-selection-badge">Select Node</span></div>
                        <div class="panel-body detail-list" id="event-details-content">
                            <div class="text-muted">Click a node in the attack graph to view details.</div>
                        </div>
                    </div>
                </div>

                <!-- Middle Column -->
                <div class="panel graph-container">
                    <div class="panel-header">Attack Chain Graph</div>
                    <div id="cy"></div>
                </div>

                <!-- Right Column -->
                <div style="display: flex; flex-direction: column; gap: 1rem; overflow-y: auto;">
                    <div class="panel" style="flex: 1">
                        <div class="panel-header">
                            <div>AI Incident Explanation</div>
                            ${this.explanation?.limitations.includes('Deterministic') 
                                ? '<span class="fallback-badge">Deterministic Fallback</span>' 
                                : '<span class="ai-badge">Evidence-Grounded AI Analysis</span>'}
                        </div>
                        <div class="panel-body">
                            ${this.renderExplanation()}
                        </div>
                    </div>
                    
                    <div class="panel" style="flex: 1">
                        <div class="panel-header">MITRE ATT&CK</div>
                        <div class="panel-body mitre-list">
                            ${this.renderMitre()}
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        document.getElementById('refresh-btn')?.addEventListener('click', this.onRefresh);
        this.renderGraph();
    }
    
    private renderExplanation(): string {
        if (!this.explanation) return '<div class="text-muted">Not available</div>';
        const e = this.explanation;
        return `
            <div class="ai-summary">${e.summary}</div>
            <div class="ai-section">
                <h4>Attack Chain</h4>
                <p>${e.attack_chain}</p>
            </div>
            <div class="ai-section">
                <h4>Evidence</h4>
                <p>${e.evidence}</p>
            </div>
            <div class="ai-section">
                <h4>Investigation Recommendations</h4>
                <p>${e.investigation_recommendations}</p>
            </div>
            <button id="download-report-btn" class="btn-refresh" style="margin-top: 1rem;">DOWNLOAD INVESTIGATION REPORT</button>
            <div class="text-muted" style="font-size: 0.7rem; margin-top: 1rem;">Generated from structured ThreatWeave evidence</div>
        `;
    }

    private renderMitre(): string {
        if (!this.incident || this.incident.mitre_mappings.length === 0) {
            return '<div class="text-muted">Not available</div>';
        }
        return this.incident.mitre_mappings.map(m => `
            <div class="mitre-card">
                <div style="display: flex; justify-content: space-between">
                    <span class="mitre-id">${m.technique_id || 'UNKNOWN'}</span>
                    <span class="badge ${m.confidence}">${m.confidence}</span>
                </div>
                <div class="mitre-name">${m.technique_name || 'Not available'}</div>
                <div class="mitre-tactic">${m.tactic || ''}</div>
            </div>
        `).join('');
    }

    private renderGraph() {
        if (!this.incident) return;
        
        const elements: cytoscape.ElementDefinition[] = [];
        
        this.incident.events.forEach(ev => {
            elements.push({
                data: { 
                    id: ev.event_id, 
                    label: ev.event_id.split('_').slice(1).join('_'), // e.g., 01_RECON
                    raw: ev
                }
            });
        });
        
        this.incident.edges.forEach((edge, i) => {
            elements.push({
                data: {
                    id: `edge_${i}`,
                    source: edge.source,
                    target: edge.target,
                    weight: edge.weight,
                    label: edge.evidence_strength
                }
            });
        });

        const cyContainer = document.getElementById('cy');
        if (!cyContainer) return;

        this.cy = cytoscape({
            container: cyContainer,
            elements: elements,
            style: [
                {
                    selector: 'node',
                    style: {
                        'background-color': '#0ea5e9',
                        'label': 'data(label)',
                        'color': '#e2e8f0',
                        'font-size': '10px',
                        'text-valign': 'bottom',
                        'text-margin-y': 5,
                        'width': 20,
                        'height': 20
                    }
                },
                {
                    selector: 'node[label *= "NOISE"]',
                    style: {
                        'background-color': '#94a3b8'
                    }
                },
                {
                    selector: 'node[label *= "EXPLOIT"]',
                    style: {
                        'background-color': '#ef4444'
                    }
                },
                {
                    selector: 'edge',
                    style: {
                        'width': 1,
                        'line-color': '#292d36',
                        'target-arrow-color': '#292d36',
                        'target-arrow-shape': 'triangle',
                        'curve-style': 'bezier',
                        'opacity': 0.6
                    }
                },
                {
                    selector: 'node:selected',
                    style: {
                        'border-width': 2,
                        'border-color': '#8b5cf6',
                        'background-color': '#8b5cf6'
                    }
                }
            ],
            layout: {
                name: 'breadthfirst',
                directed: true,
                padding: 30,
                spacingFactor: 1.5
            }
        });

        document.getElementById('download-report-btn')?.addEventListener('click', () => {
            if (!this.incident || !this.explanation) return;
            const content = `# ThreatWeave Investigation Report\n\n**Scenario**: TC-10 — Full Multi-Stage APT Replay\n**Threat Level**: CRITICAL\n\n## Incident Summary\n${this.explanation.summary}\n\n## Attack Chain\n${this.explanation.attack_chain}\n\n## Evidence\n${this.explanation.evidence}\n\n## Investigation Recommendations\n${this.explanation.investigation_recommendations}`;
            const blob = new Blob([content], { type: 'text/markdown' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'ThreatWeave_Investigation_Report.md';
            a.click();
            URL.revokeObjectURL(url);
        });

        this.cy.on('tap', 'node', (evt) => {
            const data = evt.target.data('raw') as IncidentEvent;
            this.updateEventDetails(data);
        });
    }

    private updateEventDetails(ev: IncidentEvent) {
        const container = document.getElementById('event-details-content');
        const badge = document.getElementById('event-selection-badge');
        if (!container || !badge) return;
        
        badge.textContent = ev.event_id;
        
        container.innerHTML = `
            <div class="detail-item"><span class="detail-label">Source IP</span><span class="detail-value">${ev.source_ip || 'Not available'}</span></div>
            <div class="detail-item"><span class="detail-label">Dest IP</span><span class="detail-value">${ev.destination_ip || 'Not available'}</span></div>
            <div class="detail-item"><span class="detail-label">Source Port</span><span class="detail-value">${ev.source_port ?? 'Not available'}</span></div>
            <div class="detail-item"><span class="detail-label">Dest Port</span><span class="detail-value">${ev.destination_port ?? 'Not available'}</span></div>
            <div class="detail-item"><span class="detail-label">Protocol</span><span class="detail-value">${ev.protocol || 'Not available'}</span></div>
            <div class="detail-item"><span class="detail-label">Supervised Score</span><span class="detail-value">${ev.supervised_score.toFixed(3)}</span></div>
            <div class="detail-item"><span class="detail-label">Anomaly Score</span><span class="detail-value">${ev.anomaly_score.toFixed(3)}</span></div>
            <div class="detail-item"><span class="detail-label">Detection Source</span><span class="detail-value badge ${ev.detection_source}">${ev.detection_source}</span></div>
        `;
    }
}
