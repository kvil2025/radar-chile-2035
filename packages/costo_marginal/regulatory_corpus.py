from typing import List, Dict, Optional

REGULATORY_DOCUMENTS = [
    {
        "id": "REG-DFL4",
        "title": "DFL 4 - Ley General de Servicios Eléctricos (LGSE)",
        "law_reference": "DFL 4/20.018 de 2006",
        "doc_type": "LEY",
        "category": "MERCADO_Y_TARIFAS",
        "summary": "Marco fundamental de la regulación eléctrica en Chile. Regula la generación, transmisión y distribución, el régimen de concesiones, el libre acceso a la red y el cálculo de costos marginales y precios de nudo.",
        "key_articles": [
            {"art": "Art. 1", "desc": "Deber del Estado de velar por el cumplimiento de normas de calidad y seguridad en los servicios eléctricos."},
            {"art": "Art. 72-1", "desc": "Definición y régimen de Pequeños Medios de Generación Distribuida (PMGD) con excedentes <= 9 MW."},
            {"art": "Art. 149", "desc": "Cálculo del Costo Marginal instantáneo de energía y potencia por el Coordinador Eléctrico Nacional."},
            {"art": "Art. 78", "desc": "Acceso abierto y no discriminatorio a los sistemas de transmisión nacional y zonal."}
        ]
    },
    {
        "id": "REG-LEY21505",
        "title": "Ley 21.505 — Promoción del Almacenamiento de Energía Eléctrica y la Electromovilidad",
        "law_reference": "Ley 21.505 de Noviembre 2022",
        "doc_type": "LEY",
        "category": "ALMACENAMIENTO_BESS",
        "summary": "Habilita la participación de sistemas de almacenamiento BESS puros (standalone) en el mercado eléctrico con derecho a remuneración por capacidad de potencia y energía en el mercado spot.",
        "key_articles": [
            {"art": "Art. 1", "desc": "Reconocimiento de los Sistemas de Almacenamiento de Energía (SAE) como agentes del mercado mayorista."},
            {"art": "Art. 3", "desc": "Mecanismo de remuneración de potencia de suficiencia para BESS standalone."},
            {"art": "Art. 4", "desc": "Incentivos y exenciones para electromovilidad y redes inteligentes."}
        ]
    },
    {
        "id": "REG-DS88",
        "title": "Decreto Supremo 88 — Reglamento para Medios de Generación de Pequeña Escala (PMGD)",
        "law_reference": "DS 88 de Octubre 2020 (Min. Energía)",
        "doc_type": "DECRETO",
        "category": "PMGD_DISTRIBUCION",
        "summary": "Establece el régimen de Precio Estabilizado por bloques horarios para PMGD solares, eólicos y mini-hidro, y las normas técnicas de conexión a redes de media tensión.",
        "key_articles": [
            {"art": "Art. 15", "desc": "Metodología de cálculo del Precio Estabilizado por bandas horarias (Punta, Media, Baja)."},
            {"art": "Art. 22", "desc": "Régimen transitorio de 12 años para proyectos con ICC aprobado previo a vigencia."}
        ]
    },
    {
        "id": "REG-LEY20257",
        "title": "Ley 20.257 / Ley 20.698 — Fomento a las Energías Renovables No Convencionales (ERNC)",
        "law_reference": "Ley 20.257 de 2008 / Ley 20.698 de 2013",
        "doc_type": "LEY",
        "category": "TRANSICION_ENERGETICA",
        "summary": "Estableció la cuota obligatoria de inyección ERNC (20% al 2025) e impulsó las licitaciones públicas de suministro regulado de clientes residenciales y comerciales.",
        "key_articles": [
            {"art": "Art. 150 bis", "desc": "Obligación de las empresas generadoras de acreditar cuota mínima de energía renovable inyectada."},
            {"art": "Art. 131", "desc": "Licitaciones de suministro por bloques de energía diurno y nocturno."}
        ]
    },
    {
        "id": "REG-CNE-PRECIOS",
        "title": "Resoluciones Exentas CNE — Fijación de Precios de Nudo Promedio (PNP) y Costos de Transmisión",
        "law_reference": "Resoluciones Semestrales CNE",
        "doc_type": "RESOLUCION",
        "category": "TARIFAS_Y_REGULACION",
        "summary": "Informes Técnicos Definitivos semestrales emitidos por la Comisión Nacional de Energía que fijan los precios de nudo aplicables a los contratos regulados y los cargos por servicio público de transmisión.",
        "key_articles": [
            {"art": "ITD PNP", "desc": "Indexación y traspaso de costos de combustibles (GNL/Carbón) a tarifas finales."},
            {"art": "Plan Expansión", "desc": "Decretos de expansión de transmisión troncal (ej. Kimal-Lo Aguirre 500 kV)."}
        ]
    }
]

class RegulatoryCorpusEngine:
    """
    Searchable Chilean Energy Regulatory Knowledge Base.
    """

    @staticmethod
    def get_all_documents() -> List[Dict]:
        return REGULATORY_DOCUMENTS

    @staticmethod
    def search_documents(query: str = "", category: Optional[str] = None) -> List[Dict]:
        results = REGULATORY_DOCUMENTS
        if category and category != "ALL":
            results = [d for d in results if d.get("category") == category]
        if query:
            q_lower = query.lower()
            results = [
                d for d in results
                if q_lower in d["title"].lower() or q_lower in d["summary"].lower() or any(q_lower in a["desc"].lower() for a in d.get("key_articles", []))
            ]
        return results
