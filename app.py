from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, FloatField
from wtforms.validators import InputRequired, Length, NumberRange
from datetime import datetime
import os
import json
import pickle
import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import folium
from folium import plugins
import logging
from config import config
from ml_model import DiseaseRiskPredictor
from database_models import db, DiseaseEntry

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import Supabase integration
try:
    from supabase_config import get_supabase_manager
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    logger.warning("Supabase integration not available")

def create_app():
    """Application factory function"""
    app = Flask(__name__)

    # Load configuration
    env = os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(config[env])

    # Initialize database
    db.init_app(app)

    # Initialize the ML model
    risk_predictor = DiseaseRiskPredictor()
    
    # Initialize Supabase manager
    supabase_manager = None
    if SUPABASE_AVAILABLE and os.getenv('SUPABASE_URL'):
        try:
            supabase_manager = get_supabase_manager()
            logger.info("Supabase integration enabled")
        except Exception as e:
            logger.warning(f"Failed to initialize Supabase: {e}")

    class DiseaseEntryForm(FlaskForm):
        disease_name = SelectField('Disease Name', 
                                  choices=[
                                      ('dengue', 'Dengue'),
                                      ('malaria', 'Malaria'),
                                      ('chikungunya', 'Chikungunya'),
                                      ('typhoid', 'Typhoid'),
                                      ('hepatitis_a', 'Hepatitis A'),
                                      ('tuberculosis', 'Tuberculosis'),
                                      ('covid19', 'COVID-19'),
                                      ('influenza', 'Influenza'),
                                      ('other', 'Other')
                                  ],
                                  validators=[InputRequired()])
        patient_age = FloatField('Patient Age', validators=[InputRequired(), NumberRange(min=0, max=150)])
        address = TextAreaField('Address', validators=[InputRequired(), Length(min=10, max=500)])
        additional_info = TextAreaField('Additional Information', validators=[Length(max=1000)])
        occurrence_date = StringField('Date of Occurrence', 
                                      validators=[InputRequired()],
                                      render_kw={'type': 'datetime-local'})

    @app.route('/')
    def index():
        """Home page with recent disease entries and risk map"""
        try:
            recent_entries = []
            
            # Try Supabase first, then fallback to local DB
            if supabase_manager:
                try:
                    supabase_entries = supabase_manager.get_disease_entries(limit=10)
                    recent_entries = supabase_entries
                except Exception as e:
                    logger.warning(f"Failed to get entries from Supabase: {e}")
            
            # Fallback to local database
            if not recent_entries:
                recent_entries = DiseaseEntry.query.order_by(DiseaseEntry.created_at.desc()).limit(10).all()
                
            return render_template('index.html', recent_entries=recent_entries)
        except Exception as e:
            flash(f'Error loading data: {str(e)}', 'error')
            return render_template('index.html', recent_entries=[])

    @app.route('/register', methods=['GET', 'POST'])
    def register_disease():
        """Register a new disease entry"""
        form = DiseaseEntryForm()
        
        if form.validate_on_submit():
            try:
                # Geocode the address
                geolocator = Nominatim(user_agent=app.config['NOMINATIM_USER_AGENT'])
                location = geolocator.geocode(form.address.data, timeout=10)
                
                if location is None:
                    flash('Could not geocode the provided address. Please check and try again.', 'error')
                    return render_template('register.html', form=form)
                
                # Convert string datetime to datetime object
                try:
                    occurrence_datetime = datetime.strptime(form.occurrence_date.data, '%Y-%m-%dT%H:%M')
                except ValueError:
                    flash('Invalid date format. Please select a valid date and time.', 'error')
                    return render_template('register.html', form=form)
                
                # Create entry data
                entry_data = {
                    'patient_name': 'Anonymous',  # For privacy
                    'age': int(form.patient_age.data),
                    'disease_type': form.disease_name.data,
                    'severity': 3,  # Default severity
                    'address': form.address.data,
                    'latitude': float(location.latitude),
                    'longitude': float(location.longitude),
                    'created_at': occurrence_datetime.isoformat()
                }
                
                entry_id = None
                
                # Try to save to Supabase first
                if supabase_manager:
                    try:
                        result = supabase_manager.create_disease_entry(entry_data)
                        if result:
                            entry_id = result.get('id')
                            flash('Disease entry registered successfully in Supabase!', 'success')
                        else:
                            raise Exception("Failed to create entry in Supabase")
                    except Exception as e:
                        logger.warning(f"Failed to save to Supabase: {e}")
                
                # Fallback to local database
                if not entry_id:
                    entry = DiseaseEntry(
                        disease_name=form.disease_name.data,
                        patient_age=form.patient_age.data,
                        address=form.address.data,
                        latitude=location.latitude,
                        longitude=location.longitude,
                        additional_info=form.additional_info.data,
                        occurrence_date=occurrence_datetime
                    )
                    
                    db.session.add(entry)
                    db.session.commit()
                    entry_id = entry.id
                    flash('Disease entry registered successfully!', 'success')
                
                return redirect(url_for('risk_prediction', entry_id=entry_id))
                
            except Exception as e:
                if 'db' in locals():
                    db.session.rollback()
                flash(f'Error registering disease entry: {str(e)}', 'error')
        
        return render_template('register.html', form=form)

    @app.route('/risk-prediction/<int:entry_id>')
    def risk_prediction(entry_id):
        """Show risk prediction for a specific entry"""
        try:
            # Try to get entry from local DB first
            entry = DiseaseEntry.query.get(entry_id)
            
            if not entry and supabase_manager:
                # Try to get from Supabase
                entries = supabase_manager.get_disease_entries(limit=1000)
                entry = next((e for e in entries if e.get('id') == entry_id), None)
            
            if not entry:
                flash('Disease entry not found.', 'error')
                return redirect(url_for('index'))
            
            # Train/update the model with latest data
            risk_predictor.train_model()
            
            # Generate risk predictions
            if hasattr(entry, 'latitude'):
                lat, lng, disease = entry.latitude, entry.longitude, entry.disease_name
            else:
                lat, lng, disease = entry['latitude'], entry['longitude'], entry['disease_type']
            
            risk_areas = risk_predictor.predict_risk_areas(lat, lng, disease)
            
            # Create risk map
            risk_map = create_risk_map(lat, lng, risk_areas)
            
            return render_template('risk_prediction.html', 
                                 entry=entry, 
                                 risk_areas=risk_areas,
                                 risk_map=risk_map)
        except Exception as e:
            flash(f'Error generating risk prediction: {str(e)}', 'error')
            return redirect(url_for('index'))

    @app.route('/api/entries')
    def api_entries():
        """API endpoint to get all disease entries"""
        try:
            entries = []
            
            # Try Supabase first
            if supabase_manager:
                try:
                    entries = supabase_manager.get_disease_entries(limit=1000)
                except Exception as e:
                    logger.warning(f"Failed to get entries from Supabase: {e}")
            
            # Fallback to local database
            if not entries:
                entries = DiseaseEntry.query.all()
                entries = [entry.to_dict() for entry in entries]
            
            return jsonify(entries)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/risk-map/<float:lat>/<float:lng>/<disease>')
    def api_risk_map(lat, lng, disease):
        """API endpoint to get risk map data"""
        try:
            risk_predictor.train_model()
            risk_areas = risk_predictor.predict_risk_areas(lat, lng, disease)
            return jsonify(risk_areas)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/dashboard')
    def dashboard():
        """Dashboard with statistics and visualizations"""
        try:
            entries = []
            
            # Get entries from Supabase or local DB
            if supabase_manager:
                try:
                    entries = supabase_manager.get_entries_for_ml()
                except Exception as e:
                    logger.warning(f"Failed to get ML data from Supabase: {e}")
            
            if not entries:
                entries = DiseaseEntry.query.all()
                entries = [entry.to_dict() for entry in entries]
            
            # Calculate statistics
            total_entries = len(entries)
            
            if entries:
                # Group by disease type
                disease_counts = {}
                for entry in entries:
                    disease_type = entry.get('disease_type', entry.get('disease_name', 'Unknown'))
                    disease_counts[disease_type] = disease_counts.get(disease_type, 0) + 1
                
                # Get most common disease
                most_common = max(disease_counts, key=disease_counts.get) if disease_counts else 'N/A'
            else:
                disease_counts = {}
                most_common = 'N/A'
            
            return render_template('dashboard.html',
                                 total_entries=total_entries,
                                 disease_counts=disease_counts,
                                 most_common=most_common,
                                 entries=entries[:10])  # Show recent 10 entries
        except Exception as e:
            flash(f'Error loading dashboard: {str(e)}', 'error')
            return render_template('dashboard.html',
                                 total_entries=0,
                                 disease_counts={},
                                 most_common='N/A',
                                 entries=[])

    @app.route('/health')
    def health():
        """Health check endpoint"""
        try:
            # Test database connection
            if supabase_manager:
                supabase_healthy = supabase_manager.test_connection()
            else:
                supabase_healthy = False
            
            # Test local database
            try:
                db.session.execute('SELECT 1')
                local_db_healthy = True
            except:
                local_db_healthy = False
            
            return jsonify({
                'status': 'healthy',
                'supabase': supabase_healthy,
                'local_db': local_db_healthy,
                'timestamp': datetime.utcnow().isoformat()
            })
        except Exception as e:
            return jsonify({
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }), 500

    def create_risk_map(center_lat, center_lng, risk_areas):
        """Create a folium map with risk areas"""
        try:
            # Create base map
            m = folium.Map(
                location=[center_lat, center_lng],
                zoom_start=12,
                tiles='OpenStreetMap'
            )
            
            # Add center marker
            folium.Marker(
                [center_lat, center_lng],
                popup='Disease Entry Location',
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m)
            
            # Add risk area circles
            for area in risk_areas:
                risk_level = area.get('risk_level', 0)
                
                # Color based on risk level
                if risk_level > 0.7:
                    color = 'red'
                    fillColor = 'red'
                elif risk_level > 0.4:
                    color = 'orange'
                    fillColor = 'orange'
                else:
                    color = 'yellow'
                    fillColor = 'yellow'
                
                folium.Circle(
                    location=[area['lat'], area['lng']],
                    radius=area.get('radius', 1000),
                    popup=f"Risk Level: {risk_level:.2f}",
                    color=color,
                    fillColor=fillColor,
                    fillOpacity=0.3,
                    weight=2
                ).add_to(m)
            
            return m._repr_html_()
        except Exception as e:
            logger.error(f"Error creating risk map: {e}")
            return "<div class='alert alert-warning'>Map could not be loaded</div>"

    return app

# Create the app instance
app = create_app()

if __name__ == '__main__':
    # Initialize database tables
    with app.app_context():
        db.create_all()
        
        # Generate sample data if in development and no data exists
        if app.config['DEBUG'] and DiseaseEntry.query.count() == 0:
            from sample_data import create_sample_data
            create_sample_data()
            logger.info("Sample data generated")
    
    port = int(os.environ.get('PORT', 5000))
    debug = app.config['DEBUG']
    logger.info(f"Starting app on port {port}, debug={debug}")
    app.run(host='0.0.0.0', port=port, debug=debug)
