import React from 'react';
import { Indicator } from '../types';
import { Pickaxe, TrendingUp, TrendingDown, Eye } from 'lucide-react';

interface PanelCommoditiesMiningProps {
  indicators: Indicator[];
  onSelectIndicator: (indicator: Indicator) => void;
}

export const PanelCommoditiesMining: React.FC<PanelCommoditiesMiningProps> = ({ indicators, onSelectIndicator }) => {
  const commIndicators = indicators.filter(
    i => i.category === 'COMMODITIES' || i.category === 'MINING' || i.category === 'CHINA' || i.category === 'ENERGY_TECH'
  );

  return (
    <div className="glass-panel p-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2.5">
          <div className="w-8 h-8 rounded-lg bg-gold-primary/15 border border-gold-primary/30 flex items-center justify-center text-gold-primary">
            <Pickaxe className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-base font-bold text-white font-heading">Commodities, Minería & Tracción Global</h3>
            <p className="text-xs text-slate-400">Cobre, Oro, Litio, Petróleo, Demanda China e Inversión en Datacenters / IA</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
        {commIndicators.map((ind) => (
          <div
            key={ind.id}
            onClick={() => onSelectIndicator(ind)}
            className="p-3.5 rounded-xl bg-bg-card border border-border-subtle hover:border-gold-primary/40 hover:bg-bg-card-hover transition-all cursor-pointer group flex flex-col justify-between"
          >
            <div className="flex items-start justify-between">
              <div>
                <span className="text-[10px] font-mono text-gold-light bg-gold-primary/10 border border-gold-primary/20 px-1.5 py-0.5 rounded font-bold">
                  {ind.code}
                </span>
                <h4 className="text-xs font-semibold text-slate-200 mt-1 line-clamp-1 group-hover:text-gold-light transition-colors">
                  {ind.name}
                </h4>
              </div>
              <Eye className="w-3.5 h-3.5 text-slate-500 group-hover:text-gold-primary transition-colors" />
            </div>

            <div className="mt-3 flex items-baseline justify-between">
              <span className="text-lg font-black font-heading text-white">
                {ind.latest_value !== undefined ? ind.latest_value : '—'} <span className="text-xs font-normal text-slate-400">{ind.unit}</span>
              </span>
              {ind.change_mom !== undefined && ind.change_mom !== null && (
                <span className={`text-[11px] font-mono font-semibold flex items-center space-x-0.5 ${ind.change_mom >= 0 ? 'text-emerald-400' : 'text-accent-orange'}`}>
                  {ind.change_mom >= 0 ? <TrendingUp className="w-3 h-3" /> : <TrendingDown className="w-3 h-3" />}
                  <span>{ind.change_mom > 0 ? `+${ind.change_mom}%` : `${ind.change_mom}%`}</span>
                </span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
