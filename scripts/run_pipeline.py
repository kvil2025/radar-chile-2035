import sys
import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from packages.common.database import init_db, SessionLocal
from packages.data.pipeline import IngestionPipeline
from packages.indicators.derived_engine import DerivedIndicatorsEngine
from packages.scoring.engine import ScoringEngine
from packages.scenarios.regimes import EconomicRegimeClassifier
from packages.scenarios.scenario_engine import ScenarioEngine
from packages.scenarios.chile_impact import ChileImpactEngine
from packages.scenarios.alerts import AlertEngine

def run_full_pipeline():
    print("=" * 70)
    print("🚀 RADAR CHILE 2035 — Full Quantitative Intelligence Pipeline")
    print(f"⏰ Execution Timestamp: {datetime.datetime.utcnow().isoformat()} UTC")
    print("=" * 70)

    init_db()
    db = SessionLocal()

    try:
        # STEP 1: Ingestion
        print("\n📥 STEP 1: Ingestion from Official Connectors...")
        ingestion = IngestionPipeline(db=db)
        runs = ingestion.run_all(days_back=60)
        for r in runs:
            print(f"   • {r.source_name:25} | Received: {r.records_received:3} | Inserted: {r.records_inserted:3} | Status: {r.status}")

        # STEP 2: Derived Indicators & Signals
        print("\n⚡ STEP 2: Derived Indicators & Quantitative Signals...")
        derived = DerivedIndicatorsEngine(db=db)
        derived_res = derived.run()
        print(f"   • Derived Calculations: {derived_res['derived_calculated']} | Signals Generated: {derived_res['signals_generated']}")

        # STEP 3: Scoring Engine (v0.1)
        print("\n🎯 STEP 3: Quantitative Scoring Engine (Methodology v0.1)...")
        scoring = ScoringEngine(db=db)
        scores_res = scoring.run_all()
        for stype, sval in scores_res.items():
            print(f"   • {stype:25} : {sval:5.1f} / 100")

        # STEP 4: Regime Classification
        print("\n🧭 STEP 4: Global Economic Regime Classifier...")
        classifier = EconomicRegimeClassifier(db=db)
        regime_res = classifier.classify()
        print(f"   • Regime: {regime_res['regime_code']} (Confidence: {int(regime_res['confidence']*100)}%)")
        print(f"   • Rationale: {regime_res['rationale']}")

        # STEP 5: Scenarios S1-S4
        print("\n🔮 STEP 5: Macro Scenarios S1-S4...")
        sc_engine = ScenarioEngine(db=db)
        scenarios = sc_engine.evaluate_scenarios()
        for sc in scenarios:
            print(f"   • {sc['scenario_code']:25} | Prob: {sc['probability']*100:4.1f}% ({sc['probability_type']}) | Risk: {sc['risk_level']}")

        # STEP 6: Chile Transmission Channels
        print("\n🇨🇱 STEP 6: Chile Transmission Impact Engine...")
        chile_engine = ChileImpactEngine(db=db)
        chile_res = chile_engine.evaluate_channels()
        print(f"   • Net Opportunity Score: {chile_res['net_opportunity_score']}")
        print(f"   • Primary Positive Channel: {chile_res['primary_positive_channel']}")
        print(f"   • Primary Risk Channel: {chile_res['primary_risk_channel']}")

        # STEP 7: Alert Evaluation
        print("\n🚨 STEP 7: Alert Engine Evaluation...")
        alert_engine = AlertEngine(db=db)
        alerts = alert_engine.evaluate_alerts()
        print(f"   • Active Alerts Triggered: {len(alerts)}")
        for a in alerts:
            print(f"     [{a['severity']}] {a['title']} (Val: {a['current_value']})")

        print("\n" + "=" * 70)
        print("✅ Pipeline run completed successfully with complete data traceability!")
        print("=" * 70)

    except Exception as e:
        print(f"❌ Error during pipeline execution: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    run_full_pipeline()
