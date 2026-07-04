import httpx
from lab_manager.docker_manager import docker_manager
from .engine import scenario_engine
from fastapi import HTTPException, BackgroundTasks

async def start_scenario(lab_id: str, background_tasks: BackgroundTasks):
    # 1. Check container running
    labs = docker_manager.list_labs()
    lab = next((l for l in labs if l["id"] == lab_id), None)
    if not lab or lab["status"] != "Running":
        raise HTTPException(status_code=400, detail="Lab is not running")

    url = lab["url"]
    
    # 2. Gather metadata
    metadata = {
        "status": 200,
        "title": "Mock Vulnerable Application",
        "response_time": "15ms",
        "available_ports": [lab["port"]]
    }
    
    # Try fetching real data from docker
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            resp = await client.get(url)
            metadata["status"] = resp.status_code
            if "<title>" in resp.text:
                metadata["title"] = resp.text.split("<title>")[1].split("</title>")[0]
            metadata["response_time"] = f"{resp.elapsed.total_seconds() * 1000:.2f}ms"
    except Exception as e:
        print("Warning: Metadata gathering fell back to mock due to:", str(e))
        
    # 3. Launch execution iteration in background
    background_tasks.add_task(scenario_engine.run_simulation, lab_id, url)
    
    return {"status": "Simulation Started", "target_metadata": metadata}
