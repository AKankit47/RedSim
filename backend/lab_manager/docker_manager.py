import random
import time
from typing import List, Dict, Optional

# Try importing Docker — gracefully degrade to mock mode if unavailable
try:
    import docker
    from docker.models.containers import Container
    _DOCKER_AVAILABLE = True
except ImportError:
    _DOCKER_AVAILABLE = False

# ─── Lab Registry ────────────────────────────────────────────────────────────
# Maps container name → metadata. Ports are HOST ports (as in docker-compose).

LAB_REGISTRY: Dict[str, Dict] = {
    "juiceshop": {
        "id": "juiceshop",
        "name": "OWASP Juice Shop",
        "image": "bkimminich/juice-shop",
        "port": 3000,
        "category": "OWASP",
        "description": "Modern vulnerable web app covering OWASP Top 10 (XSS, SQLi, broken auth, etc.)",
        "difficulty": "Beginner–Advanced",
    },
    "dvwa": {
        "id": "dvwa",
        "name": "DVWA",
        "image": "vulnerables/web-dvwa",
        "port": 3001,
        "category": "Web",
        "description": "Damn Vulnerable Web Application — beginner-friendly SQLi, XSS, CSRF, File Inclusion",
        "difficulty": "Beginner",
    },
    "webgoat": {
        "id": "webgoat",
        "name": "WebGoat",
        "image": "webgoat/webgoat",
        "port": 8081,
        "category": "OWASP",
        "description": "OWASP WebGoat — interactive Java EE-based security training platform",
        "difficulty": "Intermediate",
    },
    "bwapp": {
        "id": "bwapp",
        "name": "bWAPP",
        "image": "raesene/bwapp",
        "port": 3003,
        "category": "Web",
        "description": "Buggy Web Application — 100+ intentional web vulnerabilities",
        "difficulty": "Beginner–Intermediate",
    },
    "mutillidae": {
        "id": "mutillidae",
        "name": "Mutillidae II",
        "image": "webpwnized/mutillidae",
        "port": 3004,
        "category": "Web",
        "description": "OWASP Mutillidae II — free, intentionally vulnerable web application",
        "difficulty": "Intermediate",
    },
    "dvna": {
        "id": "dvna",
        "name": "DVNA",
        "image": "appsecco/dvna",
        "port": 9090,
        "category": "API",
        "description": "Damn Vulnerable Node Application — OWASP Top 10 flaws in a Node.js app",
        "difficulty": "Intermediate",
    },
    "nodegoat": {
        "id": "nodegoat",
        "name": "NodeGoat",
        "image": "owasp/nodegoat",
        "port": 4000,
        "category": "API",
        "description": "OWASP NodeGoat — hands-on OWASP Top 10 learning in a Node.js environment",
        "difficulty": "Intermediate",
    },
    "hackazon": {
        "id": "hackazon",
        "name": "Hackazon",
        "image": "mutzel/hackazon",
        "port": 3005,
        "category": "Network",
        "description": "Vulnerable Amazon-style e-commerce site with realistic attack surface",
        "difficulty": "Advanced",
    },
}

# ─── CPU / RAM helpers ────────────────────────────────────────────────────────

def _calc_cpu_percent(stats: dict) -> float:
    """Calculate CPU usage percentage from a Docker stats snapshot."""
    try:
        cpu_delta = (
            stats["cpu_stats"]["cpu_usage"]["total_usage"]
            - stats["precpu_stats"]["cpu_usage"]["total_usage"]
        )
        system_delta = (
            stats["cpu_stats"]["system_cpu_usage"]
            - stats["precpu_stats"]["system_cpu_usage"]
        )
        num_cpus = stats["cpu_stats"].get("online_cpus") or len(
            stats["cpu_stats"]["cpu_usage"].get("percpu_usage", [1])
        )
        if system_delta > 0:
            return round((cpu_delta / system_delta) * num_cpus * 100.0, 2)
    except (KeyError, ZeroDivisionError):
        pass
    return 0.0


def _calc_ram_mb(stats: dict) -> float:
    """Return RAM usage in MB from a Docker stats snapshot."""
    try:
        usage = stats["memory_stats"]["usage"]
        cache = stats["memory_stats"].get("stats", {}).get("cache", 0)
        return round((usage - cache) / (1024 * 1024), 1)
    except KeyError:
        return 0.0


# ─── Mock state (used when Docker is unavailable) ─────────────────────────────

_MOCK_RUNNING: set = set()   # lab IDs that are "running" in mock mode
_MOCK_START_TIMES: Dict[str, float] = {}  # lab_id → epoch when started


def _mock_cpu(lab_id: str) -> float:
    """Return a slowly drifting fake CPU% for a mock-running container."""
    t = time.time() - _MOCK_START_TIMES.get(lab_id, time.time())
    return round(abs(15 + 10 * (t % 60) / 60 + random.uniform(-2, 2)), 2)


def _mock_ram(lab_id: str) -> float:
    """Return a slowly drifting fake RAM MB for a mock-running container."""
    t = time.time() - _MOCK_START_TIMES.get(lab_id, time.time())
    base = 180 + (hash(lab_id) % 120)
    return round(base + 20 * (t % 30) / 30, 1)


# ─── DockerManager ────────────────────────────────────────────────────────────

