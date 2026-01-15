# AI 3D Print Platform 🚀

> **Volledig geautomatiseerd platform voor het omzetten van chat prompts en foto's naar 3D printbare modellen voor je Bambu Lab P2S printer**

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688.svg)](https://fastapi.tiangolo.com)
[![Hyperbrowser](https://img.shields.io/badge/Hyperbrowser-Browser--Use-orange.svg)](https://hyperbrowser.ai)

## ✨ Features

- 🤖 **AI Browser Automation** - Hyperbrowser Browser-Use agent voor volledige automatisering
- 💬 **Text-to-3D** - Omzet chat prompts direct naar 3D modellen  
- 📸 **Image-to-3D** - Upload foto's en krijg 3D modellen terug
- 🧠 **Geheugen Systeem** - Sessie management en gebruikers geschiedenis
- 🎨 **Mooie Interface** - React frontend met 3D model viewer
- 💾 **Bestandsbeheer** - Cloud opslag met deelbare links
- 🖨️ **P2S Compatible** - Geoptimaliseerd voor Bambu Lab P2S printer
- 📦 **Multiple Formats** - Export naar STL, GLB, FBX, OBJ, USDZ

## 🏗️ Architectuur

```
├── backend/              # FastAPI backend met Hyperbrowser
│   ├── main.py          # API endpoints en agent integratie
│   └── requirements.txt # Python dependencies
├── frontend/            # React + Next.js frontend  
│   ├── app/            # Next.js app router
│   ├── components/     # React components
│   └── public/         # Static assets
├── .env.example        # Environment variables template
└── README.md           # Deze file!
```

## 🚀 Quick Start

### 1. Clone de Repository

```bash
git clone https://github.com/vandurmedries/ai-3d-print-platform.git
cd ai-3d-print-platform
```

### 2. Backend Setup

```bash
cd backend

# Installeer dependencies
pip install -r requirements.txt

# Maak .env file aan
cat > .env << EOF
HYPERBROWSER_API_KEY=your_hyperbrowser_api_key_here
PORT=8000
EOF

# Start de backend server
python main.py
```

### 3. Test de API

```bash
# Health check
curl http://localhost:8000/health

# Text-to-3D conversie
curl -X POST http://localhost:8000/api/text-to-3D \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Een moderne vaas met geometrische patronen",
    "user_id": "test_user",
    "model_format": "stl"
  }'
```

## 📚 API Documentatie

### Endpoints

#### `POST /api/text-to-3d`
Converteer text prompt naar 3D model

**Request Body:**
```json
{
  "prompt": "string",
  "user_id": "string",
  "session_id": "string (optional)",
  "model_format": "stl|glb|fbx|obj"
}
```

**Response:**
```json
{
  "success": true,
  "job_id": "uuid",
  "model_url": "https://...",
  "session_id": "session_uuid",
  "message": "3D model succesvol gegenereerd"
}
```

#### `POST /api/image-to-3d`
Converteer afbeelding naar 3D model

**Form Data:**
- `file`: Image file (JPG, PNG, WEBP)
- `user_id`: User ID string

#### `GET /api/user/{user_id}/models`
Haal alle modellen van gebruiker op (geheugen)

#### `GET /api/model/{model_id}`
Haal specifiek model op

#### `POST /api/model/{model_id}/share`
Genereer deelbare link voor model

#### `DELETE /api/model/{model_id}`
Verwijder model

## 🔧 Configuratie

### Hyperbrowser Setup

1. Ga naar [hyperbrowser.ai](https://hyperbrowser.ai) en maak een account aan
2. Haal je API key op van het dashboard
3. Voeg deze toe aan je `.env` file

### Browser-Use Agent Opties

De agent gebruikt deze configuratie voor optimale resultaten:

```python
{
    "llm": "gemini-2.5-flash",      # Snelste LLM
    "maxSteps": 30,                  # Maximum acties
    "keepBrowserOpen": True,         # Sessie behouden
    "useVision": True,               # Screenshots gebruiken
    "sessionOptions": {
        "acceptCookies": True,       # Auto-accept cookies
        "stealth": True              # Anti-detectie
    }
}
```

## 🎨 Frontend (Optioneel)

Voor de complete ervaring met visuele interface:

```bash
cd frontend
npm install
npm run dev
```

Bezoek `http://localhost:3000` voor de web interface.

## 🖨️ Bambu Lab P2S Integratie

Het platform genereert modellen die direct compatible zijn met je P2S:

1. **Format**: STL of 3MF (geoptimaliseerd voor Bambu Studio)
2. **Scale Validatie**: Automatische check binnen print volume
3. **Mesh Optimalisatie**: Clean topology voor betrouwbare prints
4. **Supports**: Optionele automatische support generatie

### Printen

1. Download het gegenereerde .stl bestand
2. Open in Bambu Studio
3. Check oriëntatie en supports
4. Slice en print!

## 🧠 Geheugen & Sessies

Het platform onthoudt je modellen en sessies:

```python
# Eerste generatie
result1 = generate_model(
    prompt="Moderne vaas",
    user_id="user123"
)

# Gebruik dezelfde sessie voor volgende generatie
result2 = generate_model(
    prompt="Maak de vaas hoger",
    user_id="user123",
    session_id=result1["session_id"]  # Context behouden!
)
```

## 🔐 Security

- **API Keys**: Nooit committen in Git
- **User Data**: Encrypted storage
- **Sessions**: Auto-expiry na 1 uur inactiviteit
- **Rate Limiting**: Built-in protection

## 🚢 Deployment

### Railway (Aanbevolen)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login en deploy
railway login
railway init
railway up
```

### Replit

1. Import GitHub repo
2. Add Hyperbrowser API key als Secret
3. Run!

### Docker

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY backend/ .
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
```

## 📊 Performance

- **Text-to-3D**: ~2-3 minuten (afhankelijk van complexiteit)
- **Image-to-3D**: ~1-2 minuten
- **Concurrent Sessions**: 10+ parallelle taken mogelijk
- **Model Quality**: High-poly meshes, print-ready

## 🤝 Contributing

Pull requests zijn welkom! Voor grote wijzigingen, open eerst een issue.

## 📝 License

[MIT](https://choosealicense.com/licenses/mit/)

## 🎯 Roadmap

- [ ] Frontend met 3D viewer en real-time preview
- [ ] PostgreSQL database voor persistente opslag
- [ ] Multi-image to 3D (360° foto's → model)
- [ ] Batch processing (meerdere prompts tegelijk)
- [ ] Auto-texturing en materialen
- [ ] Bambu Lab direct integration (send-to-printer)
- [ ] AI prompt suggestions en optimalisatie
- [ ] Community model sharing platform

## 💡 Use Cases

1. **Product Prototyping**: Van idee naar fysiek prototype in minuten
2. **Custom Decoratie**: Persoonlijke vazen, planters, houders
3. **Rapid Iteration**: Snel testen van verschillende designs
4. **Educational**: Leer 3D modeling via AI assistentie
5. **Art Projects**: Creatieve sculpturen en installaties

## 🐛 Troubleshooting

**Agent faalt te genereren:**
- Check Hyperbrowser API key
- Verhoog `maxSteps` naar 40+
- Try een andere LLM (`gpt-4o`)

**Model is niet printbaar:**
- Check mesh in Bambu Studio voor fouten
- Gebruik "Repair" functie in slicer
- Probeer ander 3D generatie platform (Tripo vs Meshy)

**Geheugen werkt niet:**
- Verify `session_id` wordt doorgegeven
- Check `keepBrowserOpen: true` in config
- Sessions expiren na 1 uur

## 📧 Contact

Vragen? Open een [issue](https://github.com/vandurmedries/ai-3d-print-platform/issues) of stuur een PR!

---

**Gemaakt met ❤️ voor de maker community**  
*Powered by [Hyperbrowser](https://hyperbrowser.ai) Browser-Use Agent*
