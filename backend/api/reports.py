from fastapi import APIRouter
from fastapi.responses import FileResponse
import os
from report_generator.pdf_generator import PDFGenerator

router = APIRouter(prefix="/api/reports", tags=["reports"])

@router.get("/")
def list_reports():
    return {"message": "List of available reports"}

@router.post("/generate/{scenario_id}")
def generate_report(scenario_id: str):
    data = {
        "title": f"Test Execution - {scenario_id}",
        "risk_score": 85,
        "events": [
            {"phase": "Credential Access", "mitre_tactic": "TA0006", "severity": "HIGH", "action": "Brute Force"},
            {"phase": "Privilege Escalation", "mitre_tactic": "TA0004", "severity": "CRITICAL", "action": "Token Impersonation"},
        ]
    }
    path = PDFGenerator.generate_report(scenario_id, data)
    return {"message": "Report generated", "path": path}

@router.get("/{scenario_id}/download")
def download_report(scenario_id: str):
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "reports_output", f"{scenario_id}_report.pdf"))
    if os.path.exists(path):
         return FileResponse(path, media_type="application/pdf", filename=f"{scenario_id}_report.pdf")
    return {"error": "Report not found"}
