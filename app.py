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
from ml_model import DiseaseRiskPredictor
from database_models import db, DiseaseEntry

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///disease_monitoring.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Initialize the ML model
risk_predictor = DiseaseRiskPredictor()

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
            geolocator = Nominatim(user_agent="disease_monitoring_portal")
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
            
            # Create new disease entry
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
            
            flash('Disease entry registered successfully!', 'success')
            return redirect(url_for('risk_prediction', entry_id=entry.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error registering disease entry: {str(e)}', 'error')
    
    return render_template('register.html', form=form)

@app.route('/risk-prediction/<int:entry_id>')
def risk_prediction(entry_id):
    """Show risk prediction for a specific entry"""
    try:
        entry = DiseaseEntry.query.get_or_404(entry_id)
        
        # Train/update the model with latest data
        risk_predictor.train_model()
        
        # Generate risk predictions
        risk_areas = risk_predictor.predict_risk_areas(
            entry.latitude, 
            entry.longitude, 
            entry.disease_name
        )
        
        # Create risk map
        risk_map = create_risk_map(entry, risk_areas)
        
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
        entries = DiseaseEntry.query.all()
        return jsonify([{
            'id': entry.id,
            'disease_name': entry.disease_name,
            'patient_age': entry.patient_age,
            'address': entry.address,
            'latitude': entry.latitude,
            'longitude': entry.longitude,
            'occurrence_date': entry.occurrence_date.isoformat(),
            'created_at': entry.created_at.isoformat()
        } for entry in entries])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/risk-map/<float:lat>/<float:lng>/<disease>')
def api_risk_map(lat, lng, disease):
    """API endpoint to get risk predictions for a location"""
    try:
        risk_predictor.train_model()
        risk_areas = risk_predictor.predict_risk_areas(lat, lng, disease)
        return jsonify(risk_areas)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def create_risk_map(entry, risk_areas):
    """Create a folium map showing risk areas"""
    # Create base map centered on the entry location
    m = folium.Map(
        location=[entry.latitude, entry.longitude],
        zoom_start=12,
        tiles='OpenStreetMap'
    )
    
    # Add the disease entry marker
    folium.Marker(
        [entry.latitude, entry.longitude],
        popup=f"<b>{entry.disease_name.title()}</b><br>{entry.address}<br>{entry.occurrence_date.strftime('%Y-%m-%d')}",
        icon=folium.Icon(color='red', icon='exclamation-sign')
    ).add_to(m)
    
    # Add risk areas as circles
    colors = ['red', 'orange', 'yellow', 'green']
    risk_levels = ['Very High', 'High', 'Medium', 'Low']
    
    for i, area in enumerate(risk_areas):
        if i < len(colors):
            folium.Circle(
                location=[area['lat'], area['lng']],
                radius=area['radius'],
                popup=f"Risk Level: {risk_levels[i]}<br>Score: {area['risk_score']:.2f}",
                color=colors[i],
                fillColor=colors[i],
                fillOpacity=0.3
            ).add_to(m)
    
    # Add legend
    legend_html = """
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 150px; height: 120px; 
                background-color: white; border:2px solid grey; z-index: 9999; 
                font-size: 14px; padding: 10px">
    <p><b>Risk Levels</b></p>
    <p><i class="fa fa-circle" style="color:red"></i> Very High</p>
    <p><i class="fa fa-circle" style="color:orange"></i> High</p>
    <p><i class="fa fa-circle" style="color:yellow"></i> Medium</p>
    <p><i class="fa fa-circle" style="color:green"></i> Low</p>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))
    
    return m._repr_html_()

@app.route('/dashboard')
def dashboard():
    """Dashboard with analytics and statistics"""
    try:
        # Get statistics
        total_entries = DiseaseEntry.query.count()
        disease_counts = db.session.query(
            DiseaseEntry.disease_name,
            db.func.count(DiseaseEntry.id)
        ).group_by(DiseaseEntry.disease_name).all()
        
        recent_entries = DiseaseEntry.query.order_by(
            DiseaseEntry.created_at.desc()
        ).limit(5).all()
        
        return render_template('dashboard.html',
                             total_entries=total_entries,
                             disease_counts=disease_counts,
                             recent_entries=recent_entries)
    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'error')
        return render_template('dashboard.html',
                             total_entries=0,
                             disease_counts=[],
                             recent_entries=[])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Create sample data if database is empty
        if DiseaseEntry.query.count() == 0:
            print("Creating sample data...")
            from sample_data import create_sample_data
            create_sample_data()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
