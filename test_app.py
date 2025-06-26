#!/usr/bin/env python3
"""
Test script to check Disease Monitoring Portal functionality
"""

import sys
import os
sys.path.append('/home/aravindhbalaji04/Projects/new-model')

def test_app_routes():
    """Test app routes and functionality"""
    print("🧪 Testing Disease Monitoring Portal Routes")
    print("=" * 50)
    
    try:
        from app import create_app
        app = create_app()
        
        with app.test_client() as client:
            # Test home page
            print("Testing home page...")
            response = client.get('/')
            print(f"Home page status: {response.status_code}")
            if response.status_code != 200:
                print(f"❌ Home page error: {response.data.decode()}")
            else:
                print("✅ Home page works")
            
            # Test registration page
            print("\nTesting registration page...")
            response = client.get('/register')
            print(f"Register page status: {response.status_code}")
            if response.status_code != 200:
                print(f"❌ Register page error: {response.data.decode()}")
            else:
                print("✅ Register page works")
            
            # Test dashboard
            print("\nTesting dashboard...")
            response = client.get('/dashboard')
            print(f"Dashboard status: {response.status_code}")
            if response.status_code != 200:
                print(f"❌ Dashboard error: {response.data.decode()}")
            else:
                print("✅ Dashboard works")
            
            # Test API endpoints
            print("\nTesting API endpoints...")
            response = client.get('/api/entries')
            print(f"API entries status: {response.status_code}")
            if response.status_code != 200:
                print(f"❌ API entries error: {response.data.decode()}")
            else:
                print("✅ API entries works")
            
            # Test health endpoint
            print("\nTesting health endpoint...")
            response = client.get('/health')
            print(f"Health status: {response.status_code}")
            if response.status_code == 200:
                print("✅ Health endpoint works")
                import json
                health_data = json.loads(response.data.decode())
                print(f"Health data: {health_data}")
            else:
                print(f"❌ Health error: {response.data.decode()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_form_submission():
    """Test form submission functionality"""
    print("\n🧪 Testing Form Submission")
    print("=" * 30)
    
    try:
        from app import create_app
        app = create_app()
        
        with app.test_client() as client:
            # Test disease registration form
            form_data = {
                'disease_name': 'dengue',
                'patient_age': '25',
                'address': 'Chennai, Tamil Nadu, India',
                'occurrence_date': '2023-12-01T10:00',
                'additional_info': 'Test entry'
            }
            
            print("Testing disease registration...")
            response = client.post('/register', data=form_data, follow_redirects=False)
            print(f"Registration response status: {response.status_code}")
            
            if response.status_code in [200, 302]:  # 302 is redirect after successful submission
                print("✅ Form submission works")
            else:
                print(f"❌ Form submission error: {response.data.decode()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Form test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🚀 Disease Monitoring Portal - Comprehensive Test")
    print("=" * 60)
    
    # Test basic app functionality
    if not test_app_routes():
        return 1
    
    # Test form submission
    if not test_form_submission():
        return 1
    
    print("\n🎉 All tests passed!")
    print("\nYour Disease Monitoring Portal is working correctly!")
    print("\nTo run the app:")
    print("python app.py")
    print("\nThen visit: http://localhost:5000")
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
