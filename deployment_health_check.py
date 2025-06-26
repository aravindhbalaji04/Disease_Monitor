#!/usr/bin/env python3
"""
Post-deployment health check for Render
"""

import requests
import sys
import json
from datetime import datetime

def check_deployment_health(base_url):
    """Check if the deployed app is healthy"""
    
    print("🏥 Disease Monitoring Portal - Deployment Health Check")
    print("=" * 60)
    print(f"Testing: {base_url}")
    print(f"Time: {datetime.now().isoformat()}")
    print()
    
    tests = [
        ("Main Page", "/"),
        ("Health Check", "/health"),
        ("Registration Page", "/register"),
        ("Dashboard", "/dashboard"),
        ("API Entries", "/api/entries")
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, endpoint in tests:
        try:
            url = f"{base_url}{endpoint}"
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                print(f"✅ {test_name}: PASS ({response.status_code})")
                passed += 1
                
                # Special check for health endpoint
                if endpoint == "/health":
                    try:
                        health_data = response.json()
                        print(f"   Supabase: {'✅' if health_data.get('supabase') else '❌'}")
                        print(f"   Status: {health_data.get('status', 'unknown')}")
                    except:
                        pass
                        
            else:
                print(f"❌ {test_name}: FAIL ({response.status_code})")
                
        except requests.exceptions.Timeout:
            print(f"⏰ {test_name}: TIMEOUT (>30s)")
        except requests.exceptions.RequestException as e:
            print(f"❌ {test_name}: ERROR ({str(e)[:50]}...)")
        except Exception as e:
            print(f"❌ {test_name}: UNEXPECTED ERROR ({str(e)[:50]}...)")
    
    print()
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your deployment is healthy! 🎉")
        print()
        print("🌟 Your Disease Monitoring Portal is live and ready!")
        print(f"🔗 Visit: {base_url}")
        return True
    else:
        print("⚠️  Some tests failed. Check the Render logs for details.")
        return False

def main():
    """Main function"""
    if len(sys.argv) != 2:
        print("Usage: python deployment_health_check.py <your-render-url>")
        print("Example: python deployment_health_check.py https://disease-monitoring-portal-abc123.onrender.com")
        return 1
    
    base_url = sys.argv[1].rstrip('/')
    
    if check_deployment_health(base_url):
        return 0
    else:
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
