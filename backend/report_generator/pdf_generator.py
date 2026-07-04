import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

REPORTS_DIR = os.path.join(os.path.dirname(__file__), "..", "reports_output")
os.makedirs(REPORTS_DIR, exist_ok=True)

class PDFGenerator:
    @staticmethod
    def generate_report(scenario_id: str, data: dict):
        filepath = os.path.join(REPORTS_DIR, f"{scenario_id}_report.pdf")
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []
        
        title = data.get("title", f"Simulation Report: {scenario_id}")
        elements.append(Paragraph(f"RedSim Executive Report - {title}", styles['Title']))
        elements.append(Spacer(1, 12))
        
        elements.append(Paragraph(f"<b>Overall Risk Score:</b> {data.get('risk_score', 0)} / 100", styles['Heading2']))
        elements.append(Paragraph("This document provides a breakdown of simulated attacker behavior along with MITRE ATT&CK mappings and indicator metrics.", styles['Normal']))
        elements.append(Spacer(1, 12))
        
        elements.append(Paragraph("Attack Timeline & Mapping", styles['Heading2']))
        timeline_data = [["Phase", "MITRE Tactic", "Severity", "Action"]]
        for ev in data.get("events", []):
            timeline_data.append([
                str(ev.get("phase", "N/A")),
                str(ev.get("mitre_tactic", "N/A")),
                str(ev.get("severity", "MEDIUM")),
                str(ev.get("action", ""))[:40] + "..."
            ])
            
        t = Table(timeline_data)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.darkblue),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,1), (-1,-1), colors.aliceblue),
        ]))
        elements.append(t)
        
        elements.append(Spacer(1, 24))
        elements.append(Paragraph("IOCs & Recommendations", styles['Heading2']))
        elements.append(Paragraph("1. Validate SIEM ingested the attached Event logs mapping to MITRE TA0006.<br/>2. Verify endpoint sensor triggers against execution of 'cmd.exe /c whoami'.<br/>3. Isolate user tokens failing to meet condition policies.", styles['Normal']))
        
        doc.build(elements)
        return filepath
