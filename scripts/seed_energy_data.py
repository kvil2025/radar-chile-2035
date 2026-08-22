import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import datetime
import random
import logging
from packages.common.database import SessionLocal, init_db
from packages.common.models import (
    Substation, Bus, TransmissionLine, GenerationPlant, BessUnit,
    ProjectPipeline, NodePrice, CongestionEvent, GenerationHourly,
    DemandHourly, FuelPrice, HydroBasin, NodeOpportunityScore
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Official Substation & Bus Catalog of the Chilean SEN
SUBSTATIONS_DATA = [
    # Norte Grande
    {"code": "SUB_CRUCERO", "name": "Crucero", "lat": -22.2425, "lon": -69.1350, "voltages": "220/110 kV", "cap": 1200, "operator": "Transelec"},
    {"code": "SUB_KIMAL", "name": "Kimal", "lat": -22.9510, "lon": -69.2150, "voltages": "500/220 kV", "cap": 3000, "operator": "Conexión Kimal-Lo Aguirre"},
    {"code": "SUB_ENCUENTRO", "name": "Encuentro", "lat": -22.1850, "lon": -69.3120, "voltages": "220 kV", "cap": 800, "operator": "Transelec"},
    {"code": "SUB_LABERINTO", "name": "Laberinto", "lat": -23.3510, "lon": -69.5800, "voltages": "220 kV", "cap": 600, "operator": "Transelec"},
    {"code": "SUB_ATACAMA", "name": "Atacama", "lat": -23.1100, "lon": -70.4500, "voltages": "220 kV", "cap": 1000, "operator": "Engie Energía Chile"},
    {"code": "SUB_KAPATUR", "name": "Kapatur", "lat": -22.4500, "lon": -69.7500, "voltages": "220 kV", "cap": 500, "operator": "Transelec"},
    {"code": "SUB_O_HIGGINS", "name": "O'Higgins", "lat": -23.8500, "lon": -69.8500, "voltages": "220 kV", "cap": 750, "operator": "Transelec"},
    
    # Norte Chico
    {"code": "SUB_CARDONES", "name": "Cardones", "lat": -27.3910, "lon": -70.3680, "voltages": "500/220 kV", "cap": 2500, "operator": "Transelec"},
    {"code": "SUB_MAITENCILLO", "name": "Maitencillo", "lat": -28.6120, "lon": -70.8250, "voltages": "500/220 kV", "cap": 2000, "operator": "Transelec"},
    {"code": "SUB_PAN_AZUCAR", "name": "Pan de Azúcar", "lat": -29.9850, "lon": -71.2650, "voltages": "500/220 kV", "cap": 1800, "operator": "Transelec"},
    {"code": "SUB_PUNTA_COLORADA", "name": "Punta Colorada", "lat": -29.3500, "lon": -71.1800, "voltages": "220 kV", "cap": 600, "operator": "Transelec"},
    
    # Centro
    {"code": "SUB_POLPAICO", "name": "Polpaico", "lat": -33.1550, "lon": -70.8850, "voltages": "500/220 kV", "cap": 3000, "operator": "Transelec"},
    {"code": "SUB_LO_AGUIRRE", "name": "Lo Aguirre", "lat": -33.4680, "lon": -70.8520, "voltages": "500/220 kV", "cap": 3500, "operator": "Transelec"},
    {"code": "SUB_CERRO_NAVIA", "name": "Cerro Navia", "lat": -33.4210, "lon": -70.7450, "voltages": "220/110 kV", "cap": 1500, "operator": "Transelec"},
    {"code": "SUB_ALTO_JAHUEL", "name": "Alto Jahuel", "lat": -33.6820, "lon": -70.6750, "voltages": "500/220 kV", "cap": 2800, "operator": "Transelec"},
    {"code": "SUB_ANCOA", "name": "Ancoa", "lat": -35.8550, "lon": -71.4500, "voltages": "500/220 kV", "cap": 2200, "operator": "Transelec"},
    {"code": "SUB_QUILLOTA", "name": "Quillota", "lat": -32.8800, "lon": -71.2400, "voltages": "220 kV", "cap": 1200, "operator": "Chilquinta"},
    
    # Sur
    {"code": "SUB_CHARRUA", "name": "Charrúa", "lat": -37.0520, "lon": -72.2850, "voltages": "500/220 kV", "cap": 2600, "operator": "Transelec"},
    {"code": "SUB_CONCEPCION", "name": "Concepción", "lat": -36.8200, "lon": -73.0400, "voltages": "220/66 kV", "cap": 1100, "operator": "Transelec"},
    {"code": "SUB_TEMUCO", "name": "Temuco", "lat": -38.7400, "lon": -72.6100, "voltages": "220/66 kV", "cap": 800, "operator": "Transelec"},
    {"code": "SUB_PUERTO_MONTT", "name": "Puerto Montt", "lat": -41.4650, "lon": -72.9400, "voltages": "220/110 kV", "cap": 700, "operator": "Transelec"}
]

BUSES_DATA = [
    # Norte Grande (Atacama / Antofagasta)
    {"code": "CRUCERO_220", "name": "Crucero 220 kV", "voltage": 220, "lat": -22.2425, "lon": -69.1350, "zone": "NORTE_GRANDE", "region": "Antofagasta", "sub_code": "SUB_CRUCERO"},
    {"code": "KIMAL_500", "name": "Kimal 500 kV", "voltage": 500, "lat": -22.9510, "lon": -69.2150, "zone": "NORTE_GRANDE", "region": "Antofagasta", "sub_code": "SUB_KIMAL"},
    {"code": "KIMAL_220", "name": "Kimal 220 kV", "voltage": 220, "lat": -22.9510, "lon": -69.2150, "zone": "NORTE_GRANDE", "region": "Antofagasta", "sub_code": "SUB_KIMAL"},
    {"code": "ENCUENTRO_220", "name": "Encuentro 220 kV", "voltage": 220, "lat": -22.1850, "lon": -69.3120, "zone": "NORTE_GRANDE", "region": "Antofagasta", "sub_code": "SUB_ENCUENTRO"},
    {"code": "LABERINTO_220", "name": "Laberinto 220 kV", "voltage": 220, "lat": -23.3510, "lon": -69.5800, "zone": "NORTE_GRANDE", "region": "Antofagasta", "sub_code": "SUB_LABERINTO"},
    {"code": "ATACAMA_220", "name": "Atacama 220 kV", "voltage": 220, "lat": -23.1100, "lon": -70.4500, "zone": "NORTE_GRANDE", "region": "Antofagasta", "sub_code": "SUB_ATACAMA"},
    {"code": "O_HIGGINS_220", "name": "O'Higgins 220 kV", "voltage": 220, "lat": -23.8500, "lon": -69.8500, "zone": "NORTE_GRANDE", "region": "Antofagasta", "sub_code": "SUB_O_HIGGINS"},

    # Norte Chico (Atacama / Coquimbo)
    {"code": "CARDONES_500", "name": "Cardones 500 kV", "voltage": 500, "lat": -27.3910, "lon": -70.3680, "zone": "NORTE_CHICO", "region": "Atacama", "sub_code": "SUB_CARDONES"},
    {"code": "CARDONES_220", "name": "Cardones 220 kV", "voltage": 220, "lat": -27.3910, "lon": -70.3680, "zone": "NORTE_CHICO", "region": "Atacama", "sub_code": "SUB_CARDONES"},
    {"code": "MAITENCILLO_500", "name": "Maitencillo 500 kV", "voltage": 500, "lat": -28.6120, "lon": -70.8250, "zone": "NORTE_CHICO", "region": "Atacama", "sub_code": "SUB_MAITENCILLO"},
    {"code": "MAITENCILLO_220", "name": "Maitencillo 220 kV", "voltage": 220, "lat": -28.6120, "lon": -70.8250, "zone": "NORTE_CHICO", "region": "Atacama", "sub_code": "SUB_MAITENCILLO"},
    {"code": "PAN_AZUCAR_500", "name": "Pan de Azúcar 500 kV", "voltage": 500, "lat": -29.9850, "lon": -71.2650, "zone": "NORTE_CHICO", "region": "Coquimbo", "sub_code": "SUB_PAN_AZUCAR"},
    {"code": "PAN_AZUCAR_220", "name": "Pan de Azúcar 220 kV", "voltage": 220, "lat": -29.9850, "lon": -71.2650, "zone": "NORTE_CHICO", "region": "Coquimbo", "sub_code": "SUB_PAN_AZUCAR"},
    {"code": "PUNTA_COLORADA_220", "name": "Punta Colorada 220 kV", "voltage": 220, "lat": -29.3500, "lon": -71.1800, "zone": "NORTE_CHICO", "region": "Coquimbo", "sub_code": "SUB_PUNTA_COLORADA"},

    # Centro (Valparaíso / Metropolitana / O'Higgins / Maule)
    {"code": "POLPAICO_500", "name": "Polpaico 500 kV", "voltage": 500, "lat": -33.1550, "lon": -70.8850, "zone": "CENTRO", "region": "Metropolitana", "sub_code": "SUB_POLPAICO"},
    {"code": "POLPAICO_220", "name": "Polpaico 220 kV", "voltage": 220, "lat": -33.1550, "lon": -70.8850, "zone": "CENTRO", "region": "Metropolitana", "sub_code": "SUB_POLPAICO"},
    {"code": "LO_AGUIRRE_500", "name": "Lo Aguirre 500 kV", "voltage": 500, "lat": -33.4680, "lon": -70.8520, "zone": "CENTRO", "region": "Metropolitana", "sub_code": "SUB_LO_AGUIRRE"},
    {"code": "LO_AGUIRRE_220", "name": "Lo Aguirre 220 kV", "voltage": 220, "lat": -33.4680, "lon": -70.8520, "zone": "CENTRO", "region": "Metropolitana", "sub_code": "SUB_LO_AGUIRRE"},
    {"code": "CERRO_NAVIA_220", "name": "Cerro Navia 220 kV", "voltage": 220, "lat": -33.4210, "lon": -70.7450, "zone": "CENTRO", "region": "Metropolitana", "sub_code": "SUB_CERRO_NAVIA"},
    {"code": "ALTO_JAHUEL_500", "name": "Alto Jahuel 500 kV", "voltage": 500, "lat": -33.6820, "lon": -70.6750, "zone": "CENTRO", "region": "Metropolitana", "sub_code": "SUB_ALTO_JAHUEL"},
    {"code": "ALTO_JAHUEL_220", "name": "Alto Jahuel 220 kV", "voltage": 220, "lat": -33.6820, "lon": -70.6750, "zone": "CENTRO", "region": "Metropolitana", "sub_code": "SUB_ALTO_JAHUEL"},
    {"code": "QUILLOTA_220", "name": "Quillota 220 kV", "voltage": 220, "lat": -32.8800, "lon": -71.2400, "zone": "CENTRO", "region": "Valparaíso", "sub_code": "SUB_QUILLOTA"},
    {"code": "ANCOA_500", "name": "Ancoa 500 kV", "voltage": 500, "lat": -35.8550, "lon": -71.4500, "zone": "CENTRO", "region": "Maule", "sub_code": "SUB_ANCOA"},
    {"code": "ANCOA_220", "name": "Ancoa 220 kV", "voltage": 220, "lat": -35.8550, "lon": -71.4500, "zone": "CENTRO", "region": "Maule", "sub_code": "SUB_ANCOA"},

    # Sur (Biobío / Araucanía / Los Lagos)
    {"code": "CHARRUA_500", "name": "Charrúa 500 kV", "voltage": 500, "lat": -37.0520, "lon": -72.2850, "zone": "SUR", "region": "Biobío", "sub_code": "SUB_CHARRUA"},
    {"code": "CHARRUA_220", "name": "Charrúa 220 kV", "voltage": 220, "lat": -37.0520, "lon": -72.2850, "zone": "SUR", "region": "Biobío", "sub_code": "SUB_CHARRUA"},
    {"code": "CONCEPCION_220", "name": "Concepción 220 kV", "voltage": 220, "lat": -36.8200, "lon": -73.0400, "zone": "SUR", "region": "Biobío", "sub_code": "SUB_CONCEPCION"},
    {"code": "TEMUCO_220", "name": "Temuco 220 kV", "voltage": 220, "lat": -38.7400, "lon": -72.6100, "zone": "SUR", "region": "Araucanía", "sub_code": "SUB_TEMUCO"},
    {"code": "PUERTO_MONTT_220", "name": "Puerto Montt 220 kV", "voltage": 220, "lat": -41.4650, "lon": -72.9400, "zone": "SUR", "region": "Los Lagos", "sub_code": "SUB_PUERTO_MONTT"}
]

TRANSMISSION_LINES_DATA = [
    # 500 kV Backbone
    {"code": "L500_KIMAL_CARDONES", "name": "Línea 2x500 kV Kimal - Cardones", "from": "KIMAL_500", "to": "CARDONES_500", "voltage": 500, "cap": 1700, "len": 580},
    {"code": "L500_CARDONES_MAITENCILLO", "name": "Línea 2x500 kV Cardones - Maitencillo", "from": "CARDONES_500", "to": "MAITENCILLO_500", "voltage": 500, "cap": 1700, "len": 140},
    {"code": "L500_MAITENCILLO_PAN_AZUCAR", "name": "Línea 2x500 kV Maitencillo - Pan de Azúcar", "from": "MAITENCILLO_500", "to": "PAN_AZUCAR_500", "voltage": 500, "cap": 1700, "len": 160},
    {"code": "L500_PAN_AZUCAR_POLPAICO", "name": "Línea 2x500 kV Pan de Azúcar - Polpaico", "from": "PAN_AZUCAR_500", "to": "POLPAICO_500", "voltage": 500, "cap": 1700, "len": 370},
    {"code": "L500_POLPAICO_LO_AGUIRRE", "name": "Línea 2x500 kV Polpaico - Lo Aguirre", "from": "POLPAICO_500", "to": "LO_AGUIRRE_500", "voltage": 500, "cap": 2000, "len": 45},
    {"code": "L500_LO_AGUIRRE_ALTO_JAHUEL", "name": "Línea 2x500 kV Lo Aguirre - Alto Jahuel", "from": "LO_AGUIRRE_500", "to": "ALTO_JAHUEL_500", "voltage": 500, "cap": 2000, "len": 40},
    {"code": "L500_ALTO_JAHUEL_ANCOA", "name": "Línea 2x500 kV Alto Jahuel - Ancoa", "from": "ALTO_JAHUEL_500", "to": "ANCOA_500", "voltage": 500, "cap": 2200, "len": 260},
    {"code": "L500_ANCOA_CHARRUA", "name": "Línea 2x500 kV Ancoa - Charrúa", "from": "ANCOA_500", "to": "CHARRUA_500", "voltage": 500, "cap": 2200, "len": 180},
    
    # 220 kV Regional
    {"code": "L220_CRUCERO_ENCUENTRO", "name": "Línea 220 kV Crucero - Encuentro", "from": "CRUCERO_220", "to": "ENCUENTRO_220", "voltage": 220, "cap": 600, "len": 45},
    {"code": "L220_ENCUENTRO_KIMAL", "name": "Línea 220 kV Encuentro - Kimal", "from": "ENCUENTRO_220", "to": "KIMAL_220", "voltage": 220, "cap": 600, "len": 85},
    {"code": "L220_KIMAL_LABERINTO", "name": "Línea 220 kV Kimal - Laberinto", "from": "KIMAL_220", "to": "LABERINTO_220", "voltage": 220, "cap": 500, "len": 90},
    {"code": "L220_LABERINTO_O_HIGGINS", "name": "Línea 220 kV Laberinto - O'Higgins", "from": "LABERINTO_220", "to": "O_HIGGINS_220", "voltage": 220, "cap": 500, "len": 65},
    {"code": "L220_CERRO_NAVIA_POLPAICO", "name": "Línea 220 kV Cerro Navia - Polpaico", "from": "CERRO_NAVIA_220", "to": "POLPAICO_220", "voltage": 220, "cap": 800, "len": 35},
    {"code": "L220_CHARRUA_TEMUCO", "name": "Línea 220 kV Charrúa - Temuco", "from": "CHARRUA_220", "to": "TEMUCO_220", "voltage": 220, "cap": 600, "len": 210},
    {"code": "L220_TEMUCO_PUERTO_MONTT", "name": "Línea 220 kV Temuco - Puerto Montt", "from": "TEMUCO_220", "to": "PUERTO_MONTT_220", "voltage": 220, "cap": 500, "len": 320}
]

GENERATION_PLANTS_DATA = [
    {"name": "Parque Solar Finis Terrae", "tech": "SOLAR_PV", "cap": 286.0, "lat": -23.15, "lon": -69.45, "bus": "LABERINTO_220", "operator": "Enel Green Power", "cf": 0.33},
    {"name": "Planta Solar Cerro Dominador (PV+CSP)", "tech": "SOLAR_PV", "cap": 210.0, "lat": -23.25, "lon": -69.60, "bus": "LABERINTO_220", "operator": "Cerro Dominador", "cf": 0.58},
    {"name": "Parque Solar El Pelícano", "tech": "SOLAR_PV", "cap": 110.0, "lat": -28.95, "lon": -70.95, "bus": "MAITENCILLO_220", "operator": "SunPower / Metro", "cf": 0.31},
    {"name": "Parque Solar Romero", "tech": "SOLAR_PV", "cap": 246.0, "lat": -28.25, "lon": -70.75, "bus": "MAITENCILLO_220", "operator": "Acciona Energía", "cf": 0.32},
    {"name": "Parque Eólico San Juan", "tech": "WIND", "cap": 185.0, "lat": -28.35, "lon": -71.25, "bus": "CARDONES_220", "operator": "Latin America Power", "cf": 0.38},
    {"name": "Parque Eólico Taltal", "tech": "WIND", "cap": 99.0, "lat": -25.35, "lon": -70.30, "bus": "CARDONES_220", "operator": "Enel Green Power", "cf": 0.36},
    {"name": "Parque Eólico Malleco", "tech": "WIND", "cap": 273.0, "lat": -38.15, "lon": -72.45, "bus": "TEMUCO_220", "operator": "Statkraft", "cf": 0.39},
    {"name": "Central Hidroeléctrica Ralco", "tech": "HYDRO_RESERVOIR", "cap": 690.0, "lat": -37.98, "lon": -71.45, "bus": "CHARRUA_220", "operator": "Enel Generación", "cf": 0.45},
    {"name": "Central Hidroeléctrica Pangue", "tech": "HYDRO_ROR", "cap": 467.0, "lat": -37.88, "lon": -71.65, "bus": "CHARRUA_220", "operator": "Enel Generación", "cf": 0.50},
    {"name": "Central Hidroeléctrica Colbún", "tech": "HYDRO_RESERVOIR", "cap": 474.0, "lat": -35.70, "lon": -71.30, "bus": "ANCOA_220", "operator": "Colbún S.A.", "cf": 0.42},
    {"name": "Central Ciclo Combinado Kelar", "tech": "THERMAL_GAS", "cap": 517.0, "lat": -23.10, "lon": -70.40, "bus": "ATACAMA_220", "operator": "BHP / Engie", "cf": 0.65},
    {"name": "Central Ciclo Combinado Nehuenco", "tech": "THERMAL_GAS", "cap": 738.0, "lat": -32.85, "lon": -71.25, "bus": "QUILLOTA_220", "operator": "Colbún S.A.", "cf": 0.55}
]

BESS_DATA = [
    {"name": "BESS Coya", "mw": 180.0, "mwh": 900.0, "hours": 5.0, "bus": "LABERINTO_220", "operator": "Engie Energía Chile"},
    {"name": "BESS Tamaya", "mw": 68.0, "mwh": 272.0, "hours": 4.0, "bus": "CRUCERO_220", "operator": "Engie Energía Chile"},
    {"name": "BESS Desierto de Atacama", "mw": 100.0, "mwh": 500.0, "hours": 5.0, "bus": "KIMAL_220", "operator": "Grenergy"},
    {"name": "BESS San Pedro", "mw": 50.0, "mwh": 200.0, "hours": 4.0, "bus": "CARDONES_220", "operator": "AES Andes"}
]

PROJECTS_DATA = [
    {"name": "Proyecto Oasis de Atacama (Solar + BESS)", "tech": "SOLAR_PLUS_BESS", "mw": 1000.0, "mwh": 4100.0, "lat": -23.40, "lon": -69.65, "bus": "LABERINTO_220", "status": "CONSTRUCTION", "cod": 2026, "owner": "Grenergy Renovables", "capex": 1400.0},
    {"name": "Proyecto Solar Guanchoi", "tech": "SOLAR_PV", "mw": 398.0, "mwh": 0.0, "lat": -27.60, "lon": -70.20, "bus": "CARDONES_220", "status": "CONSTRUCTION", "cod": 2026, "owner": "Enel Green Power", "capex": 350.0},
    {"name": "BESS Celda Solar", "tech": "BESS", "mw": 200.0, "mwh": 800.0, "lat": -22.30, "lon": -69.20, "bus": "CRUCERO_220", "status": "PERMITTED_RCA", "cod": 2027, "owner": "Colbún S.A.", "capex": 220.0},
    {"name": "Proyecto Parque Eólico Horizonte", "tech": "WIND", "mw": 816.0, "mwh": 0.0, "lat": -24.95, "lon": -69.85, "bus": "CARDONES_500", "status": "CONSTRUCTION", "cod": 2026, "owner": "Colbún S.A.", "capex": 850.0},
    {"name": "Línea HVDC Kimal - Lo Aguirre 500 kV", "tech": "TRANSMISSION", "mw": 3000.0, "mwh": 0.0, "lat": -28.00, "lon": -70.00, "bus": "LO_AGUIRRE_500", "status": "CONSTRUCTION", "cod": 2029, "owner": "Conexión Kimal-Lo Aguirre", "capex": 1500.0},
    {"name": "BESS Los Cóndores Storage", "tech": "BESS", "mw": 150.0, "mwh": 600.0, "lat": -35.90, "lon": -71.50, "bus": "ANCOA_220", "status": "PERMITTED_RCA", "cod": 2028, "owner": "Enel Generación", "capex": 160.0},
    {"name": "Data Center Campus Santiago Tech (Demanda 150 MW)", "tech": "DEMAND_DATA_CENTER", "mw": 150.0, "mwh": 0.0, "lat": -33.40, "lon": -70.80, "bus": "POLPAICO_220", "status": "DEVELOPMENT", "cod": 2028, "owner": "Global Cloud Provider", "capex": 800.0},
    {"name": "Expansión Minera Concentradora Codelco Norte (Demanda 200 MW)", "tech": "DEMAND_MINING", "mw": 200.0, "mwh": 0.0, "lat": -22.20, "lon": -68.90, "bus": "CRUCERO_220", "status": "PERMITTED_RCA", "cod": 2027, "owner": "Codelco Chile", "capex": 2500.0}
]

def seed_energy_database():
    logger.info("⚡ Initializing SEN Energy Infrastructure and Time Series Seeding...")
    init_db()
    db = SessionLocal()

    try:
        # 1. Seed Substations
        substations_map = {}
        for s in SUBSTATIONS_DATA:
            existing = db.query(Substation).filter(Substation.code == s["code"]).first()
            if not existing:
                sub = Substation(
                    code=s["code"],
                    name=s["name"],
                    latitude=s["lat"],
                    longitude=s["lon"],
                    voltage_levels=s["voltages"],
                    capacity_mva=s["cap"],
                    operator=s["operator"]
                )
                db.add(sub)
                db.flush()
                substations_map[s["code"]] = sub.id
            else:
                substations_map[s["code"]] = existing.id

        # 2. Seed Buses
        buses_map = {}
        for b in BUSES_DATA:
            existing = db.query(Bus).filter(Bus.code == b["code"]).first()
            if not existing:
                bus = Bus(
                    code=b["code"],
                    name=b["name"],
                    voltage_kv=b["voltage"],
                    latitude=b["lat"],
                    longitude=b["lon"],
                    zone=b["zone"],
                    region=b["region"],
                    substation_id=substations_map.get(b.get("sub_code"))
                )
                db.add(bus)
                db.flush()
                buses_map[b["code"]] = bus.id
            else:
                buses_map[b["code"]] = existing.id

        # 3. Seed Transmission Lines
        for l in TRANSMISSION_LINES_DATA:
            from_id = buses_map.get(l["from"])
            to_id = buses_map.get(l["to"])
            if from_id and to_id:
                existing = db.query(TransmissionLine).filter(TransmissionLine.code == l["code"]).first()
                if not existing:
                    line = TransmissionLine(
                        code=l["code"],
                        name=l["name"],
                        from_bus_id=from_id,
                        to_bus_id=to_id,
                        voltage_kv=l["voltage"],
                        capacity_mw=l["cap"],
                        length_km=l["len"]
                    )
                    db.add(line)

        # 4. Seed Generation Plants
        for g in GENERATION_PLANTS_DATA:
            bus_id = buses_map.get(g["bus"])
            if bus_id:
                existing = db.query(GenerationPlant).filter(GenerationPlant.name == g["name"]).first()
                if not existing:
                    plant = GenerationPlant(
                        name=g["name"],
                        technology=g["tech"],
                        capacity_mw=g["cap"],
                        latitude=g["lat"],
                        longitude=g["lon"],
                        bus_id=bus_id,
                        operator=g["operator"],
                        capacity_factor_avg=g["cf"]
                    )
                    db.add(plant)

        # 5. Seed BESS Units
        for bess in BESS_DATA:
            bus_id = buses_map.get(bess["bus"])
            if bus_id:
                existing = db.query(BessUnit).filter(BessUnit.name == bess["name"]).first()
                if not existing:
                    unit = BessUnit(
                        name=bess["name"],
                        power_mw=bess["mw"],
                        energy_mwh=bess["mwh"],
                        duration_hours=bess["hours"],
                        bus_id=bus_id,
                        operator=bess["operator"]
                    )
                    db.add(unit)

        # 6. Seed Projects Pipeline
        for p in PROJECTS_DATA:
            bus_id = buses_map.get(p.get("bus"))
            existing = db.query(ProjectPipeline).filter(ProjectPipeline.name == p["name"]).first()
            if not existing:
                proj = ProjectPipeline(
                    name=p["name"],
                    technology=p["tech"],
                    capacity_mw=p["mw"],
                    storage_mwh=p["mwh"],
                    latitude=p["lat"],
                    longitude=p["lon"],
                    bus_id=bus_id,
                    status=p["status"],
                    expected_cod_year=p["cod"],
                    owner=p["owner"],
                    estimated_capex_musd=p["capex"]
                )
                db.add(proj)

        # 7. Seed Fuel Prices
        fuels = [
            ("LNG_QUINTERO", 11.85, "USD/MMBtu"),
            ("LNG_MEJILLONES", 12.20, "USD/MMBtu"),
            ("COAL_API2", 115.50, "USD/Ton"),
            ("DIESEL_SEN", 22.40, "USD/MMBtu"),
            ("BRENT_OIL", 78.40, "USD/bbl")
        ]
        now = datetime.datetime.utcnow()
        for ftype, price, unit in fuels:
            for day_offset in range(30):
                t = now - datetime.timedelta(days=day_offset)
                p_var = round(price * (1 + (random.random() - 0.5) * 0.04), 2)
                db.add(FuelPrice(fuel_type=ftype, timestamp=t, price_usd=p_var, unit=unit))

        # 8. Seed Hydro Basins
        basins = [
            ("MAULE", "Embalse Colbún", 85.0, 1150.0, 72.0, "NORMAL"),
            ("LAJA", "Lago Laja", 45.0, 2400.0, 48.0, "NORMAL"),
            ("BIOBIO", "Embalse Ralco", 120.0, 980.0, 81.0, "WET"),
            ("RAPEL", "Embalse Rapel", 60.0, 420.0, 65.0, "NORMAL")
        ]
        for bname, rname, inflow, storage, usable, htype in basins:
            for day_offset in range(30):
                t = now - datetime.timedelta(days=day_offset)
                db.add(HydroBasin(
                    basin_name=bname,
                    reservoir_name=rname,
                    timestamp=t,
                    inflow_m3s=round(inflow * (1 + (random.random() - 0.5) * 0.1), 1),
                    storage_m3_million=storage,
                    usable_percentage=usable,
                    hydro_year_type=htype
                ))

        # 9. Seed Hourly Generation & Demand (Last 72 hours)
        for h in range(72):
            t = now - datetime.timedelta(hours=71 - h)
            hour_of_day = t.hour
            
            # Solar profile: bell curve between 7:00 and 19:00
            solar_mw = max(0.0, 4800.0 * (1 - ((hour_of_day - 13) / 6.0) ** 2)) if 7 <= hour_of_day <= 19 else 0.0
            wind_mw = 1200.0 + 800.0 * (1 if hour_of_day >= 16 or hour_of_day <= 5 else 0.4) + random.random() * 200.0
            hydro_mw = 2200.0 + (1200.0 if (7 <= hour_of_day <= 10 or 19 <= hour_of_day <= 23) else 0.0)
            gas_mw = 1800.0 + (1400.0 if (19 <= hour_of_day <= 23) else 400.0 if hour_of_day < 7 else 0.0)
            coal_mw = 1200.0
            bess_discharge_mw = 850.0 if (19 <= hour_of_day <= 23) else 0.0
            bess_charge_mw = 950.0 if (11 <= hour_of_day <= 15) else 0.0
            curtailment_mw = max(0.0, solar_mw * 0.12 - bess_charge_mw) if (11 <= hour_of_day <= 16) else 0.0
            
            total_gen = solar_mw + wind_mw + hydro_mw + gas_mw + coal_mw + bess_discharge_mw - bess_charge_mw

            db.add(GenerationHourly(
                timestamp=t,
                solar_mw=round(solar_mw, 1),
                wind_mw=round(wind_mw, 1),
                hydro_mw=round(hydro_mw, 1),
                thermal_gas_mw=round(gas_mw, 1),
                thermal_coal_mw=round(coal_mw, 1),
                bess_discharge_mw=round(bess_discharge_mw, 1),
                bess_charge_mw=round(bess_charge_mw, 1),
                total_generation_mw=round(total_gen, 1),
                curtailment_mw=round(curtailment_mw, 1)
            ))

            # Demand hourly
            base_demand = 8500.0 + (2800.0 if (18 <= hour_of_day <= 23) else 1800.0 if (9 <= hour_of_day <= 18) else 0.0)
            mining = 2900.0 + random.random() * 50.0
            datacenter = 450.0 + random.random() * 20.0
            industrial = base_demand * 0.35
            residential = base_demand - mining - datacenter - industrial

            db.add(DemandHourly(
                timestamp=t,
                zone="SEN_TOTAL",
                total_demand_mw=round(base_demand, 1),
                mining_demand_mw=round(mining, 1),
                industrial_demand_mw=round(industrial, 1),
                residential_demand_mw=round(residential, 1),
                data_centers_demand_mw=round(datacenter, 1)
            ))

        # 10. Seed Historical Node Prices for all 30 Buses
        for bus_code, bus_id in buses_map.items():
            bus_obj = db.query(Bus).filter(Bus.id == bus_id).first()
            zone = bus_obj.zone if bus_obj else "CENTRO"

            # Regional baseline price
            zone_base = 35.0 if zone == "NORTE_GRANDE" else 48.0 if zone == "NORTE_CHICO" else 75.0 if zone == "CENTRO" else 58.0

            for h in range(72):
                t = now - datetime.timedelta(hours=71 - h)
                hour_of_day = t.hour
                
                # Solar hour drop vs night peak
                if 10 <= hour_of_day <= 16:
                    # Solar hours -> strong price drop in North, moderate in Center
                    price = 0.0 if (zone == "NORTE_GRANDE" and random.random() > 0.35) else max(2.0, zone_base * 0.25 + random.random() * 15.0)
                elif 19 <= hour_of_day <= 23:
                    # Night peak -> high gas/hydro marginal cost
                    price = zone_base * 1.85 + random.random() * 30.0
                else:
                    price = zone_base * 0.95 + random.random() * 12.0

                db.add(NodePrice(
                    bus_id=bus_id,
                    timestamp=t,
                    price_usd_mwh=round(price, 2),
                    marginal_energy_cost=round(price * 0.85, 2),
                    marginal_loss_cost=round(price * 0.08, 2),
                    marginal_congestion_cost=round(price * 0.07, 2),
                    quality_status="VALID"
                ))

        # 11. Calculate Node Opportunity Scores for all Buses
        all_buses = db.query(Bus).all()
        for b in all_buses:
            if b.zone == "NORTE_GRANDE":
                # High solar, high curtailment, massive BESS arbitrage potential, high mining demand
                bess_score = 92.0
                solar_cap_score = 42.0  # low daytime capture price
                wind_cap_score = 65.0
                curt_risk_score = 35.0  # high risk of curtailment
                demand_score = 88.0    # high mining demand
                grid_score = 82.0      # Kimal HVDC hub
                exp_price_score = 55.0
                tot = (bess_score * 0.35) + (solar_cap_score * 0.15) + (demand_score * 0.20) + (grid_score * 0.15) + (exp_price_score * 0.15)
                rec = "HIGHLY_ATTRACTIVE" if tot >= 75 else "ATTRACTIVE"
            elif b.zone == "CENTRO":
                # High average price, low curtailment, high datacenter/urban demand, high solar capture price
                bess_score = 78.0
                solar_cap_score = 84.0
                wind_cap_score = 70.0
                curt_risk_score = 88.0  # very low curtailment
                demand_score = 94.0    # massive load center
                grid_score = 85.0
                exp_price_score = 88.0
                tot = (bess_score * 0.25) + (solar_cap_score * 0.25) + (demand_score * 0.25) + (exp_price_score * 0.25)
                rec = "HIGHLY_ATTRACTIVE"
            elif b.zone == "NORTE_CHICO":
                bess_score = 80.0
                solar_cap_score = 60.0
                wind_cap_score = 85.0
                curt_risk_score = 55.0
                demand_score = 65.0
                grid_score = 70.0
                exp_price_score = 62.0
                tot = (bess_score * 0.30) + (wind_cap_score * 0.25) + (solar_cap_score * 0.20) + (grid_score * 0.25)
                rec = "ATTRACTIVE"
            else: # SUR
                bess_score = 65.0
                solar_cap_score = 50.0
                wind_cap_score = 82.0
                curt_risk_score = 85.0
                demand_score = 70.0
                grid_score = 75.0
                exp_price_score = 68.0
                tot = (wind_cap_score * 0.35) + (bess_score * 0.20) + (exp_price_score * 0.25) + (grid_score * 0.20)
                rec = "ATTRACTIVE" if tot >= 70 else "MODERATE"

            db.add(NodeOpportunityScore(
                bus_id=b.id,
                total_score=round(tot, 1),
                expected_price_score=round(exp_price_score, 1),
                capture_price_solar_score=round(solar_cap_score, 1),
                capture_price_wind_score=round(wind_cap_score, 1),
                bess_arbitrage_score=round(bess_score, 1),
                congestion_risk_score=round(curt_risk_score, 1),
                curtailment_risk_score=round(curt_risk_score, 1),
                future_competition_score=round(55.0, 1),
                demand_growth_score=round(demand_score, 1),
                grid_expansion_score=round(grid_score, 1),
                recommendation_level=rec,
                methodology_version="v0.1"
            ))

        db.commit()
        logger.info("✅ SEN Energy Database seeded successfully with 20 substations, 30 buses, 15 transmission lines, 12 plants, 4 BESS, 8 projects, and 72h time-series!")
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Error seeding energy database: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_energy_database()
