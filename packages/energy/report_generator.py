import datetime
from typing import Dict, Any, List
from packages.common.schemas import ProjectEvaluationResult

class InvestmentReportGenerator:
    """
    Generates institutional investment diligence reports, executive memorandums,
    and multi-sheet Excel financial models (SpreadsheetML) for SEN project siting.
    """

    @staticmethod
    def generate_excel_spreadsheetml(res: ProjectEvaluationResult, project_title: str = "Proyecto de Generación y Almacenamiento SEN 2035") -> str:
        """
        Builds a multi-tab Microsoft Excel SpreadsheetML document with full styling,
        financial formulas, and formatted tables for Excel, Google Sheets, and LibreOffice.
        """
        req = res.request
        top_bus = res.top_buses_ranking[0] if res.top_buses_ranking else None
        now_str = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M UTC")

        # 25-Year cash flow rows
        cash_flow_rows = []
        discount_rate = req.discount_rate_pct / 100.0
        capex = res.estimated_capex_musd
        opex = res.estimated_opex_musd_year
        annual_gen = (req.capacity_mw * 8760.0 * 0.32) if "SOLAR" in req.technology else (req.capacity_mw * 8760.0 * 0.38)
        base_price = top_bus.capture_price_solar if top_bus and "SOLAR" in req.technology else 45.0
        bess_spread = top_bus.bess_arbitrage_spread if top_bus else 50.0

        cum_cf = -capex
        for y in range(1, req.lifetime_years + 1):
            deg = (1.0 - 0.005) ** y
            bess_deg = (1.0 - 0.015) ** y
            gen_rev = (annual_gen * deg * base_price) / 1e6
            bess_rev = (req.storage_mwh * 350.0 * bess_spread * bess_deg) / 1e6 if req.storage_mwh > 0 else 0.0
            gross = gen_rev + bess_rev
            net = gross - opex
            cum_cf += net
            disc_cf = net / ((1.0 + discount_rate) ** y)
            cash_flow_rows.append((y, round(gen_rev, 2), round(bess_rev, 2), round(gross, 2), round(opex, 2), round(net, 2), round(cum_cf, 2), round(disc_cf, 2)))

        xml = f"""<?xml version="1.0"?>
<?mso-application progid="Excel.Sheet"?>
<Workbook xmlns="urn:schemas-microsoft-com:office:spreadsheet"
 xmlns:o="urn:schemas-microsoft-com:office:office"
 xmlns:x="urn:schemas-microsoft-com:office:excel"
 xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet"
 xmlns:html="http://www.w3.org/TR/REC-html40">
 <Styles>
  <Style ss:ID="Default" ss:Name="Normal">
   <Alignment ss:Vertical="Bottom"/>
   <Borders/>
   <Font ss:FontName="Calibri" x:Family="Swiss" ss:Size="11" ss:Color="#000000"/>
   <Interior/>
   <NumberFormat/>
   <Protection/>
  </Style>
  <Style ss:ID="TitleStyle">
   <Font ss:FontName="Calibri" ss:Size="16" ss:Bold="1" ss:Color="#0D2560"/>
  </Style>
  <Style ss:ID="SubtitleStyle">
   <Font ss:FontName="Calibri" ss:Size="11" ss:Italic="1" ss:Color="#555555"/>
  </Style>
  <Style ss:ID="HeaderNavy">
   <Font ss:FontName="Calibri" ss:Size="11" ss:Bold="1" ss:Color="#FFFFFF"/>
   <Interior ss:Color="#0D2560" ss:Pattern="Solid"/>
   <Alignment ss:Horizontal="Center" ss:Vertical="Center"/>
  </Style>
  <Style ss:ID="HeaderGold">
   <Font ss:FontName="Calibri" ss:Size="11" ss:Bold="1" ss:Color="#000000"/>
   <Interior ss:Color="#C9A84C" ss:Pattern="Solid"/>
   <Alignment ss:Horizontal="Center" ss:Vertical="Center"/>
  </Style>
  <Style ss:ID="CurrencyStyle">
   <NumberFormat ss:Format="&quot;$&quot;#,##0.00"/>
   <Alignment ss:Horizontal="Right"/>
  </Style>
  <Style ss:ID="PercentStyle">
   <NumberFormat ss:Format="0.0%"/>
   <Alignment ss:Horizontal="Right"/>
  </Style>
  <Style ss:ID="BoldCell">
   <Font ss:FontName="Calibri" ss:Size="11" ss:Bold="1"/>
  </Style>
  <Style ss:ID="TotalStyle">
   <Font ss:FontName="Calibri" ss:Size="11" ss:Bold="1" ss:Color="#0D2560"/>
   <Interior ss:Color="#E9ECEF" ss:Pattern="Solid"/>
   <NumberFormat ss:Format="&quot;$&quot;#,##0.00"/>
   <Alignment ss:Horizontal="Right"/>
  </Style>
 </Styles>

 <!-- WORKSHEET 1: RESUMEN EJECUTIVO -->
 <Worksheet ss:Name="Resumen Ejecutivo">
  <Table ss:DefaultColumnWidth="120">
   <Column ss:Width="200"/>
   <Column ss:Width="160"/>
   <Column ss:Width="250"/>
   <Row>
    <Cell ss:StyleID="TitleStyle"><Data ss:Type="String">{project_title}</Data></Cell>
   </Row>
   <Row>
    <Cell ss:StyleID="SubtitleStyle"><Data ss:Type="String">RADAR CHILE 2035 — Diligence Report • Generado el {now_str}</Data></Cell>
   </Row>
   <Row></Row>
   <Row>
    <Cell ss:StyleID="HeaderNavy"><Data ss:Type="String">PARÁMETRO</Data></Cell>
    <Cell ss:StyleID="HeaderNavy"><Data ss:Type="String">VALOR</Data></Cell>
    <Cell ss:StyleID="HeaderNavy"><Data ss:Type="String">NOTAS / SUPUESTOS</Data></Cell>
   </Row>
   <Row>
    <Cell ss:StyleID="BoldCell"><Data ss:Type="String">Tecnología Evaluada</Data></Cell>
    <Cell><Data ss:Type="String">{req.technology}</Data></Cell>
    <Cell><Data ss:Type="String">Módulo de generación y/o almacenamiento BESS</Data></Cell>
   </Row>
   <Row>
    <Cell ss:StyleID="BoldCell"><Data ss:Type="String">Capacidad de Potencia</Data></Cell>
    <Cell><Data ss:Type="String">{req.capacity_mw} MW</Data></Cell>
    <Cell><Data ss:Type="String">Potencia nominal de conexión al SEN</Data></Cell>
   </Row>
   <Row>
    <Cell ss:StyleID="BoldCell"><Data ss:Type="String">Capacidad Almacenamiento BESS</Data></Cell>
    <Cell><Data ss:Type="String">{req.storage_mwh} MWh</Data></Cell>
    <Cell><Data ss:Type="String">{round(req.storage_mwh / (req.capacity_mw + 1e-6), 1)} horas de duración (LFP 4h standard)</Data></Cell>
   </Row>
   <Row>
    <Cell ss:StyleID="BoldCell"><Data ss:Type="String">Año de Entrada (COD)</Data></Cell>
    <Cell><Data ss:Type="String">{req.target_cod_year}</Data></Cell>
    <Cell><Data ss:Type="String">{"Post Kimal-Lo Aguirre (Expansión 500kV activa)" if req.target_cod_year >= 2029 else "Previo a Kimal-Lo Aguirre"}</Data></Cell>
   </Row>
   <Row>
    <Cell ss:StyleID="BoldCell"><Data ss:Type="String">Vida Útil del Proyecto</Data></Cell>
    <Cell><Data ss:Type="String">{req.lifetime_years} Años</Data></Cell>
    <Cell><Data ss:Type="String">Degradación anual 0.5% solar / 1.5% BESS</Data></Cell>
   </Row>
   <Row>
    <Cell ss:StyleID="BoldCell"><Data ss:Type="String">Tasa de Descuento (WACC)</Data></Cell>
    <Cell ss:StyleID="PercentStyle"><Data ss:Type="Number">{discount_rate}</Data></Cell>
    <Cell><Data ss:Type="String">Costo de capital ponderado en USD</Data></Cell>
   </Row>
   <Row>
    <Cell ss:StyleID="BoldCell"><Data ss:Type="String">CAPEX Total Estimado</Data></Cell>
    <Cell ss:StyleID="CurrencyStyle"><Data ss:Type="Number">{res.estimated_capex_musd}</Data></Cell>
    <Cell><Data ss:Type="String">M USD (EPC + Conexión + BESS)</Data></Cell>
   </Row>
   <Row>
    <Cell ss:StyleID="BoldCell"><Data ss:Type="String">OPEX Anual Estimado</Data></Cell>
    <Cell ss:StyleID="CurrencyStyle"><Data ss:Type="Number">{res.estimated_opex_musd_year}</Data></Cell>
    <Cell><Data ss:Type="String">M USD/año (O&amp;M + Seguros + Peajes)</Data></Cell>
   </Row>
   <Row></Row>
   <Row>
    <Cell ss:StyleID="HeaderGold"><Data ss:Type="String">MEJOR BARRA SELECCIONADA</Data></Cell>
    <Cell ss:StyleID="HeaderGold"><Data ss:Type="String">RESULTADO FINANCIERO</Data></Cell>
    <Cell ss:StyleID="HeaderGold"><Data ss:Type="String">RECOMENDACIÓN METODOLÓGICA</Data></Cell>
   </Row>
   <Row>
    <Cell ss:StyleID="BoldCell"><Data ss:Type="String">{top_bus.bus_name if top_bus else "N/A"}</Data></Cell>
    <Cell><Data ss:Type="String">VAN: +${top_bus.npv_musd if top_bus else 0}M USD | TIR: {top_bus.irr_pct if top_bus else 0}%</Data></Cell>
    <Cell><Data ss:Type="String">{top_bus.recommendation_level if top_bus else "N/A"} (Score: {top_bus.opportunity_score if top_bus else 0})</Data></Cell>
   </Row>
  </Table>
 </Worksheet>

 <!-- WORKSHEET 2: TOP 10 SITING RANKING -->
 <Worksheet ss:Name="Top 10 Barras SEN">
  <Table ss:DefaultColumnWidth="110">
   <Column ss:Width="50"/>
   <Column ss:Width="160"/>
   <Column ss:Width="110"/>
   <Column ss:Width="100"/>
   <Column ss:Width="100"/>
   <Column ss:Width="90"/>
   <Column ss:Width="90"/>
   <Column ss:Width="90"/>
   <Column ss:Width="300"/>
   <Row>
    <Cell ss:StyleID="HeaderNavy"><Data ss:Type="String">RANK</Data></Cell>
    <Cell ss:StyleID="HeaderNavy"><Data ss:Type="String">BARRA / SUBESTACIÓN</Data></Cell>
    <Cell ss:StyleID="HeaderNavy"><Data ss:Type="String">ZONA</Data></Cell>
    <Cell ss:StyleID="HeaderNavy"><Data ss:Type="String">VAN (M USD)</Data></Cell>
    <Cell ss:StyleID="HeaderNavy"><Data ss:Type="String">TIR (%)</Data></Cell>
    <Cell ss:StyleID="HeaderNavy"><Data ss:Type="String">LCOE ($/MWh)</Data></Cell>
    <Cell ss:StyleID="HeaderNavy"><Data ss:Type="String">PAYBACK</Data></Cell>
    <Cell ss:StyleID="HeaderNavy"><Data ss:Type="String">SCORE</Data></Cell>
    <Cell ss:StyleID="HeaderNavy"><Data ss:Type="String">JUSTIFICACIÓN CUANTITATIVA</Data></Cell>
   </Row>"""

        for b in res.top_buses_ranking:
            xml += f"""
   <Row>
    <Cell ss:StyleID="BoldCell"><Data ss:Type="Number">{b.rank}</Data></Cell>
    <Cell><Data ss:Type="String">{b.bus_name}</Data></Cell>
    <Cell><Data ss:Type="String">{b.zone}</Data></Cell>
    <Cell ss:StyleID="CurrencyStyle"><Data ss:Type="Number">{b.npv_musd}</Data></Cell>
    <Cell ss:StyleID="PercentStyle"><Data ss:Type="Number">{round(b.irr_pct / 100.0, 3)}</Data></Cell>
    <Cell><Data ss:Type="Number">{b.lcoe_usd_mwh}</Data></Cell>
    <Cell><Data ss:Type="String">{b.payback_years} años</Data></Cell>
    <Cell><Data ss:Type="Number">{b.opportunity_score}</Data></Cell>
    <Cell><Data ss:Type="String">{b.summary_rationale.replace('&', 'y')}</Data></Cell>
   </Row>"""

        xml += """
  </Table>
 </Worksheet>

 <!-- WORKSHEET 3: CASH FLOW MODEL 25Y -->
 <Worksheet ss:Name="Flujo de Caja 25Y">
  <Table ss:DefaultColumnWidth="110">
   <Row>
    <Cell ss:StyleID="HeaderNavy"><Data ss:Type="String">AÑO</Data></Cell>
    <Cell ss:StyleID="HeaderNavy"><Data ss:Type="String">INGR. GEN (M USD)</Data></Cell>
    <Cell ss:StyleID="HeaderNavy"><Data ss:Type="String">INGR. BESS (M USD)</Data></Cell>
    <Cell ss:StyleID="HeaderNavy"><Data ss:Type="String">INGR. BRUTO (M USD)</Data></Cell>
    <Cell ss:StyleID="HeaderNavy"><Data ss:Type="String">OPEX (M USD)</Data></Cell>
    <Cell ss:StyleID="HeaderNavy"><Data ss:Type="String">FLUJO NETO (M USD)</Data></Cell>
    <Cell ss:StyleID="HeaderNavy"><Data ss:Type="String">ACUMULADO (M USD)</Data></Cell>
    <Cell ss:StyleID="HeaderNavy"><Data ss:Type="String">FLUJO DESCONTADO</Data></Cell>
   </Row>"""

        for r in cash_flow_rows:
            xml += f"""
   <Row>
    <Cell ss:StyleID="BoldCell"><Data ss:Type="Number">{r[0]}</Data></Cell>
    <Cell ss:StyleID="CurrencyStyle"><Data ss:Type="Number">{r[1]}</Data></Cell>
    <Cell ss:StyleID="CurrencyStyle"><Data ss:Type="Number">{r[2]}</Data></Cell>
    <Cell ss:StyleID="CurrencyStyle"><Data ss:Type="Number">{r[3]}</Data></Cell>
    <Cell ss:StyleID="CurrencyStyle"><Data ss:Type="Number">{r[4]}</Data></Cell>
    <Cell ss:StyleID="CurrencyStyle"><Data ss:Type="Number">{r[5]}</Data></Cell>
    <Cell ss:StyleID="CurrencyStyle"><Data ss:Type="Number">{r[6]}</Data></Cell>
    <Cell ss:StyleID="CurrencyStyle"><Data ss:Type="Number">{r[7]}</Data></Cell>
   </Row>"""

        xml += """
  </Table>
 </Worksheet>
</Workbook>"""
        return xml

    @staticmethod
    def generate_investment_memo_html(res: ProjectEvaluationResult, project_title: str = "Memorándum de Inversión — Generación & Almacenamiento SEN") -> str:
        """
        Generates an institutional, print-ready HTML/PDF diligence report.
        """
        req = res.request
        top_bus = res.top_buses_ranking[0] if res.top_buses_ranking else None
        now_str = datetime.datetime.now(datetime.UTC).strftime("%d de %B de %Y")

        ranking_rows_html = "".join([
            f"""
            <tr style="border-bottom: 1px solid #e2e8f0;">
                <td style="padding: 10px; font-weight: bold; text-align: center; color: #0D2560;">#{b.rank}</td>
                <td style="padding: 10px; font-weight: 600;">{b.bus_name} <br><small style="color: #64748b; font-family: monospace;">{b.bus_code}</small></td>
                <td style="padding: 10px; color: #475569;">{b.zone}</td>
                <td style="padding: 10px; text-align: right; font-weight: bold; color: #16a34a;">+${b.npv_musd:.1f}M</td>
                <td style="padding: 10px; text-align: right; font-weight: bold; color: #C9A84C;">{b.irr_pct:.1f}%</td>
                <td style="padding: 10px; text-align: right; font-family: monospace;">${b.lcoe_usd_mwh:.1f}</td>
                <td style="padding: 10px; text-align: right; color: #475569;">{b.payback_years:.1f} yrs</td>
                <td style="padding: 10px; text-align: center;"><span style="background: #f1f5f9; padding: 3px 8px; border-radius: 6px; font-weight: bold;">{b.opportunity_score:.1f}</span></td>
                <td style="padding: 10px; font-size: 11px; color: #334155; max-width: 250px;">{b.summary_rationale}</td>
            </tr>
            """
            for b in res.top_buses_ranking
        ])

        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>{project_title}</title>
    <style>
        @page {{ size: A4; margin: 15mm; }}
        body {{ font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; color: #1e293b; line-height: 1.5; margin: 0; padding: 20px; background: #fff; }}
        .header {{ border-bottom: 3px solid #0D2560; padding-bottom: 15px; margin-bottom: 25px; display: flex; justify-content: space-between; align-items: flex-end; }}
        .title {{ font-size: 24px; font-weight: 800; color: #0D2560; margin: 0; }}
        .subtitle {{ font-size: 12px; color: #64748b; margin-top: 4px; }}
        .kpi-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 25px; }}
        .kpi-card {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px; }}
        .kpi-label {{ font-size: 10px; text-transform: uppercase; color: #64748b; font-weight: 700; }}
        .kpi-value {{ font-size: 20px; font-weight: 800; color: #0D2560; margin-top: 4px; }}
        .section-title {{ font-size: 14px; font-weight: 700; color: #0D2560; border-left: 4px solid #C9A84C; padding-left: 8px; margin: 25px 0 12px 0; text-transform: uppercase; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 12px; }}
        th {{ background: #0D2560; color: #fff; text-align: left; padding: 8px 10px; font-size: 10px; text-transform: uppercase; }}
        .highlight-box {{ background: #fffbeb; border: 1px solid #fef3c7; border-left: 4px solid #C9A84C; border-radius: 8px; padding: 12px; margin-bottom: 20px; font-size: 12px; }}
        .footer {{ margin-top: 40px; padding-top: 15px; border-top: 1px solid #e2e8f0; font-size: 10px; color: #94a3b8; display: flex; justify-content: space-between; }}
        @media print {{
            body {{ padding: 0; }}
            .no-print {{ display: none; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <div>
            <div class="subtitle">RADAR CHILE 2035 — PLATAFORMA DE INTELIGENCIA ECONÓMICA Y ENERGÉTICA</div>
            <h1 class="title">MEMORÁNDUM DE INVERSIÓN & SITING REPORT</h1>
        </div>
        <div style="text-align: right; font-size: 11px; color: #64748b;">
            <strong>Fecha:</strong> {now_str}<br>
            <strong>Metodología:</strong> DCF Model v0.1 SEN
        </div>
    </div>

    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-label">Capacidad del Proyecto</div>
            <div class="kpi-value">{req.capacity_mw} MW <small style="font-size: 12px; color:#64748b;">+ {req.storage_mwh} MWh</small></div>
            <div style="font-size: 10px; color: #64748b;">Tecnología: {req.technology}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">CAPEX Total Estimado</div>
            <div class="kpi-value">${res.estimated_capex_musd:.1f}M <small style="font-size: 11px; color:#64748b;">USD</small></div>
            <div style="font-size: 10px; color: #64748b;">OPEX: ${res.estimated_opex_musd_year:.1f}M USD/año</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Mejor Retorno (TIR)</div>
            <div class="kpi-value" style="color: #C9A84C;">{top_bus.irr_pct if top_bus else 0:.1f}%</div>
            <div style="font-size: 10px; color: #16a34a; font-weight: 600;">VAN: +${top_bus.npv_musd if top_bus else 0:.1f}M USD</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Barra Recomendada</div>
            <div class="kpi-value" style="font-size: 15px;">{top_bus.bus_name if top_bus else 'N/A'}</div>
            <div style="font-size: 10px; color: #0D2560; font-weight: bold;">Score: {top_bus.opportunity_score if top_bus else 0:.1f}/100</div>
        </div>
    </div>

    <div class="highlight-box">
        <strong>⚡ Conclusión Ejecutiva de Localización:</strong><br>
        La barra <strong>{top_bus.bus_name if top_bus else 'N/A'}</strong> ({top_bus.zone if top_bus else 'N/A'}) ofrece la combinación óptima de retorno ajustado por riesgo con un VAN de <strong>+${top_bus.npv_musd if top_bus else 0:.1f}M USD</strong> y una TIR del <strong>{top_bus.irr_pct if top_bus else 0:.1f}%</strong> (Payback: {top_bus.payback_years if top_bus else 0:.1f} años). {top_bus.summary_rationale if top_bus else ''}
    </div>

    <div class="section-title">Ranking de las 10 Mejores Barras del SEN</div>
    <table>
        <thead>
            <tr>
                <th>#</th>
                <th>Barra Eléctrica</th>
                <th>Zona</th>
                <th style="text-align: right;">VAN (M USD)</th>
                <th style="text-align: right;">TIR (%)</th>
                <th style="text-align: right;">LCOE</th>
                <th style="text-align: right;">Payback</th>
                <th style="text-align: center;">Score</th>
                <th>Tesis Cuantitativa</th>
            </tr>
        </thead>
        <tbody>
            {ranking_rows_html}
        </tbody>
    </table>

    <div class="section-title">Marco Regulatorio & Compliance Aplicable</div>
    <div style="font-size: 11px; color: #475569; line-height: 1.6;">
        <ul>
            <li><strong>DFL 4 / Art. 149 (LGSE):</strong> Remuneración por inyección a costo marginal horario calculado y transferido por el Coordinador Eléctrico Nacional.</li>
            <li><strong>Ley 21.505 (Almacenamiento y Electromovilidad):</strong> Habilita el reconocimiento y pago de potencia de suficiencia para BESS standalone y sistemas híbridos renovables.</li>
            <li><strong>DS 88 (Pequeños Medios de Generación PMGD):</strong> Régimen de precio estabilizado por bandas horarias para proyectos con inyección neta ≤ 9 MW.</li>
        </ul>
    </div>

    <div class="footer">
        <div>RADAR CHILE 2035 • Plataforma de Inteligencia Cuantitativa</div>
        <div>Confidencial • Preparado para Comités de Inversión y Bancabilidad</div>
    </div>
</body>
</html>"""
        return html
