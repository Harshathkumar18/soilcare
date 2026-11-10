# 🌱 SoilVision AI — The Future of Smart Soil Analysis

> **"Understand Your Soil. Grow a Better Future."**  
> A futuristic, precision-agriculture web platform built for farmers, agricultural students, and researchers to evaluate soil health, visualize soil metrics, map farm locations, extract Soil Health Card PDFs/images, and receive personalized sustainable soil prescriptions.

---

## 🌟 Key Features

1. **Precision Environmental Design System**
   - Modern dark-green & emerald hero aesthetics with glowing accents, glassmorphism cards, soft shadows, and crisp `Manrope` + `Inter` typography.
   - Fully responsive across laptops, tablets, and mobile phones.
   - **Bilingual Interface**: One-click language switcher between **English** and **తెలుగు (Telugu)**.

2. **Interactive Soil Health Analyzer (`/analyzer`)**
   - Analyze parameters: Soil pH, Nitrogen (N), Phosphorus (P), Potassium (K), Soil Moisture %, Soil Temperature, Electrical Conductivity (EC), Organic Carbon (OC %), Micronutrients (Zn, Fe, Cu, Mn, B, S), Soil Texture/Type, Location, and Target Crop.
   - Multi-parameter evaluation against **Indian Council of Agricultural Research (ICAR)** and National Soil Health Card (SHC) benchmarks.
   - **Advanced Data Visualizations (Chart.js)**:
     - Animated circular Soil Health Score (0–100) with condition ratings (*Poor*, *Fair*, *Good*, *Excellent*).
     - 6-axis Soil Balance Radar Chart.
     - Grouped NPK Comparison Bar Chart & animated nutrient progress bars.
   - **Smart Soil Prescription**: Explains why each recommendation is made (lime/gypsum correction, compost/green manure, nutrient management, irrigation/drainage, erosion prevention, and crop suitability).

3. **Soil Report Upload, OCR & Downloadable PDF (`/upload`, `/report/<id>/pdf`)**
   - Drag-and-drop upload for **PDF**, **JPG**, and **PNG** reports (up to 10 MB) with file-type & size validation.
   - Automatic parameter extraction via `pypdf` and `pytesseract` / regex heuristics.
   - **Two-Step Verification**: Review and edit extracted measurements before analysis.
   - Downloadable official PDF Soil Health Card (`/report/<id>/pdf`) generated via `fpdf2` as well as printable HTML view (`/report/<id>`).

4. **My Soil Reports & Full CRUD History (`/reports`, `/report/<id>/edit`, `/report/<id>/delete`)**
   - Live dashboard statistics (total analyzed reports, average soil health score, nutrient deficiencies detected, saved farm locations) computed from SQLite.
   - View, edit/re-analyze, download PDF, or permanently delete saved soil records.

5. **Interactive Agricultural Map (`/map`)**
   - Built with **Leaflet.js** and **OpenStreetMap**.
   - Verified Indian Agro-Ecological Zones (Alluvial, Black/Regur, Red & Yellow, Laterite, Arid/Desert, Mountain, and Coastal Saline/Sodic).
   - Interactive farm pinning: click anywhere to drop a marker, inspect GPS coordinates, link a soil analysis, and persist farm locations in SQLite.

6. **Educational Soil Explorer & Quiz (`/problems`, `/quiz`)**
   - Interactive cards for Soil pH, NPK, Texture & Structure, Microorganisms, Organic Matter & Compost, Water Retention, Soil Erosion, and Soil Conservation.
   - Beginner & Advanced agronomic quizzes with instant explanations, percentage scoring, leaderboard, and hands-on field experiments.

7. **AI Soil Assistant (Global Chatbot Widget)**
   - Server-side integration with **Google Gemini API** (`gemini-2.5-flash`) with an intelligent **Offline Agricultural Expert Engine** fallback grounded in ICAR practices.

---

## 🛠️ Technology Stack

