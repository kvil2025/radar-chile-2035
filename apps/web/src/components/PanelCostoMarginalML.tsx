import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import {
  Sparkles,
  Database,
  BookOpen,
  Calendar,
  CloudSun,
  Search,
  CheckCircle2
} from 'lucide-react';
import {
  ResponsiveContainer,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Area,
  ComposedChart,
  BarChart,
  Bar
} from 'recharts';

export const PanelCostoMarginalML: React.FC = () => {
  const [summary, setSummary] = useState<any>(null);
  const [forecastData, setForecastData] = useState<any>(null);
  const [climateData, setClimateData] = useState<any>(null);
  const [regulatoryDocs, setRegulatoryDocs] = useState<any[]>([]);
  
  const [horizonHours, setHorizonHours] = useState<number>(72);
  const [isTraining, setIsTraining] = useState<boolean>(false);
  const [regSearchQuery, setRegSearchQuery] = useState<string>('');
  const [regCategory, setRegCategory] = useState<string>('ALL');

  // AI Advisor state
  const [aiQuery, setAiQuery] = useState<string>('');
  const [aiResponse, setAiResponse] = useState<string | null>(null);
  const [isConsultingAi, setIsConsultingAi] = useState<boolean>(false);

  const handleConsultAdvisor = async () => {
    if (!aiQuery.trim()) return;
    setIsConsultingAi(true);
    try {
      const resp = await api.consultRegulatoryAdvisor(aiQuery);
      setAiResponse(resp);
    } catch (err) {
      console.error(err);
    } finally {
      setIsConsultingAi(false);
    }
  };

  useEffect(() => {
    Promise.all([
      api.getCostoMarginalSummary().catch(() => null),
      api.getClimateCorrelations().catch(() => null),
      api.getRegulatoryCorpus().catch(() => [])
    ]).then(([s, c, r]) => {
      setSummary(s);
      setClimateData(c);
      setRegulatoryDocs(r);
    });

    handleTrain(72);
  }, []);

  const handleTrain = async (h?: number) => {
    const targetH = h || horizonHours;
    setIsTraining(true);
    try {
      const res = await api.trainAndForecastCostoMarginal(targetH);
      setForecastData(res);
    } catch (err) {
      console.error(err);
    } finally {
      setIsTraining(false);
    }
  };

  const handleSearchReg = async () => {
    try {
      const docs = await api.getRegulatoryCorpus(regSearchQuery, regCategory);
      setRegulatoryDocs(docs);
    } catch (err) {
      console.error(err);
    }
  };

  const featureChartData = forecastData?.feature_importance
    ? Object.entries(forecastData.feature_importance).map(([key, val]) => ({
        feature: key.replace('_', ' '),
        weight: val
      })).sort((a: any, b: any) => (b.weight as number) - (a.weight as number)).slice(0, 6)
    : [];

  const chartPoints = forecastData?.forecast?.map((p: any) => ({
    time: `${new Date(p.timestamp).toLocaleDateString([], { month: 'numeric', day: 'numeric' })} ${p.hour}:00`,
    cost: p.predicted_cost_usd_mwh,
    upper: p.upper_bound_95,
    lower: p.lower_bound_95
  })) || [];

  return (
    <div className="space-y-6">
      
      {/* 5-Year Historical Dataset Overview */}
      {summary && (
        <div className="p-5 rounded-2xl bg-gradient-to-r from-navy-900/90 via-[#121218] to-bg-card border border-gold-primary/30 shadow-glass flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div className="flex items-start space-x-3.5">
            <div className="w-10 h-10 rounded-xl bg-gold-primary/15 border border-gold-primary/40 flex items-center justify-center text-gold-primary shrink-0">
              <Database className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="text-[10px] font-bold uppercase tracking-wider text-gold-primary font-mono">
                  DATASET HISTÓRICO INTEGRADO (5 AÑOS)
                </span>
                <span className="px-2 py-0.5 text-[9px] font-mono bg-emerald-500/10 text-emerald-400 rounded border border-emerald-500/30">
                  {summary.total_records?.toLocaleString()} Registros Horarios
                </span>
              </div>
              <p className="text-xs text-slate-300 mt-1">
                Serie consolidada de Costos Marginales con Clima (Temperatura, Viento, Humedad, Radiación) para entrenamiento predictivo
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-6 shrink-0 font-mono text-xs text-right">
            <div>
              <span className="text-slate-400 block text-[10px] uppercase">Costo Promedio</span>
              <strong className="text-white text-base font-bold">
                ${summary.metrics?.avg_cost_usd_mwh} <small className="text-xs text-slate-400 font-normal">USD</small>
              </strong>
            </div>
            <div>
              <span className="text-slate-400 block text-[10px] uppercase">Desv. Estándar</span>
              <strong className="text-gold-light text-base font-bold">
                ±${summary.metrics?.std_dev} <small className="text-xs text-slate-400 font-normal">USD</small>
              </strong>
            </div>
          </div>
        </div>
      )}

      {/* Model Training & Forecast Controller */}
      <div className="glass-panel p-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
          <div className="flex items-center space-x-3">
            <div className="w-9 h-9 rounded-xl bg-purple-900/40 border border-blue-500/40 flex items-center justify-center text-blue-400">
              <Sparkles className="w-4 h-4" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white font-heading">
                Motor de Pronóstico de Costo Marginal (ML + Armónicos de Fourier)
              </h3>
              <p className="text-xs text-slate-400">
                Modelo de regresión regularizada con patrones estacionales (diarios, semanales, anuales) y variables climáticas
              </p>
            </div>
          </div>

          {/* Horizon Selector and Train Button */}
          <div className="flex items-center space-x-3">
            <div className="flex items-center space-x-1 bg-bg-card p-1 rounded-xl border border-border-subtle text-xs font-mono">
              {[24, 48, 72, 168].map((h) => (
                <button
                  key={h}
                  onClick={() => {
                    setHorizonHours(h);
                    handleTrain(h);
                  }}
                  className={`px-2.5 py-1 rounded-lg transition-all ${
                    horizonHours === h
                      ? 'bg-gold-primary text-black font-bold'
                      : 'text-slate-400 hover:text-white'
                  }`}
                >
                  {h === 168 ? '7 días' : `${h}h`}
                </button>
              ))}
            </div>

            <button
              onClick={() => handleTrain()}
              disabled={isTraining}
              className="px-4 py-2 rounded-xl bg-gold-primary hover:bg-gold-light text-black font-bold text-xs uppercase font-mono tracking-wider flex items-center space-x-1.5 transition-all shadow-md disabled:opacity-50"
            >
              <Sparkles className={`w-3.5 h-3.5 ${isTraining ? 'animate-spin' : ''}`} />
              <span>{isTraining ? 'Entrenando...' : 'Reentrenar'}</span>
            </button>
          </div>
        </div>

        {/* Model Metrics Strip */}
        {forecastData?.metrics && (
          <div className="grid grid-cols-1 sm:grid-cols-4 gap-3 mb-5">
            <div className="p-3 rounded-xl bg-bg-card border border-border-subtle">
              <span className="text-[10px] font-mono text-slate-400 uppercase block">Bondad de Ajuste (R²)</span>
              <span className="text-lg font-black font-heading text-emerald-400 mt-0.5 block">
                {(forecastData.metrics.r2_score * 100).toFixed(1)}%
              </span>
              <span className="text-[9px] font-mono text-slate-500">Capacidad explicativa de varianza</span>
            </div>

            <div className="p-3 rounded-xl bg-bg-card border border-border-subtle">
              <span className="text-[10px] font-mono text-slate-400 uppercase block">Error Cuadrático (RMSE)</span>
              <span className="text-lg font-black font-heading text-gold-light mt-0.5 block">
                ${forecastData.metrics.rmse_usd_mwh} <small className="text-xs text-slate-400 font-normal">USD/MWh</small>
              </span>
              <span className="text-[9px] font-mono text-slate-500">Desviación estándar de residuos</span>
            </div>

            <div className="p-3 rounded-xl bg-bg-card border border-border-subtle">
              <span className="text-[10px] font-mono text-slate-400 uppercase block">Error Absoluto (MAE)</span>
              <span className="text-lg font-black font-heading text-slate-200 mt-0.5 block">
                ${forecastData.metrics.mae_usd_mwh} <small className="text-xs text-slate-400 font-normal">USD/MWh</small>
              </span>
              <span className="text-[9px] font-mono text-slate-500">Error medio por hora</span>
            </div>

            <div className="p-3 rounded-xl bg-bg-card border border-border-subtle">
              <span className="text-[10px] font-mono text-slate-400 uppercase block">Muestras de Entrenamiento</span>
              <span className="text-lg font-black font-heading text-white mt-0.5 block">
                {forecastData.metrics.training_samples?.toLocaleString()} <small className="text-xs text-slate-400 font-normal">horas</small>
              </span>
              <span className="text-[9px] font-mono text-slate-500">Validación continua en test set</span>
            </div>
          </div>
        )}

        {/* Forecast Chart with 95% Confidence Bounds */}
        <div className="bg-bg-card border border-border-subtle rounded-xl p-4">
          <div className="flex items-center justify-between mb-3 text-xs text-slate-400 font-mono">
            <span className="flex items-center space-x-1.5 text-gold-light font-bold">
              <Calendar className="w-3.5 h-3.5" />
              <span>Curva de Pronóstico ({horizonHours} horas) con Banda de Confianza 95%</span>
            </span>
            <span className="text-[10px] text-slate-500">
              Línea dorada: Predicción central • Área sombreada: Intervalo de confianza
            </span>
          </div>

          <div className="h-72 w-full">
            {isTraining ? (
              <div className="h-full flex items-center justify-center text-xs text-slate-500 font-mono">
                Entrenando modelo y proyectando horizonte...
              </div>
            ) : (
              <ResponsiveContainer width="100%" height="100%">
                <ComposedChart data={chartPoints} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
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
                  <Area type="monotone" dataKey="upper" name="Límite Superior 95%" stroke="none" fill="#C9A84C" fillOpacity={0.15} />
                  <Area type="monotone" dataKey="lower" name="Límite Inferior 95%" stroke="none" fill="#0A0A0B" fillOpacity={0.8} />
                  <Line
                    type="monotone"
                    dataKey="cost"
                    name="Pronóstico ($/MWh)"
                    stroke="#C9A84C"
                    strokeWidth={2.5}
                    dot={{ fill: '#C9A84C', r: 2 }}
                    activeDot={{ r: 5, fill: '#00f2ff' }}
                  />
                </ComposedChart>
              </ResponsiveContainer>
            )}
          </div>
        </div>

        {/* Feature Importance & Weather Elasticity Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
          
          {/* Feature Importance */}
          <div className="p-4 rounded-xl bg-bg-card border border-border-subtle">
            <h4 className="text-xs font-bold text-white font-heading mb-1 flex items-center space-x-1.5">
              <span>Importancia de Variables en el Modelo</span>
            </h4>
            <p className="text-[11px] text-slate-400 mb-3">Pesos relativos de los ciclos armónicos y factores climáticos</p>
            
            <div className="h-44 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={featureChartData} layout="vertical" margin={{ top: 5, right: 20, left: 40, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#22222a" />
                  <XAxis type="number" stroke="#64748b" fontSize={10} />
                  <YAxis type="category" dataKey="feature" stroke="#94a3b8" fontSize={10} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#111114',
                      borderColor: 'rgba(201, 168, 76, 0.4)',
                      borderRadius: '8px',
                      fontSize: '11px',
                      color: '#fff'
                    }}
                  />
                  <Bar dataKey="weight" name="Peso del Factor" fill="#C9A84C" radius={[0, 4, 4, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Climate Sensitivity */}
          {climateData?.temperature_sensitivity && (
            <div className="p-4 rounded-xl bg-bg-card border border-border-subtle flex flex-col justify-between">
              <div>
                <h4 className="text-xs font-bold text-white font-heading mb-1 flex items-center space-x-1.5">
                  <CloudSun className="w-4 h-4 text-gold-primary" />
                  <span>Sensibilidad Térmica & Olas de Calor</span>
                </h4>
                <p className="text-[11px] text-slate-400 mb-4">Impacto de temperaturas extremas en la demanda y costo marginal</p>

                <div className="grid grid-cols-3 gap-2.5">
                  <div className="p-2.5 rounded-lg bg-navy-900/60 border border-navy-700 text-center">
                    <span className="text-[9px] font-mono text-blue-300 block uppercase">Ola de Frío (&lt;8°C)</span>
                    <span className="text-sm font-bold font-heading text-white mt-1 block">
                      ${climateData.temperature_sensitivity.cold_spell_avg_cost_usd}
                    </span>
                    <span className="text-[9px] font-mono text-slate-400">USD/MWh</span>
                  </div>

                  <div className="p-2.5 rounded-lg bg-navy-900/60 border border-navy-700 text-center">
                    <span className="text-[9px] font-mono text-slate-300 block uppercase">Clima Templado</span>
                    <span className="text-sm font-bold font-heading text-white mt-1 block">
                      ${climateData.temperature_sensitivity.mild_weather_avg_cost_usd}
                    </span>
                    <span className="text-[9px] font-mono text-slate-400">USD/MWh</span>
                  </div>

                  <div className="p-2.5 rounded-lg bg-amber-950/30 border border-amber-800/40 text-center">
                    <span className="text-[9px] font-mono text-amber-300 block uppercase">Ola Calor (&gt;25°C)</span>
                    <span className="text-sm font-bold font-heading text-amber-300 mt-1 block">
                      ${climateData.temperature_sensitivity.heatwave_avg_cost_usd}
                    </span>
                    <span className="text-[9px] font-mono text-amber-400/80">+{climateData.temperature_sensitivity.heatwave_premium_pct}% prima</span>
                  </div>
                </div>
              </div>

              <p className="text-[10px] text-slate-400 mt-4 leading-relaxed bg-[#111114] p-2.5 rounded-lg border border-border-subtle">
                💡 <strong>Insight Cuantitativo</strong>: Durante olas de calor en verano la demanda por climatización eleva el costo marginal en un <strong>+{climateData.temperature_sensitivity.heatwave_premium_pct}%</strong> debido al despacho de unidades térmicas peaking a diésel.
              </p>
            </div>
          )}

        </div>

      </div>

      {/* Searchable Chilean Energy Regulatory Knowledge Base */}
      <div className="glass-panel p-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-navy-800 border border-navy-700 flex items-center justify-center text-blue-400">
              <BookOpen className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <h3 className="text-base font-bold text-white font-heading">
                  Cuerpo Regulatorio Eléctrico de Chile (DFL 4, BESS, PMGD & CNE)
                </h3>
                <span className="px-2 py-0.5 rounded text-[9px] font-mono font-bold bg-navy-800 text-blue-300 border border-navy-700">
                  BASE DE CONOCIMIENTO
                </span>
              </div>
              <p className="text-xs text-slate-400">
                Leyes vigentes, decretos tarifarios y normas de conexión integradas desde la base regulatoria
              </p>
            </div>
          </div>

          {/* Search bar & filter */}
          <div className="flex flex-wrap items-center gap-2">
            <div className="flex items-center space-x-1 bg-[#111114] p-1 rounded-xl border border-border-subtle text-[11px] font-mono">
              {['ALL', 'ALMACENAMIENTO_BESS', 'PMGD_DISTRIBUCION', 'MERCADO_Y_TARIFAS'].map((cat) => (
                <button
                  key={cat}
                  onClick={() => {
                    setRegCategory(cat);
                    api.getRegulatoryCorpus(regSearchQuery, cat).then(setRegulatoryDocs);
                  }}
                  className={`px-2 py-1 rounded-lg transition-all ${
                    regCategory === cat
                      ? 'bg-gold-primary text-black font-bold'
                      : 'text-slate-400 hover:text-white'
                  }`}
                >
                  {cat === 'ALL' ? 'Todas' : cat.replace('_', ' ')}
                </button>
              ))}
            </div>

            <div className="relative">
              <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                placeholder="Buscar artículo..."
                value={regSearchQuery}
                onChange={(e) => setRegSearchQuery(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSearchReg()}
                className="bg-[#111114] border border-border-subtle focus:border-gold-primary/60 rounded-xl pl-8 pr-3 py-1.5 text-xs text-white outline-none w-36 sm:w-48"
              />
            </div>
          </div>
        </div>

        {/* Regulatory Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {regulatoryDocs.map((doc) => (
            <div
              key={doc.id}
              className="p-4 rounded-xl bg-bg-card border border-border-subtle hover:border-gold-primary/40 transition-all flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between text-[10px] font-mono text-gold-primary mb-1.5">
                  <span className="bg-navy-900 border border-navy-700 px-2 py-0.5 rounded text-blue-300">
                    {doc.doc_type}
                  </span>
                  <span>{doc.law_reference}</span>
                </div>
                
                <h4 className="text-xs font-bold text-white font-heading mt-1">
                  {doc.title}
                </h4>

                <p className="text-xs text-slate-300 mt-2 leading-relaxed">
                  {doc.summary}
                </p>

                {doc.key_articles && doc.key_articles.length > 0 && (
                  <div className="mt-3 space-y-1.5 pt-2.5 border-t border-border-subtle">
                    <span className="text-[9px] font-mono text-slate-400 uppercase font-bold block">Artículos Clave:</span>
                    {doc.key_articles.map((art: any, aIdx: number) => (
                      <div key={aIdx} className="text-[11px] text-slate-300 flex items-start space-x-1.5">
                        <span className="text-gold-light font-mono shrink-0">{art.art}:</span>
                        <span className="text-slate-400">{art.desc}</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              <div className="mt-4 pt-2.5 border-t border-border-subtle flex items-center justify-between text-[10px] font-mono text-slate-500">
                <span>Categoría: <strong className="text-slate-300">{doc.category?.replace('_', ' ')}</strong></span>
                <span className="text-emerald-400 flex items-center space-x-1">
                  <CheckCircle2 className="w-3 h-3" />
                  <span>Vigente</span>
                </span>
              </div>
            </div>
          ))}
        </div>

        {/* Interactive AI Regulatory Advisor (Gemini) */}
        <div className="mt-8 p-5 rounded-2xl bg-gradient-to-r from-navy-950/80 to-[#111115] border border-gold-primary/30 space-y-4">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 rounded-xl bg-gold-primary/15 border border-gold-primary/40 flex items-center justify-center text-gold-primary">
              <Sparkles className="w-4 h-4" />
            </div>
            <div>
              <h4 className="text-sm font-bold text-white tracking-wide">Asesor Legal & Regulatorio IA (Google Gemini)</h4>
              <p className="text-[11px] text-slate-400 font-mono">Consulta dudas jurídicas sobre DFL 4, Ley 21.505 BESS, DS 88 PMGD y Resoluciones CNE</p>
            </div>
          </div>

          <div className="flex flex-col sm:flex-row gap-2">
            <input
              type="text"
              placeholder="Ej: ¿Qué requisitos del DS 88 aplican para conectar un BESS de 9 MW en régimen PMGD?"
              value={aiQuery}
              onChange={(e) => setAiQuery(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleConsultAdvisor()}
              className="flex-1 bg-[#0a0a0c] border border-border-subtle focus:border-gold-primary/60 rounded-xl px-4 py-2.5 text-xs text-white outline-none"
            />
            <button
              onClick={handleConsultAdvisor}
              disabled={isConsultingAi}
              className="px-5 py-2.5 bg-gradient-to-r from-gold-primary to-gold-light text-black font-bold text-xs rounded-xl hover:opacity-95 transition-all flex items-center justify-center space-x-1.5 disabled:opacity-50"
            >
              <Sparkles className={`w-3.5 h-3.5 ${isConsultingAi ? 'animate-spin' : ''}`} />
              <span>{isConsultingAi ? 'Consultando Leyes...' : 'Consultar a la IA'}</span>
            </button>
          </div>

          {aiResponse && (
            <div className="p-4 rounded-xl bg-[#09090b] border border-border-subtle text-xs text-slate-200 leading-relaxed font-sans prose prose-invert max-w-none whitespace-pre-wrap animate-in fade-in duration-200">
              {aiResponse}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
