import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { Bot, Sparkles, Send, RefreshCw, MessageSquareQuote, CheckCircle2 } from 'lucide-react';

export const PanelChiefEconomist: React.FC = () => {
  const [briefing, setBriefing] = useState<any>(null);
  const [isLoadingBriefing, setIsLoadingBriefing] = useState<boolean>(true);
  
  const [question, setQuestion] = useState<string>('');
  const [chatHistory, setChatHistory] = useState<Array<{ q: string; a: string; time: string }>>([]);
  const [isAsking, setIsAsking] = useState<boolean>(false);

  const loadBriefing = async () => {
    setIsLoadingBriefing(true);
    try {
      const data = await api.getBriefing();
      setBriefing(data);
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoadingBriefing(false);
    }
  };

  useEffect(() => {
    loadBriefing();
  }, []);

  const handleAskQuestion = async (customQ?: string) => {
    const qToSend = customQ || question;
    if (!qToSend.trim() || isAsking) return;

    setIsAsking(true);
    try {
      const res = await api.askChiefEconomist(qToSend);
      setChatHistory(prev => [
        {
          q: qToSend,
          a: res.answer,
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        },
        ...prev
      ]);
      if (!customQ) setQuestion('');
    } catch (err) {
      console.error(err);
    } finally {
      setIsAsking(false);
    }
  };

  const quickQuestions = [
    "¿Por qué el Chile Opportunity Index está en 52.3?",
    "¿Cómo afecta el rendimiento del bono US10Y al dólar en Chile?",
    "¿Qué condiciones se requieren para confirmar un superciclo del cobre?",
    "¿Qué impacto tiene la inflación en las decisiones de la Fed y el Banco Central?"
  ];

  return (
    <div className="space-y-6">
      
      {/* Top Banner / Q&A Box */}
      <div className="glass-panel p-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-5">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-gold-primary/15 border border-gold-primary/40 flex items-center justify-center text-gold-primary">
              <Bot className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <h3 className="text-base font-bold text-white font-heading">
                  Economista Jefe Cuantitativo (AI Agent)
                </h3>
                <span className="px-2 py-0.5 rounded text-[9px] font-mono font-bold bg-gold-primary/15 text-gold-light border border-gold-primary/30 flex items-center space-x-1">
                  <Sparkles className="w-2.5 h-2.5" />
                  <span>GEMINI POWERED</span>
                </span>
              </div>
              <p className="text-xs text-slate-400">
                Interpretación y respuestas estrictamente fundamentadas en el estado oficial de la base de datos
              </p>
            </div>
          </div>

          <button
            onClick={loadBriefing}
            disabled={isLoadingBriefing}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-xl bg-navy-800 hover:bg-navy-700 text-xs font-semibold text-gold-light border border-navy-700 transition-all self-start sm:self-auto disabled:opacity-50"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isLoadingBriefing ? 'animate-spin' : ''}`} />
            <span>Actualizar Informe</span>
          </button>
        </div>

        {/* Question input */}
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleAskQuestion();
          }}
          className="relative mt-2"
        >
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Haz una pregunta macroeconómica cuantitativa sobre Chile o el mundo..."
            className="w-full bg-[#111114] border border-border-subtle focus:border-gold-primary/60 rounded-xl px-4 py-3 text-xs text-white placeholder-slate-500 outline-none pr-12 transition-all shadow-inner"
          />
          <button
            type="submit"
            disabled={isAsking || !question.trim()}
            className="absolute right-2 top-2 px-3 py-1.5 rounded-lg bg-gold-primary text-black font-bold text-xs hover:bg-gold-light transition-all disabled:opacity-40"
          >
            {isAsking ? <RefreshCw className="w-3.5 h-3.5 animate-spin" /> : <Send className="w-3.5 h-3.5" />}
          </button>
        </form>

        {/* Quick Questions Chips */}
        <div className="flex items-center space-x-2 overflow-x-auto pt-3 pb-1">
          <span className="text-[10px] font-mono text-slate-500 whitespace-nowrap">Sugerencias:</span>
          {quickQuestions.map((q, idx) => (
            <button
              key={idx}
              onClick={() => handleAskQuestion(q)}
              disabled={isAsking}
              className="text-[11px] whitespace-nowrap px-2.5 py-1 rounded-lg bg-navy-950/80 hover:bg-navy-900 border border-navy-800 text-slate-300 hover:text-gold-light transition-colors"
            >
              {q}
            </button>
          ))}
        </div>
      </div>

      {/* Chat History Responses if any */}
      {chatHistory.length > 0 && (
        <div className="space-y-4">
          {chatHistory.map((item, idx) => (
            <div key={idx} className="glass-panel p-5 border-l-4 border-l-gold-primary animate-in fade-in duration-300">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center space-x-2">
                  <MessageSquareQuote className="w-4 h-4 text-gold-primary" />
                  <span className="text-xs font-bold text-white font-heading">{item.q}</span>
                </div>
                <span className="text-[10px] font-mono text-slate-500">{item.time}</span>
              </div>
              <div className="text-xs text-slate-200 leading-relaxed prose prose-invert max-w-none whitespace-pre-line mt-2">
                {item.a}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Full Executive Briefing Document */}
      <div className="glass-panel p-6">
        <div className="border-b border-border-subtle pb-4 mb-5 flex items-center justify-between">
          <div>
            <span className="text-[10px] font-mono text-gold-primary uppercase font-bold tracking-wider">
              INFORME EJECUTIVO DE INTELIGENCIA
            </span>
            <h2 className="text-lg font-bold text-white font-heading mt-0.5">
              {briefing?.title || 'Informe Semanal — RADAR CHILE 2035'}
            </h2>
          </div>
          <div className="flex items-center space-x-2 text-[10px] font-mono text-emerald-400 bg-emerald-500/10 border border-emerald-500/30 px-2.5 py-1 rounded-lg">
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>Datos 100% Verificados</span>
          </div>
        </div>

        {isLoadingBriefing ? (
          <div className="py-12 flex flex-col items-center justify-center space-y-3">
            <RefreshCw className="w-6 h-6 text-gold-primary animate-spin" />
            <span className="text-xs font-mono text-slate-400">
              Analizando estado del sistema y generando informe ejecutivo...
            </span>
          </div>
        ) : (
          <div className="text-xs text-slate-300 leading-relaxed whitespace-pre-line font-sans space-y-4">
            {briefing?.content}
          </div>
        )}
      </div>

    </div>
  );
};
