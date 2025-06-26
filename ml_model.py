import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score
from geopy.distance import geodesic
import pickle
import os
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class DiseaseRiskPredictor:
    """
    Machine Learning model for predicting disease risk areas based on historical data
    """
    
    def __init__(self):
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        self.scaler = StandardScaler()
        self.disease_encoder = LabelEncoder()
        self.is_trained = False
        self.model_path = 'disease_risk_model.pkl'
        self.feature_columns = [
            'latitude', 'longitude', 'patient_age', 'disease_encoded',
            'month', 'day_of_year', 'population_density_proxy'
        ]
        
        # Load pre-trained model if exists
        self.load_model()
    
    def prepare_features(self, data):
        """
        Prepare features for training or prediction
        """
        df = data.copy()
        
        # Extract temporal features
        df['occurrence_date'] = pd.to_datetime(df['occurrence_date'])
        df['month'] = df['occurrence_date'].dt.month
        df['day_of_year'] = df['occurrence_date'].dt.dayofyear
        
        # Population density proxy (inverse of distance from city center)
        # This is a simplified proxy - in real implementation, use actual population data
        city_center_lat, city_center_lng = df['latitude'].mean(), df['longitude'].mean()
        df['population_density_proxy'] = df.apply(
            lambda row: 1 / (geodesic(
                (city_center_lat, city_center_lng),
                (row['latitude'], row['longitude'])
            ).kilometers + 1), axis=1
        )
        
        # Encode disease names
        if not hasattr(self.disease_encoder, 'classes_') or len(self.disease_encoder.classes_) == 0:
            self.disease_encoder.fit(df['disease_name'])
        
        df['disease_encoded'] = self.disease_encoder.transform(df['disease_name'])
        
        return df[self.feature_columns]
    
    def calculate_risk_score(self, data):
        """
        Calculate risk scores based on disease type, temporal factors, and spatial clustering
        """
        df = data.copy()
        
        # Base risk scores for different diseases
        disease_risk_map = {
            'dengue': 0.85,
            'malaria': 0.80,
            'chikungunya': 0.75,
            'covid19': 0.90,
            'tuberculosis': 0.70,
            'typhoid': 0.65,
            'hepatitis_a': 0.60,
            'influenza': 0.55,
            'other': 0.50
        }
        
        df['base_risk'] = df['disease_name'].map(disease_risk_map).fillna(0.50)
        
        # Temporal risk factors (higher risk in certain seasons)
        df['occurrence_date'] = pd.to_datetime(df['occurrence_date'])
        df['month'] = df['occurrence_date'].dt.month
        
        # Monsoon season (June-September) increases risk for vector-borne diseases
        seasonal_multiplier = df.apply(lambda row: 
            1.3 if row['month'] in [6, 7, 8, 9] and row['disease_name'] in ['dengue', 'malaria', 'chikungunya']
            else 1.0, axis=1
        )
        
        # Age-based risk (children and elderly are more vulnerable)
        age_multiplier = df['patient_age'].apply(lambda age:
            1.2 if age < 10 or age > 60 else 1.0
        )
        
        # Calculate final risk score
        risk_score = df['base_risk'] * seasonal_multiplier * age_multiplier
        
        # Normalize to 0-1 range
        risk_score = np.clip(risk_score, 0, 1)
        
        return risk_score
    
    def train_model(self, supabase_manager=None):
        """
        Train the risk prediction model using historical disease data
        """
        try:
            # Get data priority: Supabase first, then local DB
            entries = []
            
            if supabase_manager:
                try:
                    entries = supabase_manager.get_entries_for_ml()
                    print(f"Retrieved {len(entries)} entries from Supabase")
                except Exception as e:
                    print(f"Failed to get data from Supabase: {e}")
            
            # Fallback to local DB if no Supabase data
            if not entries:
                try:
                    from database_models import DiseaseEntry
                    local_entries = DiseaseEntry.query.all()
                    entries = [entry.to_dict() for entry in local_entries]
                    print(f"Retrieved {len(entries)} entries from local DB")
                except Exception as e:
                    print(f"Failed to get data from local DB: {e}")
            
            if len(entries) < 10:
                print("Insufficient data for training. Using sample data for demo.")
                # Create sample data for demo purposes
                sample_data = self._generate_sample_data()
                entries.extend(sample_data)
            
            # Convert to DataFrame
            data = []
            for entry in entries:
                # Handle both dictionary and object formats
                if isinstance(entry, dict):
                    data.append({
                        'latitude': entry.get('latitude'),
                        'longitude': entry.get('longitude'),
                        'disease_type': entry.get('disease_type', entry.get('disease_name', 'unknown')),
                        'severity': entry.get('severity', 'medium'),
                        'created_at': entry.get('created_at')
                    })
                else:
                    # SQLAlchemy object format
                    data.append({
                        'latitude': entry.latitude,
                        'longitude': entry.longitude,
                        'disease_type': entry.disease_name,
                        'severity': getattr(entry, 'severity', 'medium'),
                        'created_at': entry.occurrence_date
                    })
            
            df = pd.DataFrame(data)
            
            # Prepare features
            X = self.prepare_features(df)
            
            # Calculate target risk scores
            y = self.calculate_risk_score(df)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Scale features
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Train model
            self.model.fit(X_train_scaled, y_train)
            
            # Evaluate model
            y_pred = self.model.predict(X_test_scaled)
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            print(f"Model Training Complete - MSE: {mse:.4f}, R2: {r2:.4f}")
            
            self.is_trained = True
            self.save_model()
            
            return True
            
        except Exception as e:
            print(f"Error training model: {str(e)}")
            return False
    
    def predict_risk_areas(self, center_lat, center_lng, disease_name, radius_km=5):
        """
        Predict risk areas around a given location
        """
        if not self.is_trained:
            print("Model not trained. Training with available data...")
            if not self.train_model():
                return self._default_risk_areas(center_lat, center_lng)
        
        try:
            # Generate prediction points in a grid around the center
            risk_areas = []
            
            # Define risk zones with different radii
            zones = [
                {'radius': 500, 'risk_level': 'Very High'},
                {'radius': 1000, 'risk_level': 'High'},
                {'radius': 2000, 'risk_level': 'Medium'},
                {'radius': 3000, 'risk_level': 'Low'}
            ]
            
            for zone in zones:
                # Calculate coordinates for the zone
                lat_offset = zone['radius'] / 111000  # Approximate degrees per meter
                lng_offset = zone['radius'] / (111000 * np.cos(np.radians(center_lat)))
                
                zone_lat = center_lat + (np.random.uniform(-1, 1) * lat_offset)
                zone_lng = center_lng + (np.random.uniform(-1, 1) * lng_offset)
                
                # Prepare features for prediction
                prediction_data = pd.DataFrame({
                    'latitude': [zone_lat],
                    'longitude': [zone_lng],
                    'patient_age': [35],  # Average age
                    'disease_name': [disease_name],
                    'occurrence_date': [datetime.now()]
                })
                
                X_pred = self.prepare_features(prediction_data)
                X_pred_scaled = self.scaler.transform(X_pred)
                
                # Make prediction
                risk_score = self.model.predict(X_pred_scaled)[0]
                
                risk_areas.append({
                    'lat': zone_lat,
                    'lng': zone_lng,
                    'risk_score': float(risk_score),
                    'risk_level': zone['risk_level'],
                    'radius': zone['radius']
                })
            
            # Sort by risk score (highest first)
            risk_areas.sort(key=lambda x: x['risk_score'], reverse=True)
            
            return risk_areas
            
        except Exception as e:
            print(f"Error predicting risk areas: {str(e)}")
            return self._default_risk_areas(center_lat, center_lng)
    
    def _default_risk_areas(self, center_lat, center_lng):
        """
        Generate default risk areas when model prediction fails
        """
        zones = [
            {'radius': 500, 'risk_score': 0.8, 'risk_level': 'Very High'},
            {'radius': 1000, 'risk_score': 0.6, 'risk_level': 'High'},
            {'radius': 2000, 'risk_score': 0.4, 'risk_level': 'Medium'},
            {'radius': 3000, 'risk_score': 0.2, 'risk_level': 'Low'}
        ]
        
        risk_areas = []
        for zone in zones:
            lat_offset = zone['radius'] / 111000
            lng_offset = zone['radius'] / (111000 * np.cos(np.radians(center_lat)))
            
            risk_areas.append({
                'lat': center_lat + (np.random.uniform(-0.5, 0.5) * lat_offset),
                'lng': center_lng + (np.random.uniform(-0.5, 0.5) * lng_offset),
                'risk_score': zone['risk_score'],
                'risk_level': zone['risk_level'],
                'radius': zone['radius']
            })
        
        return risk_areas
    
    def _generate_sample_data(self):
        """Generate sample data for demo purposes when no real data is available"""
        import random
        from datetime import datetime, timedelta
        
        diseases = ['dengue', 'malaria', 'chikungunya', 'zika', 'tuberculosis']
        severities = ['low', 'medium', 'high']
        
        sample_data = []
        for i in range(20):
            # Generate random coordinates around major cities
            base_coords = [
                (12.9716, 77.5946),  # Bangalore
                (19.0760, 72.8777),  # Mumbai
                (28.7041, 77.1025),  # Delhi
                (22.5726, 88.3639),  # Kolkata
                (13.0827, 80.2707),  # Chennai
            ]
            
            base_lat, base_lng = random.choice(base_coords)
            lat = base_lat + random.uniform(-0.5, 0.5)
            lng = base_lng + random.uniform(-0.5, 0.5)
            
            sample_data.append({
                'latitude': lat,
                'longitude': lng,
                'disease_type': random.choice(diseases),
                'severity': random.choice(severities),
                'created_at': (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat()
            })
        
        return sample_data
    
    def save_model(self):
        """Save the trained model to disk"""
        try:
            model_data = {
                'model': self.model,
                'scaler': self.scaler,
                'disease_encoder': self.disease_encoder,
                'is_trained': self.is_trained,
                'feature_columns': self.feature_columns
            }
            
            with open(self.model_path, 'wb') as f:
                pickle.dump(model_data, f)
            
            print("Model saved successfully")
            
        except Exception as e:
            print(f"Error saving model: {str(e)}")
    
    def load_model(self):
        """Load a pre-trained model from disk"""
        try:
            if os.path.exists(self.model_path):
                with open(self.model_path, 'rb') as f:
                    model_data = pickle.load(f)
                
                self.model = model_data['model']
                self.scaler = model_data['scaler']
                self.disease_encoder = model_data['disease_encoder']
                self.is_trained = model_data['is_trained']
                self.feature_columns = model_data['feature_columns']
                
                print("Model loaded successfully")
            
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            self.is_trained = False
