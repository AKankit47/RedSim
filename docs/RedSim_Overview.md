# RedSim: Professional Architecture and Workflow Overview

## Executive Summary
RedSim is an advanced, production-grade cybersecurity training platform designed to bridge the gap between theoretical learning and practical defense. By providing a sandbox of containerized vulnerable web applications and coupling them with a dynamic telemetry-generation engine, RedSim empowers blue teams to monitor, detect, and respond to simulated red team operations—all without executing actual malicious code on host networks.

## Core Architecture

RedSim utilizes a modern, decoupled microservices architecture to ensure scalability and reliability:

1. **Frontend Presentation Layer (React & Vite)**
   - Delivers a premium, responsive Executive Dashboard featuring real-time data visualization via Recharts and Framer Motion.
   - Provides operators with immediate visibility into Active Alerts, Global Risk metrics, and Monitored Host availability.

2. **Backend Management Engine (FastAPI & Python)**
   - Acts as the central nervous system of RedSim via fully asynchronous non-blocking endpoints.
   - Controls the lifecycle of vulnerable Docker environments using the Docker SDK.
   - Handles simulated attack playbooks via the **Scenario Engine**.

3. **Telemetry & Detection Pipeline**
   - **Log Generator:** Translates simulated actions into realistic endpoint logging formats (Sysmon, Windows Event Logs, Apache Access Logs).
   - **Detection Engine (SIEM equivalent):** Parses incoming telemetry streams against predefined cybersecurity rulesets (e.g., Sigma rules) and maps detections directly to the **MITRE ATT&CK Framework**.

4. **Vulnerable Infrastructure (Docker & Rancher Desktop)**
   - Spins up modular, isolated training labs (e.g., OWASP Juice Shop, DVWA, WebGoat) inside a secure bridge network (`redsim-labs`).

## The RedSim Workflow

### 1. Lab Initialization
Operators select a training module from the dashboard. The backend translates this request into Docker SDK commands, dynamically standing up vulnerable web services and registering their resource bounds in real time.

### 2. Scenario Execution & Simulation
Rather than launching destructive exploit scripts (like Metasploit), RedSim executes structured "Scenarios". These scenarios emulate exact adversarial behaviors outlined by MITRE, simulating the logical steps of an attack chain.

### 3. Telemetry Synthesis
As the scenario executes (e.g., simulating a SQL Injection or Lateral Movement), the backend Log Generator drops forensic footprints mirroring what a real incident response team would see in the wild.

### 4. Detection & Analytics Mapping
The backend Detection Engine ingests the forensic data, identifies malicious patterns, and pushes the event stream to the React frontend. The dashboard automatically visualizes the breach, drawing exact correlations to MITRE ATT&CK Tactics (such as *Initial Access* or *Credential Access*).

## Key Advantages & Value Proposition

- **Zero-Risk Environment:** All exploitations and active threats are encapsulated natively via mock telemetry or securely bounded within isolated Docker containers. There is no risk of lateral network infection.
- **Cost-Effective Training:** Negates the requirement for expensive, dedicated physical cyber ranges.
- **Actionable Blue Team Training:** Focuses heavily on the *defensive* perspective, helping engineers write and validate better detection rules against standard telemetry without waiting for a real incident.
- **Extensible Modularity:** Since the labs rely on standard Docker containers, expanding RedSim heavily modular—simply drop a new vulnerable image into the `docker-compose.yml` to instantly expand the curriculum.