class DockerManager:
    def __init__(self):
        self.client = None
        self.mock_mode = True

        if _DOCKER_AVAILABLE:
            try:
                self.client = docker.from_env()
                self.client.ping()          # verify daemon is actually reachable
                self.mock_mode = False
                print("[OK] Docker daemon connected -- real container mode active.")
            except Exception as e:
                print(f"[WARN] Docker unavailable ({e}). Running in DEMO / MOCK mode.")
        else:
            print("[WARN] docker-py not installed. Running in DEMO / MOCK mode.")

    # ── Internal helpers ──────────────────────────────────────────────────────

    def _get_container(self, lab_id: str):
        if not self.client:
            return None
        try:
            return self.client.containers.get(lab_id)
        except Exception:
            return None

    # ── Public API ────────────────────────────────────────────────────────────

    def list_labs(self) -> List[Dict]:
        """Return all known labs with live status and resource stats."""
        results = []

        for lab_id, info in LAB_REGISTRY.items():
            entry = dict(info)
            entry["status"] = "Stopped"
            entry["url"] = None
            entry["cpu"] = None
            entry["ram_mb"] = None

            if self.mock_mode:
                if lab_id in _MOCK_RUNNING:
                    entry["status"] = "Running"
                    entry["url"] = f"http://localhost:{info['port']}"
                    entry["cpu"] = _mock_cpu(lab_id)
                    entry["ram_mb"] = _mock_ram(lab_id)
                results.append(entry)
                continue

            container = self._get_container(lab_id)
            if container:
                container.reload()
                if container.status == "running":
                    entry["status"] = "Running"
                    entry["url"] = f"http://localhost:{info['port']}"
                    try:
                        raw = container.stats(stream=False)
                        entry["cpu"] = _calc_cpu_percent(raw)
                        entry["ram_mb"] = _calc_ram_mb(raw)
                    except Exception:
                        pass
                elif container.status == "exited":
                    entry["status"] = "Stopped"
                else:
                    entry["status"] = container.status.capitalize()
            results.append(entry)

        return results

    def start_lab(self, lab_id: str) -> Dict:
        if lab_id not in LAB_REGISTRY:
            return {"error": f"Unknown lab: {lab_id}"}

        if self.mock_mode:
            _MOCK_RUNNING.add(lab_id)
            _MOCK_START_TIMES[lab_id] = time.time()
            return {
                "status": "Started",
                "url": f"http://localhost:{LAB_REGISTRY[lab_id]['port']}",
                "mode": "demo",
            }

        info = LAB_REGISTRY[lab_id]
        try:
            container = self._get_container(lab_id)
            if container:
                if container.status != "running":
                    container.start()
            else:
                self.client.containers.run(
                    info["image"],
                    name=lab_id,
                    ports={f"{info['port']}/tcp": info["port"]},
                    detach=True,
                    restart_policy={"Name": "unless-stopped"},
                )
            return {"status": "Started", "url": f"http://localhost:{info['port']}"}
        except Exception as e:
            return {"error": str(e)}

    def stop_lab(self, lab_id: str) -> Dict:
        if self.mock_mode:
            _MOCK_RUNNING.discard(lab_id)
            _MOCK_START_TIMES.pop(lab_id, None)
            return {"status": "Stopped", "mode": "demo"}

        try:
            container = self._get_container(lab_id)
            if container and container.status == "running":
                container.stop(timeout=5)
            return {"status": "Stopped"}
        except Exception as e:
            return {"error": str(e)}

    def restart_lab(self, lab_id: str) -> Dict:
        if lab_id not in LAB_REGISTRY:
            return {"error": f"Unknown lab: {lab_id}"}

        if self.mock_mode:
            _MOCK_RUNNING.add(lab_id)
            _MOCK_START_TIMES[lab_id] = time.time()
            return {
                "status": "Restarted",
                "url": f"http://localhost:{LAB_REGISTRY[lab_id]['port']}",
                "mode": "demo",
            }

        try:
            container = self._get_container(lab_id)
            if container:
                container.restart(timeout=5)
                return {
                    "status": "Restarted",
                    "url": f"http://localhost:{LAB_REGISTRY[lab_id]['port']}",
                }
            return {"error": "Container not found. Start it first."}
        except Exception as e:
            return {"error": str(e)}

    def get_stats(self, lab_id: str) -> Dict:
        """Return live CPU% and RAM MB for a running container."""
        if self.mock_mode:
            if lab_id not in _MOCK_RUNNING:
                return {"error": "Container not running"}
            return {"cpu": _mock_cpu(lab_id), "ram_mb": _mock_ram(lab_id)}

        container = self._get_container(lab_id)
        if not container or container.status != "running":
            return {"error": "Container not running"}
        try:
            raw = container.stats(stream=False)
            return {
                "cpu": _calc_cpu_percent(raw),
                "ram_mb": _calc_ram_mb(raw),
            }
        except Exception as e:
            return {"error": str(e)}

    def status(self) -> Dict:
        if self.mock_mode:
            return {"docker": "Running", "mode": "demo"}

        try:
            self.client.ping()
            return {"docker": "Running"}
        except Exception:
            return {"docker": "Unavailable"}


docker_manager = DockerManager()
