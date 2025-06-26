#!/usr/bin/env python3
"""
Setup Supabase tables using SQL Editor
"""

import os
from dotenv import load_dotenv

load_dotenv()

def print_sql_setup():
    """Print the SQL commands to run in Supabase SQL Editor"""
    
    print("🚀 Supabase Database Setup Instructions")
    print("=" * 50)
    print()
    print("1. Go to your Supabase project: https://supabase.com/dashboard/project/wpqgehbmjwesbelimcmt")
    print("2. Click on 'SQL Editor' in the left sidebar")
    print("3. Click 'New Query' and copy-paste the following SQL:")
    print()
    print("=" * 50)
    print("📝 SQL TO RUN IN SUPABASE SQL EDITOR:")
    print("=" * 50)
    
    sql_script = """
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

-- Insert some sample data
INSERT INTO disease_entries (patient_name, age, disease_type, severity, address, latitude, longitude) VALUES
('Anonymous', 25, 'dengue', 3, 'Mumbai, Maharashtra, India', 19.0760, 72.8777),
('Anonymous', 34, 'malaria', 4, 'Delhi, India', 28.7041, 77.1025),
('Anonymous', 45, 'typhoid', 2, 'Bangalore, Karnataka, India', 12.9716, 77.5946),
('Anonymous', 28, 'covid19', 3, 'Chennai, Tamil Nadu, India', 13.0827, 80.2707),
('Anonymous', 52, 'tuberculosis', 4, 'Kolkata, West Bengal, India', 22.5726, 88.3639);

-- Check if everything was created successfully
SELECT 'Table created successfully!' as status, COUNT(*) as sample_entries FROM disease_entries;
"""
    
    print(sql_script)
    print("=" * 50)
    print()
    print("4. Click 'Run' to execute the SQL")
    print("5. You should see 'Table created successfully!' with sample entries count")
    print()
    print("✅ After running the SQL, your database will be ready!")
    print()

def test_connection():
    """Test the connection after setup"""
    try:
        from supabase_config import get_supabase_manager
        
        print("🧪 Testing connection...")
        manager = get_supabase_manager()
        
        # Test connection
        response = manager.client.table('disease_entries').select('id').limit(1).execute()
        count = len(response.data)
        print(f"✅ Connection successful! Found {count} entries")
        
        # Show sample entry
        if response.data:
            print("📝 Sample entry:", response.data[0])
        
        return True
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

if __name__ == "__main__":
    print_sql_setup()
    
    input("\nPress Enter after you've run the SQL in Supabase SQL Editor...")
    
    if test_connection():
        print("\n🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Run your app: python app.py")
        print("2. Test registration at: http://localhost:5000/register")
        print("3. Deploy to Railway/Render/Heroku")
    else:
        print("\n⚠️  Connection test failed. Please check:")
        print("1. Did you run the SQL in Supabase SQL Editor?")
        print("2. Are your environment variables correct?")
        print("3. Try refreshing your Supabase project")
