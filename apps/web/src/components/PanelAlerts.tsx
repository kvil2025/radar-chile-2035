import React from 'react';
import { Alert } from '../types';
import { Bell, AlertTriangle, AlertCircle, Info, ShieldAlert } from 'lucide-react';

interface PanelAlertsProps {
  alerts: Alert[];
}

export const PanelAlerts: React.FC<PanelAlertsProps> = ({ alerts }) => {
  const getSeverityBadge = (severity: string) => {
    switch (severity) {
      case 'CRITICAL':
        return {
          icon: <ShieldAlert className="w-4 h-4 text-red-400" />,
          style: 'bg-red-500/15 border-red-500/40 text-red-400',
          label: 'CRÍTICA'
        };
      case 'WARNING':
        return {
          icon: <AlertTriangle className="w-4 h-4 text-accent-orange" />,
          style: 'bg-accent-orange/15 border-accent-orange/40 text-accent-orange',
          label: 'ADVERTENCIA'
        };
      case 'WATCH':
        return {
          icon: <AlertCircle className="w-4 h-4 text-amber-400" />,
          style: 'bg-amber-500/15 border-amber-500/40 text-amber-400',
          label: 'OBSERVACIÓN'
        };
      default:
        return {
          icon: <Info className="w-4 h-4 text-blue-400" />,
          style: 'bg-blue-500/15 border-blue-500/40 text-blue-400',
          label: 'INFORMATIVA'
        };
    }
  };

  return (
    <div className="glass-panel p-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2.5">
          <div className="w-8 h-8 rounded-lg bg-accent-orange/15 border border-accent-orange/30 flex items-center justify-center text-accent-orange">
            <Bell className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-base font-bold text-white font-heading">Centro de Alertas Cuantitativas</h3>
            <p className="text-xs text-slate-400">Detección continua de quiebres de umbrales y señales críticas de mercado</p>
          </div>
        </div>
        <span className="px-2.5 py-1 rounded-lg bg-navy-900 border border-navy-700 text-xs font-mono text-slate-300">
          {alerts.length} Activas
        </span>
      </div>

      <div className="space-y-3">
        {alerts.length === 0 ? (
          <div className="p-4 rounded-xl bg-bg-card border border-border-subtle text-center text-xs text-slate-400">
            No hay alertas críticas activas en este momento.
          </div>
        ) : (
          alerts.map((al) => {
            const badge = getSeverityBadge(al.severity);
            return (
              <div
                key={al.id}
                className="p-4 rounded-xl bg-bg-card border border-border-subtle hover:border-gold-primary/30 transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-3"
              >
                <div className="flex items-start space-x-3">
                  <div className="mt-0.5">{badge.icon}</div>
                  <div>
                    <div className="flex items-center space-x-2">
                      <span className={`text-[9px] font-bold font-mono px-2 py-0.5 rounded border uppercase ${badge.style}`}>
                        {badge.label}
                      </span>
                      <h4 className="text-xs font-bold text-white font-heading">
                        {al.title}
                      </h4>
                    </div>
                    <p className="text-xs text-slate-300 mt-1 leading-relaxed">
                      {al.description}
                    </p>
                  </div>
                </div>

                <div className="flex items-center space-x-3 self-end sm:self-center text-right shrink-0">
                  {al.current_value !== undefined && al.current_value !== null && (
                    <div className="font-mono text-xs">
                      <span className="text-slate-500 block text-[10px]">Valor Actual</span>
                      <span className="text-slate-200 font-bold">{al.current_value}</span>
                    </div>
                  )}
                  {al.trigger_value !== undefined && al.trigger_value !== null && (
                    <div className="font-mono text-xs">
                      <span className="text-slate-500 block text-[10px]">Umbral</span>
                      <span className="text-gold-light font-bold">{al.trigger_value}</span>
                    </div>
                  )}
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};
