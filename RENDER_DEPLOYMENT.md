# 🚀 Deploy to Render - Web Service Project

Your Disease Monitoring Portal is ready to deploy to Render as a regular web service! This is the simplest and most reliable method.

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

# Add your GitHub repository (replace with your actual repo URL)
git remote add origin https://github.com/yourusername/disease-monitoring-portal.git

# Push to GitHub
git push -u origin main
```

## 🌐 Step 2: Deploy on Render (Web Service)

### Simple Web Service Deployment:
1. Go to [render.com](https://render.com) and sign up/login
2. Click **"New"** → **"Web Service"**
3. **Connect Repository**: Select your GitHub repository
4. **Configure Service**:
   - **Name**: `disease-monitoring-portal`
   - **Environment**: `Python 3`
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. **Environment Variables**: Add all variables (see Step 3)
6. **Create Web Service**: Click to deploy

## 🔐 Step 3: Set Environment Variables

In your Render service dashboard, go to **Environment** tab and add these variables:

```env
FLASK_ENV=production
SECRET_KEY=Hwy+mkUB7Gn+DG5P4vAW+WsvLtdh4/G1AROBhGmQYesH5FBO/8YV7U+RRH6rPBEcuCx4ccv1AtjKCLNILijHuA==
SUPABASE_URL=https://wpqgehbmjwesbelimcmt.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndwcWdlaGJtandlc2JlbGltY210Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA4NDEyMjksImV4cCI6MjA2NjQxNzIyOX0.aFlmKjxTMuqbA7rtQv2dKdweAOaY2yLdFwqksz7a6XY
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndwcWdlaGJtandlc2JlbGltY210Iiwicm9zZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MDg0MTIyOSwiZXhwIjoyMDY2NDE3MjI5fQ.5q9PVrJZh9TigbR_3wTtl0VuD3oAty5ij2y_60kqJ9I
SUPABASE_DATABASE_URL=postgresql://postgres:SmoothOperator%4004@db.wpqgehbmjwesbelimcmt.supabase.co:5432/postgres
DATABASE_URL=postgresql://postgres:SmoothOperator%4004@db.wpqgehbmjwesbelimcmt.supabase.co:5432/postgres
```

### 💡 **Pro Tips for Environment Variables:**
- Click **"Add Environment Variable"** for each one
- Copy-paste carefully to avoid typos
- Use the **"Hide"** option for sensitive values like keys
- Save after adding all variables

## ⚡ Step 4: Deploy and Monitor

1. **Deploy**: Click **"Create Web Service"** to start deployment
2. **Monitor Build**: Watch the build logs in real-time
3. **Wait**: Initial deployment takes 3-5 minutes
4. **Live URL**: Your app will be available at:
   ```
   https://disease-monitoring-portal-XXXX.onrender.com
   ```

## 🔍 Step 5: Verify Deployment

Test these URLs after deployment:
- **Main App**: `https://your-app-url.onrender.com/`
- **Health Check**: `https://your-app-url.onrender.com/health`
- **Register**: `https://your-app-url.onrender.com/register`
- **Dashboard**: `https://your-app-url.onrender.com/dashboard`
- **API**: `https://your-app-url.onrender.com/api/entries`

### Quick Health Check:
```bash
curl https://your-app-url.onrender.com/health
```
Should return:
```json
{
  "status": "healthy",
  "supabase": true,
  "local_db": false,
  "timestamp": "2025-06-26T..."
}
```

## 🎯 Render Web Service Features

### ✅ **Advantages of Web Service vs Blueprint:**
- **Simpler Setup**: No YAML configuration needed
- **Direct Control**: Full control over build and start commands
- **Easy Updates**: Simple environment variable management
- **Better Debugging**: Clear build logs and error messages
- **Flexible Configuration**: Easy to modify settings

### 📊 **Free Tier Benefits:**
- 750 build hours per month
- Automatic SSL certificates
- Custom domains (paid plans)
- Built-in monitoring
- Automatic restarts on failure

### ⚠️ **Free Tier Limitations:**
- Apps sleep after 15 minutes of inactivity
- Slower cold starts (15-30 seconds)
- Limited concurrent connections

## 🔧 Advanced Configuration

### Auto-Deploy Setup:
1. In your service dashboard, go to **Settings**
2. Enable **Auto-Deploy** from GitHub
3. Choose branch (usually `main`)
4. Now every git push will trigger automatic deployment

### Health Check Configuration:
1. Go to **Settings** → **Health & Alerts**
2. Set **Health Check Path**: `/health`
3. Configure alert notifications

### Custom Domain (Paid Plans):
1. Go to **Settings** → **Custom Domains**
2. Add your domain
3. Update DNS records as instructed

## 🔧 Troubleshooting

### Common Issues:

1. **Build Failures**:
   ```
   - Check requirements.txt for correct versions
   - Ensure Python version compatibility (3.8+)
   - Verify all dependencies are included
   ```

2. **App Won't Start**:
   ```
   - Verify start command: gunicorn app:app
   - Check environment variables are set
   - Review application logs
   ```

3. **Database Connection Errors**:
   ```
   - Verify Supabase credentials in environment variables
   - Check URL encoding for special characters in password
   - Test Supabase connection from local machine
   ```

4. **Slow Performance**:
   ```
   - Cold starts are normal on free tier
   - Consider upgrading to paid tier for always-on
   - Optimize app startup time
   ```

### Debug Steps:
1. **Check Build Logs**: Review complete build process
2. **Check Application Logs**: Look for runtime errors
3. **Test Locally**: Ensure app works with production settings
4. **Verify Environment**: Double-check all environment variables

### Useful Commands:
```bash
# Test production build locally
FLASK_ENV=production python app.py

# Test health endpoint
curl -X GET https://your-app.onrender.com/health

# Check app status
curl -I https://your-app.onrender.com/
```

## 🎉 Success!

Once deployed, your Disease Monitoring Portal will be live with:
- ✅ **AI Risk Prediction**: Random Forest model for disease outbreak prediction
- ✅ **Interactive Maps**: Folium-powered risk visualization
- ✅ **Supabase Integration**: Production-ready database
- ✅ **RESTful API**: Programmatic access to disease data
- ✅ **Real-time Dashboard**: Analytics and monitoring
- ✅ **Mobile Responsive**: Works on all devices
- ✅ **Security Features**: Input validation, CSRF protection
- ✅ **Health Monitoring**: Built-in status checks

### 🔄 **Automatic Updates:**
- Push to GitHub → Automatic deployment
- Zero-downtime deployments
- Rollback capability

---

**🌟 Your Disease Monitoring Portal is now helping public health teams worldwide!** 🏥🌍

**Deployment Time**: ~5 minutes | **Cost**: Free tier available | **Scalability**: Production-ready
