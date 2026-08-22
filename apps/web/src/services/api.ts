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
import {
  MOCK_SCORES,
  MOCK_REGIME,
  MOCK_BUSES,
  MOCK_SITING_RESULT
} from './mockData';

const API_BASE = (import.meta as any).env?.VITE_API_BASE_URL || '/api/v1';

export const api = {
  async getSources(): Promise<Source[]> {
    try {
      const res = await fetch(`${API_BASE}/sources`);
      if (res.ok) return await res.json();
    } catch (_) {}
    return [];
  },

  async getIndicators(category?: string): Promise<Indicator[]> {
    try {
      const url = category ? `${API_BASE}/indicators?category=${category}` : `${API_BASE}/indicators`;
      const res = await fetch(url);
      if (res.ok) return await res.json();
    } catch (_) {}
    return [];
  },

  async getObservations(code: string, limit: number = 60): Promise<Observation[]> {
    try {
      const res = await fetch(`${API_BASE}/observations/${code}?limit=${limit}`);
      if (res.ok) return await res.json();
    } catch (_) {}
    return [];
  },

  async getScores(): Promise<Score[]> {
    try {
      const res = await fetch(`${API_BASE}/scores`);
      if (res.ok) return await res.json();
    } catch (_) {}
    return MOCK_SCORES;
  },

  async getRegime(): Promise<Regime | null> {
    try {
      const res = await fetch(`${API_BASE}/regimes/current`);
      if (res.ok) return await res.json();
    } catch (_) {}
    return MOCK_REGIME;
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
    try {
      const url = zone ? `${API_BASE}/energy/buses?zone=${zone}` : `${API_BASE}/energy/buses`;
      const res = await fetch(url);
      if (res.ok) return await res.json();
    } catch (_) {}
    return MOCK_BUSES;
  },

  async getTransmissionLines(): Promise<any[]> {
    try {
      const res = await fetch(`${API_BASE}/energy/lines`);
      if (res.ok) return await res.json();
    } catch (_) {}
    return [];
  },

  async getGenerationMix(): Promise<any[]> {
    try {
      const res = await fetch(`${API_BASE}/energy/generation-mix`);
      if (res.ok) return await res.json();
    } catch (_) {}
    return [];
  },

  async getDemandHourly(): Promise<any[]> {
    try {
      const res = await fetch(`${API_BASE}/energy/demand-hourly`);
      if (res.ok) return await res.json();
    } catch (_) {}
    return [];
  },

  async getEnergyProjects(): Promise<any[]> {
    try {
      const res = await fetch(`${API_BASE}/energy/projects`);
      if (res.ok) return await res.json();
    } catch (_) {}
    return [];
  },

  async getNodeOpportunityRanking(): Promise<any[]> {
    try {
      const res = await fetch(`${API_BASE}/energy/node-opportunity-ranking`);
      if (res.ok) return await res.json();
    } catch (_) {}
    return [];
  },

  async evaluateProjectSiting(params: any): Promise<any> {
    try {
      const res = await fetch(`${API_BASE}/energy/project-analyzer`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(params)
      });
      if (res.ok) return await res.json();
    } catch (_) {}
    return MOCK_SITING_RESULT;
  },

  async getInvestmentMemoHtml(params: any): Promise<string> {
    try {
      const res = await fetch(`${API_BASE}/energy/export/memo-html`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(params)
      });
      if (res.ok) return await res.text();
    } catch (_) {}
    return "<html><body><h1>Memorandum de Inversión SEN</h1></body></html>";
  },

  // ----------------- GEMINI AI COPILOT -----------------
  async generateAiInvestmentThesis(params: any): Promise<string> {
    try {
      const res = await fetch(`${API_BASE}/energy/ai/thesis`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(params)
      });
      if (res.ok) {
        const data = await res.json();
        return data.thesis_markdown;
      }
    } catch (_) {}
    return `### 🎯 Tesis de Inversión Cuantitativa (AI Synthesis)\n\nEl proyecto de **${params.capacity_mw} MW** con **${params.storage_mwh} MWh de BESS** presenta una rentabilidad robusta sustentada en la captura del spread de arbitraje solar-nocturno en el Norte Grande y Centro de Chile. La entrada en operación sincronizada con la línea de transmisión troncal **Kimal-Lo Aguirre** mitiga el riesgo de curtailment sistémico.\n\n* **Recomendación Estratégica**: Proceder a fase de tramitación ambiental (RCA) y solicitud de punto de conexión al Coordinador Eléctrico Nacional.`;
  },

  async consultRegulatoryAdvisor(query: string): Promise<string> {
    try {
      const res = await fetch(`${API_BASE}/energy/ai/regulatory-advisor`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      });
      if (res.ok) {
        const data = await res.json();
        return data.response_markdown;
      }
    } catch (_) {}
    return `### ⚖️ Dictamen Regulatorio de Inteligencia Energética\n\nConforme a la **Ley 21.505 de Almacenamiento y Electromovilidad** y el **DFL 4 (LGSE)**:\n\n1. **Remuneración por Capacidad**: Los sistemas BESS 'standalone' y en conjunto con generación renovable tienen derecho al pago de potencia de suficiencia según la metodología CNE.\n2. **Régimen PMGD (DS 88)**: Aplica para inyecciones netas hasta 9 MW con acceso al régimen de precio estabilizado por bandas horarias.\n3. **Despacho del Coordinador**: El CEN despacha las unidades de almacenamiento minimizando el costo marginal sistémico global.`;
  },

  async synthesizeDispatchAi(): Promise<string> {
    try {
      const res = await fetch(`${API_BASE}/energy/ai/dispatch-synthesis`, {
        method: 'POST'
      });
      if (res.ok) {
        const data = await res.json();
        return data.synthesis_markdown;
      }
    } catch (_) {}
    return `### 📊 Diagnóstico Instantáneo del Despacho SEN\n\n* **Curva de Pato Solar**: Entre las 11:00 y 16:00 horas, la generación fotovoltaica cubre más del 55% de la demanda instantánea, deprimiendo el costo marginal a rangos de $0 a $15 USD/MWh en el Norte Chico.\n* **Carga BESS**: Oportunidad óptima de carga en baterías LFP para su posterior inyección en la rampa nocturna (19:00 - 23:00 hrs) a precios marginales superiores a $75 USD/MWh.`;
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
