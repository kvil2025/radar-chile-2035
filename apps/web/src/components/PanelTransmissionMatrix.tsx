import React from 'react';
import { ChileImpactOverview } from '../types';
import { Network, ArrowRight } from 'lucide-react';

interface PanelTransmissionMatrixProps {
  overview: ChileImpactOverview | null;
}

export const PanelTransmissionMatrix: React.FC<PanelTransmissionMatrixProps> = ({ overview }) => {
  if (!overview) return null;

  return (
    <div className="glass-panel p-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 mb-5">
        <div className="flex items-center space-x-2.5">
          <div className="w-8 h-8 rounded-lg bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
            <Network className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-base font-bold text-white font-heading">Matriz de Transmisión a Chile (Chile Impact Engine)</h3>
            <p className="text-xs text-slate-400">Canales de transmisión macroeconómica y balance neto de impacto</p>
          </div>
        </div>

        {/* Net Opportunity Score Badge */}
        <div className="flex items-center space-x-3 bg-bg-card border border-gold-primary/30 px-3.5 py-1.5 rounded-xl self-start md:self-auto">
          <span className="text-xs text-slate-400 font-mono">Net Opportunity:</span>
          <span className={`text-base font-black font-heading ${overview.net_opportunity_score >= 0 ? 'text-gold-light' : 'text-accent-orange'}`}>
            {overview.net_opportunity_score >= 0 ? `+${overview.net_opportunity_score}` : overview.net_opportunity_score} pts
          </span>
        </div>
      </div>

      {/* Channels List */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
        {overview.channels.map((ch) => {
          const isPositive = ch.current_impact_score >= 0;
          return (
            <div
              key={ch.id}
              className="p-4 rounded-xl bg-bg-card border border-border-subtle hover:border-gold-primary/30 transition-all flex flex-col justify-between"
            >
              <div>
                {/* Channel mapping */}
                <div className="flex items-center justify-between gap-2 mb-2">
                  <div className="flex items-center space-x-1.5 text-xs font-bold font-mono">
                    <span className="text-blue-300 bg-navy-900 px-2 py-0.5 rounded border border-navy-700">
                      {ch.global_indicator_code}
                    </span>
                    <ArrowRight className="w-3.5 h-3.5 text-slate-500" />
                    <span className="text-red-300 bg-red-950/60 px-2 py-0.5 rounded border border-red-800/40">
                      {ch.chile_indicator_code}
                    </span>
                  </div>

                  <span className={`text-xs font-bold font-mono px-2 py-0.5 rounded border ${isPositive ? 'text-emerald-400 bg-emerald-500/10 border-emerald-500/30' : 'text-accent-orange bg-accent-orange/10 border-accent-orange/30'}`}>
                    {isPositive ? `+${ch.current_impact_score}` : ch.current_impact_score} pts
                  </span>
                </div>

                <h4 className="text-xs font-semibold text-white font-heading mt-1">
                  {ch.channel_name}
                </h4>

                <p className="text-[11px] text-slate-400 mt-1.5 leading-relaxed">
                  {ch.description}
                </p>
              </div>

              <div className="mt-3 pt-2.5 border-t border-border-subtle flex items-center justify-between text-[10px] font-mono text-slate-500">
                <span>Velocidad: <strong className="text-slate-300">{ch.transmission_speed}</strong></span>
                <span>Elasticidad: <strong className="text-slate-300">{ch.elasticity}</strong></span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
