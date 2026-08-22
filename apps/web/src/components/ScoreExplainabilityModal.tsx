import React from 'react';
import { Score } from '../types';
import { X, CheckCircle, ShieldCheck, Sparkles } from 'lucide-react';

interface ScoreExplainabilityModalProps {
  score: Score | null;
  onClose: () => void;
}

export const ScoreExplainabilityModal: React.FC<ScoreExplainabilityModalProps> = ({ score, onClose }) => {
  if (!score) return null;

  const displayName = score.metadata_json?.name || score.score_type.replace('_', ' ');

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-in fade-in duration-200">
      <div className="bg-[#111114] border border-gold-primary/40 rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto shadow-2xl p-6 relative">
        
        {/* Header */}
        <div className="flex items-start justify-between border-b border-border-subtle pb-4 mb-5">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-gold-primary/15 border border-gold-primary/30 flex items-center justify-center text-gold-primary">
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="text-[10px] font-bold uppercase tracking-wider text-gold-primary font-mono">
                  EXPLICABILIDAD CUANTITATIVA
                </span>
                <span className="px-2 py-0.5 text-[9px] font-mono bg-slate-800 text-slate-300 rounded">
                  METODOLOGÍA {score.methodology_version}
                </span>
              </div>
              <h2 className="text-xl font-bold text-white font-heading mt-0.5">
                {displayName}: <span className="text-gold-light">{score.value.toFixed(1)} / 100</span>
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

        {/* Math explanation formula box */}
        <div className="bg-navy-900/40 border border-navy-700/50 rounded-xl p-4 mb-5 text-xs text-slate-300 space-y-1">
          <p className="font-mono text-blue-300 font-semibold">
            Score = ∑ (Componente_Normalizado × Peso)
          </p>
          <p className="text-slate-400">
            Cada variable observada se valida contra rangos físicos, se normaliza de 0 a 100 según su dirección económica y contribuye de forma aditiva y transparente al índice final.
          </p>
        </div>

        {/* Contributors Breakdown Table */}
        <div className="space-y-3">
          <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 font-mono">
            Desglose de Componentes ({score.contributors.length})
          </h4>

          <div className="divide-y divide-border-subtle border border-border-subtle rounded-xl overflow-hidden bg-bg-card">
            {score.contributors.map((c, i) => (
              <div key={i} className="p-3.5 hover:bg-white/[0.02] transition-colors flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                <div className="space-y-1">
                  <div className="flex items-center space-x-2">
                    <span className="text-xs font-bold font-mono text-white bg-slate-800 px-1.5 py-0.5 rounded">
                      {c.indicator_code}
                    </span>
                    <span className="text-xs text-slate-300 font-medium">{c.indicator_name}</span>
                  </div>
                  <div className="flex items-center space-x-3 text-[11px] text-slate-400 font-mono">
                    <span>Valor Observado: <strong className="text-slate-200">{c.raw_value} {c.unit}</strong></span>
                    <span>Peso: <strong>{(c.weight * 100).toFixed(0)}%</strong></span>
                    <span>Dirección: <strong className={c.direction > 0 ? 'text-emerald-400' : 'text-accent-orange'}>{c.direction > 0 ? '+ Expansión' : '- Tensión/Estrés'}</strong></span>
                  </div>
                </div>

                {/* Score points & quality badge */}
                <div className="flex items-center space-x-4 self-end sm:self-center">
                  <div className="text-right">
                    <span className="text-xs font-mono text-slate-400 block">Aporte al índice</span>
                    <span className="text-sm font-bold font-mono text-gold-light">
                      +{c.contribution_points.toFixed(1)} pts
                    </span>
                  </div>
                  <div className="flex items-center space-x-1 text-[10px] font-mono px-2 py-1 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                    <CheckCircle className="w-3 h-3" />
                    <span>VALID</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Footer info */}
        <div className="mt-6 pt-4 border-t border-border-subtle flex items-center justify-between text-xs text-slate-400">
          <div className="flex items-center space-x-1.5">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            <span>Nivel de confianza en cálculo: <strong>{Math.round(score.confidence * 100)}%</strong></span>
          </div>
          <button
            onClick={onClose}
            className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-xl text-xs font-semibold transition-colors"
          >
            Cerrar
          </button>
        </div>

      </div>
    </div>
  );
};
