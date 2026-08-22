import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { GenerationHourly, DemandHourly } from '../types/energy';
import { Activity, Sun, Wind, Droplets, Flame, BatteryCharging } from 'lucide-react';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend
} from 'recharts';

export const PanelGenerationAndDemandMix: React.FC = () => {
  const [genData, setGenData] = useState<GenerationHourly[]>([]);
  const [demandData, setDemandData] = useState<DemandHourly[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    setIsLoading(true);
    Promise.all([
      api.getGenerationMix(),
      api.getDemandHourly()
    ]).then(([gens, demands]) => {
      setGenData(gens);
      setDemandData(demands);
      setIsLoading(false);
    }).catch(err => {
      console.error(err);
      setIsLoading(false);
    });
  }, []);

  const chartData = genData.map((g, idx) => {
    const d = demandData[idx] || {};
    return {
      time: g.timestamp ? `${new Date(g.timestamp).getHours()}:00` : '',
      solar: g.solar_mw,
      wind: g.wind_mw,
      hydro: g.hydro_mw,
      gas: g.thermal_gas_mw,
      coal: g.thermal_coal_mw,
      bess_discharge: g.bess_discharge_mw,
      curtailment: g.curtailment_mw,
      total_demand: d.total_demand_mw || g.total_generation_mw,
      mining_demand: d.mining_demand_mw || 2900,
      datacenter_demand: d.data_centers_demand_mw || 450
    };
  });

  const latest = genData[genData.length - 1];

  return (
    <div className="space-y-6">
      
      {/* Realtime KPI Strip */}
      {latest && (
        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-6 gap-3">
          <div className="glass-panel p-3.5">
            <span className="text-[10px] font-mono text-slate-400 uppercase flex items-center space-x-1">
              <Sun className="w-3 h-3 text-gold-primary" />
              <span>Solar PV</span>
            </span>
            <span className="text-lg font-black font-heading text-white mt-1 block">
              {latest.solar_mw.toFixed(0)} <small className="text-xs text-slate-400 font-normal">MW</small>
            </span>
          </div>

          <div className="glass-panel p-3.5">
            <span className="text-[10px] font-mono text-slate-400 uppercase flex items-center space-x-1">
              <Wind className="w-3 h-3 text-blue-400" />
              <span>Eólica</span>
            </span>
            <span className="text-lg font-black font-heading text-white mt-1 block">
              {latest.wind_mw.toFixed(0)} <small className="text-xs text-slate-400 font-normal">MW</small>
            </span>
          </div>

          <div className="glass-panel p-3.5">
            <span className="text-[10px] font-mono text-slate-400 uppercase flex items-center space-x-1">
              <Droplets className="w-3 h-3 text-cyan-400" />
              <span>Hidro</span>
            </span>
            <span className="text-lg font-black font-heading text-white mt-1 block">
              {latest.hydro_mw.toFixed(0)} <small className="text-xs text-slate-400 font-normal">MW</small>
            </span>
          </div>

          <div className="glass-panel p-3.5">
            <span className="text-[10px] font-mono text-slate-400 uppercase flex items-center space-x-1">
              <Flame className="w-3 h-3 text-amber-500" />
              <span>Gas / Térmico</span>
            </span>
            <span className="text-lg font-black font-heading text-white mt-1 block">
              {(latest.thermal_gas_mw + latest.thermal_coal_mw).toFixed(0)} <small className="text-xs text-slate-400 font-normal">MW</small>
            </span>
          </div>

          <div className="glass-panel p-3.5">
            <span className="text-[10px] font-mono text-slate-400 uppercase flex items-center space-x-1">
              <BatteryCharging className="w-3 h-3 text-emerald-400" />
              <span>BESS Storage</span>
            </span>
            <span className="text-lg font-black font-heading text-white mt-1 block">
              {latest.bess_discharge_mw > 0 ? `+${latest.bess_discharge_mw.toFixed(0)}` : latest.bess_charge_mw > 0 ? `-${latest.bess_charge_mw.toFixed(0)}` : '0'} <small className="text-xs text-slate-400 font-normal">MW</small>
            </span>
          </div>

          <div className="glass-panel p-3.5">
            <span className="text-[10px] font-mono text-slate-400 uppercase block">Renovable %</span>
            <span className="text-lg font-black font-heading text-gold-light mt-1 block">
              {latest.renewable_share_pct ? `${latest.renewable_share_pct.toFixed(1)}%` : '—'}
            </span>
          </div>
        </div>
      )}

      {/* Hourly Generation & Demand Mix Chart */}
      <div className="glass-panel p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-2.5">
            <div className="w-8 h-8 rounded-lg bg-gold-primary/15 border border-gold-primary/30 flex items-center justify-center text-gold-primary">
              <Activity className="w-4 h-4" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white font-heading">
                Despacho Horario por Tecnología & Vertimiento (SEN)
              </h3>
              <p className="text-xs text-slate-400">
                Curva de pato, penetración solar diurna, arbitraje BESS nocturno y curtailment
              </p>
            </div>
          </div>
        </div>

        <div className="h-72 w-full mt-2">
          {isLoading ? (
            <div className="h-full flex items-center justify-center text-xs text-slate-500 font-mono">
              Cargando perfil de despacho horario...
            </div>
          ) : (
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={chartData} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#22222a" />
                <XAxis dataKey="time" stroke="#64748b" fontSize={10} />
                <YAxis stroke="#64748b" fontSize={10} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#111114',
                    borderColor: 'rgba(201, 168, 76, 0.4)',
                    borderRadius: '12px',
                    fontSize: '11px',
                    color: '#fff'
                  }}
                />
                <Legend iconType="circle" wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
                <Area type="monotone" dataKey="solar" name="Solar PV" stackId="1" stroke="#C9A84C" fill="#C9A84C" fillOpacity={0.6} />
                <Area type="monotone" dataKey="wind" name="Eólica" stackId="1" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.5} />
                <Area type="monotone" dataKey="hydro" name="Hidroeléctrica" stackId="1" stroke="#06b6d4" fill="#06b6d4" fillOpacity={0.5} />
                <Area type="monotone" dataKey="gas" name="Gas Natural" stackId="1" stroke="#f59e0b" fill="#f59e0b" fillOpacity={0.5} />
                <Area type="monotone" dataKey="bess_discharge" name="BESS Descarga" stackId="1" stroke="#10b981" fill="#10b981" fillOpacity={0.7} />
              </AreaChart>
            </ResponsiveContainer>
          )}
        </div>
      </div>

    </div>
  );
};
