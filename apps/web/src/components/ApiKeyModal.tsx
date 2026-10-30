import React, { useState, useEffect } from 'react';
import { Key, Eye, EyeOff, CheckCircle2, AlertCircle, X, ExternalLink, Sparkles, Trash2 } from 'lucide-react';
import { getStoredGeminiKey, setStoredGeminiKey } from '../services/api';

interface ApiKeyModalProps {
  isOpen: boolean;
  onClose: () => void;
  onKeyUpdated?: () => void;
}

export const ApiKeyModal: React.FC<ApiKeyModalProps> = ({ isOpen, onClose, onKeyUpdated }) => {
  const [apiKey, setApiKey] = useState('');
  const [showKey, setShowKey] = useState(false);
  const [isTesting, setIsTesting] = useState(false);
  const [testResult, setTestResult] = useState<{ success: boolean; message: string } | null>(null);
  const [isSaved, setIsSaved] = useState(false);

  useEffect(() => {
    if (isOpen) {
      const stored = getStoredGeminiKey();
      setApiKey(stored || '');
      setIsSaved(!!stored);
      setTestResult(null);
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const handleTestKey = async () => {
    if (!apiKey.trim()) {
      setTestResult({ success: false, message: 'Ingresa una API Key para validar.' });
      return;
    }

    setIsTesting(true);
    setTestResult(null);

    try {
      const res = await fetch(`https://generativelanguage.googleapis.com/v1beta/models?key=${apiKey.trim()}`);
      if (res.ok) {
        setTestResult({
          success: true,
          message: '¡Conexión exitosa! Clave válida y autorizada para interactuar con Gemini 2.5 / 3.5 Flash.'
        });
      } else {
        const errorData = await res.json().catch(() => ({}));
        setTestResult({
          success: false,
          message: errorData?.error?.message || 'Error al validar la clave con Google Cloud.'
        });
      }
    } catch (e: any) {
      setTestResult({
        success: false,
        message: 'No se pudo conectar con el servidor de Google. Revisa tu conexión.'
      });
    } finally {
      setIsTesting(false);
    }
  };

  const handleSave = () => {
    setStoredGeminiKey(apiKey);
    setIsSaved(!!apiKey.trim());
    if (onKeyUpdated) onKeyUpdated();
    onClose();
  };

  const handleRemove = () => {
    setStoredGeminiKey('');
    setApiKey('');
    setIsSaved(false);
    setTestResult(null);
    if (onKeyUpdated) onKeyUpdated();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-md animate-fade-in">
      <div className="relative w-full max-w-lg p-6 rounded-2xl bg-[#0f1117] border border-gold-primary/30 shadow-2xl text-slate-100">
        
        {/* Header */}
        <div className="flex items-start justify-between pb-4 border-b border-border-subtle">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-gold-primary/15 border border-gold-primary/40 flex items-center justify-center text-gold-primary">
              <Key className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <h3 className="text-base font-bold text-white font-heading">
                  Configuración de API Key (BYOK)
                </h3>
                <span className="px-2 py-0.5 text-[9px] font-mono bg-navy-800 text-blue-300 rounded border border-navy-700">
                  Google Gemini
                </span>
              </div>
              <p className="text-xs text-slate-400 mt-0.5">
                Usa tu propia clave para interactuar con la IA sin límites
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/60 transition-all"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="py-4 space-y-4">
          <div className="p-3.5 rounded-xl bg-navy-950/70 border border-navy-800 text-xs text-slate-300 leading-relaxed">
            <div className="flex items-center space-x-2 text-gold-light font-semibold mb-1">
              <Sparkles className="w-3.5 h-3.5" />
              <span>Acceso Directo e Ilimitado</span>
            </div>
            Al conectar tu propia API key de Google Gemini, todas las tesis de inversión, dictámenes legales RAG y diagnósticos de despacho se procesan con tu cuota personal, garantizando máxima velocidad sin restricciones del servidor.
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-200 mb-1.5">
              Google Gemini API Key
            </label>
            <div className="relative">
              <input
                type={showKey ? 'text' : 'password'}
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                placeholder="AIzaSy..."
                className="w-full px-3.5 py-2.5 pr-10 text-xs font-mono bg-bg-card rounded-xl border border-border-subtle focus:border-gold-primary focus:outline-none text-slate-100 placeholder-slate-500 transition-all"
              />
              <button
                type="button"
                onClick={() => setShowKey(!showKey)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-200 transition-colors"
              >
                {showKey ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
            </div>
          </div>

          {/* Test connection results */}
          {testResult && (
            <div
              className={`p-3 rounded-xl border flex items-start space-x-2 text-xs leading-relaxed animate-fade-in ${
                testResult.success
                  ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300'
                  : 'bg-red-500/10 border-red-500/30 text-red-300'
              }`}
            >
              {testResult.success ? (
                <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
              ) : (
                <AlertCircle className="w-4 h-4 text-red-400 shrink-0 mt-0.5" />
              )}
              <span>{testResult.message}</span>
            </div>
          )}

          <div className="flex items-center justify-between text-xs text-slate-400 pt-1">
            <a
              href="https://aistudio.google.com/app/apikey"
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center space-x-1.5 text-blue-400 hover:text-blue-300 transition-colors"
            >
              <span>Obtener API Key gratis en Google AI Studio</span>
              <ExternalLink className="w-3 h-3" />
            </a>

            {isSaved && (
              <span className="inline-flex items-center space-x-1 text-emerald-400 text-[11px] font-mono">
                <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                <span>Clave activa</span>
              </span>
            )}
          </div>
        </div>

        {/* Footer Actions */}
        <div className="flex items-center justify-between pt-4 border-t border-border-subtle gap-2">
          {isSaved ? (
            <button
              onClick={handleRemove}
              className="flex items-center space-x-1.5 px-3 py-2 text-xs font-semibold text-red-400 hover:text-red-300 hover:bg-red-500/10 rounded-xl transition-all"
            >
              <Trash2 className="w-3.5 h-3.5" />
              <span>Remover clave</span>
            </button>
          ) : (
            <div />
          )}

          <div className="flex items-center space-x-2">
            <button
              onClick={handleTestKey}
              disabled={isTesting || !apiKey.trim()}
              className="px-3.5 py-2 text-xs font-semibold text-slate-200 bg-bg-card hover:bg-bg-card-hover border border-border-subtle hover:border-gold-primary/40 rounded-xl transition-all disabled:opacity-40"
            >
              {isTesting ? 'Probando...' : 'Probar Conexión'}
            </button>
            <button
              onClick={handleSave}
              className="px-4 py-2 text-xs font-bold text-navy-950 bg-gold-primary hover:bg-gold-light rounded-xl transition-all shadow-gold active:scale-95"
            >
              Guardar y Usar
            </button>
          </div>
        </div>

      </div>
    </div>
  );
};
