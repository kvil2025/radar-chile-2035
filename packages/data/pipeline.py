import datetime
import logging
from typing import Optional
from sqlalchemy.orm import Session
from packages.common.database import SessionLocal, init_db
from packages.common.models import Indicator, Observation, IngestionRun
from packages.data.quality.validator import DataQualityValidator
from packages.data.connectors.fred import FREDConnector
from packages.data.connectors.banco_central import BancoCentralChileConnector
from packages.data.connectors.commodities import CommoditiesConnector
from packages.data.connectors.world_bank import WorldBankOECDConnector
from packages.data.connectors.chile_sectorial import ChileSectorialConnector

logger = logging.getLogger(__name__)

class IngestionPipeline:
    """
    Orchestrates the ingestion, validation, and storage of macroeconomic,
    financial and commodity observations across all official data providers.
    """

    def __init__(self, db: Optional[Session] = None):
        self.db_provided = db is not None
        self.db = db if db is not None else SessionLocal()
        self.connectors = [
            FREDConnector(),
            BancoCentralChileConnector(),
            CommoditiesConnector(),
            WorldBankOECDConnector(),
            ChileSectorialConnector()
        ]

    def run_all(self, days_back: int = 90) -> list[IngestionRun]:
        """Run ingestion pipeline across all configured connectors."""
        start_date = datetime.date.today() - datetime.timedelta(days=days_back)
        end_date = datetime.date.today()
        
        runs: list[IngestionRun] = []
        for connector in self.connectors:
            run = self.run_connector(connector, start_date=start_date, end_date=end_date)
            runs.append(run)

        return runs

    def run_connector(
        self, 
        connector, 
        start_date: Optional[datetime.date] = None, 
        end_date: Optional[datetime.date] = None
    ) -> IngestionRun:
        started_at = datetime.datetime.utcnow()
        provider_name = connector.provider_name
        logger.info(f"🚀 Starting ingestion run for provider: {provider_name}")

        ingestion_run = IngestionRun(
            source_name=provider_name,
            started_at=started_at,
            status="RUNNING"
        )
        self.db.add(ingestion_run)
        self.db.commit()
        self.db.refresh(ingestion_run)

        records_received = 0
        records_inserted = 0
        records_rejected = 0
        errors: list[str] = []

        try:
            raw_observations = connector.fetch_observations(start_date=start_date, end_date=end_date)
            records_received = len(raw_observations)

            # Pre-fetch all indicators for quick ID lookup
            indicator_map = {ind.code: ind for ind in self.db.query(Indicator).all()}

            for raw_obs in raw_observations:
                indicator = indicator_map.get(raw_obs.indicator_code)
                if not indicator:
                    errors.append(f"Indicator code '{raw_obs.indicator_code}' not found in database registry.")
                    records_rejected += 1
                    continue

                # Run Data Quality Validation
                val_res = DataQualityValidator.validate_observation(
                    indicator_code=raw_obs.indicator_code,
                    value=raw_obs.value,
                    timestamp=raw_obs.timestamp
                )

                if not val_res.is_valid and val_res.quality_status == "INVALID":
                    records_rejected += 1
                    errors.append(f"Rejected invalid value for {raw_obs.indicator_code} at {raw_obs.timestamp}: {val_res.reasons}")
                    continue

                # Check if observation already exists (idempotency)
                existing_obs = self.db.query(Observation).filter(
                    Observation.indicator_id == indicator.id,
                    Observation.timestamp == raw_obs.timestamp
                ).first()

                if existing_obs:
                    # Update if changed
                    existing_obs.value = raw_obs.value
                    existing_obs.quality_status = val_res.quality_status
                    existing_obs.metadata_json = raw_obs.metadata
                    records_inserted += 1
                else:
                    new_obs = Observation(
                        indicator_id=indicator.id,
                        timestamp=raw_obs.timestamp,
                        value=raw_obs.value,
                        original_value=raw_obs.original_value,
                        original_unit=raw_obs.original_unit,
                        quality_status=val_res.quality_status,
                        source_timestamp=raw_obs.source_timestamp,
                        ingested_at=datetime.datetime.utcnow(),
                        metadata_json=raw_obs.metadata
                    )
                    self.db.add(new_obs)
                    records_inserted += 1

            self.db.commit()
            status = "SUCCESS" if len(errors) == 0 else "PARTIAL"

        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Ingestion pipeline failed for {provider_name}: {e}", exc_info=True)
            status = "FAILED"
            errors.append(str(e))

        finished_at = datetime.datetime.utcnow()
        duration = (finished_at - started_at).total_seconds()

        ingestion_run.finished_at = finished_at
        ingestion_run.duration_seconds = duration
        ingestion_run.records_received = records_received
        ingestion_run.records_inserted = records_inserted
        ingestion_run.records_rejected = records_rejected
        ingestion_run.errors = errors if errors else None
        ingestion_run.status = status

        self.db.commit()
        self.db.refresh(ingestion_run)

        logger.info(
            f"🏁 Completed ingestion for {provider_name}: received={records_received}, "
            f"inserted={records_inserted}, rejected={records_rejected}, duration={duration:.2f}s, status={status}"
        )
        return ingestion_run

    def close(self):
        if not self.db_provided:
            self.db.close()
        for connector in self.connectors:
            connector.close()
