import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { NodeOpportunityScore } from '../types/energy';
import { Award } from 'lucide-react';

export const PanelNodeOpportunityRanking: React.FC = () => {
  const [ranking, setRanking] = useState<NodeOpportunityScore[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    setIsLoading(true);
    api.getNodeOpportunityRanking()
      .then(data => {
        setRanking(data);
        setIsLoading(false);
      })
      .catch(err => {
        console.error(err);
        setIsLoading(false);
      });
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
    <div className="glass-panel p-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-6">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gold-primary/15 border border-gold-primary/30 flex items-center justify-center text-gold-primary">
            <Award className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h3 className="text-base font-bold text-white font-heading">
                Ranking de Oportunidad Nodal del SEN (Node Opportunity Score)
              </h3>
              <span className="px-2 py-0.5 rounded text-[9px] font-mono font-bold bg-gold-primary/10 text-gold-light border border-gold-primary/30">
                METODOLOGÍA v0.1
              </span>
            </div>
            <p className="text-xs text-slate-400">
              Evaluación multidimensional de barras: Precio Esperado, Captura Solar/Eólica, Arbitraje BESS y Riesgo de Congestión
            </p>
          </div>
        </div>

        <span className="text-xs font-mono text-slate-400 bg-navy-900 px-3 py-1.5 rounded-xl border border-navy-700 self-start sm:self-auto">
          {ranking.length} Barras Analizadas
        </span>
      </div>

      {isLoading ? (
        <div className="py-12 text-center text-xs text-slate-500 font-mono">
          Cargando matriz de scoring nodal...
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-border-subtle text-slate-400 font-mono text-[10px] uppercase">
                <th className="py-3 px-2">#</th>
                <th className="py-3 px-2">Barra Eléctrica</th>
                <th className="py-3 px-2">Zona</th>
                <th className="py-3 px-2 text-center">Score Total</th>
                <th className="py-3 px-2 text-right">Arbitraje BESS</th>
                <th className="py-3 px-2 text-right">Captura Solar</th>
                <th className="py-3 px-2 text-right">Captura Eólica</th>
                <th className="py-3 px-2 text-right">Demanda Local</th>
                <th className="py-3 px-2 text-right">Expansión Red</th>
                <th className="py-3 px-2 text-center">Nivel</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border-subtle">
              {ranking.map((bus, idx) => (
                <tr key={bus.id} className="hover:bg-bg-card-hover transition-colors">
                  <td className="py-3 px-2 font-mono text-slate-500 font-bold">
                    {idx + 1}
                  </td>

                  <td className="py-3 px-2 font-bold text-white">
                    {bus.bus_name || bus.bus_code}
                    <span className="text-[10px] font-mono text-slate-500 block font-normal">
                      {bus.bus_code}
                    </span>
                  </td>

                  <td className="py-3 px-2">
                    <span className="text-[10px] font-mono text-slate-300 bg-navy-900 px-2 py-0.5 rounded border border-navy-700">
                      {bus.zone?.replace('_', ' ')}
                    </span>
                  </td>

                  <td className="py-3 px-2 text-center">
                    <span className="text-sm font-black font-heading text-gold-light">
                      {bus.total_score.toFixed(1)}
                    </span>
                  </td>

                  <td className="py-3 px-2 text-right font-mono font-semibold text-emerald-400">
                    {bus.bess_arbitrage_score.toFixed(0)}
                  </td>

                  <td className="py-3 px-2 text-right font-mono text-slate-300">
                    {bus.capture_price_solar_score.toFixed(0)}
                  </td>

                  <td className="py-3 px-2 text-right font-mono text-slate-300">
                    {bus.capture_price_wind_score.toFixed(0)}
                  </td>

                  <td className="py-3 px-2 text-right font-mono text-blue-400">
                    {bus.demand_growth_score.toFixed(0)}
                  </td>

                  <td className="py-3 px-2 text-right font-mono text-slate-400">
                    {bus.grid_expansion_score.toFixed(0)}
                  </td>

                  <td className="py-3 px-2 text-center">
                    <span className={`text-[9px] font-mono font-bold px-2 py-0.5 rounded border uppercase ${getBadgeStyle(bus.recommendation_level)}`}>
                      {bus.recommendation_level}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

    </div>
  );
};
