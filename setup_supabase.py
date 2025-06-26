#!/usr/bin/env python3
"""
Simple Supabase schema setup script
"""

import os
import sys
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_supabase_schema():
    """Setup Supabase schema using direct SQL execution"""
    try:
        import psycopg2
        
        database_url = os.getenv('SUPABASE_DATABASE_URL')
        if not database_url:
            logger.error("SUPABASE_DATABASE_URL not found")
            return False
        
        # Connect to database
        logger.info("Connecting to Supabase database...")
        conn = psycopg2.connect(database_url)
        cur = conn.cursor()
        
        # Create the disease_entries table
        schema_sql = """
        -- Create disease_entries table
        CREATE TABLE IF NOT EXISTS disease_entries (
            id SERIAL PRIMARY KEY,
            patient_name VARCHAR(255) DEFAULT 'Anonymous',
            age INTEGER NOT NULL CHECK (age > 0),
            disease_type VARCHAR(100) NOT NULL,
            severity INTEGER DEFAULT 3 CHECK (severity BETWEEN 1 AND 5),
            address TEXT NOT NULL,
            latitude DECIMAL(10, 8),
            longitude DECIMAL(11, 8),
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        
        -- Create indexes for better performance
        CREATE INDEX IF NOT EXISTS idx_disease_entries_disease_type ON disease_entries (disease_type);
        CREATE INDEX IF NOT EXISTS idx_disease_entries_created_at ON disease_entries (created_at);
        CREATE INDEX IF NOT EXISTS idx_disease_entries_severity ON disease_entries (severity);
        CREATE INDEX IF NOT EXISTS idx_disease_entries_location ON disease_entries (latitude, longitude);
        
        -- Enable Row Level Security (RLS)
        ALTER TABLE disease_entries ENABLE ROW LEVEL SECURITY;
        
        -- Create policy for read access
        DROP POLICY IF EXISTS "Enable read access for all users" ON disease_entries;
        CREATE POLICY "Enable read access for all users" ON disease_entries
            FOR SELECT USING (true);
        
        -- Create policy for insert access
        DROP POLICY IF EXISTS "Enable insert access for all users" ON disease_entries;
        CREATE POLICY "Enable insert access for all users" ON disease_entries
            FOR INSERT WITH CHECK (true);
        
        -- Create policy for update access
        DROP POLICY IF EXISTS "Enable update access for all users" ON disease_entries;
        CREATE POLICY "Enable update access for all users" ON disease_entries
            FOR UPDATE USING (true);
        """
        
        # Execute schema
        logger.info("Creating database schema...")
        cur.execute(schema_sql)
        conn.commit()
        
        # Test the table
        cur.execute("SELECT COUNT(*) FROM disease_entries;")
        count = cur.fetchone()[0]
        logger.info(f"✅ Schema created successfully! Current entries: {count}")
        
        cur.close()
        conn.close()
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Schema setup failed: {e}")
        return False

def test_supabase_connection():
    """Test Supabase connection using the Python client"""
    try:
        from supabase_config import get_supabase_manager
        
        logger.info("Testing Supabase client connection...")
        manager = get_supabase_manager()
        
        # Test connection
        response = manager.client.table('disease_entries').select('id').limit(1).execute()
        logger.info("✅ Supabase client connection successful!")
        
        # Get count
        response = manager.client.table('disease_entries').select('id', count='exact').execute()
        count = response.count
        logger.info(f"✅ Current entries in database: {count}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Supabase client test failed: {e}")
        return False

def main():
    print("🚀 Supabase Schema Setup")
    print("=" * 30)
    
    # Check environment variables
    required_vars = ['SUPABASE_URL', 'SUPABASE_ANON_KEY', 'SUPABASE_DATABASE_URL']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"❌ Missing environment variables: {missing_vars}")
        return 1
    
    # Setup schema
    if not setup_supabase_schema():
        return 1
    
    # Test connection
    if not test_supabase_connection():
        return 1
    
    print("\n🎉 Supabase setup completed successfully!")
    print("\nNext steps:")
    print("1. Run your app: python app.py")
    print("2. Test at: http://localhost:5000")
    print("3. Deploy to your chosen platform")
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
