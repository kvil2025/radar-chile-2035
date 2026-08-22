import React from 'react';
import { Scenario } from '../types';
import { Layers } from 'lucide-react';

interface PanelScenariosProps {
  scenarios: Scenario[];
}

export const PanelScenarios: React.FC<PanelScenariosProps> = ({ scenarios }) => {
  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'LOW':
        return 'text-emerald-400 bg-emerald-500/10 border-emerald-500/30';
      case 'MODERATE':
        return 'text-amber-400 bg-amber-500/10 border-amber-500/30';
      case 'HIGH':
      case 'CRITICAL':
        return 'text-accent-orange bg-accent-orange/10 border-accent-orange/30';
      default:
        return 'text-slate-400 bg-slate-800 border-slate-700';
    }
  };

  const getOpportunityColor = (opp: string) => {
    switch (opp) {
      case 'TRANSFORMATIVE':
      case 'HIGH':
        return 'text-gold-light bg-gold-primary/15 border-gold-primary/40';
      case 'MODERATE':
        return 'text-blue-400 bg-blue-500/10 border-blue-500/30';
      default:
        return 'text-slate-400 bg-slate-800 border-slate-700';
    }
  };

  return (
    <div className="glass-panel p-6">
      <div className="flex items-center justify-between mb-5">
        <div className="flex items-center space-x-2.5">
          <div className="w-8 h-8 rounded-lg bg-gold-primary/15 border border-gold-primary/30 flex items-center justify-center text-gold-primary">
            <Layers className="w-4 h-4" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h3 className="text-base font-bold text-white font-heading">Escenarios Macroeconómicos Canónicos</h3>
              <span className="px-2 py-0.5 text-[9px] font-bold font-mono uppercase bg-slate-800 text-slate-300 rounded">
                MODEL_ESTIMATE
              </span>
            </div>
            <p className="text-xs text-slate-400">Probabilidad dinámica estimada por evidencia empírica e impacto esperado en Chile</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {scenarios.map((sc) => {
          const probPct = Math.round(sc.probability * 100);
          return (
            <div
              key={sc.id}
              className="p-4 rounded-xl bg-bg-card border border-border-subtle hover:border-gold-primary/40 hover:bg-bg-card-hover transition-all flex flex-col justify-between"
            >
              <div>
                {/* Header */}
                <div className="flex items-start justify-between gap-2 mb-2">
                  <div>
                    <span className="text-[10px] font-mono text-slate-400 font-bold uppercase block">
                      {sc.scenario_code}
                    </span>
                    <h4 className="text-sm font-bold text-white font-heading">
                      {sc.name}
                    </h4>
                  </div>
                  <div className="text-right">
                    <span className="text-xl font-black font-heading text-gold-light">
                      {probPct}%
                    </span>
                    <span className="text-[9px] font-mono text-slate-500 block uppercase">
                      Probabilidad
                    </span>
                  </div>
                </div>

                {/* Probability Bar */}
                <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden my-2">
                  <div
                    className="h-full bg-gradient-to-r from-navy-700 to-gold-primary rounded-full transition-all duration-500"
                    style={{ width: `${Math.max(5, probPct)}%` }}
                  />
                </div>

                <p className="text-xs text-slate-300 my-2">
                  {sc.description}
                </p>

                {/* Expected Chile Effect Box */}
                <div className="mt-3 p-3 rounded-lg bg-navy-900/40 border border-navy-700/50 text-xs">
                  <span className="text-[10px] font-bold uppercase tracking-wider text-gold-primary font-mono block mb-1">
                    🇨🇱 Efecto Proyectado en Chile:
                  </span>
                  <p className="text-slate-300 text-[11px] leading-relaxed">
                    {sc.expected_chile_effect}
                  </p>
                </div>
              </div>

              {/* Badges footer */}
              <div className="mt-4 pt-3 border-t border-border-subtle flex items-center justify-between">
                <span className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded border ${getRiskColor(sc.risk_level)}`}>
                  RIESGO: {sc.risk_level}
                </span>
                <span className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded border ${getOpportunityColor(sc.opportunity_level)}`}>
                  OPORTUNIDAD: {sc.opportunity_level}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
