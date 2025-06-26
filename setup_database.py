#!/usr/bin/env python3
"""
Database setup script for Disease Monitoring Portal
This script sets up the database schema in Supabase
"""

import os
import sys
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_database():
    """Setup database schema and initial data"""
    try:
        # Import after loading environment variables
        from supabase_config import get_supabase_manager
        from database_models import db, DiseaseEntry
        from app import create_app
        
        logger.info("Starting database setup...")
        
        # Test Supabase connection
        supabase_manager = get_supabase_manager()
        if not supabase_manager.test_connection():
            logger.error("Failed to connect to Supabase")
            return False
        
        # Setup database schema in Supabase
        logger.info("Setting up database schema...")
        if supabase_manager.setup_database_schema():
            logger.info("✅ Database schema setup completed successfully")
        else:
            logger.error("❌ Failed to setup database schema")
            return False
        
        # Create Flask app and setup SQLAlchemy tables (for local development)
        if os.getenv('FLASK_ENV') == 'development':
            logger.info("Setting up local SQLAlchemy tables...")
            app = create_app()
            with app.app_context():
                db.create_all()
                logger.info("✅ Local SQLAlchemy tables created")
        
        # Generate sample data if requested
        if len(sys.argv) > 1 and sys.argv[1] == '--sample-data':
            logger.info("Generating sample data...")
            from sample_data import generate_sample_data
            entries = generate_sample_data(50)
            
            # Insert sample data into Supabase
            for entry_data in entries:
                # Convert the entry data to dict format for Supabase
                supabase_data = {
                    'patient_name': entry_data['patient_name'],
                    'age': entry_data['age'],
                    'disease_type': entry_data['disease_type'],
                    'severity': entry_data['severity'],
                    'address': entry_data['address'],
                    'latitude': entry_data['latitude'],
                    'longitude': entry_data['longitude'],
                    'created_at': entry_data['date_reported'].isoformat()
                }
                
                result = supabase_manager.create_disease_entry(supabase_data)
                if not result:
                    logger.warning(f"Failed to insert sample entry: {entry_data['patient_name']}")
            
            logger.info("✅ Sample data generated and inserted")
        
        logger.info("🎉 Database setup completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Database setup failed: {e}")
        return False

def verify_setup():
    """Verify that the database setup is working correctly"""
    try:
        from supabase_config import get_supabase_manager
        
        logger.info("Verifying database setup...")
        
        supabase_manager = get_supabase_manager()
        
        # Test connection
        if not supabase_manager.test_connection():
            logger.error("❌ Database connection failed")
            return False
        
        # Test data retrieval
        entries = supabase_manager.get_disease_entries(limit=5)
        logger.info(f"✅ Successfully retrieved {len(entries)} entries")
        
        # Test ML data retrieval
        ml_data = supabase_manager.get_entries_for_ml()
        logger.info(f"✅ Successfully retrieved {len(ml_data)} entries for ML")
        
        logger.info("🎉 Database verification completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Database verification failed: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Disease Monitoring Portal - Database Setup")
    print("=" * 50)
    
    # Check environment variables
    required_vars = ['SUPABASE_URL', 'SUPABASE_ANON_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"❌ Missing required environment variables: {missing_vars}")
        logger.error("Please set up your .env file with Supabase credentials")
        return 1
    
    # Setup database
    if not setup_database():
        logger.error("❌ Database setup failed")
        return 1
    
    # Verify setup
    if not verify_setup():
        logger.error("❌ Database verification failed")
        return 1
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Run the application: python app.py")
    print("2. Open your browser to: http://localhost:5000")
    print("3. Register some disease entries to test the system")
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
