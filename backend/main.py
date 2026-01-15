"""
AI 3D Print Platform - Backend API
FastAPI server voor text/image-to-3D conversie met Hyperbrowser Browser-Use agent
"""
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import os
from dotenv import load_dotenv
import asyncio
from hyperbrowser import Hyperbrowser
import uuid
from datetime import datetime

load_dotenv()

app = FastAPI(title="AI 3D Print Platform", version="1.0.0")

# CORS configuratie
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Hyperbrowser client
client = Hyperbrowser(api_key=os.getenv("HYPERBROWSER_API_KEY"))

# In-memory database (later vervangen met PostgreSQL)
models_db = {}
sessions_db = {}

class TextTo3DRequest(BaseModel):
    prompt: str
    user_id: str
    session_id: Optional[str] = None
    model_format: str = "stl"

class ImageTo3DRequest(BaseModel):
    image_url: str
    user_id: str
    session_id: Optional[str] = None

@app.get("/")
async def root():
    return {
        "message": "AI 3D Print Platform API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.post("/api/text-to-3d")
async def text_to_3d(request: TextTo3DRequest, background_tasks: BackgroundTasks):
    """
    Converteer text prompt naar 3D model
    Gebruikt Hyperbrowser Browser-Use agent om Meshy/Tripo te automatiseren
    """
    try:
        job_id = str(uuid.uuid4())
        
        # Browser-Use agent taak
        task_prompt = f"""
        1. Ga naar https://www.meshy.ai of https://www.tripo3d.ai
        2. Gebruik de text-to-3D feature
        3. Voer deze prompt in: "{request.prompt}"
        4. Wacht tot het 3D model volledig gegenereerd is
        5. Download het model in {request.model_format.upper()} formaat
        6. Return de download URL
        """
        
        # Start Browser-Use taak met geheugen
        result = await client.agents.browser_use.start_and_wait({
            "task": task_prompt,
            "llm": "gemini-2.5-flash",
            "maxSteps": 30,
            "sessionId": request.session_id,
            "keepBrowserOpen": True,
            "useVision": True,
            "sessionOptions": {
                "acceptCookies": True,
                "stealth": True
            }
        })
        
        # Sla model op in database
        model_data = {
            "id": job_id,
            "user_id": request.user_id,
            "prompt": request.prompt,
            "model_url": result.data.finalResult,
            "session_id": result.sessionId if hasattr(result, 'sessionId') else None,
            "created_at": datetime.now().isoformat(),
            "format": request.model_format
        }
        models_db[job_id] = model_data
        
        return {
            "success": True,
            "job_id": job_id,
            "model_url": result.data.finalResult,
            "session_id": model_data["session_id"],
            "message": "3D model succesvol gegenereerd"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/api/image-to-3d")
async def image_to_3d(file: UploadFile = File(...), user_id: str = "default"):
    """
    Converteer afbeelding naar 3D model
    """
    try:
        # Upload image naar tijdelijke locatie
        image_bytes = await file.read()
        temp_path = f"/tmp/{uuid.uuid4()}_{file.filename}"
        
        with open(temp_path, "wb") as f:
            f.write(image_bytes)
        
        job_id = str(uuid.uuid4())
        
        task_prompt = f"""
        1. Ga naar https://www.meshy.ai
        2. Gebruik de Image-to-3D feature
        3. Upload de afbeelding van {temp_path}
        4. Genereer een high-quality 3D model
        5. Download als STL bestand
        6. Return de download link
        """
        
        result = await client.agents.browser_use.start_and_wait({
            "task": task_prompt,
            "llm": "gemini-2.5-flash",
            "maxSteps": 30,
            "useVision": True
        })
        
        model_data = {
            "id": job_id,
            "user_id": user_id,
            "source_image": file.filename,
            "model_url": result.data.finalResult,
            "created_at": datetime.now().isoformat()
        }
        models_db[job_id] = model_data
        
        # Cleanup
        os.remove(temp_path)
        
        return {
            "success": True,
            "job_id": job_id,
            "model_url": result.data.finalResult
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/api/user/{user_id}/models")
async def get_user_models(user_id: str):
    """
    Haal alle modellen van gebruiker op (geheugen functie)
    """
    user_models = [m for m in models_db.values() if m["user_id"] == user_id]
    return {
        "user_id": user_id,
        "total": len(user_models),
        "models": user_models
    }

@app.get("/api/model/{model_id}")
async def get_model(model_id: str):
    """
    Haal specifiek model op
    """
    if model_id not in models_db:
        raise HTTPException(status_code=404, detail="Model niet gevonden")
    
    return models_db[model_id]

@app.post("/api/model/{model_id}/share")
async def share_model(model_id: str):
    """
    Genereer deelbare link voor model
    """
    if model_id not in models_db:
        raise HTTPException(status_code=404, detail="Model niet gevonden")
    
    share_token = str(uuid.uuid4())
    share_url = f"https://your-domain.com/shared/{share_token}"
    
    models_db[model_id]["share_url"] = share_url
    models_db[model_id]["share_token"] = share_token
    
    return {
        "success": True,
        "share_url": share_url,
        "message": "Model kan nu gedeeld worden"
    }

@app.delete("/api/model/{model_id}")
async def delete_model(model_id: str):
    """
    Verwijder model
    """
    if model_id not in models_db:
        raise HTTPException(status_code=404, detail="Model niet gevonden")
    
    del models_db[model_id]
    
    return {
        "success": True,
        "message": "Model verwijderd"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
