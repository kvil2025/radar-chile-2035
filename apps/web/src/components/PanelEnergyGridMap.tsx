import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { Bus } from '../types/energy';
import { MapPin, Eye } from 'lucide-react';

interface PanelEnergyGridMapProps {
  onSelectBus: (bus: Bus) => void;
}

export const PanelEnergyGridMap: React.FC<PanelEnergyGridMapProps> = ({ onSelectBus }) => {
  const [buses, setBuses] = useState<Bus[]>([]);
  const [selectedZone, setSelectedZone] = useState<string>('ALL');
  const [selectedVoltage, setSelectedVoltage] = useState<string>('ALL');

  useEffect(() => {
    api.getEnergyBuses().then((busesData) => {
      setBuses(busesData);
    }).catch(err => {
      console.error(err);
    });
  }, []);

  const filteredBuses = buses.filter(b => {
    if (selectedZone !== 'ALL' && b.zone !== selectedZone) return false;
    if (selectedVoltage === '500' && b.voltage_kv !== 500) return false;
    if (selectedVoltage === '220' && b.voltage_kv !== 220) return false;
    return true;
  });

  const getScoreBadge = (score?: number) => {
    if (!score) return 'text-slate-400 bg-slate-800 border-slate-700';
    if (score >= 80) return 'text-emerald-400 bg-emerald-500/10 border-emerald-500/30';
    if (score >= 68) return 'text-gold-light bg-gold-primary/10 border-gold-primary/30';
    if (score >= 55) return 'text-blue-400 bg-blue-500/10 border-blue-500/30';
    return 'text-accent-orange bg-accent-orange/10 border-accent-orange/30';
  };

  return (
    <div className="space-y-6">
      
      {/* Filters Header */}
      <div className="glass-panel p-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-blue-500/15 border border-blue-500/30 flex items-center justify-center text-blue-400">
              <MapPin className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white font-heading">
                Topología del Sistema Eléctrico Nacional (SEN)
              </h3>
              <p className="text-xs text-slate-400">
                Barras eléctricas, precios nodales y niveles de oportunidad a lo largo de Chile
              </p>
            </div>
          </div>

          {/* Filter Pills */}
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-[10px] font-mono text-slate-500 mr-1">Zona:</span>
            {['ALL', 'NORTE_GRANDE', 'NORTE_CHICO', 'CENTRO', 'SUR'].map((z) => (
              <button
                key={z}
                onClick={() => setSelectedZone(z)}
                className={`px-2.5 py-1 rounded-lg text-xs font-semibold transition-all ${
                  selectedZone === z
                    ? 'bg-gold-primary text-black font-bold'
                    : 'bg-bg-card hover:bg-bg-card-hover text-slate-400 hover:text-white border border-border-subtle'
                }`}
              >
                {z === 'ALL' ? 'Todas' : z.replace('_', ' ')}
              </button>
            ))}

            <span className="text-[10px] font-mono text-slate-500 ml-2 mr-1">Voltaje:</span>
            {['ALL', '500', '220'].map((v) => (
              <button
                key={v}
                onClick={() => setSelectedVoltage(v)}
                className={`px-2.5 py-1 rounded-lg text-xs font-semibold transition-all ${
                  selectedVoltage === v
                    ? 'bg-navy-700 text-gold-light border border-gold-primary/40'
                    : 'bg-bg-card hover:bg-bg-card-hover text-slate-400 hover:text-white border border-border-subtle'
                }`}
              >
                {v === 'ALL' ? 'Todos' : `${v} kV`}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Grid of Buses */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3.5">
        {filteredBuses.map((bus) => (
          <div
            key={bus.id}
            onClick={() => onSelectBus(bus)}
            className="p-4 rounded-xl bg-bg-card border border-border-subtle hover:border-gold-primary/40 hover:bg-bg-card-hover transition-all cursor-pointer group flex flex-col justify-between"
          >
            <div>
              <div className="flex items-start justify-between">
                <div>
                  <div className="flex items-center space-x-1.5">
                    <span className="text-[10px] font-mono text-gold-light bg-navy-900 border border-navy-700 px-1.5 py-0.5 rounded font-bold">
                      {bus.voltage_kv} kV
                    </span>
                    <span className="text-[10px] font-mono text-slate-400">
                      {bus.zone.replace('_', ' ')}
                    </span>
                  </div>
                  <h4 className="text-sm font-bold text-white font-heading mt-1.5 group-hover:text-gold-light transition-colors">
                    {bus.name}
                  </h4>
                </div>
                <Eye className="w-4 h-4 text-slate-500 group-hover:text-gold-primary transition-colors" />
              </div>

              <div className="mt-3 flex items-center justify-between">
                <div>
                  <span className="text-[9px] font-mono text-slate-400 block uppercase">Precio Nodal Actual</span>
                  <span className="text-lg font-black font-heading text-white">
                    ${bus.latest_price !== undefined ? bus.latest_price.toFixed(1) : '—'} <small className="text-xs font-normal text-slate-400">USD/MWh</small>
                  </span>
                </div>

                <div className="text-right">
                  <span className="text-[9px] font-mono text-slate-400 block uppercase">Opportunity Score</span>
                  <span className={`text-xs font-bold font-mono px-2 py-0.5 rounded border inline-block mt-0.5 ${getScoreBadge(bus.opportunity_score)}`}>
                    {bus.opportunity_score ? `${bus.opportunity_score.toFixed(1)} / 100` : '—'}
                  </span>
                </div>
              </div>
            </div>

            <div className="mt-3 pt-2.5 border-t border-border-subtle flex items-center justify-between text-[10px] font-mono text-slate-500">
              <span>Región: <strong className="text-slate-300">{bus.region}</strong></span>
              <span className="text-gold-primary group-hover:underline">Ver Gráfico →</span>
            </div>
          </div>
        ))}
      </div>

    </div>
  );
};
