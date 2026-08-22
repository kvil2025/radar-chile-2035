import logging
from packages.common.database import SessionLocal
from packages.scenarios.alerts import AlertEngine

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("worker.alerts")

def run_alert_evaluation_job():
    logger.info("🚨 Alert Evaluator checking active threshold triggers...")
    db = SessionLocal()
    try:
        engine = AlertEngine(db=db)
        alerts = engine.evaluate_alerts()
        logger.info(f"✅ Alert Evaluator completed: {len(alerts)} alerts triggered.")
    except Exception as e:
        logger.error(f"❌ Alert Evaluator failed: {e}", exc_info=True)
    finally:
        db.close()

if __name__ == "__main__":
    run_alert_evaluation_job()
