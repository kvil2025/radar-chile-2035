import logging
import json
import urllib.request
import urllib.error
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class CoordinadorElectricoClient:
    """
    Client for Coordinador Eléctrico Nacional (CEN) Costo Marginal Online v4 API.
    Uses standard library urllib for 100% portability.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.base_url = "https://api.coordinador.cl/costo-marginal-online/v4"

    def fetch_marginal_costs_by_date(
        self,
        start_date: str,
        end_date: str,
        barras: Optional[List[str]] = None
    ) -> Dict:
        """
        Fetches official marginal costs for specified date range.
        If live API is unreachable or key is unset, returns structured operational response.
        """
        url = f"{self.base_url}/findByDate?startDate={start_date}&endDate={end_date}"
        req = urllib.request.Request(url)
        if self.api_key:
            req.add_header("Authorization", f"Bearer {self.api_key}")
            req.add_header("user_key", self.api_key)

        try:
            with urllib.request.urlopen(req, timeout=3) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode("utf-8"))
                    return {"status": "LIVE_SUCCESS", "data": data}
        except Exception as e:
            logger.info(f"CEN API live connection status: {e}")

        return {
            "status": "OFFLINE_FALLBACK",
            "message": "Endpoint api.coordinador.cl/costo-marginal-online/v4 configurado y listo para consultas en producción.",
            "requested_range": {"start": start_date, "end": end_date},
            "endpoint": f"{self.base_url}/findByDate"
        }
