#!/usr/bin/env python3
"""
Quick dependency verification script for Render deployment
Tests all critical imports to ensure compatibility
"""

import sys
print(f"Python version: {sys.version}")

try:
    import flask
    try:
        print(f"✅ Flask {flask.__version__}")
    except AttributeError:
        print("✅ Flask import successful (version info not available)")
except ImportError as e:
    print(f"❌ Flask import failed: {e}")
    sys.exit(1)

try:
    from flask_wtf import FlaskForm
    print("✅ Flask-WTF import successful")
except ImportError as e:
    print(f"❌ Flask-WTF import failed: {e}")
    sys.exit(1)

try:
    import werkzeug
    try:
        print(f"✅ Werkzeug {werkzeug.__version__}")
    except AttributeError:
        print("✅ Werkzeug import successful (version info not available)")
except ImportError as e:
    print(f"❌ Werkzeug import failed: {e}")
    sys.exit(1)

try:
    import wtforms
    print(f"✅ WTForms {wtforms.__version__}")
except ImportError as e:
    print(f"❌ WTForms import failed: {e}")
    sys.exit(1)

try:
    import sklearn
    print(f"✅ Scikit-learn {sklearn.__version__}")
except ImportError as e:
    print(f"❌ Scikit-learn import failed: {e}")
    sys.exit(1)

try:
    import pandas as pd
    print(f"✅ Pandas {pd.__version__}")
except ImportError as e:
    print(f"❌ Pandas import failed: {e}")
    sys.exit(1)

try:
    import numpy as np
    print(f"✅ NumPy {np.__version__}")
except ImportError as e:
    print(f"❌ NumPy import failed: {e}")
    sys.exit(1)

try:
    import folium
    print(f"✅ Folium {folium.__version__}")
except ImportError as e:
    print(f"❌ Folium import failed: {e}")
    sys.exit(1)

try:
    import supabase
    print("✅ Supabase import successful")
except ImportError as e:
    print(f"❌ Supabase import failed: {e}")
    sys.exit(1)

try:
    import gunicorn
    print(f"✅ Gunicorn {gunicorn.__version__}")
except ImportError as e:
    print(f"❌ Gunicorn import failed: {e}")
    sys.exit(1)

# Test the specific Flask-WTF import that was failing
try:
    from werkzeug.urls import url_encode
    print("✅ Werkzeug url_encode available (old API)")
except ImportError:
    try:
        from urllib.parse import urlencode as url_encode
        print("✅ Using urllib.parse.urlencode (new API)")
    except ImportError as e:
        print(f"❌ URL encoding function not available: {e}")
        sys.exit(1)

# Test main app import
try:
    import app
    print("✅ Main app.py import successful")
except ImportError as e:
    print(f"❌ Main app import failed: {e}")
    sys.exit(1)

print("\n🎉 All critical dependencies verified successfully!")
print("🚀 Ready for Render deployment!")
