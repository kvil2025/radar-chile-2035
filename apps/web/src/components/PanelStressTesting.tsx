import React, { useState } from 'react';
import { api } from '../services/api';
import { Sliders, Play, TrendingUp, TrendingDown, Activity, Sparkles, RefreshCw } from 'lucide-react';

export const PanelStressTesting: React.FC = () => {
  const [copperPrice, setCopperPrice] = useState<number>(4.80);
  const [us10yYield, setUs10yYield] = useState<number>(4.20);
  const [oilPrice, setOilPrice] = useState<number>(78.0);
  const [chinaPmi, setChinaPmi] = useState<number>(51.5);
  const [dxyIndex, setDxyIndex] = useState<number>(103.5);

  const [simulationResult, setSimulationResult] = useState<any>(null);
  const [isSimulating, setIsSimulating] = useState<boolean>(false);

  const handleSimulate = async () => {
    setIsSimulating(true);
    try {
      const data = await api.simulateShock({
        copper_price: Number(copperPrice),
        us10y_yield: Number(us10yYield),
        oil_price: Number(oilPrice),
        china_pmi: Number(chinaPmi),
        dxy_index: Number(dxyIndex),
      });
      setSimulationResult(data);
    } catch (err) {
      console.error(err);
    } finally {
      setIsSimulating(false);
    }
  };

  return (
    <div className="space-y-6">
      
      {/* Simulation Controls Panel */}
      <div className="glass-panel p-6">
        <div className="flex items-center space-x-3 mb-6">
          <div className="w-10 h-10 rounded-xl bg-cyan-500/15 border border-cyan-500/30 flex items-center justify-center text-cyan-400">
            <Sliders className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h3 className="text-base font-bold text-white font-heading">
                Simulador de Shocks Macroeconómicos & Stress Testing
              </h3>
              <span className="px-2 py-0.5 rounded text-[9px] font-mono font-bold bg-cyan-500/10 text-cyan-300 border border-cyan-500/30">
                MODELO DE ELASTICIDADES
              </span>
            </div>
            <p className="text-xs text-slate-400">
              Ajusta los parámetros macro globales para proyectar el impacto en tipo de cambio (CLP/USD), finanzas públicas e índices
            </p>
          </div>
        </div>

        {/* Sliders Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-6">
          
          {/* Copper */}
          <div className="p-4 rounded-xl bg-bg-card border border-border-subtle">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-semibold text-slate-300">Precio del Cobre</span>
              <span className="text-sm font-black font-mono text-gold-light">${copperPrice.toFixed(2)} USD/lb</span>
            </div>
            <input
              type="range"
              min={3.00}
              max={6.00}
              step={0.05}
              value={copperPrice}
              onChange={(e) => setCopperPrice(parseFloat(e.target.value))}
              className="w-full accent-gold-primary cursor-pointer"
            />
            <div className="flex justify-between text-[9px] font-mono text-slate-500 mt-1">
              <span>$3.00 (Estrés)</span>
              <span>$4.38 (Actual)</span>
              <span>$6.00 (Boom)</span>
            </div>
          </div>

          {/* US10Y */}
          <div className="p-4 rounded-xl bg-bg-card border border-border-subtle">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-semibold text-slate-300">Tasa Bono US10Y</span>
              <span className="text-sm font-black font-mono text-blue-400">{us10yYield.toFixed(2)} %</span>
            </div>
            <input
              type="range"
              min={2.50}
              max={6.50}
              step={0.05}
              value={us10yYield}
              onChange={(e) => setUs10yYield(parseFloat(e.target.value))}
              className="w-full accent-blue-400 cursor-pointer"
            />
            <div className="flex justify-between text-[9px] font-mono text-slate-500 mt-1">
              <span>2.50% (Dovish)</span>
              <span>4.69% (Actual)</span>
              <span>6.50% (Hawkish)</span>
            </div>
          </div>

          {/* China PMI */}
          <div className="p-4 rounded-xl bg-bg-card border border-border-subtle">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-semibold text-slate-300">PMI Manufacturero China</span>
              <span className="text-sm font-black font-mono text-red-400">{chinaPmi.toFixed(1)} pts</span>
            </div>
            <input
              type="range"
              min={40.0}
              max={60.0}
              step={0.5}
              value={chinaPmi}
              onChange={(e) => setChinaPmi(parseFloat(e.target.value))}
              className="w-full accent-red-400 cursor-pointer"
            />
            <div className="flex justify-between text-[9px] font-mono text-slate-500 mt-1">
              <span>40.0 (Contracción)</span>
              <span>50.0 (Neutro)</span>
              <span>60.0 (Expansión)</span>
            </div>
          </div>

          {/* DXY */}
          <div className="p-4 rounded-xl bg-bg-card border border-border-subtle">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-semibold text-slate-300">Índice Dólar DXY</span>
              <span className="text-sm font-black font-mono text-emerald-400">{dxyIndex.toFixed(1)}</span>
            </div>
            <input
              type="range"
              min={90.0}
              max={120.0}
              step={0.5}
              value={dxyIndex}
              onChange={(e) => setDxyIndex(parseFloat(e.target.value))}
              className="w-full accent-emerald-400 cursor-pointer"
            />
            <div className="flex justify-between text-[9px] font-mono text-slate-500 mt-1">
              <span>90.0 (USD Débil)</span>
              <span>104.5 (Actual)</span>
              <span>120.0 (USD Fuerte)</span>
            </div>
          </div>

          {/* Oil */}
          <div className="p-4 rounded-xl bg-bg-card border border-border-subtle">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-semibold text-slate-300">Petróleo Brent</span>
              <span className="text-sm font-black font-mono text-amber-400">${oilPrice.toFixed(1)} USD/bbl</span>
            </div>
            <input
              type="range"
              min={45.0}
              max={120.0}
              step={1.0}
              value={oilPrice}
              onChange={(e) => setOilPrice(parseFloat(e.target.value))}
              className="w-full accent-amber-400 cursor-pointer"
            />
            <div className="flex justify-between text-[9px] font-mono text-slate-500 mt-1">
              <span>$45 (Bajo)</span>
              <span>$78 (Actual)</span>
              <span>$120 (Shock de Oferta)</span>
            </div>
          </div>

          {/* Trigger Button */}
          <div className="p-4 rounded-xl bg-bg-card border border-border-subtle flex flex-col justify-end">
            <button
              onClick={handleSimulate}
              disabled={isSimulating}
              className="w-full py-3 rounded-xl bg-gradient-to-r from-gold-primary to-gold-light text-black font-bold text-xs uppercase tracking-wider flex items-center justify-center space-x-2 shadow-lg shadow-gold-primary/20 hover:opacity-95 transition-all disabled:opacity-50"
            >
              {isSimulating ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin" />
                  <span>Calculando Shock...</span>
                </>
              ) : (
                <>
                  <Play className="w-4 h-4 fill-current" />
                  <span>Simular Shock en Chile</span>
                </>
              )}
            </button>
          </div>

        </div>
      </div>

      {/* Simulation Results Display */}
      {simulationResult && (
        <div className="glass-panel p-6 animate-in fade-in duration-300">
          <div className="border-b border-border-subtle pb-4 mb-5 flex items-center justify-between">
            <div className="flex items-center space-x-2.5">
              <div className="w-8 h-8 rounded-lg bg-gold-primary/15 border border-gold-primary/30 flex items-center justify-center text-gold-primary">
                <Activity className="w-4 h-4" />
              </div>
              <div>
                <h3 className="text-base font-bold text-white font-heading">
                  Resultados del Escenario Simulado
                </h3>
                <p className="text-xs text-slate-400">
                  Proyecciones cuantitativas bajo elasticidades macroeconómicas empíricas
                </p>
              </div>
            </div>
            <span className="px-2.5 py-1 rounded-lg bg-navy-900 border border-gold-primary/30 text-xs font-mono text-gold-light">
              Régimen Simulado: {simulationResult.projections.simulated_regime}
            </span>
          </div>

          {/* KPI Output Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
            
            {/* Projected CLP */}
            <div className="p-4 rounded-xl bg-bg-card border border-border-subtle">
              <span className="text-[10px] font-mono text-slate-400 uppercase block">Tipo de Cambio Proyectado</span>
              <div className="flex items-baseline space-x-2 mt-1">
                <span className="text-2xl font-black font-heading text-white">
                  ${simulationResult.projections.projected_clp_usd}
                </span>
                <span className="text-xs text-slate-400 font-mono">CLP</span>
              </div>
              <span className={`text-[11px] font-mono font-semibold flex items-center space-x-1 mt-1 ${simulationResult.projections.clp_delta <= 0 ? 'text-emerald-400' : 'text-accent-orange'}`}>
                {simulationResult.projections.clp_delta <= 0 ? <TrendingDown className="w-3.5 h-3.5" /> : <TrendingUp className="w-3.5 h-3.5" />}
                <span>{simulationResult.projections.clp_delta > 0 ? `+${simulationResult.projections.clp_delta}` : simulationResult.projections.clp_delta} pesos</span>
              </span>
            </div>

            {/* Projected Fiscal Impact */}
            <div className="p-4 rounded-xl bg-bg-card border border-border-subtle">
              <span className="text-[10px] font-mono text-slate-400 uppercase block">Impacto Fiscal Anual</span>
              <div className="flex items-baseline space-x-2 mt-1">
                <span className={`text-2xl font-black font-heading ${simulationResult.projections.fiscal_impact_usd_million >= 0 ? 'text-emerald-400' : 'text-accent-orange'}`}>
                  {simulationResult.projections.fiscal_impact_usd_million >= 0 ? `+${simulationResult.projections.fiscal_impact_usd_million}` : simulationResult.projections.fiscal_impact_usd_million}
                </span>
                <span className="text-xs text-slate-400 font-mono">M USD</span>
              </div>
              <span className="text-[10px] font-mono text-slate-500 block mt-1">
                Regla Fiscal: $280M / 10¢ Cobre
              </span>
            </div>

            {/* Simulated Chile Opportunity */}
            <div className="p-4 rounded-xl bg-bg-card border border-border-subtle">
              <span className="text-[10px] font-mono text-slate-400 uppercase block">Chile Opportunity Simulado</span>
              <div className="flex items-baseline space-x-2 mt-1">
                <span className="text-2xl font-black font-heading text-gold-light">
                  {simulationResult.projections.simulated_chile_opportunity_score}
                </span>
                <span className="text-xs text-slate-400 font-mono">/ 100</span>
              </div>
              <span className="text-[10px] font-mono text-slate-400 block mt-1">
                Score Base: 52.3
              </span>
            </div>

            {/* Simulated Dollar Stress */}
            <div className="p-4 rounded-xl bg-bg-card border border-border-subtle">
              <span className="text-[10px] font-mono text-slate-400 uppercase block">Dollar Stress Simulado</span>
              <div className="flex items-baseline space-x-2 mt-1">
                <span className="text-2xl font-black font-heading text-blue-400">
                  {simulationResult.projections.simulated_dollar_stress_score}
                </span>
                <span className="text-xs text-slate-400 font-mono">/ 100</span>
              </div>
              <span className="text-[10px] font-mono text-slate-400 block mt-1">
                Score Base: 51.6
              </span>
            </div>

          </div>

          {/* AI Qualitative Synthesis */}
          <div className="p-5 rounded-xl bg-navy-950/60 border border-navy-800 text-xs">
            <div className="flex items-center space-x-2 mb-2 text-gold-primary font-bold font-mono text-[11px] uppercase tracking-wider">
              <Sparkles className="w-3.5 h-3.5" />
              <span>Evaluación Cuantitativa del Motor IA:</span>
            </div>
            <div className="text-slate-200 leading-relaxed whitespace-pre-line font-sans">
              {simulationResult.ai_assessment}
            </div>
          </div>

        </div>
      )}

    </div>
  );
};
