import time
import datetime
import logging
from packages.common.database import SessionLocal, init_db
from packages.data.pipeline import IngestionPipeline

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("worker.ingestion")

def run_ingestion_job():
    logger.info("🕒 Ingestion Worker waking up for daily collection...")
    init_db()
    db = SessionLocal()
    try:
        pipeline = IngestionPipeline(db=db)
        runs = pipeline.run_all(days_back=7)
        total_inserted = sum(r.records_inserted for r in runs)
        logger.info(f"✅ Ingestion Worker completed. Inserted: {total_inserted} records.")
    except Exception as e:
        logger.error(f"❌ Ingestion Worker failed: {e}", exc_info=True)
    finally:
        db.close()

if __name__ == "__main__":
    run_ingestion_job()
