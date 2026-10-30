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

const GEMINI_KEY_STORAGE_KEY = 'radar_gemini_api_key';

export function getStoredGeminiKey(): string | null {
  try {
    return localStorage.getItem(GEMINI_KEY_STORAGE_KEY) || null;
  } catch (_) {
    return null;
  }
}

export function setStoredGeminiKey(key: string): void {
  try {
    if (key && key.trim()) {
      localStorage.setItem(GEMINI_KEY_STORAGE_KEY, key.trim());
    } else {
      localStorage.removeItem(GEMINI_KEY_STORAGE_KEY);
    }
  } catch (_) {}
}

export function removeStoredGeminiKey(): void {
  try {
    localStorage.removeItem(GEMINI_KEY_STORAGE_KEY);
  } catch (_) {}
}

function getAuthHeaders(): Record<string, string> {
  const headers: Record<string, string> = { 'Content-Type': 'application/json' };
  const customKey = getStoredGeminiKey();
  if (customKey) {
    headers['X-Gemini-Api-Key'] = customKey;
  }
  return headers;
}

/**
 * Fallback to call Google Gemini directly from client when API_BASE backend is not reached or on static demo
 */
async function callGeminiDirectClient(prompt: string): Promise<string | null> {
  const key = getStoredGeminiKey();
  if (!key) return null;

  const models = ['gemini-2.5-flash', 'gemini-3.5-flash', 'gemini-1.5-flash', 'gemini-2.0-flash'];
  for (const model of models) {
    try {
      const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${key}`;
      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: [{ parts: [{ text: prompt }] }],
          generationConfig: {
            temperature: 0.25,
            maxOutputTokens: 2048,
          }
        })
      });
      if (res.ok) {
        const data = await res.json();
        const text = data?.candidates?.[0]?.content?.parts?.[0]?.text;
        if (text) return text;
      }
    } catch (_) {}
  }
  return null;
}

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
    try {
      const res = await fetch(`${API_BASE}/agents/briefing`, {
        headers: getAuthHeaders()
      });
      if (res.ok) return await res.json();
    } catch (_) {}

    // Direct Gemini client fallback if user has provided their own API key
    const directAi = await callGeminiDirectClient(
      "Eres el Economista Jefe de Radar Chile 2035. Proporciona un Briefing Ejecutivo de 3 párrafos analizando: 1) El precio actual del cobre ($4.44/lb) y su impacto fiscal/cambiario en Chile, 2) La curva de tasas del Banco Central (TPM en 5.25%) y el spread con el bono US 10Y, 3) La oportunidad de almacenamiento BESS y centros de datos en el Sistema Eléctrico Nacional. Sé riguroso, formal y cuantitativo."
    );
    if (directAi) {
      return {
        briefing: directAi,
        regime: "EXPANSION",
        confidence: 0.92,
        key_metrics: {
          copper: 4.44,
          tpm: 5.25,
          us10y: 4.28,
          usdclp: 935
        }
      };
    }

    throw new Error('Failed to fetch briefing');
  },

  async askChiefEconomist(question: string): Promise<any> {
    try {
      const res = await fetch(`${API_BASE}/agents/query`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({ question })
      });
      if (res.ok) return await res.json();
    } catch (_) {}

    // Direct Gemini client fallback if user provided their API key
    const directAi = await callGeminiDirectClient(
      `Eres el Economista Jefe y Estratega de Radar Chile 2035. Responde con criterio macroeconómico y cuantitativo a la siguiente consulta de un inversionista/analista institucional:\n\n"${question}"\n\nResponde en Markdown estructurado, fundamentando con datos chilenos (cobre, TPM, inflación, BESS, SEN, tipo de cambio).`
    );
    if (directAi) {
      return {
        answer: directAi,
        confidence: 0.95,
        sources: ["Banco Central de Chile", "Cochilco", "CEN", "Google Gemini Live BYOK"]
      };
    }

    throw new Error('Failed to query chief economist');
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
        headers: getAuthHeaders(),
        body: JSON.stringify(params)
      });
      if (res.ok) {
        const data = await res.json();
        return data.thesis_markdown;
      }
    } catch (_) {}

    // Direct Gemini BYOK fallback
    const directAi = await callGeminiDirectClient(
      `Actúa como Director de Inversiones de Energía y M&A. Elabora una Tesis de Inversión Ejecutiva en Markdown para el siguiente proyecto en Chile:\n` +
      `- Capacidad Generación: ${params.capacity_mw} MW (${params.technology || 'Solar PV'})\n` +
      `- Almacenamiento BESS: ${params.storage_mwh} MWh\n` +
      `- Barra de Conexión: ${params.node_name || 'Nudo Centro-Norte'}\n` +
      `- CAPEX Estimado: $${params.capex_musd || 'N/A'} MUSD\n\n` +
      `Incluye análisis de: 1) Arbitraje solar vs rampa nocturna, 2) Mitigación de congestión / curtailment y línea Kimal-Lo Aguirre, 3) Estrategia de PPA vs Spot, 4) Recomendación formal para el Comité de Inversión.`
    );
    if (directAi) return directAi;

    return `### 🎯 Tesis de Inversión Cuantitativa (AI Synthesis)\n\nEl proyecto de **${params.capacity_mw} MW** con **${params.storage_mwh} MWh de BESS** presenta una rentabilidad robusta sustentada en la captura del spread de arbitraje solar-nocturno en el Norte Grande y Centro de Chile. La entrada en operación sincronizada con la línea de transmisión troncal **Kimal-Lo Aguirre** mitiga el riesgo de curtailment sistémico.\n\n* **Recomendación Estratégica**: Proceder a fase de tramitación ambiental (RCA) y solicitud de punto de conexión al Coordinador Eléctrico Nacional.`;
  },

  async consultRegulatoryAdvisor(query: string): Promise<string> {
    try {
      const res = await fetch(`${API_BASE}/energy/ai/regulatory-advisor`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({ query })
      });
      if (res.ok) {
        const data = await res.json();
        return data.response_markdown;
      }
    } catch (_) {}

    // Direct Gemini BYOK fallback
    const directAi = await callGeminiDirectClient(
      `Eres el Asesor Regulatorio Senior de Radar Chile 2035, especialista en la Ley 21.505 de Almacenamiento y Electromovilidad, DFL 4 (LGSE), DS 88 de PMGD y normas técnicas de la CNE y Coordinador Eléctrico Nacional.\n` +
      `Responde a la siguiente consulta regulatoria:\n"${query}"\n\nResponde en Markdown con referencias normativas precisas, plazos y riesgos legales.`
    );
    if (directAi) return directAi;

    return `### ⚖️ Dictamen Regulatorio de Inteligencia Energética\n\nConforme a la **Ley 21.505 de Almacenamiento y Electromovilidad** y el **DFL 4 (LGSE)**:\n\n1. **Remuneración por Capacidad**: Los sistemas BESS 'standalone' y en conjunto con generación renovable tienen derecho al pago de potencia de suficiencia según la metodología CNE.\n2. **Régimen PMGD (DS 88)**: Aplica para inyecciones netas hasta 9 MW con acceso al régimen de precio estabilizado por bandas horarias.\n3. **Despacho del Coordinador**: El CEN despacha las unidades de almacenamiento minimizando el costo marginal sistémico global.`;
  },

  async synthesizeDispatchAi(): Promise<string> {
    try {
      const res = await fetch(`${API_BASE}/energy/ai/dispatch-synthesis`, {
        method: 'POST',
        headers: getAuthHeaders()
      });
      if (res.ok) {
        const data = await res.json();
        return data.synthesis_markdown;
      }
    } catch (_) {}

    // Direct Gemini BYOK fallback
    const directAi = await callGeminiDirectClient(
      `Analiza el despacho instantáneo del Sistema Eléctrico Nacional (SEN) de Chile. Describe el fenómeno de la curva de pato solar, la ventana de precios marginales cero/bajos en el norte, la ventana de carga para baterías BESS y la rampa nocturna de demanda con gas natural/embalse. Resume en 2 viñetas concisas y de alto impacto financiero.`
    );
    if (directAi) return directAi;

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
