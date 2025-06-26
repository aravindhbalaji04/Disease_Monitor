# 🚀 Deploy to Render - Step by Step Guide

Your Disease Monitoring Portal is ready to deploy to Render! Follow these steps:

## 📋 Prerequisites
- GitHub account
- Render account (free at render.com)
- Your Supabase credentials ready

## 🛠️ Step 1: Push to GitHub

```bash
# Initialize git if not done already
git init

# Add all files
git add .

# Commit your code
git commit -m "Ready for Render deployment"

# Add your GitHub repository
git remote add origin https://github.com/yourusername/disease-monitoring-portal.git

# Push to GitHub
git push -u origin main
```

## 🌐 Step 2: Deploy on Render

### Option A: Using render.yaml (Recommended)
1. Go to [render.com](https://render.com) and sign up/login
2. Click **"New"** → **"Blueprint"**
3. Connect your GitHub repository
4. Render will detect the `render.yaml` file automatically
5. Set your environment variables (see Step 3)
6. Click **"Apply"** to deploy

### Option B: Manual Setup
1. Go to [render.com](https://render.com) and sign up/login
2. Click **"New"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `disease-monitoring-portal`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Add environment variables (see Step 3)
6. Click **"Create Web Service"**

## 🔐 Step 3: Set Environment Variables

In your Render service dashboard, go to **Environment** and add these variables:

```
FLASK_ENV=production
SECRET_KEY=Hwy+mkUB7Gn+DG5P4vAW+WsvLtdh4/G1AROBhGmQYesH5FBO/8YV7U+RRH6rPBEcuCx4ccv1AtjKCLNILijHuA==
SUPABASE_URL=https://wpqgehbmjwesbelimcmt.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndwcWdlaGJtandlc2JlbGltY210Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA4NDEyMjksImV4cCI6MjA2NjQxNzIyOX0.aFlmKjxTMuqbA7rtQv2dKdweAOaY2yLdFwqksz7a6XY
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndwcWdlaGJtandlc2JlbGltY210Iiwicm9zZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MDg0MTIyOSwiZXhwIjoyMDY2NDE3MjI5fQ.5q9PVrJZh9TigbR_3wTtl0VuD3oAty5ij2y_60kqJ9I
SUPABASE_DATABASE_URL=postgresql://postgres:SmoothOperator%4004@db.wpqgehbmjwesbelimcmt.supabase.co:5432/postgres
DATABASE_URL=postgresql://postgres:SmoothOperator%4004@db.wpqgehbmjwesbelimcmt.supabase.co:5432/postgres
```

## ⚡ Step 4: Deploy and Test

1. **Deploy**: Render will automatically build and deploy your app
2. **Monitor**: Watch the build logs in the Render dashboard
3. **Test**: Once deployed, your app will be available at:
   ```
   https://disease-monitoring-portal-XXXX.onrender.com
   ```
4. **Health Check**: Test your deployment:
   ```
   https://your-app-url.onrender.com/health
   ```

## 🔍 Step 5: Verify Deployment

Test these URLs after deployment:
- **Main App**: `https://your-app-url.onrender.com/`
- **Register**: `https://your-app-url.onrender.com/register`
- **Dashboard**: `https://your-app-url.onrender.com/dashboard`
- **API**: `https://your-app-url.onrender.com/api/entries`
- **Health**: `https://your-app-url.onrender.com/health`

## 🎯 Render-Specific Features

### Free Tier Limitations:
- Apps sleep after 15 minutes of inactivity
- 750 build hours per month
- Slower cold starts

### Performance Tips:
- Enable **Auto-Deploy** for automatic updates on git push
- Use **Health Check Path**: `/health`
- Consider upgrading to paid tier for always-on service

## 🔧 Troubleshooting

### Common Issues:

1. **Build Failures**:
   - Check `requirements.txt` for correct package versions
   - Ensure Python version compatibility

2. **Database Connection**:
   - Verify Supabase credentials in environment variables
   - Check URL encoding for special characters in password

3. **App Won't Start**:
   - Verify `gunicorn app:app` command
   - Check logs in Render dashboard

### Debug Commands:
```bash
# Test locally before deployment
python app.py

# Test health endpoint
curl https://your-app-url.onrender.com/health
```

## 🎉 Success!

Once deployed, your Disease Monitoring Portal will be live on Render with:
- ✅ Supabase integration
- ✅ AI risk prediction
- ✅ Interactive maps
- ✅ Real-time dashboard
- ✅ REST API
- ✅ Health monitoring

Your app will automatically redeploy whenever you push changes to GitHub!

---

**🌟 Pro Tips:**
- Set up a custom domain in Render settings
- Enable branch deploys for testing
- Use Render's built-in SSL certificates
- Monitor performance with Render's metrics
