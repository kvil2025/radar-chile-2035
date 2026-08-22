import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { ProjectEvaluationResult } from '../types/energy';
import { Zap, Award, Sparkles } from 'lucide-react';

export const PanelProjectSitingOptimizer: React.FC = () => {
  const [technology, setTechnology] = useState<string>('SOLAR_PLUS_BESS');
  const [capacityMw, setCapacityMw] = useState<number>(100.0);
  const [storageMwh, setStorageMwh] = useState<number>(400.0);
  const [targetCodYear, setTargetCodYear] = useState<number>(2029);
  const [lifetimeYears, setLifetimeYears] = useState<number>(25);
  const [discountRatePct, setDiscountRatePct] = useState<number>(8.0);

  const [result, setResult] = useState<ProjectEvaluationResult | null>(null);
  const [isCalculating, setIsCalculating] = useState<boolean>(false);

  const handleEvaluate = async () => {
    setIsCalculating(true);
    try {
      const res = await api.evaluateProjectSiting({
        technology,
        capacity_mw: Number(capacityMw),
        storage_mwh: Number(storageMwh),
        target_cod_year: Number(targetCodYear),
        lifetime_years: Number(lifetimeYears),
        discount_rate_pct: Number(discountRatePct)
      });
      setResult(res);
    } catch (err) {
      console.error('Error evaluating project siting:', err);
    } finally {
      setIsCalculating(false);
    }
  };

  useEffect(() => {
    handleEvaluate();
  }, []);

  const getBadgeStyle = (level: string) => {
    switch (level) {
      case 'HIGHLY_ATTRACTIVE':
        return 'text-emerald-400 bg-emerald-500/10 border-emerald-500/30';
      case 'ATTRACTIVE':
        return 'text-gold-light bg-gold-primary/10 border-gold-primary/30';
      case 'MODERATE':
        return 'text-blue-400 bg-blue-500/10 border-blue-500/30';
      default:
        return 'text-slate-400 bg-slate-800 border-slate-700';
    }
  };

  return (
    <div className="space-y-6">
      
      {/* Configuration & Parameter Form */}
      <div className="glass-panel p-6">
        <div className="flex items-center space-x-3 mb-6">
          <div className="w-10 h-10 rounded-xl bg-gold-primary/15 border border-gold-primary/40 flex items-center justify-center text-gold-primary">
            <Zap className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h3 className="text-base font-bold text-white font-heading">
                Optimizador de Localización de Proyectos (Siting Engine)
              </h3>
              <span className="px-2 py-0.5 rounded text-[9px] font-mono font-bold bg-gold-primary/15 text-gold-light border border-gold-primary/30">
                DCF FINANCIAL MODEL v0.1
              </span>
            </div>
            <p className="text-xs text-slate-400">
              Evalúa proyectos de generación y almacenamiento para identificar las barras con mayor NPV, IRR y menor riesgo de curtailment
            </p>
          </div>
        </div>

        {/* Form Inputs Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-4 mb-6">
          
          {/* Technology */}
          <div className="p-3.5 rounded-xl bg-bg-card border border-border-subtle lg:col-span-2">
            <label className="text-[10px] font-mono text-slate-400 block uppercase mb-1">Tecnología de Generación</label>
            <select
              value={technology}
              onChange={(e) => {
                const val = e.target.value;
                setTechnology(val);
                if (val === 'SOLAR_PV') setStorageMwh(0);
                if (val === 'WIND') setStorageMwh(0);
                if (val === 'SOLAR_PLUS_BESS' && storageMwh === 0) setStorageMwh(capacityMw * 4);
              }}
              className="w-full bg-[#111114] border border-border-subtle focus:border-gold-primary/60 rounded-lg px-3 py-2 text-xs text-white outline-none"
            >
              <option value="SOLAR_PLUS_BESS">Solar PV + BESS Storage (Híbrido)</option>
              <option value="SOLAR_PV">Solar Fotovoltaica Pura (PV)</option>
              <option value="BESS">BESS Standalone (Almacenamiento Puro)</option>
              <option value="WIND">Parque Eólico (Wind)</option>
            </select>
          </div>

          {/* Capacity MW */}
          <div className="p-3.5 rounded-xl bg-bg-card border border-border-subtle">
            <label className="text-[10px] font-mono text-slate-400 block uppercase mb-1">Potencia (MW)</label>
            <input
              type="number"
              min={1}
              max={1500}
              value={capacityMw}
              onChange={(e) => {
                const mw = parseFloat(e.target.value) || 0;
                setCapacityMw(mw);
                if (technology === 'SOLAR_PLUS_BESS') setStorageMwh(mw * 4);
              }}
              className="w-full bg-[#111114] border border-border-subtle focus:border-gold-primary/60 rounded-lg px-3 py-2 text-xs text-white font-mono font-bold outline-none"
            />
          </div>

          {/* Storage MWh */}
          <div className="p-3.5 rounded-xl bg-bg-card border border-border-subtle">
            <label className="text-[10px] font-mono text-slate-400 block uppercase mb-1">BESS Storage (MWh)</label>
            <input
              type="number"
              min={0}
              max={6000}
              value={storageMwh}
              onChange={(e) => setStorageMwh(parseFloat(e.target.value) || 0)}
              className="w-full bg-[#111114] border border-border-subtle focus:border-gold-primary/60 rounded-lg px-3 py-2 text-xs text-white font-mono font-bold outline-none"
            />
          </div>

          {/* Target COD Year */}
          <div className="p-3.5 rounded-xl bg-bg-card border border-border-subtle">
            <label className="text-[10px] font-mono text-slate-400 block uppercase mb-1">Año Entrada (COD)</label>
            <select
              value={targetCodYear}
              onChange={(e) => setTargetCodYear(parseInt(e.target.value))}
              className="w-full bg-[#111114] border border-border-subtle focus:border-gold-primary/60 rounded-lg px-3 py-2 text-xs text-white outline-none"
            >
              {[2026, 2027, 2028, 2029, 2030, 2032, 2035].map((y) => (
                <option key={y} value={y}>{y} {y >= 2029 ? '(Post Kimal-Lo Aguirre)' : ''}</option>
              ))}
            </select>
          </div>

          {/* Discount Rate */}
          <div className="p-3.5 rounded-xl bg-bg-card border border-border-subtle">
            <label className="text-[10px] font-mono text-slate-400 block uppercase mb-1">Tasa Descuento (%)</label>
            <input
              type="number"
              step={0.5}
              min={4}
              max={15}
              value={discountRatePct}
              onChange={(e) => setDiscountRatePct(parseFloat(e.target.value) || 8.0)}
              className="w-full bg-[#111114] border border-border-subtle focus:border-gold-primary/60 rounded-lg px-3 py-2 text-xs text-white font-mono font-bold outline-none"
            />
          </div>

          {/* Lifetime Years */}
          <div className="p-3.5 rounded-xl bg-bg-card border border-border-subtle">
            <label className="text-[10px] font-mono text-slate-400 block uppercase mb-1">Vida Útil (Años)</label>
            <input
              type="number"
              min={10}
              max={40}
              value={lifetimeYears}
              onChange={(e) => setLifetimeYears(parseInt(e.target.value) || 25)}
              className="w-full bg-[#111114] border border-border-subtle focus:border-gold-primary/60 rounded-lg px-3 py-2 text-xs text-white font-mono font-bold outline-none"
            />
          </div>

        </div>

        {/* Action Buttons */}
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center space-x-2">
            <button
              onClick={async () => {
                try {
                  const blob = await api.downloadExcelModel({
                    technology,
                    capacity_mw: Number(capacityMw),
                    storage_mwh: Number(storageMwh),
                    target_cod_year: Number(targetCodYear),
                    lifetime_years: Number(lifetimeYears),
                    discount_rate_pct: Number(discountRatePct)
                  });
                  const url = window.URL.createObjectURL(blob);
                  const a = document.createElement('a');
                  a.href = url;
                  a.download = `Modelo_Financiero_SEN_${technology}_${capacityMw}MW.xls`;
                  document.body.appendChild(a);
                  a.click();
                  a.remove();
                } catch (e) {
                  console.error(e);
                }
              }}
              className="px-4 py-2 rounded-xl bg-navy-800 hover:bg-navy-700 text-gold-light border border-navy-700 hover:border-gold-primary/40 font-mono text-xs font-semibold flex items-center space-x-1.5 transition-all"
            >
              <span>📥 Descargar Modelo Excel (.xls)</span>
            </button>

            <button
              onClick={async () => {
                try {
                  const html = await api.getInvestmentMemoHtml({
                    technology,
                    capacity_mw: Number(capacityMw),
                    storage_mwh: Number(storageMwh),
                    target_cod_year: Number(targetCodYear),
                    lifetime_years: Number(lifetimeYears),
                    discount_rate_pct: Number(discountRatePct)
                  });
                  const win = window.open('', '_blank');
                  if (win) {
                    win.document.write(html);
                    win.document.close();
                  }
                } catch (e) {
                  console.error(e);
                }
              }}
              className="px-4 py-2 rounded-xl bg-bg-card hover:bg-bg-card-hover text-slate-300 border border-border-subtle hover:text-white font-mono text-xs font-semibold flex items-center space-x-1.5 transition-all"
            >
              <span>📄 Ver Memorándum de Inversión (PDF)</span>
            </button>
          </div>

          <button
            onClick={handleEvaluate}
            disabled={isCalculating}
            className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-gold-primary to-gold-light text-black font-bold text-xs uppercase tracking-wider flex items-center space-x-2 shadow-lg shadow-gold-primary/20 hover:opacity-95 transition-all disabled:opacity-50"
          >
            <Sparkles className={`w-4 h-4 ${isCalculating ? 'animate-spin' : ''}`} />
            <span>{isCalculating ? 'Calculando Top Barras...' : 'Optimizar Localización en el SEN'}</span>
          </button>
        </div>

      </div>

      {/* Financial Summary & Ranking Table */}
      {result && (
        <div className="space-y-6 animate-in fade-in duration-300">
          
          {/* Financial KPIs Banner */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="glass-panel p-5">
              <span className="text-[10px] font-mono text-slate-400 uppercase block">CAPEX Total Estimado</span>
              <span className="text-2xl font-black font-heading text-white mt-1 block">
                ${result.estimated_capex_musd.toFixed(1)} <small className="text-xs text-slate-400 font-normal">M USD</small>
              </span>
              <span className="text-[10px] font-mono text-slate-500 mt-1 block">
                {capacityMw} MW Gen + {storageMwh} MWh BESS
              </span>
            </div>

            <div className="glass-panel p-5">
              <span className="text-[10px] font-mono text-slate-400 uppercase block">OPEX Anual Estimado</span>
              <span className="text-2xl font-black font-heading text-slate-200 mt-1 block">
                ${result.estimated_opex_musd_year.toFixed(1)} <small className="text-xs text-slate-400 font-normal">M USD/año</small>
              </span>
              <span className="text-[10px] font-mono text-slate-500 mt-1 block">
                O&M, seguros y peajes de transmisión
              </span>
            </div>

            <div className="glass-panel p-5 border-l-4 border-l-gold-primary">
              <span className="text-[10px] font-mono text-gold-primary uppercase font-bold block">Mejor Barra Identificada</span>
              <span className="text-xl font-bold font-heading text-white mt-1 block">
                {result.top_buses_ranking[0]?.bus_name}
              </span>
              <span className="text-[11px] font-mono text-emerald-400 font-semibold mt-1 block">
                NPV: +${result.top_buses_ranking[0]?.npv_musd.toFixed(1)}M USD • IRR: {result.top_buses_ranking[0]?.irr_pct.toFixed(1)}%
              </span>
            </div>
          </div>

          {/* Ranking Table */}
          <div className="glass-panel p-6 overflow-hidden">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-2">
                <Award className="w-5 h-5 text-gold-primary" />
                <h4 className="text-sm font-bold text-white font-heading">
                  Top 10 Barras del SEN para Inyección & Retorno Económico
                </h4>
              </div>
              <span className="text-[10px] font-mono text-slate-400">
                Ordenado por Valor Presente Neto (NPV)
              </span>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead>
                  <tr className="border-b border-border-subtle text-slate-400 font-mono text-[10px] uppercase">
                    <th className="py-3 px-2">Rank</th>
                    <th className="py-3 px-2">Barra / Subestación</th>
                    <th className="py-3 px-2">Zona</th>
                    <th className="py-3 px-2 text-right">NPV (M USD)</th>
                    <th className="py-3 px-2 text-right">IRR (%)</th>
                    <th className="py-3 px-2 text-right">LCOE ($/MWh)</th>
                    <th className="py-3 px-2 text-right">Payback</th>
                    <th className="py-3 px-2 text-center">Score</th>
                    <th className="py-3 px-3">Justificación Cuantitativa</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border-subtle">
                  {result.top_buses_ranking.map((bus) => (
                    <tr key={bus.bus_id} className="hover:bg-bg-card-hover transition-colors group">
                      <td className="py-3.5 px-2">
                        <span className={`w-6 h-6 rounded-lg flex items-center justify-center font-bold font-mono text-xs ${
                          bus.rank === 1 ? 'bg-gold-primary text-black' : bus.rank === 2 ? 'bg-slate-300 text-black' : bus.rank === 3 ? 'bg-amber-700 text-white' : 'bg-slate-800 text-slate-400'
                        }`}>
                          {bus.rank}
                        </span>
                      </td>

                      <td className="py-3.5 px-2">
                        <span className="font-bold text-white block group-hover:text-gold-light transition-colors">
                          {bus.bus_name}
                        </span>
                        <span className="text-[10px] font-mono text-slate-500">
                          {bus.bus_code}
                        </span>
                      </td>

                      <td className="py-3.5 px-2">
                        <span className="text-[10px] font-mono text-slate-300 bg-navy-900 px-2 py-0.5 rounded border border-navy-700">
                          {bus.zone}
                        </span>
                      </td>

                      <td className="py-3.5 px-2 text-right font-mono font-bold text-emerald-400">
                        +${bus.npv_musd.toFixed(1)}M
                      </td>

                      <td className="py-3.5 px-2 text-right font-mono font-bold text-gold-light">
                        {bus.irr_pct.toFixed(1)}%
                      </td>

                      <td className="py-3.5 px-2 text-right font-mono text-slate-300">
                        ${bus.lcoe_usd_mwh.toFixed(1)}
                      </td>

                      <td className="py-3.5 px-2 text-right font-mono text-slate-400">
                        {bus.payback_years.toFixed(1)} años
                      </td>

                      <td className="py-3.5 px-2 text-center">
                        <span className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded border ${getBadgeStyle(bus.recommendation_level)}`}>
                          {bus.opportunity_score}
                        </span>
                      </td>

                      <td className="py-3.5 px-3 text-[11px] text-slate-300 max-w-xs leading-relaxed">
                        {bus.summary_rationale}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

          </div>

        </div>
      )}

    </div>
  );
};
