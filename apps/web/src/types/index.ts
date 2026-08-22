export interface Source {
  id: number;
  name: string;
  provider: string;
  url?: string;
  country: string;
  frequency: string;
  reliability_score: number;
}

export interface Indicator {
  id: number;
  code: string;
  name: string;
  description?: string;
  category: string;
  unit: string;
  frequency: string;
  direction: number;
  latest_value?: number;
  latest_timestamp?: string;
  change_mom?: number;
}

export interface Observation {
  id: number;
  indicator_id: number;
  timestamp: string;
  value: number;
  original_unit?: string;
  quality_status: string;
}

export interface ScoreContributor {
  indicator_code: string;
  indicator_name: string;
  weight: number;
  raw_value: number;
  normalized_value: number;
  contribution_points: number;
  direction: number;
  unit: string;
  quality_status?: string;
}

export interface Score {
  id: number;
  score_type: string;
  timestamp: string;
  value: number;
  confidence: number;
  methodology_version: string;
  contributors: ScoreContributor[];
  trend: 'UP' | 'DOWN' | 'STABLE';
  delta_30d: number;
  metadata_json?: {
    name?: string;
    description?: string;
    [key: string]: any;
  };
}

export interface Regime {
  id: number;
  timestamp: string;
  regime_code: string;
  confidence: number;
  primary_driver: string;
  rationale: string;
  indicators_state?: {
    copper_usd_lb?: number;
    gold_usd_oz?: number;
    us10y_pct?: number;
    us30y_pct?: number;
    us_cpi_pct?: number;
    dxy_index?: number;
    china_pmi?: number;
    ai_capex_growth_pct?: number;
    evaluated_probabilities?: Record<string, number>;
  };
}

export interface Scenario {
  id: number;
  scenario_code: string;
  name: string;
  description: string;
  probability: number;
  probability_type: string;
  drivers?: string[];
  supporting_indicators?: string[];
  contradicting_indicators?: string[];
  expected_chile_effect: string;
  risk_level: string;
  opportunity_level: string;
}

export interface TransmissionChannel {
  id: number;
  channel_name: string;
  global_indicator_code: string;
  chile_indicator_code: string;
  transmission_speed: string;
  elasticity: number;
  description: string;
  current_impact_score: number;
  updated_at: string;
}

export interface ChileImpactOverview {
  net_opportunity_score: number;
  primary_positive_channel: string;
  primary_risk_channel: string;
  channels: TransmissionChannel[];
}

export interface Alert {
  id: number;
  severity: 'INFO' | 'WATCH' | 'WARNING' | 'CRITICAL';
  title: string;
  description: string;
  indicator_id?: number;
  indicator_code?: string;
  trigger_value?: number;
  current_value?: number;
  status: 'ACTIVE' | 'ACKNOWLEDGED' | 'RESOLVED';
  created_at: string;
}

export interface ResearchDocument {
  id: number;
  title: string;
  source: string;
  url?: string;
  published_at?: string;
  category: string;
  summary: string;
  relevance: number;
}
