import type { StructuredIncident } from '../types/incident';
import type { LLMExplanation } from '../types/explanation';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

export class ApiService {
    static async getScenarios(): Promise<any[]> {
        try {
            const response = await fetch(`${API_BASE_URL}/api/demo/scenarios`);
            if (!response.ok) return [];
            return await response.json();
        } catch {
            return [];
        }
    }

    static async getIncident(scenarioId: string = "TC-10"): Promise<StructuredIncident | null> {
        try {
            const response = await fetch(`${API_BASE_URL}/api/demo/scenario/${scenarioId}`);
            if (!response.ok) {
                if (response.status === 404) return null;
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error("Failed to fetch incident:", error);
            throw error;
        }
    }

    static async getExplanation(): Promise<LLMExplanation | null> {
        try {
            const response = await fetch(`${API_BASE_URL}/api/demo/explanation`);
            if (!response.ok) {
                if (response.status === 404) return null;
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error("Failed to fetch explanation:", error);
            throw error;
        }
    }
}
