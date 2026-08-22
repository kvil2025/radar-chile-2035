import {
  Indicator,
  Observation,
  Score,
  Regime,
  Scenario,
  ChileImpactOverview,
  Alert,
  ResearchDocument,
  Source
} from '../types';

const API_BASE = '/api/v1';

export const api = {
  async getSources(): Promise<Source[]> {
    const res = await fetch(`${API_BASE}/sources`);
    if (!res.ok) throw new Error('Failed to fetch sources');
    return res.json();
  },

  async getIndicators(category?: string): Promise<Indicator[]> {
    const url = category ? `${API_BASE}/indicators?category=${category}` : `${API_BASE}/indicators`;
    const res = await fetch(url);
    if (!res.ok) throw new Error('Failed to fetch indicators');
    return res.json();
  },

  async getObservations(code: string, limit: number = 60): Promise<Observation[]> {
    const res = await fetch(`${API_BASE}/observations/${code}?limit=${limit}`);
    if (!res.ok) throw new Error(`Failed to fetch observations for ${code}`);
    return res.json();
  },

  async getScores(): Promise<Score[]> {
    const res = await fetch(`${API_BASE}/scores`);
    if (!res.ok) throw new Error('Failed to fetch scores');
    return res.json();
  },

  async getRegime(): Promise<Regime> {
    const res = await fetch(`${API_BASE}/regime`);
    if (!res.ok) throw new Error('Failed to fetch current regime');
    return res.json();
  },

  async getScenarios(): Promise<Scenario[]> {
    const res = await fetch(`${API_BASE}/scenarios`);
    if (!res.ok) throw new Error('Failed to fetch scenarios');
    return res.json();
  },

  async getChileImpact(): Promise<ChileImpactOverview> {
    const res = await fetch(`${API_BASE}/chile-impact`);
    if (!res.ok) throw new Error('Failed to fetch Chile impact overview');
    return res.json();
  },

  async getAlerts(status?: string): Promise<Alert[]> {
    const url = status ? `${API_BASE}/alerts?status=${status}` : `${API_BASE}/alerts`;
    const res = await fetch(url);
    if (!res.ok) throw new Error('Failed to fetch alerts');
    return res.json();
  },

  async getResearch(): Promise<ResearchDocument[]> {
    const res = await fetch(`${API_BASE}/research`);
    if (!res.ok) throw new Error('Failed to fetch research documents');
    return res.json();
  },

  async triggerRecalculate(): Promise<any> {
    const res = await fetch(`${API_BASE}/pipeline/recalculate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });
    if (!res.ok) throw new Error('Failed to trigger recalculation');
    return res.json();
  }
};
