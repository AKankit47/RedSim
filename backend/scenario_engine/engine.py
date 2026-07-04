import time
import asyncio
from typing import List, Dict
from api.websockets import manager
from typing import List, Dict

class ScenarioEngine:
    def __init__(self):
        self.phases = [
            "Recon", 
            "Service Discovery", 
            "Directory Enumeration", 
            "Credential Attack", 
            "Privilege Escalation", 
            "Persistence", 
            "Collection"
        ]
        
    async def run_simulation(self, lab_id: str, target_url: str):
        events = []
        for phase in self.phases:
            await asyncio.sleep(2) # Simulate time taken
            event = {
                "timestamp": time.time(),
                "lab_id": lab_id,
                "phase": phase,
                "action": f"Executed synthetic action for {phase}",
                "mitre_tactic": self._map_to_mitre(phase),
                "status": "success",
                "risk_score_delta": 10
            }
            events.append(event)
            # In a real app we'd dispatch this event to WebSockets/Detection engine
            await manager.broadcast(event)
            print(f"[{lab_id}] Simulated phase complete: {phase}")
        return events

    def _map_to_mitre(self, phase: str) -> str:
        mapping = {
            "Recon": "TA0043",
            "Service Discovery": "TA0007",
            "Directory Enumeration": "TA0007",
            "Credential Attack": "TA0006",
            "Privilege Escalation": "TA0004",
            "Persistence": "TA0003",
            "Collection": "TA0009"
        }
        return mapping.get(phase, "Unknown")
        
scenario_engine = ScenarioEngine()
