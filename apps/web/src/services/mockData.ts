import { Score, Regime } from '../types';
import { Bus, ProjectEvaluationResult } from '../types/energy';

export const MOCK_SCORES: Score[] = [
  {
    id: 1,
    score_type: 'GLOBAL_MONETARY_STRESS',
    value: 62.4,
    confidence: 0.88,
    methodology_version: 'v0.1',
    trend: 'UP',
    delta_30d: 4.2,
    timestamp: new Date().toISOString(),
    metadata_json: {
      name: 'Índice de Estrés Monetario Global',
      description: 'Presión en tasas largas de EE.UU. (US 10Y a 4.38%) y fortaleza persistente del DXY.'
    },
    contributors: [
      {
        indicator_code: 'US_10Y_YIELD',
        indicator_name: 'Tasa Tesoro EE.UU. 10 Años',
        weight: 0.35,
        raw_value: 4.38,
        normalized_value: 68.0,
        contribution_points: 23.8,
        direction: 1,
        unit: '%'
      },
      {
        indicator_code: 'DXY_INDEX',
        indicator_name: 'Dólar Global (DXY)',
        weight: 0.25,
        raw_value: 104.2,
        normalized_value: 62.0,
        contribution_points: 15.5,
        direction: 1,
        unit: 'pts'
      }
    ]
  },
  {
    id: 2,
    score_type: 'COMMODITIES_MINING_CYCLE',
    value: 78.5,
    confidence: 0.92,
    methodology_version: 'v0.1',
    trend: 'UP',
    delta_30d: 5.6,
    timestamp: new Date().toISOString(),
    metadata_json: {
      name: 'Índice de Ciclo de Commodities & Minería',
      description: 'Fundamentos sólidos impulsados por demanda de transición energética, IA data centers y bajo inventario en LME.'
    },
    contributors: [
      {
        indicator_code: 'COPPER_LME',
        indicator_name: 'Cobre Grado A (LME Spot)',
        weight: 0.50,
        raw_value: 4.45,
        normalized_value: 82.0,
        contribution_points: 41.0,
        direction: 1,
        unit: 'USD/lb'
      }
    ]
  },
  {
    id: 3,
    score_type: 'CHILE_VULNERABILITY',
    value: 48.2,
    confidence: 0.85,
    methodology_version: 'v0.1',
    trend: 'STABLE',
    delta_30d: -2.4,
    timestamp: new Date().toISOString(),
    metadata_json: {
      name: 'Índice de Vulnerabilidad Cambiaria & Inflación',
      description: 'Tipo de cambio USD/CLP estabilizado en torno a $925 con expectativas de inflación ancladas al 3.5%.'
    },
    contributors: [
      {
        indicator_code: 'USD_CLP',
        indicator_name: 'Dólar Observado (USD/CLP)',
        weight: 0.40,
        raw_value: 928.5,
        normalized_value: 48.0,
        contribution_points: 19.2,
        direction: 1,
        unit: 'CLP'
      }
    ]
  },
  {
    id: 4,
    score_type: 'ENERGY_TRANSITION_SEN',
    value: 84.6,
    confidence: 0.90,
    methodology_version: 'v0.1',
    trend: 'UP',
    delta_30d: 8.5,
    timestamp: new Date().toISOString(),
    metadata_json: {
      name: 'Índice de Oportunidad Energética (SEN)',
      description: 'Spreads de arbitraje nocturno récord ($65-$95/MWh) y avance acelerado de proyectos de almacenamiento.'
    },
    contributors: [
      {
        indicator_code: 'BESS_SPREAD',
        indicator_name: 'Spread Arbitraje BESS',
        weight: 0.45,
        raw_value: 74.5,
        normalized_value: 88.0,
        contribution_points: 39.6,
        direction: 1,
        unit: 'USD/MWh'
      }
    ]
  },
  {
    id: 5,
    score_type: 'TECH_AI_DEMAND',
    value: 72.8,
    confidence: 0.82,
    methodology_version: 'v0.1',
    trend: 'UP',
    delta_30d: 3.8,
    timestamp: new Date().toISOString(),
    metadata_json: {
      name: 'Índice de Demanda Tech / IA & Data Centers',
      description: 'Expansión de capacidad de cómputo en Santiago y demanda eléctrica minera 2035.'
    },
    contributors: [
      {
        indicator_code: 'DATA_CENTER_MW',
        indicator_name: 'Demanda Data Centers',
        weight: 0.50,
        raw_value: 450,
        normalized_value: 72.0,
        contribution_points: 36.0,
        direction: 1,
        unit: 'MW'
      }
    ]
  }
];

export const MOCK_REGIME: Regime = {
  id: 1,
  regime_code: 'GOLDILOCKS_TRANSICION_CHILE',
  confidence: 0.86,
  primary_driver: 'Cobre Favorable & Inversión BESS',
  rationale: 'Chile experimenta términos de intercambio favorables impulsados por la cotización de referencia del cobre spot en la Bolsa de Metales de Londres (LME) a $4.45 USD/lb, junto con un auge histórico en inversiones de almacenamiento BESS y centros de datos que dinamizan la demanda eléctrica estructural hacia 2035.',
  timestamp: new Date().toISOString()
};

