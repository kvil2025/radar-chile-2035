export interface Bus {
  id: number;
  code: string;
  name: string;
  voltage_kv: number;
  latitude: number;
  longitude: number;
  zone: string;
  region: string;
  substation_id?: number;
  status: string;
  latest_price?: number;
  opportunity_score?: number;
  recommendation_level?: string;
}

export interface Substation {
  id: number;
  code: string;
  name: string;
  latitude: number;
  longitude: number;
  voltage_levels: string;
  capacity_mva?: number;
  operator: string;
  status: string;
}

export interface TransmissionLine {
  id: number;
  code: string;
  name: string;
  from_bus_id: number;
  to_bus_id: number;
  voltage_kv: number;
  capacity_mw: number;
  length_km: number;
  impedance_ohm: number;
  status: string;
  from_bus_name?: string;
  to_bus_name?: string;
  current_flow_mw?: number;
  utilization_pct?: number;
  is_congested: boolean;
}

export interface GenerationPlant {
  id: number;
  name: string;
  technology: string;
  capacity_mw: number;
  latitude: number;
  longitude: number;
  bus_id: number;
  operator: string;
  status: string;
  capacity_factor_avg: number;
  bus_name?: string;
}

export interface BessUnit {
  id: number;
  name: string;
  power_mw: number;
  energy_mwh: number;
  duration_hours: number;
  round_trip_efficiency: number;
  latitude?: number;
  longitude?: number;
  bus_id: number;
  operator: string;
  status: string;
  bus_name?: string;
}

export interface ProjectPipeline {
  id: number;
  name: string;
  technology: string;
  capacity_mw: number;
  storage_mwh: number;
  latitude: number;
  longitude: number;
  bus_id?: number;
  status: string;
  expected_cod_year: number;
  owner: string;
  estimated_capex_musd: number;
  description?: string;
  bus_name?: string;
}

export interface NodePrice {
  id: number;
  bus_id: number;
  timestamp: string;
  price_usd_mwh: number;
  marginal_energy_cost: number;
  marginal_loss_cost: number;
  marginal_congestion_cost: number;
  quality_status: string;
}

export interface GenerationHourly {
  id: number;
  timestamp: string;
  solar_mw: number;
  wind_mw: number;
  hydro_mw: number;
  thermal_gas_mw: number;
  thermal_coal_mw: number;
  bess_discharge_mw: number;
  bess_charge_mw: number;
  total_generation_mw: number;
  curtailment_mw: number;
  renewable_share_pct?: number;
}

export interface DemandHourly {
  id: number;
  timestamp: string;
  zone: string;
  total_demand_mw: number;
  mining_demand_mw: number;
  industrial_demand_mw: number;
  residential_demand_mw: number;
  data_centers_demand_mw: number;
}

export interface FuelPrice {
  id: number;
  fuel_type: string;
  timestamp: string;
  price_usd: number;
  unit: string;
}

export interface HydroBasin {
  id: number;
  basin_name: string;
  reservoir_name: string;
  timestamp: string;
  inflow_m3s: number;
  storage_m3_million: number;
  usable_percentage: number;
  hydro_year_type: string;
}

export interface NodeOpportunityScore {
  id: number;
  bus_id: number;
  bus_code?: string;
  bus_name?: string;
  zone?: string;
  timestamp: string;
  total_score: number;
  expected_price_score: number;
  capture_price_solar_score: number;
  capture_price_wind_score: number;
  bess_arbitrage_score: number;
  congestion_risk_score: number;
  curtailment_risk_score: number;
  future_competition_score: number;
  demand_growth_score: number;
  grid_expansion_score: number;
  recommendation_level: string;
  methodology_version: string;
}

export interface BusRankingItem {
  rank: number;
  bus_id: number;
  bus_code: string;
  bus_name: string;
  zone: string;
  region: string;
  opportunity_score: number;
  recommendation_level: string;
  avg_price_usd_mwh: number;
  capture_price_solar: number;
  capture_price_wind: number;
  bess_arbitrage_spread: number;
  curtailment_risk: string;
  congestion_risk: string;
  npv_musd: number;
  irr_pct: number;
  lcoe_usd_mwh: number;
  payback_years: number;
  summary_rationale: string;
}

export interface ProjectEvaluationRequest {
  technology: string;
  capacity_mw: number;
  storage_mwh: number;
  target_cod_year: number;
  lifetime_years: number;
  custom_capex_musd?: number;
  custom_opex_musd_year?: number;
  discount_rate_pct: number;
}

export interface ProjectEvaluationResult {
  request: ProjectEvaluationRequest;
  estimated_capex_musd: number;
  estimated_opex_musd_year: number;
  top_buses_ranking: BusRankingItem[];
  methodology: string;
  timestamp: string;
}
