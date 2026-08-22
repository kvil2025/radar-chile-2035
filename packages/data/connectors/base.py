import abc
import logging
import datetime
from dataclasses import dataclass, field
from typing import Optional, Any
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logger = logging.getLogger(__name__)

@dataclass
class RawObservation:
    indicator_code: str
    timestamp: datetime.datetime
    value: float
    original_value: Optional[float] = None
    original_unit: Optional[str] = None
    source_timestamp: Optional[datetime.datetime] = None
    quality_status: str = "VALID"
    metadata: dict[str, Any] = field(default_factory=dict)

class BaseConnector(abc.ABC):
    """
    Abstract base class for official economic and financial data connectors.
    Provides standard retry logic, timeout handling, and raw observation generation.
    """

    def __init__(self, provider_name: str, base_url: str = "", timeout: float = 15.0):
        self.provider_name = provider_name
        self.base_url = base_url
        self.timeout = timeout
        self.client = httpx.Client(timeout=timeout, headers={"User-Agent": "RadarChile2035/1.0"})

    @retry(
        reraise=True,
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.RequestError, httpx.HTTPStatusError))
    )
    def fetch_url(self, url: str, params: Optional[dict] = None, headers: Optional[dict] = None) -> httpx.Response:
        """Fetch remote HTTP endpoint with automatic retries and exponential backoff."""
        logger.info(f"[{self.provider_name}] Fetching {url}")
        res = self.client.get(url, params=params, headers=headers)
        res.raise_for_status()
        return res

    @abc.abstractmethod
    def fetch_observations(
        self, 
        indicator_codes: Optional[list[str]] = None,
        start_date: Optional[datetime.date] = None,
        end_date: Optional[datetime.date] = None
    ) -> list[RawObservation]:
        """Fetch and parse series of observations for given indicators."""
        pass

    def close(self):
        self.client.close()
