import json
import os
import datetime
from uuid import uuid4

LOGS_DIR = os.path.join(os.path.dirname(__file__), "..", "logs_output")
os.makedirs(LOGS_DIR, exist_ok=True)

class LogGenerator:
    @staticmethod
    def _get_time():
        return datetime.datetime.utcnow().isoformat()

    @staticmethod
    def generate_windows_event(scenario_id: str, events: list):
        filepath = os.path.join(LOGS_DIR, f"{scenario_id}_windows_event.json")
        entries = []
        for e in events:
            entries.append({
                "EventID": 4624 if "Credential" in e.get("phase", "") else 4688,
                "Channel": "Security",
                "Computer": e.get("host", "Target-PC"),
                "Provider": "Microsoft-Windows-Security-Auditing",
                "SystemTime": LogGenerator._get_time(),
                "EventData": {"TargetUserName": "admin", "ProcessName": "cmd.exe"}
            })
        with open(filepath, "w") as f:
            json.dump(entries, f, indent=2)
        return filepath
        
    @staticmethod
    def generate_linux_auth(scenario_id: str, events: list):
        filepath = os.path.join(LOGS_DIR, f"{scenario_id}_linux_auth.log")
        with open(filepath, "w") as f:
            for e in events:
                time_str = datetime.datetime.utcnow().strftime("%b %d %H:%M:%S")
                f.write(f"{time_str} ubuntu sshd[{uuid4().hex[:5]}]: Accepted password for root from 192.168.1.100 port 50212 ssh2\n")
        return filepath
        
    @staticmethod
    def generate_sysmon(scenario_id: str, events: list):
        filepath = os.path.join(LOGS_DIR, f"{scenario_id}_sysmon.json")
        entries = []
        for e in events:
            entries.append({
                "EventID": 1,
                "ProviderName": "Microsoft-Windows-Sysmon",
                "SystemTime": LogGenerator._get_time(),
                "EventData": {
                    "Image": "C:\\Windows\\System32\\cmd.exe",
                    "CommandLine": "cmd.exe /c whoami",
                    "ParentImage": "C:\\Windows\\Explorer.exe"
                }
            })
        with open(filepath, "w") as f:
            json.dump(entries, f, indent=2)
        return filepath

    @staticmethod
    def generate_apache_access(scenario_id: str, events: list):
        filepath = os.path.join(LOGS_DIR, f"{scenario_id}_apache.log")
        with open(filepath, "w") as f:
            for e in events:
                time_str = datetime.datetime.utcnow().strftime("%d/%b/%Y:%H:%M:%S +0000")
                f.write(f"192.168.1.100 - - [{time_str}] \"GET /api/v1/auth HTTP/1.1\" 401 232 \"-\" \"Mozilla/5.0 (Windows NT 10.0; Win64; x64)\"\n")
        return filepath
