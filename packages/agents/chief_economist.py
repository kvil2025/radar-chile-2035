import datetime
import logging
from typing import Optional
from sqlalchemy.orm import Session
from packages.common.models import Indicator, Observation, Score, Regime, Scenario, TransmissionChannel, Alert
from packages.common.database import SessionLocal
from packages.agents.gemini_client import GeminiClient

logger = logging.getLogger(__name__)

class ChiefEconomistAgent:
    """
    Chief Economist Agent for RADAR CHILE 2035.
    Generates executive macroeconomic briefings and answers analytical questions
    strictly grounded in the quantitative database state without hallucinations.
    """

    SYSTEM_PROMPT = """Eres el Economista Jefe y Estratega Cuantitativo Senior de RADAR CHILE 2035.
Tu responsabilidad es interpretar rigurosamente los datos macroeconómicos, índices cuantitativos,
regímenes y canales de transmisión calculados por la plataforma.

Reglas estrictas de respuesta:
1. DISTINGUE rigurosamente entre:
   - DATO OBSERVADO (hecho empírico con fuente)
   - INDICADOR CALCULADO (transformación matemática)
   - RÉGIMEN ACTUAL (consistencia con evidencia, nunca certeza dogmática)
   - ESCENARIO (probabilidad estimada etiquetada como MODEL_ESTIMATE)
   - ALERTA (quiebre de umbral crítico)
2. Responde estructurando siempre en tres dimensiones:
   - WHAT? (¿Qué está ocurriendo?)
   - WHY? (¿Qué componentes e indicadores explican el movimiento?)
   - SO WHAT? (¿Cómo se transmite esto a Chile y qué oportunidades/riesgos genera?)
3. NUNCA inventes datos ni asumas causalidades no fundamentadas en los canales de transmisión.
4. Redacta en español formal, preciso, ejecutivo y directo en formato Markdown.
"""

    def __init__(self, db: Optional[Session] = None, api_key: Optional[str] = None):
        self.db_provided = db is not None
        self.db = db if db is not None else SessionLocal()
        self.ai = GeminiClient(api_key=api_key)

    def generate_executive_briefing(self) -> dict:
        """Generate a complete executive briefing based on the latest database state."""
        logger.info("🧠 ChiefEconomistAgent generating executive briefing...")
        context = self._gather_macro_context()

        prompt = f"""Genera el Informe Ejecutivo Semanal de Inteligencia Macroeconómica para RADAR CHILE 2035 basado en el siguiente estado cuantitativo oficial del sistema:

{context}

Estructura el informe manteniendo rigurosamente los siguientes encabezados exactos en Markdown:
# INFORME EJECUTIVO DE INTELIGENCIA MACROECONÓMICA — RADAR CHILE 2035

## 1. DIAGNÓSTICO DEL ENTORNO GLOBAL & RÉGIMEN ACTIVO (WHAT)
Explica el régimen económico activo, el nivel de confianza y el estado del ciclo mundial.

## 2. ATRIBUCIÓN DE FACTORES & DESGLOSE DE ÍNDICES (WHY)
Analiza los 5 índices estratégicos (Chile Opportunity, Mining Cycle, Commodity Cycle, Monetary Stress, Dollar Stress), destacando los principales componentes que impulsan o restringen cada score.

## 3. CANALES DE TRANSMISIÓN & IMPACTO EN CHILE (SO WHAT)
Detalla cómo las variables externas (tasas Fed, cobre, demanda de IA, China) se transmiten a las variables locales (CLP/USD, recaudación fiscal, TPM, IMACEC) y el balance neto de oportunidad.

## 4. MATRIZ DE ESCENARIOS MACRO (S1 A S4)
Sintetiza la distribución de probabilidades estimadas (MODEL_ESTIMATE) y qué señales técnicas vigilar.

## 5. CONCLUSIONES & IMPLICANCIAS ESTRATÉGICAS
Recomendaciones prácticas para toma de decisiones empresariales y de inversión en Chile.
"""

        report_markdown = self.ai.generate_content(
            system_instruction=self.SYSTEM_PROMPT,
            prompt=prompt
        )

        return {
            "title": "Informe Ejecutivo Semanal — RADAR CHILE 2035",
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "methodology_version": "v0.1",
            "content": report_markdown,
            "grounded_context_summary": {
                "regime": self.db.query(Regime).order_by(Regime.timestamp.desc()).first().regime_code if self.db.query(Regime).count() > 0 else "N/A",
                "scores_count": self.db.query(Score).count(),
                "active_alerts_count": self.db.query(Alert).filter(Alert.status == "ACTIVE").count()
            }
        }

    def answer_macro_question(self, question: str) -> dict:
        """Answer a custom user question grounded in current quantitative context."""
        logger.info(f"🧠 ChiefEconomistAgent answering question: '{question}'")
        context = self._gather_macro_context()

        prompt = f"""Pregunta del Usuario: "{question}"

Estado Cuantitativo Actual de la Base de Datos Oficial de RADAR CHILE 2035:
{context}

Responde a la pregunta del usuario con máxima precisión analítica, citando los valores numéricos observados, los índices correspondientes y las implicancias directas para Chile. Sé directo, riguroso y cuantitativo.
"""

        answer = self.ai.generate_content(
            system_instruction=self.SYSTEM_PROMPT,
            prompt=prompt
        )

        return {
            "question": question,
            "answer": answer,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }

    def _gather_macro_context(self) -> str:
        """Build structured context string from the database."""
        lines = []

        # 1. Active Regime
        regime = self.db.query(Regime).order_by(Regime.timestamp.desc()).first()
        if regime:
            lines.append(f"=== RÉGIMEN ECONÓMICO GLOBAL ACTIVO ===")
            lines.append(f"Régimen: {regime.regime_code} (Confianza: {int(regime.confidence*100)}%)")
            lines.append(f"Driver Principal: {regime.primary_driver}")
            lines.append(f"Síntesis: {regime.rationale}\n")

        # 2. Latest Scores
        scores = self.db.query(Score).order_by(Score.timestamp.desc()).limit(5).all()
        if scores:
            lines.append(f"=== ÍNDICES ESTRATÉGICOS (SCORING v0.1) ===")
            for s in scores:
                lines.append(f"- {s.score_type}: {s.value:.1f}/100 (Confianza: {int(s.confidence*100)}%, Tendencia: {s.metadata_json.get('trend', 'STABLE') if s.metadata_json else 'STABLE'})")
            lines.append("")

        # 3. Key Observations
        indicators = self.db.query(Indicator).all()
        lines.append(f"=== OBSERVACIONES RECIENTES DE VARIABLES FUNDAMENTALES ===")
        for ind in indicators:
            latest = self.db.query(Observation).filter(
                Observation.indicator_id == ind.id
            ).order_by(Observation.timestamp.desc()).first()
            if latest:
                lines.append(f"- {ind.code} ({ind.name}): {latest.value} {ind.unit} [Calidad: {latest.quality_status}]")
        lines.append("")

        # 4. Scenarios
        scenarios = self.db.query(Scenario).all()
        if scenarios:
            lines.append(f"=== ESCENARIOS MACROECONÓMICOS (MODEL_ESTIMATE) ===")
            for sc in scenarios:
                lines.append(f"- {sc.scenario_code} ({sc.name}): Probabilidad {sc.probability*100:.1f}% | Riesgo: {sc.risk_level} | Oportunidad: {sc.opportunity_level}")
                lines.append(f"  Efecto en Chile: {sc.expected_chile_effect}")
            lines.append("")

        # 5. Transmission Channels
        channels = self.db.query(TransmissionChannel).all()
        if channels:
            lines.append(f"=== CANALES DE TRANSMISIÓN MACRO A CHILE ===")
            for ch in channels:
                lines.append(f"- {ch.channel_name} ({ch.global_indicator_code} -> {ch.chile_indicator_code}): Impact Score: {ch.current_impact_score:+.1f} pts (Velocidad: {ch.transmission_speed})")
            lines.append("")

        # 6. Active Alerts
        alerts = self.db.query(Alert).filter(Alert.status == "ACTIVE").all()
        if alerts:
            lines.append(f"=== ALERTAS CUANTITATIVAS ACTIVAS ({len(alerts)}) ===")
            for a in alerts:
                lines.append(f"- [{a.severity}] {a.title}: {a.description} (Valor: {a.current_value}, Umbral: {a.trigger_value})")

        return "\n".join(lines)

    def close(self):
        if not self.db_provided:
            self.db.close()
        self.ai.close()
