import React, { useEffect, useState } from 'react';
import { Bus, NodePrice } from '../types/energy';
import { api } from '../services/api';
import { X, Zap, Calendar, CheckCircle2 } from 'lucide-react';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ReferenceLine
} from 'recharts';

interface NodePriceChartModalProps {
  bus: Bus | null;
  onClose: () => void;
}

export const NodePriceChartModal: React.FC<NodePriceChartModalProps> = ({ bus, onClose }) => {
  const [prices, setPrices] = useState<NodePrice[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    if (!bus) return;
    setIsLoading(true);
    api.getNodePrices(bus.id)
      .then((data) => {
        setPrices(data);
        setIsLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setIsLoading(false);
      });
  }, [bus]);

  if (!bus) return null;

  const chartData = prices.map((p) => ({
    time: p.timestamp ? `${new Date(p.timestamp).toLocaleDateString([], { month: 'numeric', day: 'numeric' })} ${new Date(p.timestamp).getHours()}:00` : '',
    price: p.price_usd_mwh,
    energy: p.marginal_energy_cost,
    loss: p.marginal_loss_cost,
    congestion: p.marginal_congestion_cost
  }));

  const values = prices.map(p => p.price_usd_mwh);
  const minVal = values.length > 0 ? Math.min(...values) : 0;
  const maxVal = values.length > 0 ? Math.max(...values) : 100;
  const avgVal = values.length > 0 ? values.reduce((a, b) => a + b, 0) / values.length : 0;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-in fade-in duration-200">
      <div className="bg-[#111114] border border-gold-primary/40 rounded-2xl max-w-3xl w-full max-h-[90vh] overflow-y-auto shadow-2xl p-6 relative">
        
        {/* Header */}
        <div className="flex items-start justify-between border-b border-border-subtle pb-4 mb-5">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-gold-primary/15 border border-gold-primary/30 flex items-center justify-center text-gold-primary">
              <Zap className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="text-[10px] font-bold uppercase tracking-wider text-gold-primary font-mono bg-gold-primary/10 px-1.5 py-0.5 rounded">
                  {bus.code}
                </span>
                <span className="text-[10px] font-mono text-slate-400">
                  {bus.voltage_kv} kV • {bus.zone.replace('_', ' ')} • {bus.region}
                </span>
              </div>
              <h2 className="text-xl font-bold text-white font-heading mt-0.5">
                {bus.name}
              </h2>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 rounded-lg bg-slate-800/60 hover:bg-slate-700 text-slate-400 hover:text-white transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Stats summary row */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-5">
          <div className="p-3 rounded-xl bg-bg-card border border-border-subtle">
            <span className="text-[10px] font-mono text-slate-400 block uppercase">Último Costo Marginal</span>
            <span className="text-base font-bold font-heading text-white">
              ${bus.latest_price !== undefined ? bus.latest_price.toFixed(1) : '—'} <small className="font-normal text-xs text-slate-400">USD/MWh</small>
            </span>
          </div>
          <div className="p-3 rounded-xl bg-bg-card border border-border-subtle">
            <span className="text-[10px] font-mono text-slate-400 block uppercase">Promedio (72h)</span>
            <span className="text-base font-bold font-heading text-slate-300">
              ${avgVal.toFixed(1)} <small className="font-normal text-xs text-slate-400">USD/MWh</small>
            </span>
          </div>
          <div className="p-3 rounded-xl bg-bg-card border border-border-subtle">
            <span className="text-[10px] font-mono text-slate-400 block uppercase">Mínimo (Horas Solares)</span>
            <span className="text-base font-bold font-heading text-slate-300">
              ${minVal.toFixed(1)} <small className="font-normal text-xs text-slate-400">USD/MWh</small>
            </span>
          </div>
          <div className="p-3 rounded-xl bg-bg-card border border-border-subtle">
            <span className="text-[10px] font-mono text-slate-400 block uppercase">Máximo (Punta Nocturna)</span>
            <span className="text-base font-bold font-heading text-slate-300">
              ${maxVal.toFixed(1)} <small className="font-normal text-xs text-slate-400">USD/MWh</small>
            </span>
          </div>
        </div>

        {/* Recharts LineChart */}
        <div className="bg-bg-card border border-border-subtle rounded-xl p-4 mb-4">
          <div className="flex items-center justify-between mb-3 text-xs text-slate-400 font-mono">
            <span className="flex items-center space-x-1">
              <Calendar className="w-3.5 h-3.5 text-gold-primary" />
              <span>Serie de Costo Marginal Horario ($/MWh)</span>
            </span>
            <span className="text-emerald-400 flex items-center space-x-1">
              <CheckCircle2 className="w-3.5 h-3.5" />
              <span>Datos Coordinador Eléctrico Nacional</span>
            </span>
          </div>

          <div className="h-64 w-full">
            {isLoading ? (
              <div className="h-full flex items-center justify-center text-xs text-slate-500 font-mono">
                Cargando serie horaria de precios nodales...
              </div>
            ) : chartData.length === 0 ? (
              <div className="h-full flex items-center justify-center text-xs text-slate-500 font-mono">
                No hay observaciones históricas disponibles para esta barra.
              </div>
            ) : (
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={chartData} margin={{ top: 10, right: 10, left: -15, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#22222a" />
                  <XAxis 
                    dataKey="time" 
                    stroke="#64748b" 
                    fontSize={10} 
                  />
                  <YAxis 
                    stroke="#64748b" 
                    fontSize={10} 
                    domain={[0, 'auto']} 
                  />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#111114',
                      borderColor: 'rgba(201, 168, 76, 0.4)',
                      borderRadius: '12px',
                      fontSize: '12px',
                      color: '#fff'
                    }}
                    formatter={(value: any) => [`$${value} USD/MWh`, 'Costo Marginal']}
                  />
                  <ReferenceLine y={avgVal} stroke="#3b82f6" strokeDasharray="3 3" />
                  <Line
                    type="monotone"
                    dataKey="price"
                    stroke="#C9A84C"
                    strokeWidth={2.5}
                    dot={{ fill: '#C9A84C', r: 2 }}
                    activeDot={{ r: 5, fill: '#00f2ff' }}
                  />
                </LineChart>
              </ResponsiveContainer>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="flex justify-end">
          <button
            onClick={onClose}
            className="px-5 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-xl text-xs font-semibold transition-colors"
          >
            Cerrar
          </button>
        </div>

      </div>
    </div>
  );
};
