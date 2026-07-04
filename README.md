# RedSim

RedSim is a cybersecurity training platform that simulates red team attacks without executing actual malicious code. It uses Docker to spin up real vulnerable labs (like OWASP Juice Shop and DVWA) and generates mock telemetry (sysmon, windows event logs, etc.) based on simulated attack chains mapped to the MITRE ATT&CK framework. 

This allows defenders and blue teams to reliably train their detection rules in a safe, realistic environment.

## Architecture

- **Frontend:** React, Vite, Tailwind CSS
- **Backend:** FastAPI, Python, SQLAlchemy, Docker SDK
- **Infrastructure:** Docker Compose

## Getting Started

You'll need Python 3.10+, Node.js, and Docker Desktop (or Rancher Desktop) installed and running.

### 1. Start the Docker labs
From the root directory, spin up the vulnerable containers:
```bash
docker-compose up -d
```
*(There is no need to download the images manually—Docker will automatically pull DVWA, Juice Shop, and the other target environments the first time you run this command. This might take a few minutes depending on your internet connection).*

### 2. Start the Backend API
Open a new terminal and run:
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8080
```
It'll be available at http://localhost:8080.

### 3. Start the Frontend 
Open another terminal:
```bash
cd frontend
npm install
npm run dev
```
The React dashboard will be running at http://localhost:5173.

## License
MIT