export const MOCK_BUSES: Bus[] = [
  { id: 1, code: 'CRUCERO_220', name: 'Crucero 220 kV', voltage_kv: 220, latitude: -22.2425, longitude: -69.135, zone: 'NORTE_GRANDE', region: 'Antofagasta', status: 'OPERATIONAL', latest_price: 18.5, opportunity_score: 88.4, recommendation_level: 'HIGHLY_ATTRACTIVE' },
  { id: 2, code: 'KIMAL_500', name: 'Kimal 500 kV', voltage_kv: 500, latitude: -22.951, longitude: -69.215, zone: 'NORTE_GRANDE', region: 'Antofagasta', status: 'OPERATIONAL', latest_price: 24.2, opportunity_score: 92.6, recommendation_level: 'HIGHLY_ATTRACTIVE' },
  { id: 3, code: 'CARDONES_500', name: 'Cardones 500 kV', voltage_kv: 500, latitude: -27.391, longitude: -70.368, zone: 'NORTE_CHICO', region: 'Atacama', status: 'OPERATIONAL', latest_price: 36.8, opportunity_score: 81.2, recommendation_level: 'HIGHLY_ATTRACTIVE' },
  { id: 4, code: 'POLPAICO_500', name: 'Polpaico 500 kV', voltage_kv: 500, latitude: -33.155, longitude: -70.885, zone: 'CENTRO', region: 'Metropolitana', status: 'OPERATIONAL', latest_price: 68.5, opportunity_score: 86.5, recommendation_level: 'HIGHLY_ATTRACTIVE' },
  { id: 5, code: 'LO_AGUIRRE_500', name: 'Lo Aguirre 500 kV', voltage_kv: 500, latitude: -33.468, longitude: -70.852, zone: 'CENTRO', region: 'Metropolitana', status: 'OPERATIONAL', latest_price: 72.0, opportunity_score: 89.2, recommendation_level: 'HIGHLY_ATTRACTIVE' },
  { id: 6, code: 'CHARRUA_500', name: 'Charrúa 500 kV', voltage_kv: 500, latitude: -37.052, longitude: -72.285, zone: 'SUR', region: 'Biobío', status: 'OPERATIONAL', latest_price: 54.0, opportunity_score: 76.4, recommendation_level: 'ATTRACTIVE' }
];

export const MOCK_SITING_RESULT: ProjectEvaluationResult = {
  request: {
    technology: 'SOLAR_PLUS_BESS',
    capacity_mw: 100,
    storage_mwh: 400,
    target_cod_year: 2029,
    lifetime_years: 25,
    discount_rate_pct: 8.0
  },
  estimated_capex_musd: 168.0,
  estimated_opex_musd_year: 3.02,
  methodology: 'DCF_MODEL_v0.1_SEN_CHILE',
  timestamp: new Date().toISOString(),
  top_buses_ranking: [
    {
      rank: 1,
      bus_id: 2,
      bus_code: 'KIMAL_500',
      bus_name: 'Kimal 500 kV',
      zone: 'NORTE_GRANDE',
      region: 'Antofagasta',
      opportunity_score: 92.6,
      recommendation_level: 'HIGHLY_ATTRACTIVE',
      avg_price_usd_mwh: 34.5,
      capture_price_solar: 22.0,
      capture_price_wind: 48.0,
      bess_arbitrage_spread: 74.5,
      curtailment_risk: 'BAJO (Receptor Kimal HVDC 2029)',
      congestion_risk: 'BAJO',
      npv_musd: 64.2,
      irr_pct: 12.8,
      lcoe_usd_mwh: 42.5,
      payback_years: 7.2,
      summary_rationale: 'Excelente spread de arbitraje BESS ($74.5/MWh) y nodo de inyección directa a la línea HVDC Kimal-Lo Aguirre 2029.'
    },
    {
      rank: 2,
      bus_id: 5,
      bus_code: 'LO_AGUIRRE_500',
      bus_name: 'Lo Aguirre 500 kV',
      zone: 'CENTRO',
      region: 'Metropolitana',
      opportunity_score: 89.2,
      recommendation_level: 'HIGHLY_ATTRACTIVE',
      avg_price_usd_mwh: 72.0,
      capture_price_solar: 62.5,
      capture_price_wind: 58.0,
      bess_arbitrage_spread: 58.0,
      curtailment_risk: 'BAJO',
      congestion_risk: 'BAJO (Centro de carga)',
      npv_musd: 58.6,
      irr_pct: 12.1,
      lcoe_usd_mwh: 45.2,
      payback_years: 7.6,
      summary_rationale: 'Máximo precio de captura solar ($62.5/MWh) y proximidad inmediata al mayor polo de consumo y data centers de Santiago.'
    },
    {
      rank: 3,
      bus_id: 1,
      bus_code: 'CRUCERO_220',
      bus_name: 'Crucero 220 kV',
      zone: 'NORTE_GRANDE',
      region: 'Antofagasta',
      opportunity_score: 88.4,
      recommendation_level: 'HIGHLY_ATTRACTIVE',
      avg_price_usd_mwh: 32.0,
      capture_price_solar: 19.5,
      capture_price_wind: 46.0,
      bess_arbitrage_spread: 71.0,
      curtailment_risk: 'MODERADO',
      congestion_risk: 'BAJO',
      npv_musd: 52.4,
      irr_pct: 11.6,
      lcoe_usd_mwh: 43.1,
      payback_years: 8.1,
      summary_rationale: 'Alta radiación solar (CF 34%) y fuerte demanda minera nocturna (Codelco / Antofagasta Minerals).'
    }
  ]
};
