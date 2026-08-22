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

const API_BASE = (import.meta as any).env?.VITE_API_BASE_URL || '/api/v1';

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
  },

  async getBriefing(): Promise<any> {
    const res = await fetch(`${API_BASE}/agents/briefing`);
    if (!res.ok) throw new Error('Failed to fetch briefing');
    return res.json();
  },

  async askChiefEconomist(question: string): Promise<any> {
    const res = await fetch(`${API_BASE}/agents/query`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question })
    });
    if (!res.ok) throw new Error('Failed to query chief economist');
    return res.json();
  },

  async simulateShock(params: {
    copper_price: number;
    us10y_yield: number;
    oil_price?: number;
    china_pmi?: number;
    dxy_index?: number;
  }): Promise<any> {
    const res = await fetch(`${API_BASE}/agents/simulate-shock`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(params)
    });
    if (!res.ok) throw new Error('Failed to simulate shock');
    return res.json();
  },

  // ----------------- SEN ENERGY APIS -----------------
  async getEnergyBuses(zone?: string): Promise<any[]> {
    const url = zone ? `${API_BASE}/energy/buses?zone=${zone}` : `${API_BASE}/energy/buses`;
    const res = await fetch(url);
    if (!res.ok) throw new Error('Failed to fetch energy buses');
    return res.json();
  },

  async getTransmissionLines(): Promise<any[]> {
    const res = await fetch(`${API_BASE}/energy/lines`);
    if (!res.ok) throw new Error('Failed to fetch transmission lines');
    return res.json();
  },

  async getGenerationMix(): Promise<any[]> {
    const res = await fetch(`${API_BASE}/energy/generation-mix`);
    if (!res.ok) throw new Error('Failed to fetch generation mix');
    return res.json();
  },

  async getDemandHourly(): Promise<any[]> {
    const res = await fetch(`${API_BASE}/energy/demand-hourly`);
    if (!res.ok) throw new Error('Failed to fetch demand hourly');
    return res.json();
  },

  async getEnergyProjects(): Promise<any[]> {
    const res = await fetch(`${API_BASE}/energy/projects`);
    if (!res.ok) throw new Error('Failed to fetch energy projects');
    return res.json();
  },

  async getNodeOpportunityRanking(): Promise<any[]> {
    const res = await fetch(`${API_BASE}/energy/node-opportunity-ranking`);
    if (!res.ok) throw new Error('Failed to fetch node opportunity ranking');
    return res.json();
  },

  async evaluateProjectSiting(params: any): Promise<any> {
    const res = await fetch(`${API_BASE}/energy/project-analyzer`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(params)
    });
    if (!res.ok) throw new Error('Failed to evaluate project siting');
    return res.json();
  },

  async downloadExcelModel(params: any): Promise<Blob> {
    const res = await fetch(`${API_BASE}/energy/export/excel`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(params)
    });
    if (!res.ok) throw new Error('Failed to download Excel model');
    return res.blob();
  },

  async getInvestmentMemoHtml(params: any): Promise<string> {
    const res = await fetch(`${API_BASE}/energy/export/memo-html`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(params)
    });
    if (!res.ok) throw new Error('Failed to get Investment Memo HTML');
    return res.text();
  },

  async getNodePrices(busId: number): Promise<any[]> {
    const res = await fetch(`${API_BASE}/energy/node-prices/${busId}`);
    if (!res.ok) throw new Error('Failed to fetch node prices');
    return res.json();
  },

  // ----------------- COSTO MARGINAL ML & REGULATION -----------------
  async getCostoMarginalSummary(): Promise<any> {
    const res = await fetch(`${API_BASE}/costo-marginal/dataset-summary`);
    if (!res.ok) throw new Error('Failed to fetch costo marginal summary');
    return res.json();
  },

  async trainAndForecastCostoMarginal(horizonHours: number = 72, nEstimators: number = 60): Promise<any> {
    const res = await fetch(`${API_BASE}/costo-marginal/train-predict?horizon_hours=${horizonHours}&n_estimators=${nEstimators}`, {
      method: 'POST'
    });
    if (!res.ok) throw new Error('Failed to train forecast model');
    return res.json();
  },

  async getClimateCorrelations(): Promise<any> {
    const res = await fetch(`${API_BASE}/costo-marginal/climate-correlation`);
    if (!res.ok) throw new Error('Failed to fetch climate correlations');
    return res.json();
  },

  async getRegulatoryCorpus(query?: string, category?: string): Promise<any[]> {
    let url = `${API_BASE}/costo-marginal/regulatory-corpus?`;
    if (query) url += `query=${encodeURIComponent(query)}&`;
    if (category) url += `category=${encodeURIComponent(category)}&`;
    const res = await fetch(url);
    if (!res.ok) throw new Error('Failed to fetch regulatory corpus');
    return res.json();
  }
};
