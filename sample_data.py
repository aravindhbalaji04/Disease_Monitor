from database_models import db, DiseaseEntry
from datetime import datetime, timedelta
import random

def create_sample_data():
    """Create sample disease entries for testing and initial model training"""
    
    # Sample locations (latitude, longitude) with addresses
    sample_locations = [
        (13.0827, 80.2707, "Anna Nagar, Chennai, Tamil Nadu"),
        (13.0650, 80.2849, "T. Nagar, Chennai, Tamil Nadu"),
        (13.0878, 80.2785, "Kodambakkam, Chennai, Tamil Nadu"),
        (13.0569, 80.2378, "Adyar, Chennai, Tamil Nadu"),
        (13.1185, 80.2574, "Kilpauk, Chennai, Tamil Nadu"),
        (13.0475, 80.2540, "Mylapore, Chennai, Tamil Nadu"),
        (13.1067, 80.2206, "Velachery, Chennai, Tamil Nadu"),
        (13.0338, 80.2465, "Besant Nagar, Chennai, Tamil Nadu"),
        (13.1143, 80.2329, "Tambaram, Chennai, Tamil Nadu"),
        (13.0475, 80.1982, "Porur, Chennai, Tamil Nadu"),
        (13.0732, 80.2609, "Nungambakkam, Chennai, Tamil Nadu"),
        (13.0418, 80.2341, "Guindy, Chennai, Tamil Nadu"),
        (13.1305, 80.2155, "Ambattur, Chennai, Tamil Nadu"),
        (13.0902, 80.2093, "Koyambedu, Chennai, Tamil Nadu"),
        (13.0524, 80.2102, "Ashok Nagar, Chennai, Tamil Nadu"),
        
        # Mumbai locations
        (19.0760, 72.8777, "Mumbai Central, Mumbai, Maharashtra"),
        (19.0330, 72.8697, "Colaba, Mumbai, Maharashtra"),
        (19.0596, 72.8295, "Andheri, Mumbai, Maharashtra"),
        (19.1136, 72.8697, "Bandra, Mumbai, Maharashtra"),
        (19.0176, 72.8562, "Churchgate, Mumbai, Maharashtra"),
        
        # Delhi locations
        (28.6139, 77.2090, "Connaught Place, New Delhi, Delhi"),
        (28.5355, 77.3910, "Noida, Uttar Pradesh"),
        (28.4595, 77.0266, "Gurgaon, Haryana"),
        (28.7041, 77.1025, "Rohini, New Delhi, Delhi"),
        (28.5494, 77.2500, "Lajpat Nagar, New Delhi, Delhi"),
        
        # Bangalore locations
        (12.9716, 77.5946, "Koramangala, Bangalore, Karnataka"),
        (12.9698, 77.7499, "Whitefield, Bangalore, Karnataka"),
        (12.9279, 77.6271, "Jayanagar, Bangalore, Karnataka"),
        (12.9141, 77.6101, "JP Nagar, Bangalore, Karnataka"),
        (13.0067, 77.5636, "Malleswaram, Bangalore, Karnataka")
    ]
    
    # Disease types with different prevalence
    diseases = [
        ('dengue', 25),
        ('malaria', 20),
        ('chikungunya', 15),
        ('typhoid', 12),
        ('covid19', 18),
        ('tuberculosis', 8),
        ('hepatitis_a', 7),
        ('influenza', 10),
        ('other', 5)
    ]
    
    # Create weighted disease list for random selection
    disease_list = []
    for disease, weight in diseases:
        disease_list.extend([disease] * weight)
    
    # Generate sample entries
    sample_entries = []
    
    # Generate entries for the past 2 years
    start_date = datetime.now() - timedelta(days=730)
    
    for i in range(200):  # Create 200 sample entries
        # Random date in the past 2 years
        random_days = random.randint(0, 730)
        occurrence_date = start_date + timedelta(days=random_days)
        
        # Random location
        lat, lng, address = random.choice(sample_locations)
        
        # Add some random variation to coordinates (within ~1km)
        lat += random.uniform(-0.01, 0.01)
        lng += random.uniform(-0.01, 0.01)
        
        # Random disease
        disease = random.choice(disease_list)
        
        # Random age (weighted towards common age groups)
        age_groups = [
            (random.randint(0, 10), 15),    # Children
            (random.randint(11, 25), 20),   # Young adults
            (random.randint(26, 45), 30),   # Adults
            (random.randint(46, 65), 25),   # Middle-aged
            (random.randint(66, 90), 10)    # Elderly
        ]
        
        age_list = []
        for age_range, weight in age_groups:
            age_list.extend([age_range] * weight)
        
        age = random.choice(age_list)
        
        # Additional info (some entries have it, some don't)
        additional_info = ""
        if random.random() < 0.3:  # 30% chance of having additional info
            info_options = [
                "Patient had fever and body aches",
                "Severe symptoms reported",
                "Mild case, recovered quickly",
                "Hospital admission required",
                "Outpatient treatment",
                "Contact tracing initiated",
                "Travel history present",
                "No travel history"
            ]
            additional_info = random.choice(info_options)
        
        entry = DiseaseEntry(
            disease_name=disease,
            patient_age=age,
            address=address,
            latitude=lat,
            longitude=lng,
            additional_info=additional_info,
            occurrence_date=occurrence_date
        )
        
        sample_entries.append(entry)
    
    # Add all entries to database
    try:
        db.session.add_all(sample_entries)
        db.session.commit()
        print(f"Successfully created {len(sample_entries)} sample disease entries")
        
        # Print some statistics
        from collections import Counter
        disease_counts = Counter([entry.disease_name for entry in sample_entries])
        print("\nDisease distribution:")
        for disease, count in disease_counts.items():
            print(f"  {disease.title()}: {count}")
            
    except Exception as e:
        db.session.rollback()
        print(f"Error creating sample data: {str(e)}")

if __name__ == "__main__":
    from app import app
    with app.app_context():
        db.create_all()
        create_sample_data()
