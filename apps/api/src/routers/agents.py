from typing import Optional
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from packages.agents.chief_economist import ChiefEconomistAgent
from packages.agents.stress_testing import StressTestingAgent
from apps.api.src.dependencies import get_db

router = APIRouter(prefix="/api/v1/agents", tags=["AI Agents & Simulation"])

class AgentQueryRequest(BaseModel):
    question: str = Field(..., description="Pregunta económica o de coyuntura para el Economista Jefe")

class ShockSimulationRequest(BaseModel):
    copper_price: float = Field(..., description="Precio del Cobre simulado en USD/lb (ej. 3.60 o 5.20)")
    us10y_yield: float = Field(..., description="Rendimiento del Bono del Tesoro US10Y simulado en % (ej. 5.50 o 3.50)")
    oil_price: Optional[float] = Field(78.0, description="Precio del Petróleo Brent en USD/bbl")
    china_pmi: Optional[float] = Field(50.5, description="PMI Manufacturero de China (Index)")
    dxy_index: Optional[float] = Field(104.5, description="Índice Dólar DXY")

@router.get("/briefing")
def get_executive_briefing(db: Session = Depends(get_db)):
    """Generate or retrieve a full Chief Economist executive briefing based on verified database state."""
    agent = ChiefEconomistAgent(db=db)
    return agent.generate_executive_briefing()

@router.post("/query")
def query_chief_economist(req: AgentQueryRequest, db: Session = Depends(get_db)):
    """Ask an analytical question to the Chief Economist Agent grounded in the current quantitative database."""
    agent = ChiefEconomistAgent(db=db)
    return agent.answer_macro_question(question=req.question)

@router.post("/simulate-shock")
def simulate_macro_shock(req: ShockSimulationRequest, db: Session = Depends(get_db)):
    """Simulate a macroeconomic shock and model projected impacts on Chile's scores, exchange rate, and fiscal revenue."""
    agent = StressTestingAgent(db=db)
    return agent.simulate_shock(
        copper_price=req.copper_price,
        us10y_yield=req.us10y_yield,
        oil_price=req.oil_price or 78.0,
        china_pmi=req.china_pmi or 50.5,
        dxy_index=req.dxy_index or 104.5
    )
