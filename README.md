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

## 🚀 Deployment & Hosting

### Quick Deployment Options

#### 1. Railway (Recommended - Easy & Free)
1. **Sign up**: Go to [railway.app](https://railway.app)
2. **Deploy from GitHub**: 
   - Connect your GitHub repository
   - Railway will auto-detect Python and use the `Procfile`
3. **Set Environment Variables**: Add your Supabase credentials
4. **Deploy**: Automatic deployment on every git push

#### 2. Render (Free Tier Available)
1. **Sign up**: Go to [render.com](https://render.com)
2. **Create Web Service**: Connect your GitHub repository
3. **Configuration**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
4. **Environment Variables**: Add Supabase credentials

#### 3. Heroku (Popular Choice)
```bash
# Install Heroku CLI and login
heroku login

# Create app
heroku create your-disease-portal

# Set environment variables
heroku config:set SUPABASE_URL=your-supabase-url
heroku config:set SUPABASE_ANON_KEY=your-anon-key

# Deploy
git push heroku main
```

#### 4. DigitalOcean App Platform
1. **Create App**: Connect GitHub repository
2. **Runtime**: Python
3. **Commands**:
   - Build: `pip install -r requirements.txt`
   - Run: `gunicorn app:app`

### 🗄️ Supabase Integration

#### Step 1: Create Supabase Project
1. Go to [supabase.com](https://supabase.com) and create a new project
2. Note your project URL and API keys from Settings > API
3. Get database connection string from Settings > Database

#### Step 2: Environment Configuration
Create `.env` file with your credentials:
```bash
# Copy example file
cp .env.example .env

# Edit with your Supabase details
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_DATABASE_URL=postgresql://postgres:[password]@db.[project-ref].supabase.co:5432/postgres
```

#### Step 3: Database Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Setup database schema
python setup_database.py

# Optional: Add sample data
python setup_database.py --sample-data
```

#### Step 4: Test Integration
```bash
# Run locally
python app.py

# Test health endpoint
curl http://localhost:5000/health
```

### 🔧 Production Configuration

#### Environment Variables for Production:
```env
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=strong-random-secret-key
SUPABASE_URL=your-supabase-url
SUPABASE_ANON_KEY=your-anon-key
PORT=5000
```

#### Security Best Practices:
- Use strong SECRET_KEY in production
- Enable HTTPS (handled by hosting platforms)
- Set FLASK_DEBUG=False
- Use environment variables for all secrets
- Enable Supabase Row Level Security (RLS)

### 📊 Monitoring & Health Checks

The application includes built-in health monitoring:
- **Health Endpoint**: `/health` - Check application and database status
- **API Status**: `/api/entries` - Test API functionality
- **Database Status**: Automatic Supabase connection testing

### 🔍 Troubleshooting Deployment

#### Common Issues:
1. **Build Failures**: Check `requirements.txt` for correct package versions
2. **Database Connection**: Verify Supabase credentials and IP whitelist
3. **Memory Issues**: Upgrade to higher tier if needed
4. **Slow Geocoding**: Consider adding geocoding API key

#### Debug Commands:
```bash
# Check logs (Railway)
railway logs

# Check logs (Heroku)
heroku logs --tail

# Test database connection
python -c "from supabase_config import get_supabase_manager; print(get_supabase_manager().test_connection())"
```

### 📈 Scaling Considerations

#### For High Traffic:
1. **Database**: Enable connection pooling in Supabase
2. **Caching**: Add Redis for frequently accessed data
3. **Load Balancing**: Use multiple instances
4. **CDN**: Serve static assets via CDN
5. **Rate Limiting**: Implement API rate limiting

#### Performance Optimization:
- Enable gzip compression
- Use database indexes (already configured)
- Implement caching for ML predictions
- Optimize map rendering
