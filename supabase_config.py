"""
Supabase configuration and integration utilities
"""
import os
from typing import Optional, Dict, Any
import logging
from supabase import create_client, Client
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import psycopg2
from datetime import datetime

logger = logging.getLogger(__name__)

class SupabaseConfig:
    """Configuration class for Supabase integration"""
    
    def __init__(self):
        self.url = os.getenv('SUPABASE_URL')
        self.key = os.getenv('SUPABASE_ANON_KEY')
        self.service_role_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
        self.database_url = os.getenv('SUPABASE_DATABASE_URL')
        
        if not self.url or not self.key:
            raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set")
    
    def get_client(self) -> Client:
        """Get Supabase client instance"""
        return create_client(self.url, self.key)
    
    def get_admin_client(self) -> Optional[Client]:
        """Get Supabase admin client with service role key"""
        if self.service_role_key:
            return create_client(self.url, self.service_role_key)
        return None

class SupabaseManager:
    """Manager class for Supabase operations"""
    
    def __init__(self):
        self.config = SupabaseConfig()
        self.client = self.config.get_client()
        self.admin_client = self.config.get_admin_client()
    
    def test_connection(self) -> bool:
        """Test Supabase connection"""
        try:
            # Test with a simple query
            response = self.client.table('disease_entries').select('id').limit(1).execute()
            logger.info("Supabase connection successful")
            return True
        except Exception as e:
            logger.error(f"Supabase connection failed: {e}")
            return False
    
    def create_disease_entry(self, entry_data: Dict[str, Any]) -> Optional[Dict]:
        """Create a new disease entry in Supabase"""
        try:
            response = self.client.table('disease_entries').insert(entry_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Failed to create disease entry: {e}")
            return None
    
    def get_disease_entries(self, limit: int = 100, offset: int = 0) -> list:
        """Get disease entries from Supabase"""
        try:
            response = (self.client.table('disease_entries')
                       .select('*')
                       .range(offset, offset + limit - 1)
                       .order('created_at', desc=True)
                       .execute())
            return response.data
        except Exception as e:
            logger.error(f"Failed to get disease entries: {e}")
            return []
    
    def get_entries_for_ml(self) -> list:
        """Get disease entries formatted for ML model"""
        try:
            response = (self.client.table('disease_entries')
                       .select('latitude,longitude,disease_type,severity,created_at')
                       .execute())
            return response.data
        except Exception as e:
            logger.error(f"Failed to get ML data: {e}")
            return []
    
    def setup_database_schema(self):
        """Setup database schema in Supabase (run once)"""
        if not self.admin_client:
            logger.error("Admin client not available for schema setup")
            return False
        
        try:
            # Create disease_entries table
            schema_sql = """
            -- Enable PostGIS if not already enabled
            CREATE EXTENSION IF NOT EXISTS postgis;
            
            -- Create disease_entries table
            CREATE TABLE IF NOT EXISTS disease_entries (
                id SERIAL PRIMARY KEY,
                patient_name VARCHAR(255) NOT NULL,
                age INTEGER NOT NULL CHECK (age > 0),
                disease_type VARCHAR(100) NOT NULL,
                severity INTEGER NOT NULL CHECK (severity BETWEEN 1 AND 5),
                address TEXT NOT NULL,
                latitude DECIMAL(10, 8),
                longitude DECIMAL(11, 8),
                location_point GEOGRAPHY(POINT, 4326),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
            
            -- Create indexes for better performance
            CREATE INDEX IF NOT EXISTS idx_disease_entries_location ON disease_entries USING GIST (location_point);
            CREATE INDEX IF NOT EXISTS idx_disease_entries_disease_type ON disease_entries (disease_type);
            CREATE INDEX IF NOT EXISTS idx_disease_entries_created_at ON disease_entries (created_at);
            CREATE INDEX IF NOT EXISTS idx_disease_entries_severity ON disease_entries (severity);
            
            -- Create function to update location_point from lat/lon
            CREATE OR REPLACE FUNCTION update_location_point()
            RETURNS TRIGGER AS $$
            BEGIN
                IF NEW.latitude IS NOT NULL AND NEW.longitude IS NOT NULL THEN
                    NEW.location_point = ST_GeogFromText('POINT(' || NEW.longitude || ' ' || NEW.latitude || ')');
                END IF;
                NEW.updated_at = NOW();
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
            
            -- Create trigger to automatically update location_point
            DROP TRIGGER IF EXISTS trigger_update_location_point ON disease_entries;
            CREATE TRIGGER trigger_update_location_point
                BEFORE INSERT OR UPDATE ON disease_entries
                FOR EACH ROW
                EXECUTE FUNCTION update_location_point();
            
            -- Enable Row Level Security (RLS)
            ALTER TABLE disease_entries ENABLE ROW LEVEL SECURITY;
            
            -- Create policy for read access
            CREATE POLICY IF NOT EXISTS "Enable read access for all users" ON disease_entries
                FOR SELECT USING (true);
            
            -- Create policy for insert access
            CREATE POLICY IF NOT EXISTS "Enable insert access for all users" ON disease_entries
                FOR INSERT WITH CHECK (true);
            """
            
            # Execute schema setup
            if self.config.database_url:
                import psycopg2
                conn = psycopg2.connect(self.config.database_url)
                cur = conn.cursor()
                cur.execute(schema_sql)
                conn.commit()
                cur.close()
                conn.close()
                logger.info("Database schema setup completed")
                return True
            else:
                logger.error("Database URL not available for schema setup")
                return False
                
        except Exception as e:
            logger.error(f"Failed to setup database schema: {e}")
            return False

# Global instance
supabase_manager = None

def get_supabase_manager() -> SupabaseManager:
    """Get or create Supabase manager instance"""
    global supabase_manager
    if supabase_manager is None:
        supabase_manager = SupabaseManager()
    return supabase_manager
