import React, { useState, useEffect } from 'react';
import { Regime } from '../types';
import { RefreshCw, Activity, Compass, Key } from 'lucide-react';
import { ApiKeyModal } from './ApiKeyModal';
import { getStoredGeminiKey } from '../services/api';

interface RadarHeaderProps {
  regime: Regime | null;
  onRefresh: () => void;
  isRefreshing: boolean;
}

export const RadarHeader: React.FC<RadarHeaderProps> = ({ regime, onRefresh, isRefreshing }) => {
  const [isApiKeyModalOpen, setIsApiKeyModalOpen] = useState(false);
  const [hasCustomKey, setHasCustomKey] = useState(false);

  useEffect(() => {
    setHasCustomKey(!!getStoredGeminiKey());
  }, [isApiKeyModalOpen]);

  const getRegimeColor = (code?: string) => {
    switch (code) {
      case 'COMMODITY_SUPERCYCLE':
        return 'border-gold-primary bg-gold-primary/10 text-gold-light';
      case 'EXPANSION':
        return 'border-emerald-500 bg-emerald-500/10 text-emerald-400';
      case 'RECESSION':
        return 'border-red-500 bg-red-500/10 text-red-400';
      case 'FISCAL_STRESS':
      case 'MONETARY_STRESS':
        return 'border-accent-orange bg-accent-orange/10 text-accent-orange';
      default:
        return 'border-blue-500 bg-blue-500/10 text-blue-400';
    }
  };

  return (
    <header className="border-b border-border-subtle bg-[#0A0A0B]/80 backdrop-blur-xl sticky top-0 z-40 px-6 py-4">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row md:items-center justify-between gap-4">
        
        {/* Brand & Project Identity */}
        <div className="flex items-center space-x-4">
          <div className="w-11 h-11 rounded-xl bg-gradient-to-br from-navy-800 to-navy-900 border border-gold-primary/40 flex items-center justify-center shadow-gold">
            <Activity className="w-6 h-6 text-gold-primary" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h1 className="text-2xl font-black tracking-tight text-white font-heading">
                RADAR CHILE <span className="text-gold-primary">2035</span>
              </h1>
              <span className="px-2 py-0.5 text-[10px] font-bold uppercase tracking-wider bg-navy-900 border border-navy-700 text-blue-300 rounded-full font-mono">
                QUANTITATIVE v0.1
              </span>
            </div>
            <p className="text-xs text-slate-400">
              Plataforma de Inteligencia Económica, Transmisión Macroeconómica y Detección de Señales
            </p>
          </div>
        </div>

        {/* Global Regime & Quick Actions */}
        <div className="flex flex-wrap items-center gap-3">
          {regime && (
            <div className={`flex items-center space-x-2.5 px-3.5 py-1.5 rounded-xl border ${getRegimeColor(regime.regime_code)}`}>
              <Compass className="w-4 h-4 animate-spin-slow" />
              <div className="text-xs">
                <span className="font-semibold uppercase tracking-wider block">
                  Régimen: {regime.regime_code.replace('_', ' ')}
                </span>
                <span className="text-[10px] opacity-80">
                  Confianza: {Math.round(regime.confidence * 100)}%
                </span>
              </div>
            </div>
          )}

          <div className="flex items-center space-x-2">
            <button
              onClick={() => setIsApiKeyModalOpen(true)}
              className={`flex items-center space-x-2 px-3 py-2 rounded-xl text-xs font-semibold transition-all shadow-sm active:scale-95 border ${
                hasCustomKey
                  ? 'bg-emerald-500/10 border-emerald-500/40 text-emerald-300 hover:bg-emerald-500/20'
                  : 'bg-navy-900/80 border-navy-700 hover:border-gold-primary/50 text-slate-300 hover:text-white'
              }`}
              title="Configurar tu propia API Key de Google Gemini"
            >
              <Key className={`w-3.5 h-3.5 ${hasCustomKey ? 'text-emerald-400' : 'text-gold-primary'}`} />
              <span>{hasCustomKey ? 'Gemini BYOK: Activa' : 'API Key Gemini'}</span>
              {hasCustomKey && (
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
              )}
            </button>

            <button
              onClick={onRefresh}
              disabled={isRefreshing}
              className="flex items-center space-x-2 px-3.5 py-2 rounded-xl bg-bg-card hover:bg-bg-card-hover border border-border-subtle hover:border-gold-primary/40 text-xs font-semibold text-slate-200 transition-all shadow-sm active:scale-95 disabled:opacity-50"
            >
              <RefreshCw className={`w-3.5 h-3.5 text-gold-primary ${isRefreshing ? 'animate-spin' : ''}`} />
              <span>{isRefreshing ? 'Recalculando...' : 'Recalcular'}</span>
            </button>

            <div className="hidden sm:flex items-center space-x-1.5 px-3 py-2 rounded-xl bg-navy-900/60 border border-navy-700/50 text-[11px] font-mono text-emerald-400">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              <span>LIVE DATA VERIFIED</span>
            </div>
          </div>
        </div>

      </div>

      <ApiKeyModal
        isOpen={isApiKeyModalOpen}
        onClose={() => setIsApiKeyModalOpen(false)}
      />
    </header>
  );
};
