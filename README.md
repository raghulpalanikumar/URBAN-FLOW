# UrbanFlow - Smart City Traffic Intelligence System

A comprehensive AI-powered traffic management system that analyzes Bangalore traffic data and provides intelligent diversion strategies using machine learning.

## Project Overview

UrbanFlow is a full-stack application that:
- Analyzes real-time traffic patterns across Bangalore's road network
- Provides AI-powered route recommendations using Ollama (Phi-2 model)
- Detects closed roads and suggests optimal diversions
- Uses intelligent peripheral route analysis for congestion avoidance
- Includes a modern React-based dashboard for visualization

## Architecture

```
UrbanFlow/
├── Backend/               # Python Flask API
│   ├── app.py            # Main Flask application
│   ├── api/              # API endpoints
│   ├── services/         # Business logic
│   ├── core/             # Traffic analysis algorithms
│   ├── config/           # Configuration
│   ├── utils/            # Utilities
│   ├── data/             # Dataset
│   └── requirements.txt   # Python dependencies
├── frontend/             # React + Vite
│   ├── src/
│   │   ├── App.jsx       # Main React component
│   │   ├── App.css       # Styling
│   │   └── main.jsx      # Entry point
│   ├── package.json      # Node dependencies
│   └── vite.config.js    # Vite configuration
└── README.md
```

## Prerequisites

- **Python 3.8+** with pip
- **Node.js 16+** with npm
- **Ollama** (for AI-powered recommendations)
  - Download from https://ollama.ai
  - Run: `ollama pull phi` (or `tinyllama` for faster responses)

## Installation & Setup

### Backend Setup

1. Navigate to Backend directory:
```bash
cd Backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
   - **Windows**: `venv\Scripts\activate`
   - **Mac/Linux**: `source venv/bin/activate`

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Verify the data file exists:
```bash
# Check if the CSV is at:
# Backend/data/Banglore_traffic_Dataset.csv
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

## Running the Application

### 1. Start Ollama (in a separate terminal)

```bash
# Make sure Ollama is running
ollama serve
```

In another terminal, ensure the model is available:
```bash
ollama pull phi
```

### 2. Start the Backend API

```bash
cd Backend
python app.py
```

The API will start on `http://localhost:5000`

### 3. Start the Frontend Development Server

```bash
cd frontend
npm run dev
```

The frontend will start on `http://localhost:5173`

## API Endpoints

### Health Check
- **GET** `/health` - Check API and model status

### Traffic Analysis
- **POST** `/get_diversion` - Get diversion strategy for closed road
  ```json
  {
    "closed_road": "100 Feet Road",
    "area": "Indiranagar"
  }
  ```

- **GET** `/get_locations` - Get available areas and roads

- **GET** `/roads_by_area?area=Indiranagar` - Get roads in a specific area

- **POST** `/get_route` - Get route recommendation
  ```json
  {
    "source": "Indiranagar",
    "destination": "Whitefield"
  }
  ```

## Key Features

1. **Intelligent Traffic Analysis**
   - Real-time congestion detection
   - Speed-based route ranking
   - Incident consideration

2. **Smart Diversion Logic**
   - Peripheral area analysis when main area is congested
   - Automatic area adjustment if road is in different location
   - Critical situation detection (>90% congestion)

3. **AI-Powered Recommendations**
   - Uses Ollama with Phi-2 model for natural recommendations
   - Fallback rule-based suggestions if Ollama unavailable
   - Context-aware reasoning

4. **Modern Dashboard**
   - Real-time metrics display
   - Visual congestion indicators
   - Alternative route comparison
   - System status monitoring

## Data Structure

The CSV file contains the following columns:
- `Date` - Traffic observation date
- `Area Name` - Geographic area
- `Road/Intersection Name` - Specific road
- `Traffic Volume` - Number of vehicles
- `Average Speed` - Speed in km/h
- `Congestion Level` - Percentage (0-100%)
- `Incident Reports` - Number of incidents
- `Weather Conditions` - Current weather
- Additional metrics for environmental impact, parking, etc.

## Configuration

### Traffic Config (config/traffic_config.py)

Customize the adjacency map for your city:
```python
ADJACENCY_MAP = {
    "Area1": ["Area2", "Area3"],
    "Area2": ["Area1", "Area4"],
    # ...
}
```

### LLM Service (services/llm_service.py)

Available model options:
- `phi:latest` (Recommended - balanced performance)
- `llama3.2:latest`
- `tinyllama:latest` (Fastest)

## Troubleshooting

### Ollama Connection Error
- Ensure Ollama is running: `ollama serve`
- Verify models: `ollama list`
- Pull a model: `ollama pull phi`

### Data File Not Found
- Ensure CSV file exists at: `Backend/data/Banglore_traffic_Dataset.csv`
- Check file permissions

### CORS Errors
- Backend CORS is enabled by default (flask-cors)
- If issues persist, check flask-cors configuration in app.py

### Frontend Build Issues
- Clear node_modules: `rm -rf node_modules` (or `rmdir /s node_modules` on Windows)
- Reinstall: `npm install`
- Rebuild: `npm run build`

## Performance Tips

1. Use `tinyllama` model for faster responses on slower systems
2. Increase `OLLAMA_TIMEOUT` in `services/llm_service.py` if requests timeout
3. Cache get_locations results on frontend
4. Use peripheral area suggestions for better route diversity

## Future Enhancements

- [ ] Real-time WebSocket updates
- [ ] Multi-language support
- [ ] Mobile app (React Native)
- [ ] Advanced traffic prediction
- [ ] Integration with real traffic APIs
- [ ] User preferences and history
- [ ] Multi-city support

## License

This project is open source and available under MIT License.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review API error responses
3. Check backend console logs for detailed errors
4. Verify all dependencies are correctly installed

## Contributors

- Project: UrbanFlow Smart Traffic Intelligence
- Version: 1.0.0
"# URBAN-FLOW" 
"# URBAN-FLOW" 
