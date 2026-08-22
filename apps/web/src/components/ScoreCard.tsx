import React from 'react';
import { Score } from '../types';
import { TrendingUp, TrendingDown, Minus, Sparkles } from 'lucide-react';

interface ScoreCardProps {
  score: Score;
  onOpenExplainability: (score: Score) => void;
}

export const ScoreCard: React.FC<ScoreCardProps> = ({ score, onOpenExplainability }) => {
  const getScoreColor = (val: number, type: string) => {
    // For stress scores, higher is red/orange. For opportunity/cycle, higher is gold/green.
    const isStressType = type.includes('STRESS');
    if (isStressType) {
      if (val > 65) return 'text-accent-orange border-accent-orange/40 bg-accent-orange/10';
      if (val > 45) return 'text-amber-400 border-amber-400/40 bg-amber-400/10';
      return 'text-emerald-400 border-emerald-400/40 bg-emerald-400/10';
    } else {
      if (val >= 60) return 'text-gold-light border-gold-primary/50 bg-gold-primary/10';
      if (val >= 40) return 'text-blue-400 border-blue-400/40 bg-blue-400/10';
      return 'text-slate-400 border-slate-600/40 bg-slate-800/10';
    }
  };

  const getTrendIcon = () => {
    if (score.trend === 'UP') return <TrendingUp className="w-4 h-4 text-emerald-400" />;
    if (score.trend === 'DOWN') return <TrendingDown className="w-4 h-4 text-accent-red" />;
    return <Minus className="w-4 h-4 text-slate-400" />;
  };

  const displayName = score.metadata_json?.name || score.score_type.replace('_', ' ');
  const description = score.metadata_json?.description || '';

  return (
    <div className="glass-panel p-5 flex flex-col justify-between transition-all duration-300 hover:scale-[1.01] hover:border-gold-primary/40 relative group">
      {/* Top row */}
      <div className="flex items-start justify-between gap-2 mb-3">
        <div>
          <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 font-mono block">
            {score.score_type}
          </span>
          <h3 className="text-base font-bold text-white font-heading mt-0.5">
            {displayName}
          </h3>
        </div>
        <div className="flex items-center space-x-1.5 bg-navy-900/80 px-2 py-1 rounded-lg border border-navy-700/60 text-[11px] font-mono text-slate-300">
          {getTrendIcon()}
          <span>{score.delta_30d > 0 ? `+${score.delta_30d}` : score.delta_30d} (30d)</span>
        </div>
      </div>

      {/* Score gauge & number */}
      <div className="flex items-baseline justify-between my-2">
        <div className="flex items-baseline space-x-2">
          <span className="text-4xl font-black tracking-tight text-white font-heading">
            {score.value.toFixed(1)}
          </span>
          <span className="text-xs text-slate-500 font-mono">/ 100</span>
        </div>
        <div className={`px-2.5 py-1 rounded-lg border text-xs font-bold font-mono ${getScoreColor(score.value, score.score_type)}`}>
          {score.value >= 60 ? 'ALTO' : score.value >= 40 ? 'MODERADO' : 'BAJO'}
        </div>
      </div>

      {/* Progress bar */}
      <div className="w-full bg-slate-800/80 h-1.5 rounded-full overflow-hidden my-2">
        <div 
          className="h-full bg-gradient-to-r from-navy-600 via-blue-500 to-gold-primary rounded-full transition-all duration-500"
          style={{ width: `${Math.max(5, Math.min(100, score.value))}%` }}
        />
      </div>

      <p className="text-xs text-slate-400 line-clamp-2 my-2 min-h-[32px]">
        {description}
      </p>

      {/* Footer & WHY? Button */}
      <div className="pt-3 border-t border-border-subtle flex items-center justify-between mt-2">
        <span className="text-[11px] text-slate-400 font-mono">
          Confianza: <span className="text-slate-200">{Math.round(score.confidence * 100)}%</span>
        </span>

        <button
          onClick={() => onOpenExplainability(score)}
          className="flex items-center space-x-1.5 text-xs font-semibold text-gold-light hover:text-white bg-gold-primary/10 hover:bg-gold-primary/20 px-2.5 py-1 rounded-lg border border-gold-primary/30 transition-colors"
        >
          <Sparkles className="w-3.5 h-3.5 text-gold-primary" />
          <span>WHY?</span>
        </button>
      </div>
    </div>
  );
};
