import type { StructuredIncident } from '../types/incident';
import type { LLMExplanation } from '../types/explanation';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

export interface HealthResponse {
  status: string;
  service: string;
}

export class ApiService {
  public static readonly baseUrl = API_BASE_URL;

  public static async checkHealth(): Promise<HealthResponse> {
    try {
      const res = await fetch(`${API_BASE_URL}/health`);
      if (!res.ok) throw new Error(`Health check failed with HTTP ${res.status}`);
      return await res.json();
    } catch (err) {
      console.warn('Backend service offline or unreachable:', err);
      return { status: 'offline', service: 'ThreatWeave' };
    }
  }

  public static async getScenarios(): Promise<unknown[]> {
    try {
      const res = await fetch(`${API_BASE_URL}/api/demo/scenarios`);
      if (!res.ok) return [];
      return await res.json();
    } catch {
      return [];
    }
  }

  public static async getScenarioIncident(scenarioId: string = 'TC-10'): Promise<StructuredIncident | null> {
    try {
      const res = await fetch(`${API_BASE_URL}/api/demo/scenario/${encodeURIComponent(scenarioId)}`);
      if (!res.ok) {
        if (res.status === 404) return null;
        throw new Error(`Failed to fetch incident ${scenarioId}: HTTP ${res.status}`);
      }
      return await res.json();
    } catch (err) {
      console.error(`Incident fetch error for ${scenarioId}:`, err);
      throw err;
    }
  }

  public static async getExplanation(scenarioId: string = 'TC-10'): Promise<LLMExplanation | null> {
    try {
      const res = await fetch(`${API_BASE_URL}/api/demo/explanation?scenario_id=${encodeURIComponent(scenarioId)}`);
      if (!res.ok) {
        if (res.status === 404) return null;
        throw new Error(`Failed to fetch explanation for ${scenarioId}: HTTP ${res.status}`);
      }
      return await res.json();
    } catch (err) {
      console.error(`Explanation fetch error for ${scenarioId}:`, err);
      throw err;
    }
  }
}