- **Backend**: Python 3.10+ with [Flask 3.x](https://flask.palletsprojects.com/)
- **Database**: SQLite (persistent database file `soilcare.db`)
- **Frontend**: HTML5, Vanilla CSS3, Vanilla JavaScript ES6
- **Charts & Mapping**: [Chart.js 4.x](https://www.chartjs.org/), [Leaflet.js](https://leafletjs.com/) + OpenStreetMap
- **Document Processing & PDF Export**: `pypdf`, `Pillow`, `pytesseract`, `fpdf2`
- **AI Integration**: Google Gemini REST API with rule-based ICAR fallback

---

## 📁 Project Structure

```
Soil vision ai/
├── app.py                      # Main Flask server, views, REST APIs, PDF & CRUD routes
├── requirements.txt            # Python dependencies
├── .env.example                # Configuration template
├── .env                        # Local environment variables
├── database/
│   ├── __init__.py
│   └── db.py                   # SQLite schema, migrations, stats & CRUD operations
├── services/
│   ├── __init__.py
│   ├── soil_analysis.py        # ICAR scientific benchmark evaluation rules
│   ├── recommendations.py      # Smart Soil Prescription recommendation engine
│   ├── pdf_generator.py        # Official downloadable PDF Soil Health Card generator
│   ├── report_parser.py        # PDF & image OCR regex extraction for Soil Cards
│   ├── ai_assistant.py         # Gemini API + Offline agricultural expert system
│   ├── translations.py         # English and Telugu localization dictionary
│   └── knowledge_data.py       # Soil problems, quizzes, map zones, activities
├── templates/
│   ├── base.html               # Master layout (navbar, flash banner, Telugu switch, AI drawer)
│   ├── index.html              # Hero cross-section, animated metrics, dashboard overview
│   ├── analyzer.html           # Interactive soil analyzer & Chart.js visualizations
│   ├── reports.html            # Saved reports archive & dashboard summary cards
│   ├── report.html             # Printable official Soil Health Card
│   ├── edit_report.html        # Edit & re-analyze saved soil report form
│   ├── upload.html             # Drag-and-drop report upload & editable review table
│   ├── map.html                # Leaflet interactive map & farm location pinning
│   ├── problems.html           # Educational soil explorer & problem solutions
│   ├── quiz.html               # Soil-health quiz & field activities
│   ├── about.html              # Scientific methodology, KVK info & contact form
│   └── 404.html                # Custom 404 page
├── static/
│   ├── css/style.css           # SoilVision AI dark-green precision ag stylesheet
│   ├── js/                     # Modular frontend ES6 scripts
│   └── samples/                # Sample Soil Health Card PDF & text files
└── tests/                      # Automated unit, route, parser & audit test suites
```

---

## 🚀 Quickstart Installation Guide (Windows & VS Code)

1. Open a terminal in `C:\Users\Harsha\OneDrive\Desktop\Soil vision ai`.
2. Activate the virtual environment:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
3. Install dependencies (if needed):
   ```powershell
   pip install -r requirements.txt
   ```
4. Configure `.env` (optional: add `GEMINI_API_KEY` for live Gemini AI responses; otherwise the rule-based offline engine runs automatically).
5. Start the application:
   ```powershell
   python app.py
   ```
6. Open your browser to `http://127.0.0.1:5000/`.

---

## 🧪 Running Tests

Run the full automated test suite:
```powershell
.\venv\Scripts\python.exe -m unittest discover -s tests
```

---

## 📜 Scientific Methodology & Disclaimers

1. **ICAR Grounded Rules**: Soil reaction, salinity, and nutrient categories adhere to Indian Council of Agricultural Research (ICAR) benchmarks.
2. **Estimates vs. Lab Measurements**: Rule-based interpretations and missing-parameter estimates are clearly distinguished from laboratory-confirmed measurements. Always consult your district Krishi Vigyan Kendra (KVK) for certified soil testing and precise amendment rates.
