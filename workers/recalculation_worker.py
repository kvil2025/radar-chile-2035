import logging
from packages.common.database import SessionLocal
from packages.indicators.derived_engine import DerivedIndicatorsEngine
from packages.scoring.engine import ScoringEngine
from packages.scenarios.regimes import EconomicRegimeClassifier
from packages.scenarios.scenario_engine import ScenarioEngine
from packages.scenarios.chile_impact import ChileImpactEngine

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("worker.recalculation")

def run_recalculation_job():
    logger.info("⚡ Recalculation Worker updating all derived layers...")
    db = SessionLocal()
    try:
        DerivedIndicatorsEngine(db=db).run()
        ScoringEngine(db=db).run_all()
        EconomicRegimeClassifier(db=db).classify()
        ScenarioEngine(db=db).evaluate_scenarios()
        ChileImpactEngine(db=db).evaluate_channels()
        logger.info("✅ Recalculation Worker completed all analytics and scoring updates.")
    except Exception as e:
        logger.error(f"❌ Recalculation Worker failed: {e}", exc_info=True)
    finally:
        db.close()

if __name__ == "__main__":
    run_recalculation_job()
