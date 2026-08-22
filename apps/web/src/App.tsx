import React, { useEffect, useState } from 'react';
import { api } from './services/api';
import {
  Score,
  Regime,
  Scenario,
  ChileImpactOverview,
  Alert,
  Indicator,
  ResearchDocument
} from './types';
import { RadarHeader } from './components/RadarHeader';
import { ScoreCard } from './components/ScoreCard';
import { ScoreExplainabilityModal } from './components/ScoreExplainabilityModal';
import { PanelMacroUSA } from './components/PanelMacroUSA';
import { PanelCommoditiesMining } from './components/PanelCommoditiesMining';
import { PanelChileRealtime } from './components/PanelChileRealtime';
import { PanelScenarios } from './components/PanelScenarios';
import { PanelTransmissionMatrix } from './components/PanelTransmissionMatrix';
import { PanelAlerts } from './components/PanelAlerts';
import { TimeSeriesChartModal } from './components/TimeSeriesChartModal';
import { Compass, BookOpen } from 'lucide-react';

export const App: React.FC = () => {
  const [scores, setScores] = useState<Score[]>([]);
  const [regime, setRegime] = useState<Regime | null>(null);
  const [scenarios, setScenarios] = useState<Scenario[]>([]);
  const [chileImpact, setChileImpact] = useState<ChileImpactOverview | null>(null);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [indicators, setIndicators] = useState<Indicator[]>([]);
  const [research, setResearch] = useState<ResearchDocument[]>([]);

  const [selectedScore, setSelectedScore] = useState<Score | null>(null);
  const [selectedIndicator, setSelectedIndicator] = useState<Indicator | null>(null);
  const [isRefreshing, setIsRefreshing] = useState<boolean>(false);
  const [activeTab, setActiveTab] = useState<'OVERVIEW' | 'MARKETS' | 'SCENARIOS' | 'CHILE_IMPACT' | 'ALERTS' | 'RESEARCH'>('OVERVIEW');

  const loadData = async () => {
    try {
      const [
        scoresData,
        regimeData,
        scenariosData,
        impactData,
        alertsData,
        indicatorsData,
        researchData
      ] = await Promise.all([
        api.getScores().catch(() => []),
        api.getRegime().catch(() => null),
        api.getScenarios().catch(() => []),
        api.getChileImpact().catch(() => null),
        api.getAlerts().catch(() => []),
        api.getIndicators().catch(() => []),
        api.getResearch().catch(() => [])
      ]);

      setScores(scoresData);
      setRegime(regimeData);
      setScenarios(scenariosData);
      setChileImpact(impactData);
      setAlerts(alertsData);
      setIndicators(indicatorsData);
      setResearch(researchData);
    } catch (err) {
      console.error('Error loading Radar data:', err);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleRefresh = async () => {
    setIsRefreshing(true);
    try {
      await api.triggerRecalculate();
      await loadData();
    } catch (err) {
      console.error(err);
    } finally {
      setIsRefreshing(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0A0A0B] text-slate-100 flex flex-col justify-between selection:bg-gold-primary selection:text-black">
      <div>
        {/* Top Navbar */}
        <RadarHeader
          regime={regime}
          onRefresh={handleRefresh}
          isRefreshing={isRefreshing}
        />

        <main className="max-w-7xl mx-auto px-4 sm:px-6 py-8 space-y-8">
          
          {/* Main 5 Strategic Indices Cards Row */}
          <section>
            <div className="flex items-center justify-between mb-4">
              <div>
                <h2 className="text-lg font-bold text-white font-heading tracking-tight">
                  Índices Estratégicos Globales & Chile
                </h2>
                <p className="text-xs text-slate-400">
                  Scores cuantitativos normalizados (0-100) con ponderación y explicabilidad transparente
                </p>
              </div>
              <span className="text-[11px] font-mono text-gold-primary bg-gold-primary/10 border border-gold-primary/30 px-2.5 py-1 rounded-lg">
                Metodología v0.1
              </span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
              {scores.map((s) => (
                <ScoreCard
                  key={s.id}
                  score={s}
                  onOpenExplainability={(score) => setSelectedScore(score)}
                />
              ))}
            </div>
          </section>

          {/* Regime synthesis banner */}
          {regime && (
            <section className="p-5 rounded-2xl bg-gradient-to-r from-navy-900/80 via-[#13131a] to-bg-card border border-gold-primary/30 shadow-glass flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
              <div className="flex items-start space-x-3.5">
                <div className="w-10 h-10 rounded-xl bg-gold-primary/15 border border-gold-primary/40 flex items-center justify-center text-gold-primary shrink-0">
                  <Compass className="w-5 h-5" />
                </div>
                <div>
                  <div className="flex items-center space-x-2">
                    <span className="text-[10px] font-bold uppercase tracking-wider text-gold-primary font-mono">
                      DIAGNÓSTICO INSTITUCIONAL
                    </span>
                    <span className="px-2 py-0.5 text-[9px] font-mono bg-navy-800 text-blue-300 rounded border border-navy-700">
                      RÉGIMEN ACTIVO
                    </span>
                  </div>
                  <p className="text-xs sm:text-sm text-slate-200 mt-1 font-medium leading-relaxed">
                    {regime.rationale}
                  </p>
                </div>
              </div>

              <div className="flex items-center space-x-4 self-end md:self-center shrink-0 text-right">
                <div className="font-mono text-xs">
                  <span className="text-slate-400 block text-[10px] uppercase">Confianza</span>
                  <strong className="text-gold-light text-base font-bold">
                    {Math.round(regime.confidence * 100)}%
                  </strong>
                </div>
              </div>
            </section>
          )}

          {/* Section Navigation Tabs */}
          <div className="border-b border-border-subtle flex items-center space-x-1 sm:space-x-3 overflow-x-auto pb-1">
            {[
              { key: 'OVERVIEW', label: 'Panorama General' },
              { key: 'MARKETS', label: 'Mercados & Commodities' },
              { key: 'SCENARIOS', label: 'Escenarios (S1-S4)' },
              { key: 'CHILE_IMPACT', label: 'Transmisión Chile' },
              { key: 'ALERTS', label: `Alertas (${alerts.length})` },
              { key: 'RESEARCH', label: 'Research & RAG' },
            ].map((tab) => (
              <button
                key={tab.key}
                onClick={() => setActiveTab(tab.key as any)}
                className={`px-3.5 py-2 rounded-xl text-xs font-semibold whitespace-nowrap transition-all ${
                  activeTab === tab.key
                    ? 'bg-navy-800 border border-gold-primary/40 text-gold-light shadow-sm'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-white/[0.03]'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>

          {/* Tab Views */}
          {activeTab === 'OVERVIEW' && (
            <div className="space-y-8 animate-in fade-in duration-200">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <PanelMacroUSA
                  indicators={indicators}
                  onSelectIndicator={(ind) => setSelectedIndicator(ind)}
                />
                <PanelCommoditiesMining
                  indicators={indicators}
                  onSelectIndicator={(ind) => setSelectedIndicator(ind)}
                />
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <PanelChileRealtime
                  indicators={indicators}
                  onSelectIndicator={(ind) => setSelectedIndicator(ind)}
                />
                <PanelTransmissionMatrix overview={chileImpact} />
              </div>

              <PanelScenarios scenarios={scenarios} />
              <PanelAlerts alerts={alerts} />
            </div>
          )}

          {activeTab === 'MARKETS' && (
            <div className="space-y-6 animate-in fade-in duration-200">
              <PanelCommoditiesMining
                indicators={indicators}
                onSelectIndicator={(ind) => setSelectedIndicator(ind)}
              />
              <PanelMacroUSA
                indicators={indicators}
                onSelectIndicator={(ind) => setSelectedIndicator(ind)}
              />
              <PanelChileRealtime
                indicators={indicators}
                onSelectIndicator={(ind) => setSelectedIndicator(ind)}
              />
            </div>
          )}

          {activeTab === 'SCENARIOS' && (
            <div className="animate-in fade-in duration-200">
              <PanelScenarios scenarios={scenarios} />
            </div>
          )}

          {activeTab === 'CHILE_IMPACT' && (
            <div className="space-y-6 animate-in fade-in duration-200">
              <PanelTransmissionMatrix overview={chileImpact} />
              <PanelChileRealtime
                indicators={indicators}
                onSelectIndicator={(ind) => setSelectedIndicator(ind)}
              />
            </div>
          )}

          {activeTab === 'ALERTS' && (
            <div className="animate-in fade-in duration-200">
              <PanelAlerts alerts={alerts} />
            </div>
          )}

          {activeTab === 'RESEARCH' && (
            <div className="glass-panel p-6 animate-in fade-in duration-200">
              <div className="flex items-center space-x-2.5 mb-5">
                <div className="w-8 h-8 rounded-lg bg-navy-800 border border-navy-700 flex items-center justify-center text-blue-400">
                  <BookOpen className="w-4 h-4" />
                </div>
                <div>
                  <h3 className="text-base font-bold text-white font-heading">Documentos de Research & Capa de Conocimiento</h3>
                  <p className="text-xs text-slate-400">Informes oficiales catalogados del Banco Central, Cochilco y FMI</p>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {research.map((doc) => (
                  <div key={doc.id} className="p-4 rounded-xl bg-bg-card border border-border-subtle hover:border-gold-primary/40 transition-all flex flex-col justify-between">
                    <div>
                      <div className="flex items-center justify-between text-[10px] font-mono text-gold-primary mb-1">
                        <span>{doc.category}</span>
                        <span>Relevancia: {Math.round(doc.relevance * 100)}%</span>
                      </div>
                      <h4 className="text-xs font-bold text-white font-heading line-clamp-2">
                        {doc.title}
                      </h4>
                      <p className="text-xs text-slate-400 mt-2 line-clamp-3">
                        {doc.summary}
                      </p>
                    </div>
                    <div className="mt-4 pt-3 border-t border-border-subtle flex items-center justify-between text-[10px] font-mono text-slate-500">
                      <span>Fuente: {doc.source}</span>
                      {doc.url && (
                        <a href={doc.url} target="_blank" rel="noreferrer" className="text-gold-light hover:underline font-semibold">
                          Ver PDF / Informe →
                        </a>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

        </main>
      </div>

      {/* Modals */}
      <ScoreExplainabilityModal
        score={selectedScore}
        onClose={() => setSelectedScore(null)}
      />

      <TimeSeriesChartModal
        indicator={selectedIndicator}
        onClose={() => setSelectedIndicator(null)}
      />

      {/* Footer */}
      <footer className="border-t border-border-subtle bg-[#0A0A0B] py-6 px-6 mt-12 text-xs text-slate-500">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-3">
          <div className="flex items-center space-x-2">
            <span className="font-heading font-bold text-slate-300">RADAR CHILE 2035</span>
            <span>•</span>
            <span>Plataforma de Inteligencia Económica</span>
            <span>•</span>
            <span className="font-mono text-gold-light">v0.1</span>
          </div>
          <div className="font-mono text-[11px] text-slate-400">
            Fuentes Oficiales: FRED • Banco Central de Chile • Cochilco • World Bank • Global Markets
          </div>
        </div>
      </footer>
    </div>
  );
};
