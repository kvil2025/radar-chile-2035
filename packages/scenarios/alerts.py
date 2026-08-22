import datetime
import logging
from typing import Optional
from sqlalchemy.orm import Session
from packages.common.models import Alert, Indicator, Observation
from packages.common.database import SessionLocal

logger = logging.getLogger(__name__)

class AlertEngine:
    """
    Alert Engine: Evaluates quantitative threshold conditions across indicators.
    Generates and updates active alerts classified by severity: INFO, WATCH, WARNING, CRITICAL.
    """

    ALERT_RULES = [
        {
            "indicator_code": "US10Y",
            "threshold": 4.50,
            "operator": ">",
            "severity": "WARNING",
            "title": "US10Y Yield sobre 4.50%",
            "description_template": "El rendimiento del bono del Tesoro a 10 años se sitúa en {value:.2f}%, elevando el costo de fondeo internacional y presionando el tipo de cambio CLP."
        },
        {
            "indicator_code": "COPPER",
            "threshold": 4.20,
            "operator": ">",
            "severity": "INFO",
            "title": "Cobre sobre Umbral de Expansión Fiscal ($4.20/lb)",
            "description_template": "La cotización del cobre en ${value:.2f}/lb fortalece la recaudación fiscal vía royalty e impulsa los términos de intercambio."
        },
        {
            "indicator_code": "COPPER",
            "threshold": 3.80,
            "operator": "<",
            "severity": "CRITICAL",
            "title": "Alerta Crítica: Cobre bajo $3.80/lb",
            "description_template": "El precio del cobre ha caído a ${value:.2f}/lb, comprometiendo metas de balance fiscal y reduciendo exportaciones mineras."
        },
        {
            "indicator_code": "DXY",
            "threshold": 105.0,
            "operator": ">",
            "severity": "WARNING",
            "title": "DXY sobre 105.0 — Estrés Cambiario Emergente",
            "description_template": "El índice DXY alcanza {value:.2f}, reflejando fuerte apreciación global del dólar que encarece importaciones chilenas."
        },
        {
            "indicator_code": "CLP_USD",
            "threshold": 950.0,
            "operator": ">",
            "severity": "WATCH",
            "title": "Tipo de Cambio CLP/USD sobre $950",
            "description_template": "El dólar observado en Chile cotiza a ${value:.1f}, incrementando presiones en precios de combustibles e insumos transables."
        }
    ]

    def __init__(self, db: Optional[Session] = None):
        self.db_provided = db is not None
        self.db = db if db is not None else SessionLocal()

    def evaluate_alerts(self) -> list[dict]:
        """Evaluate all alert rules against latest observations."""
        logger.info("🚨 Running Alert Engine evaluation...")
        latest_obs = self._get_latest_observations()
        indicator_map = {ind.code: ind for ind in self.db.query(Indicator).all()}

        active_alerts = []

        for rule in self.ALERT_RULES:
            code = rule["indicator_code"]
            obs = latest_obs.get(code)
            if not obs:
                continue

            val = obs.value
            thresh = rule["threshold"]
            op = rule["operator"]

            is_triggered = False
            if op == ">" and val > thresh:
                is_triggered = True
            elif op == "<" and val < thresh:
                is_triggered = True

            if is_triggered:
                ind = indicator_map.get(code)
                desc = rule["description_template"].format(value=val)

                # Check if alert already exists
                existing = self.db.query(Alert).filter(
                    Alert.title == rule["title"],
                    Alert.status == "ACTIVE"
                ).first()

                if existing:
                    existing.current_value = val
                    existing.description = desc
                    self.db.add(existing)
                    active_alerts.append(existing)
                else:
                    new_alert = Alert(
                        severity=rule["severity"],
                        title=rule["title"],
                        description=desc,
                        indicator_id=ind.id if ind else None,
                        trigger_value=thresh,
                        current_value=val,
                        status="ACTIVE",
                        created_at=datetime.datetime.utcnow()
                    )
                    self.db.add(new_alert)
                    active_alerts.append(new_alert)

        self.db.commit()
        logger.info(f"✅ Alert evaluation complete: {len(active_alerts)} active alerts.")
        return [
            {
                "id": a.id,
                "severity": a.severity,
                "title": a.title,
                "description": a.description,
                "trigger_value": a.trigger_value,
                "current_value": a.current_value,
                "status": a.status,
                "created_at": a.created_at.isoformat() if a.created_at else None
            }
            for a in active_alerts
        ]

    def _get_latest_observations(self) -> dict[str, Observation]:
        indicators = self.db.query(Indicator).all()
        obs_map = {}
        for ind in indicators:
            latest = self.db.query(Observation).filter(
                Observation.indicator_id == ind.id
            ).order_by(Observation.timestamp.desc()).first()
            if latest:
                obs_map[ind.code] = latest
        return obs_map

    def close(self):
        if not self.db_provided:
            self.db.close()
