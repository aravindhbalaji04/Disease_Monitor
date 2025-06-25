# Disease Monitoring and Prediction Portal

A comprehensive web-based disease surveillance system that combines advanced machine learning with geospatial analysis to predict disease outbreaks and identify high-risk areas. This portal helps disease control teams make data-driven decisions to prevent and control disease spread.

## 🎯 Features

### Core Functionality
- **Disease Entry Registration**: Web-based form for registering new disease cases with automatic address geocoding
- **AI-Powered Risk Prediction**: Machine learning model that predicts high-risk areas based on historical data
- **Interactive Risk Mapping**: Folium-based maps showing risk zones with different threat levels
- **Real-time Dashboard**: Comprehensive analytics dashboard with disease statistics and trends
- **RESTful API**: Programmatic access to disease data and risk predictions

### Machine Learning Capabilities
- **Predictive Modeling**: Random Forest algorithm for risk area prediction
- **Temporal Analysis**: Seasonal and time-based risk factor analysis
- **Geospatial Clustering**: Location-based risk assessment and clustering
- **Multi-factor Risk Scoring**: Considers disease type, age, location, and seasonal factors

### Visualization & Reporting
- **Interactive Maps**: Folium-powered risk area visualization
- **Statistical Charts**: Disease distribution and trend analysis
- **Risk Level Indicators**: Color-coded risk zones (Very High, High, Medium, Low)
- **Alert System**: Automated notifications for high-risk areas

## 🛠️ Technology Stack

### Backend
- **Flask**: Web framework for the application
- **SQLAlchemy**: Database ORM for data management
- **scikit-learn**: Machine learning algorithms
- **pandas & numpy**: Data processing and analysis

### Frontend
- **Bootstrap 5**: Responsive UI framework
- **Font Awesome**: Icons and visual elements
- **Chart.js**: Interactive charts and graphs
- **Folium**: Interactive maps

### Geospatial & ML
- **geopy**: Geocoding and geospatial calculations
- **folium**: Interactive map generation
- **Random Forest**: Risk prediction algorithm
- **StandardScaler**: Feature normalization

### Database
- **SQLite**: Lightweight database for development
- **Supports**: PostgreSQL, MySQL for production

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd new-model
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**:
   ```bash
   python app.py
   ```
   This will create the SQLite database and populate it with sample data.

5. **Run the application**:
   ```bash
   python app.py
   ```

6. **Access the portal**:
   Open your browser and navigate to `http://localhost:5000`

## 🚀 Usage

### Registering a Disease Case

1. Navigate to the "Register Disease" page
2. Fill in the disease information:
   - Disease type (Dengue, Malaria, COVID-19, etc.)
   - Patient age
   - Complete address
   - Date of occurrence
   - Additional information (optional)
3. Submit the form
4. The system will automatically geocode the address and generate risk predictions

### Viewing Risk Predictions

1. After registering a case, you'll be redirected to the risk prediction page
2. View the interactive map showing risk zones
3. Review recommended actions for disease control teams
4. Access emergency contact information

### Dashboard Analytics

1. Navigate to the Dashboard
2. View disease statistics and trends
3. Monitor active alerts and high-risk areas
4. Export reports and data

### API Usage

The system provides RESTful API endpoints:

- `GET /api/entries` - Retrieve all disease entries
- `GET /api/risk-map/<lat>/<lng>/<disease>` - Get risk predictions for a location

## 🤖 Machine Learning Model

### Algorithm
The system uses a **Random Forest Regressor** for risk prediction, which:
- Analyzes historical disease data
- Considers multiple factors: location, time, disease type, demographics
- Generates risk scores for different areas
- Updates predictions as new data is added

### Features Used
- **Geospatial**: Latitude, longitude, population density proxy
- **Temporal**: Month, day of year, seasonal patterns
- **Demographic**: Patient age
- **Disease-specific**: Encoded disease type with risk indices

### Risk Scoring
Each disease has a base risk index:
- COVID-19: 0.90
- Dengue: 0.85
- Malaria: 0.80
- Chikungunya: 0.75
- Tuberculosis: 0.70
- Typhoid: 0.65
- Hepatitis A: 0.60
- Influenza: 0.55
- Other: 0.50

Risk scores are modified by:
- **Seasonal factors**: Higher risk during monsoon for vector-borne diseases
- **Age factors**: Increased risk for children (<10) and elderly (>60)
- **Spatial clustering**: Areas with previous cases have higher risk

## 📊 Database Schema

### DiseaseEntry
- `id`: Primary key
- `disease_name`: Type of disease
- `patient_age`: Age of the patient
- `address`: Complete address
- `latitude`, `longitude`: Geocoded coordinates
- `occurrence_date`: When the case occurred
- `created_at`: When the entry was created
- `additional_info`: Optional additional details

### RiskPrediction
- `id`: Primary key
- `disease_entry_id`: Foreign key to DiseaseEntry
- `predicted_lat`, `predicted_lng`: Predicted risk location
- `risk_score`: Calculated risk score (0-1)
- `risk_radius`: Radius of risk area in meters
- `prediction_date`: When prediction was made

## 🔧 Configuration

### Environment Variables
- `SECRET_KEY`: Flask secret key for session management
- `DATABASE_URL`: Database connection string (optional)
- `DEBUG`: Enable debug mode (default: True)

### Customization
- **Disease Types**: Modify the disease list in `app.py`
- **Risk Indices**: Update disease risk scores in `database_models.py`
- **Map Styling**: Customize map appearance in `app.py`
- **Alert Thresholds**: Adjust risk level thresholds in `ml_model.py`

## 🧪 Sample Data

The system includes sample data generation with:
- 200 disease entries across major Indian cities
- Multiple disease types with realistic distribution
- Temporal spread over 2 years
- Varied patient demographics

## 🛡️ Security Considerations

- **Input Validation**: All forms include server-side validation
- **CSRF Protection**: Flask-WTF provides CSRF tokens
- **SQL Injection Prevention**: SQLAlchemy ORM prevents SQL injection
- **XSS Protection**: Template escaping prevents XSS attacks

## 📈 Future Enhancements

### Technical Improvements
- **Real-time Updates**: WebSocket integration for live updates
- **Advanced ML**: Deep learning models for better predictions
- **Mobile App**: React Native or Flutter mobile application
- **API Rate Limiting**: Implement API rate limiting and authentication

### Feature Additions
- **SMS Alerts**: Automated SMS notifications to health workers
- **WhatsApp Integration**: Status updates via WhatsApp Business API
- **Weather Integration**: Include meteorological data in predictions
- **Population Data**: Real population density data integration

## 🙏 Acknowledgments

- **scikit-learn**: For machine learning algorithms
- **Folium**: For interactive mapping capabilities
- **Bootstrap**: For responsive UI components
- **OpenStreetMap**: For map data
- **Nominatim**: For geocoding services

---

**Built for public health safety and disease control management.**
