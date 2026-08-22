import sys
import datetime
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from packages.common.database import init_db, SessionLocal
from packages.common.models import (
    Source, Indicator, DerivedIndicator, Scenario, 
    TransmissionChannel, Alert, ResearchDocument
)

def seed_database():
    print("🌱 Initializing database schema...")
    init_db()
    db = SessionLocal()

    try:
        # 1. SOURCES
        print("🌱 Seeding official data sources...")
        sources_data = [
            {
                "name": "Federal Reserve Bank of St. Louis (FRED)",
                "provider": "FRED",
                "url": "https://fred.stlouisfed.org",
                "country": "USA",
                "frequency": "DAILY",
                "reliability_score": 0.99
            },
            {
                "name": "Banco Central de Chile (BCCh)",
                "provider": "BANCO_CENTRAL_CHILE",
                "url": "https://si3.bcentral.cl",
                "country": "CHL",
                "frequency": "DAILY",
                "reliability_score": 0.99
            },
            {
                "name": "Global Commodities & Financial Feeds",
                "provider": "FINANCIAL_COMMODITIES",
                "url": "https://finance.yahoo.com",
                "country": "GLOBAL",
                "frequency": "DAILY",
                "reliability_score": 0.98
            },
            {
                "name": "World Bank & OECD Open Data",
                "provider": "WORLD_BANK_OECD",
                "url": "https://data.worldbank.org",
                "country": "GLOBAL",
                "frequency": "MONTHLY",
                "reliability_score": 0.98
            },
            {
                "name": "Cochilco & INE Chile",
                "provider": "COCHILCO_INE",
                "url": "https://www.cochilco.cl",
                "country": "CHL",
                "frequency": "MONTHLY",
                "reliability_score": 0.97
            }
        ]

        source_map = {}
        for s_data in sources_data:
            existing = db.query(Source).filter_filter_by_provider = db.query(Source).filter(Source.provider == s_data["provider"]).first()
            if not existing:
                src = Source(**s_data)
                db.add(src)
                db.flush()
                source_map[s_data["provider"]] = src.id
            else:
                source_map[s_data["provider"]] = existing.id

        # 2. THE 30 MASTER INDICATORS
        print("🌱 Seeding the 30 master indicators...")
        indicators_data = [
            # A. Estados Unidos / Macro
            {
                "code": "US10Y",
                "name": "US 10-Year Treasury Constant Maturity Yield",
                "description": "Tasa de rendimiento del bono soberano de EE.UU. a 10 años. Referencia mundial de la tasa libre de riesgo y costo de capital.",
                "category": "MACRO_USA",
                "unit": "%",
                "frequency": "DAILY",
                "direction": -1,  # higher rate represents tighter financial conditions
                "provider": "FRED"
            },
            {
                "code": "US30Y",
                "name": "US 30-Year Treasury Constant Maturity Yield",
                "description": "Tasa del bono soberano de EE.UU. a 30 años. Refleja primas por plazo e inflación de largo plazo.",
                "category": "MACRO_USA",
                "unit": "%",
                "frequency": "DAILY",
                "direction": -1,
                "provider": "FRED"
            },
            {
                "code": "US2Y",
                "name": "US 2-Year Treasury Constant Maturity Yield",
                "description": "Tasa del bono del Tesoro a 2 años. Barómetro de expectativas de política monetaria de la Reserva Federal.",
                "category": "MACRO_USA",
                "unit": "%",
                "frequency": "DAILY",
                "direction": -1,
                "provider": "FRED"
            },
            {
                "code": "US_CPI",
                "name": "US Consumer Price Index YoY",
                "description": "Variación anual del Índice de Precios al Consumidor en Estados Unidos.",
                "category": "MACRO_USA",
                "unit": "%",
                "frequency": "MONTHLY",
                "direction": -1,
                "provider": "FRED"
            },
            {
                "code": "US_FED_RATE",
                "name": "Federal Funds Effective Rate",
                "description": "Tasa de interés de fondos federales establecida por la Reserva Federal.",
                "category": "MACRO_USA",
                "unit": "%",
                "frequency": "DAILY",
                "direction": -1,
                "provider": "FRED"
            },
            {
                "code": "US_FISCAL_DEFICIT",
                "name": "US Federal Surplus or Deficit (% of GDP)",
                "description": "Déficit fiscal del gobierno federal de EE.UU. como porcentaje del PIB.",
                "category": "MACRO_USA",
                "unit": "% PIB",
                "frequency": "QUARTERLY",
                "direction": -1,
                "provider": "FRED"
            },
            {
                "code": "US_DEBT",
                "name": "US Federal Debt as % of GDP",
                "description": "Deuda pública federal total de EE.UU. como porcentaje del PIB.",
                "category": "MACRO_USA",
                "unit": "% PIB",
                "frequency": "QUARTERLY",
                "direction": -1,
                "provider": "FRED"
            },

            # B. Sistema Monetario
            {
                "code": "DXY",
                "name": "US Dollar Index",
                "description": "Índice ponderado del dólar estadounidense frente a una canasta de monedas globales principales.",
                "category": "MONETARY",
                "unit": "Index",
                "frequency": "DAILY",
                "direction": -1,
                "provider": "FRED"
            },
            {
                "code": "USD_RESERVES_SHARE",
                "name": "Global FX Reserves in USD Share",
                "description": "Participación porcentual del dólar estadounidense en las reservas globales asignadas de bancos centrales.",
                "category": "MONETARY",
                "unit": "%",
                "frequency": "QUARTERLY",
                "direction": 1,
                "provider": "WORLD_BANK_OECD"
            },
            {
                "code": "FOREIGN_TREASURY_HOLDINGS",
                "name": "Foreign Holdings of US Treasuries",
                "description": "Tenencia total extranjera de bonos del Tesoro de EE.UU. (Trillones USD).",
                "category": "MONETARY",
                "unit": "Trillion USD",
                "frequency": "MONTHLY",
                "direction": 1,
                "provider": "FRED"
            },
            {
                "code": "CENTRAL_BANK_GOLD",
                "name": "Global Central Bank Net Gold Purchases",
                "description": "Compras netas de oro físico por bancos centrales globales como reserva estratégica.",
                "category": "MONETARY",
                "unit": "Tonnes",
                "frequency": "QUARTERLY",
                "direction": 1,
                "provider": "WORLD_BANK_OECD"
            },

            # C. Commodities
            {
                "code": "COPPER",
                "name": "Copper Futures (COMEX / LME)",
                "description": "Precio spot y futuros del cobre físico grado A. Principal producto de exportación chileno.",
                "category": "COMMODITIES",
                "unit": "USD/lb",
                "frequency": "DAILY",
                "direction": 1,
                "provider": "FINANCIAL_COMMODITIES"
            },
            {
                "code": "GOLD",
                "name": "Gold Spot Price",
                "description": "Precio internacional de la onza troy de oro fino.",
                "category": "COMMODITIES",
                "unit": "USD/oz",
                "frequency": "DAILY",
                "direction": 1,
                "provider": "FINANCIAL_COMMODITIES"
            },
            {
                "code": "OIL",
                "name": "Brent Crude Oil",
                "description": "Precio del barril de petróleo crudo Brent. Insumo importado clave para la matriz de costos chilena.",
                "category": "COMMODITIES",
                "unit": "USD/bbl",
                "frequency": "DAILY",
                "direction": -1,  # higher oil raises Chilean energy import costs
                "provider": "FINANCIAL_COMMODITIES"
            },
            {
                "code": "LITHIUM",
                "name": "Lithium Carbonate Battery Grade Spot",
                "description": "Precio de referencia internacional del carbonato de litio grado batería.",
                "category": "COMMODITIES",
                "unit": "USD/tonne",
                "frequency": "WEEKLY",
                "direction": 1,
                "provider": "FINANCIAL_COMMODITIES"
            },
            {
                "code": "IRON_ORE",
                "name": "Iron Ore 62% Fe CFR China",
                "description": "Precio del mineral de hierro con 62% de contenido metálico entregado en puertos de China.",
                "category": "COMMODITIES",
                "unit": "USD/dmt",
                "frequency": "DAILY",
                "direction": 1,
                "provider": "FINANCIAL_COMMODITIES"
            },

            # D. China / Demanda Mundial
            {
                "code": "CHINA_PMI",
                "name": "China NBS Manufacturing PMI",
                "description": "Índice de Gerentes de Compras del sector manufacturero chino (>50 indica expansión).",
                "category": "CHINA",
                "unit": "Index",
                "frequency": "MONTHLY",
                "direction": 1,
                "provider": "WORLD_BANK_OECD"
            },
            {
                "code": "CHINA_INDUSTRIAL_PRODUCTION",
                "name": "China Industrial Production YoY",
                "description": "Crecimiento anual de la producción industrial de la República Popular China.",
                "category": "CHINA",
                "unit": "%",
                "frequency": "MONTHLY",
                "direction": 1,
                "provider": "WORLD_BANK_OECD"
            },
            {
                "code": "CHINA_COPPER_IMPORTS",
                "name": "China Unwrought Copper Imports YoY",
                "description": "Variación porcentual anual del volumen de importaciones chinas de cobre en bruto.",
                "category": "CHINA",
                "unit": "%",
                "frequency": "MONTHLY",
                "direction": 1,
                "provider": "WORLD_BANK_OECD"
            },

            # E. Chile
            {
                "code": "CLP_USD",
                "name": "Tipo de Cambio Dólar Observado",
                "description": "Paridad peso chileno por dólar estadounidense informado oficialmente por el Banco Central de Chile.",
                "category": "CHILE",
                "unit": "CLP/USD",
                "frequency": "DAILY",
                "direction": -1,  # higher CLP/USD represents depreciation
                "provider": "BANCO_CENTRAL_CHILE"
            },
            {
                "code": "CHILE_TPM",
                "name": "Tasa de Política Monetaria (TPM Chile)",
                "description": "Tasa de interés de política monetaria fijada por el Consejo del Banco Central de Chile.",
                "category": "CHILE",
                "unit": "%",
                "frequency": "DAILY",
                "direction": -1,
                "provider": "BANCO_CENTRAL_CHILE"
            },
            {
                "code": "CHILE_CPI",
                "name": "IPC Chile Inflación Anual",
                "description": "Variación porcentual en 12 meses del Índice de Precios al Consumidor en Chile.",
                "category": "CHILE",
                "unit": "%",
                "frequency": "MONTHLY",
                "direction": -1,
                "provider": "BANCO_CENTRAL_CHILE"
            },
            {
                "code": "CHILE_IMACEC",
                "name": "IMACEC Variación Anual",
                "description": "Índice Mensual de Actividad Económica de Chile (variación en doce meses).",
                "category": "CHILE",
                "unit": "%",
                "frequency": "MONTHLY",
                "direction": 1,
                "provider": "BANCO_CENTRAL_CHILE"
            },
            {
                "code": "CHILE_GDP",
                "name": "PIB Real de Chile YoY",
                "description": "Crecimiento anual del Producto Interno Bruto real de Chile.",
                "category": "CHILE",
                "unit": "%",
                "frequency": "QUARTERLY",
                "direction": 1,
                "provider": "BANCO_CENTRAL_CHILE"
            },
            {
                "code": "CHILE_FISCAL_BALANCE",
                "name": "Balance Fiscal Efectivo de Chile (% PIB)",
                "description": "Resultado presupuestario del Gobierno Central de Chile como porcentaje del PIB.",
                "category": "CHILE",
                "unit": "% PIB",
                "frequency": "QUARTERLY",
                "direction": 1,
                "provider": "BANCO_CENTRAL_CHILE"
            },

            # F. Minería
            {
                "code": "CHILE_COPPER_PRODUCTION",
                "name": "Producción Nacional de Cobre Mina",
                "description": "Producción mensual de cobre mina en Chile (Miles de Toneladas Métricas de Cobre Fino).",
                "category": "MINING",
                "unit": "kMTF",
                "frequency": "MONTHLY",
                "direction": 1,
                "provider": "COCHILCO_INE"
            },
            {
                "code": "CHILE_MINING_CAPEX",
                "name": "Catastro de Inversión Minera Chile",
                "description": "Cartera de proyectos de inversión minera evaluados por Cochilco a 10 años (Miles de millones USD).",
                "category": "MINING",
                "unit": "Billion USD",
                "frequency": "ANNUAL",
                "direction": 1,
                "provider": "COCHILCO_INE"
            },
            {
                "code": "CHILE_COPPER_EXPORTS",
                "name": "Exportaciones de Cobre Valor FOB",
                "description": "Monto total mensual exportado de cobre chileno en millones de dólares FOB.",
                "category": "MINING",
                "unit": "Million USD",
                "frequency": "MONTHLY",
                "direction": 1,
                "provider": "BANCO_CENTRAL_CHILE"
            },

            # G. Energía / Tecnología
            {
                "code": "CHILE_ELECTRICITY_DEMAND",
                "name": "Generación y Demanda Bruta SEN Chile",
                "description": "Generación mensual total de energía eléctrica en el Sistema Eléctrico Nacional (GWh).",
                "category": "ENERGY_TECH",
                "unit": "GWh",
                "frequency": "MONTHLY",
                "direction": 1,
                "provider": "COCHILCO_INE"
            },
            {
                "code": "AI_DATA_CENTER_CAPEX_PROXY",
                "name": "Global AI Infrastructure & Data Center CAPEX Growth",
                "description": "Crecimiento anual promedio del gasto de capital de los principales hyperscalers en infraestructura de cómputo e IA.",
                "category": "ENERGY_TECH",
                "unit": "% YoY",
                "frequency": "QUARTERLY",
                "direction": 1,
                "provider": "FINANCIAL_COMMODITIES"
            }
        ]

        for ind_data in indicators_data:
            provider = ind_data.pop("provider")
            source_id = source_map.get(provider)
            existing = db.query(Indicator).filter(Indicator.code == ind_data["code"]).first()
            if not existing:
                ind = Indicator(**ind_data, source_id=source_id)
                db.add(ind)
        db.flush()

        # 3. DERIVED INDICATORS
        print("🌱 Seeding derived indicators definitions...")
        derived_data = [
            {
                "code": "YIELD_SPREAD_10Y_2Y",
                "name": "US Yield Curve Spread 10Y - 2Y",
                "formula": "US10Y - US2Y",
                "description": "Diferencial de tasas soberanas 10Y vs 2Y. Valores negativos indican curva invertida.",
                "category": "MONETARY"
            },
            {
                "code": "US_REAL_RATE_10Y",
                "name": "US 10Y Real Rate Proxy",
                "formula": "US10Y - US_CPI",
                "description": "Rendimiento real del bono a 10 años descontada la inflación YoY.",
                "category": "MACRO_USA"
            },
            {
                "code": "GOLD_COPPER_RATIO",
                "name": "Gold / Copper Valuation Ratio",
                "formula": "GOLD / (COPPER * 100)",
                "description": "Ratio de aversión al riesgo sistémico vs actividad industrial.",
                "category": "COMMODITIES"
            },
            {
                "code": "COPPER_OIL_RATIO",
                "name": "Copper / Oil Terms of Trade Ratio",
                "formula": "COPPER / OIL",
                "description": "Términos de intercambio relativos entre exportación clave de Chile (cobre) e importación clave (petróleo).",
                "category": "COMMODITIES"
            }
        ]

        for d_data in derived_data:
            existing = db.query(DerivedIndicator).filter(DerivedIndicator.code == d_data["code"]).first()
            if not existing:
                db.add(DerivedIndicator(**d_data))
        db.flush()

        # 4. SCENARIOS
        print("🌱 Seeding canonical macro scenarios...")
        scenarios_data = [
            {
                "scenario_code": "S1_SOFT_LANDING",
                "name": "S1 — Soft Landing (Aterrizaje Suave)",
                "description": "Desaceleración ordenada en EE.UU. con inflación convergiendo a meta sin recesión. Recortes paulatinos de tasas de la Fed y liquidez global estable.",
                "probability": 0.35,
                "probability_type": "MODEL_ESTIMATE",
                "drivers": ["Desinflación en servicios en EE.UU.", "Mercado laboral equilibrado", "Crecimiento chino moderado"],
                "supporting_indicators": ["US_CPI < 3.0%", "CHINA_PMI > 50.0", "US10Y estable entre 3.8% y 4.3%"],
                "contradicting_indicators": ["DXY > 107", "Yield curve steepening desordenado"],
                "expected_chile_effect": "Condiciones financieras externas favorables, apreciación moderada del CLP hacia rango $900-$930, Banco Central de Chile con holgura para normalizar TPM.",
                "risk_level": "LOW",
                "opportunity_level": "MODERATE",
                "methodology_version": "v0.1"
            },
            {
                "scenario_code": "S2_FISCAL_DOMINANCE",
                "name": "S2 — Fiscal Dominance (Dominancia Fiscal)",
                "description": "Presión estructural por déficit y deuda pública en EE.UU. obliga a mantener tasas de largo plazo elevadas. Apreciación del oro como refugio monetario y desdolarización marginal.",
                "probability": 0.30,
                "probability_type": "MODEL_ESTIMATE",
                "drivers": ["Déficit fiscal US > 6% del PIB", "Emisión masiva de Treasuries", "Compras récord de oro por bancos centrales"],
                "supporting_indicators": ["US30Y > 4.75%", "GOLD > $2,400/oz", "US_DEBT > 120% PIB"],
                "contradicting_indicators": ["Consolidación fiscal en Washington", "Colapso del precio del oro"],
                "expected_chile_effect": "Costo de capital de largo plazo elevado para proyectos mineros y de infraestructura; no obstante, el alto precio del oro y metales mitiga el impacto fiscal en Chile.",
                "risk_level": "HIGH",
                "opportunity_level": "MODERATE",
                "methodology_version": "v0.1"
            },
            {
                "scenario_code": "S3_GLOBAL_RECESSION",
                "name": "S3 — Global Recession (Recesión Global)",
                "description": "Contracción económica sincronizada en mercados desarrollados y severo freno manufacturero en China. Caída abrupta en demanda y precios de commodities.",
                "probability": 0.15,
                "probability_type": "MODEL_ESTIMATE",
                "drivers": ["Agotamiento del consumo en EE.UU.", "Crisis inmobiliaria e industrial en China", "Tensión geopolítica global"],
                "supporting_indicators": ["CHINA_PMI < 48.0", "COPPER < $3.80/lb", "Spread 10Y-2Y con fuerte desinversión por recortes de pánico"],
                "contradicting_indicators": ["COPPER > $4.50/lb", "Exportaciones chilenas en máximos"],
                "expected_chile_effect": "Caída drástica de ingresos fiscales por menor cobre y royalty, fuerte depreciación del CLP sobre $1.000, contracción en IMACEC minero.",
                "risk_level": "CRITICAL",
                "opportunity_level": "LOW",
                "methodology_version": "v0.1"
            },
            {
                "scenario_code": "S4_COMMODITY_SUPERCYCLE",
                "name": "S4 — Commodity Supercycle (Superciclo de Electrificación e IA)",
                "description": "La demanda estructural por cobre, litio y conductores para la electrificación global y datacenters de IA sobrepasa la oferta global, manteniendo precios altos sostenidos.",
                "probability": 0.20,
                "probability_type": "MODEL_ESTIMATE",
                "drivers": ["Inversión masiva en centros de datos de IA y red eléctrica", "Transición a energías renovables", "Escasez de nuevos yacimientos de cobre de alta ley"],
                "supporting_indicators": ["COPPER > $4.60/lb", "AI_DATA_CENTER_CAPEX_PROXY > +25% YoY", "Inventarios LME en mínimos"],
                "contradicting_indicators": ["Sustitución masiva de cobre", "Paralización de proyectos de datacenters"],
                "expected_chile_effect": "Superávit récord en balanza comercial, auge de inversiones mineras (CAPEX > USD 65B), fuerte recaudación tributaria y revalorización del CLP.",
                "risk_level": "MODERATE",
                "opportunity_level": "TRANSFORMATIVE",
                "methodology_version": "v0.1"
            }
        ]

        for sc_data in scenarios_data:
            existing = db.query(Scenario).filter(Scenario.scenario_code == sc_data["scenario_code"]).first()
            if not existing:
                db.add(Scenario(**sc_data))
        db.flush()

        # 5. TRANSMISSION CHANNELS
        print("🌱 Seeding Chile transmission channels...")
        channels_data = [
            {
                "channel_name": "Tasas Externas → Tipo de Cambio → Inflación Chile",
                "global_indicator_code": "US10Y",
                "chile_indicator_code": "CLP_USD",
                "transmission_speed": "IMMEDIATE_1D",
                "elasticity": 0.45,
                "description": "Un aumento de 50 pb en el US10Y tiende a generar una depreciación de 2.5% a 4% en el tipo de cambio CLP/USD en el corto plazo por arbitraje de tasas y salida de capitales.",
                "current_impact_score": -18.5
            },
            {
                "channel_name": "Precio del Cobre → Ingresos Fiscales & Royalty",
                "global_indicator_code": "COPPER",
                "chile_indicator_code": "CHILE_FISCAL_BALANCE",
                "transmission_speed": "MEDIUM_TERM_1Q",
                "elasticity": 0.75,
                "description": "Cada aumento de 10 centavos de dólar/lb en el precio promedio anual del cobre aporta aproximadamente USD 250M-300M adicionales en recaudación fiscal directa a la Tesorería.",
                "current_impact_score": 38.0
            },
            {
                "channel_name": "Demanda China → Exportaciones Mineras Chilenas",
                "global_indicator_code": "CHINA_PMI",
                "chile_indicator_code": "CHILE_COPPER_EXPORTS",
                "transmission_speed": "SHORT_TERM_1M",
                "elasticity": 0.60,
                "description": "China absorbe más del 50% del concentrado y cátodos de cobre de Chile. Un PMI > 50 tracciona despachos y órdenes de compra con embarque directo en puertos chilenos.",
                "current_impact_score": 22.0
            },
            {
                "channel_name": "Inversión en IA / Datacenters → Demanda Energética SEN",
                "global_indicator_code": "AI_DATA_CENTER_CAPEX_PROXY",
                "chile_indicator_code": "CHILE_ELECTRICITY_DEMAND",
                "transmission_speed": "STRUCTURAL_1Y",
                "elasticity": 0.35,
                "description": "La expansión de datacenters en la Región Metropolitana y centros industriales en el norte genera contratos PPA de largo plazo y requerimientos de expansión de transmisión eléctrica.",
                "current_impact_score": 15.0
            }
        ]

        for ch_data in channels_data:
            existing = db.query(TransmissionChannel).filter(TransmissionChannel.channel_name == ch_data["channel_name"]).first()
            if not existing:
                db.add(TransmissionChannel(**ch_data))
        db.flush()

        # 6. INITIAL ALERTS
        print("🌱 Seeding active and watch alerts...")
        alerts_data = [
            {
                "severity": "WATCH",
                "title": "Yield Curve Spread 10Y-2Y en Proceso de Desinversión",
                "description": "El diferencial de la curva soberana de EE.UU. ha salido de terreno negativo profundo, lo que históricamente antecede giros en la política de la Fed.",
                "trigger_value": 0.0,
                "current_value": 0.15,
                "status": "ACTIVE"
            },
            {
                "severity": "INFO",
                "title": "Precio del Cobre Consolidando sobre $4.30/lb",
                "description": "La cotización internacional del cobre muestra soporte sólido impulsada por bajos inventarios de refinerías y expectativas de demanda en transición energética.",
                "trigger_value": 4.20,
                "current_value": 4.38,
                "status": "ACTIVE"
            },
            {
                "severity": "WARNING",
                "title": "DXY Sobre Nivel de Resistencia 104.5",
                "description": "La fortaleza del dólar global incrementa la presión cambiaria sobre monedas emergentes de la región, afectando las proyecciones de importación de combustibles.",
                "trigger_value": 104.5,
                "current_value": 104.8,
                "status": "ACTIVE"
            }
        ]

        for al_data in alerts_data:
            existing = db.query(Alert).filter(Alert.title == al_data["title"]).first()
            if not existing:
                db.add(Alert(**al_data))
        db.flush()

        # 7. RESEARCH DOCUMENTS
        print("🌱 Seeding baseline research documents...")
        docs_data = [
            {
                "title": "Informe de Política Monetaria (IPoM) — Banco Central de Chile",
                "source": "Banco Central de Chile",
                "url": "https://www.bcentral.cl/publicaciones/ipom",
                "published_at": datetime.datetime(2026, 6, 15),
                "category": "MACRO_CHILE",
                "summary": "Análisis trimestral de la evolución macroeconómica, balance de riesgos de inflación y trayectoria proyectada de la Tasa de Política Monetaria.",
                "relevance": 0.98
            },
            {
                "title": "Tendencias del Mercado Internacional del Cobre — Cochilco",
                "source": "Comisión Chilena del Cobre",
                "url": "https://www.cochilco.cl/informes",
                "published_at": datetime.datetime(2026, 7, 1),
                "category": "MINING_COMMODITIES",
                "summary": "Proyecciones de balance de oferta y demanda mundial de cobre, demanda asociada a electromovilidad, inteligencia artificial e infraestructura.",
                "relevance": 0.96
            },
            {
                "title": "IMF Global Financial Stability Report: Monetary Transmission and Sovereign Fragilities",
                "source": "Fondo Monetario Internacional",
                "url": "https://www.imf.org/en/Publications/GFSR",
                "published_at": datetime.datetime(2026, 4, 20),
                "category": "GLOBAL_MONETARY",
                "summary": "Evaluación del impacto del costo de la deuda soberana en economías avanzadas sobre los flujos de capital hacia mercados emergentes.",
                "relevance": 0.94
            }
        ]

        for r_doc in docs_data:
            existing = db.query(ResearchDocument).filter(ResearchDocument.title == r_doc["title"]).first()
            if not existing:
                db.add(ResearchDocument(**r_doc))

        db.commit()
        print("✅ Database successfully seeded with sources, indicators, scenarios, channels, alerts and research documents!")

    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
