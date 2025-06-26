# Complete Deployment Guide

This guide covers hosting your Disease Monitoring Portal on various platforms and integrating with Supabase.

## 🚀 Quick Start with Supabase

### Step 1: Set up Supabase Project

1. Go to [supabase.com](https://supabase.com) and create a new project
2. Note down your project URL and API keys from Settings > API
3. Copy your database connection string from Settings > Database

### Step 2: Configure Environment Variables

Create a `.env` file based on `.env.example`:

```bash
# Copy the example file
cp .env.example .env

# Edit with your Supabase credentials
nano .env
```

Fill in your Supabase details:
```env
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
SUPABASE_DATABASE_URL=postgresql://postgres:[password]@db.[project-ref].supabase.co:5432/postgres
```

### Step 3: Set up Database Schema

Run the schema setup script:

```python
python setup_database.py
```

## 🌐 Hosting Options

### Option 1: Railway (Recommended - Easy)

1. **Create Railway Account**: Go to [railway.app](https://railway.app)

2. **Deploy from GitHub**:
   ```bash
   # Push your code to GitHub first
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

3. **Connect Repository**: 
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository

4. **Set Environment Variables**:
   - Go to Variables tab
   - Add all variables from your `.env` file

5. **Deploy**: Railway will automatically deploy your app

### Option 2: Render

1. **Create Render Account**: Go to [render.com](https://render.com)

2. **Create Web Service**:
   - Connect your GitHub repository
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`

3. **Environment Variables**: Add your Supabase credentials

### Option 3: Heroku

1. **Install Heroku CLI**: 
   ```bash
   # Install Heroku CLI
   curl https://cli-assets.heroku.com/install.sh | sh
   
   # Login to Heroku
   heroku login
   ```

2. **Create Heroku App**:
   ```bash
   heroku create your-disease-portal
   ```

3. **Set Environment Variables**:
   ```bash
   heroku config:set FLASK_ENV=production
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set SUPABASE_URL=your-supabase-url
   heroku config:set SUPABASE_ANON_KEY=your-anon-key
   heroku config:set SUPABASE_DATABASE_URL=your-database-url
   ```

4. **Deploy**:
   ```bash
   git push heroku main
   ```

### Option 4: DigitalOcean App Platform

1. **Create DigitalOcean Account**: Go to [digitalocean.com](https://digitalocean.com)

2. **Create App**:
   - Apps → Create App
   - Connect GitHub repository
   - Choose Python as runtime

3. **Configure**:
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `gunicorn app:app`
   - Add environment variables

## 🔧 Local Development with Supabase

### Setup Virtual Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Initialize Database

```python
# Run the database setup
python -c "from supabase_config import get_supabase_manager; get_supabase_manager().setup_database_schema()"
```

### Run Development Server

```bash
python app.py
```

## 📊 Testing Your Deployment

### 1. Health Check Endpoint

Your app includes a health check endpoint at `/health`. Test it:

```bash
curl https://your-app-url.com/health
```

### 2. API Endpoints

Test the API endpoints:

```bash
# Get all entries
curl https://your-app-url.com/api/entries

# Get risk prediction
curl -X POST https://your-app-url.com/api/predict \
  -H "Content-Type: application/json" \
  -d '{"latitude": 40.7128, "longitude": -74.0060}'
```

## 🛠️ Production Optimizations

### 1. Environment Configuration

Make sure your production environment has:
- `FLASK_ENV=production`
- Strong `SECRET_KEY`
- Proper database connection pooling

### 2. Monitoring Setup

Add logging and monitoring:

```python
import logging
logging.basicConfig(level=logging.INFO)
```

### 3. Security Headers

Add security headers in production:

```python
from flask_talisman import Talisman

# Add to your app.py
Talisman(app)
```

## 🔍 Troubleshooting

### Common Issues:

1. **Database Connection Errors**:
   - Check your `SUPABASE_DATABASE_URL`
   - Ensure your IP is whitelisted in Supabase

2. **Import Errors**:
   - Make sure all dependencies are in `requirements.txt`
   - Check Python version compatibility

3. **Geocoding Issues**:
   - The app gracefully handles geocoding failures
   - Consider adding a geocoding API key for better reliability

### Debug Mode:

For debugging, set:
```env
FLASK_ENV=development
FLASK_DEBUG=True
```

## 📈 Scaling Considerations

1. **Database Connection Pooling**: Configure proper connection pooling
2. **Caching**: Add Redis caching for frequently accessed data
3. **Load Balancing**: Use multiple instances behind a load balancer
4. **CDN**: Serve static assets through a CDN

## 🔐 Security Best Practices

1. **Environment Variables**: Never commit secrets to version control
2. **HTTPS**: Always use HTTPS in production
3. **Input Validation**: The app includes comprehensive input validation
4. **SQL Injection**: Using SQLAlchemy ORM prevents SQL injection
5. **Rate Limiting**: Consider adding rate limiting for API endpoints

## 📞 Support

If you encounter issues:
1. Check the application logs
2. Verify environment variables
3. Test database connectivity
4. Check Supabase dashboard for errors

Your Disease Monitoring Portal is now ready for production deployment! 🎉
