# 🔧 Render Deployment Troubleshooting

## Issue: ModuleNotFoundError: No module named 'your_application'

### **Problem**: 
Render is using the wrong start command `gunicorn your_application.wsgi` instead of `gunicorn app:app`.

### **Root Cause**: 
Render's auto-detection sometimes suggests Django-style commands for Flask apps.

### **Solutions**:

#### **Solution 1: Manual Override (Recommended)**
1. Go to your Render service dashboard
2. Click on **"Settings"** tab
3. Scroll to **"Start Command"** field
4. **Clear** any auto-detected command
5. **Enter manually**: `gunicorn app:app --bind 0.0.0.0:$PORT`
6. Click **"Save Changes"**
7. **Manual Deploy** to trigger redeploy

#### **Solution 2: Use Start Script**
1. In Render dashboard, set Start Command to: `./start.sh`
2. This uses the included backup start script
3. Save and redeploy

#### **Solution 3: Force Procfile Recognition**
1. Ensure Procfile contains: `web: gunicorn app:app --bind 0.0.0.0:$PORT`
2. Leave Start Command **empty** in Render dashboard
3. Render should auto-detect from Procfile
4. If not, use Solution 1

### **Verification**:
After fixing, your app should start successfully and show:
```
Starting Disease Monitoring Portal...
Python version: Python 3.11.0
Gunicorn version: gunicorn (version 21.2.0)
[INFO] Starting gunicorn 21.2.0
[INFO] Listening at: http://0.0.0.0:10000
```

### **Test Your Deployment**:
```bash
# Health check
curl https://your-app-url.onrender.com/health

# Should return:
{
  "status": "healthy",
  "supabase": true,
  "local_db": false
}
```

### **Common Render Deployment Issues**:

1. **Wrong Start Command** ← **(YOU ARE HERE)**
2. **Missing Environment Variables**
3. **Build Command Issues**
4. **Port Binding Problems**
5. **Database Connection Failures**

### **Quick Debug Commands**:
```bash
# Test locally first
gunicorn app:app --bind 0.0.0.0:5000

# Check if app module exists
python -c "import app; print('App module found')"

# Verify requirements
pip list | grep -E "(flask|gunicorn|supabase)"
```

### **Need More Help?**
- Check Render build logs for specific errors
- Verify all environment variables are set
- Test the app locally with the same command
- Review RENDER_DEPLOYMENT.md for full instructions
