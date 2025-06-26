#!/bin/bash

# Disease Monitoring Portal - Quick Setup Script
# This script helps you set up the application quickly

set -e  # Exit on any error

echo "🚀 Disease Monitoring Portal - Quick Setup"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN} $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}  $1${NC}"
}

print_error() {
    echo -e "${RED} $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ  $1${NC}"
}

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is required but not installed"
    exit 1
fi

print_status "Python 3 found"

# Check if pip is installed
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    print_error "pip is required but not installed"
    exit 1
fi

print_status "pip found"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_info "Creating virtual environment..."
    python3 -m venv venv
    print_status "Virtual environment created"
else
    print_info "Virtual environment already exists"
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_info "Upgrading pip..."
pip install --upgrade pip

# Install requirements
print_info "Installing dependencies..."
pip install -r requirements.txt
print_status "Dependencies installed"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    print_info "Creating .env file..."
    cp .env.example .env
    print_warning "Please edit .env file with your Supabase credentials"
    print_info "You can run: nano .env"
else
    print_info ".env file already exists"
fi

# Check if Supabase credentials are set
if [ -f ".env" ]; then
    source .env
    if [ -z "$SUPABASE_URL" ] || [ "$SUPABASE_URL" = "https://your-project.supabase.co" ]; then
        print_warning "Supabase credentials not configured"
        print_info "Running in local development mode with SQLite"
        SUPABASE_CONFIGURED=false
    else
        print_status "Supabase credentials found"
        SUPABASE_CONFIGURED=true
    fi
fi

# Setup database
print_info "Setting up database..."

if [ "$SUPABASE_CONFIGURED" = true ]; then
    print_info "Setting up Supabase database..."
    python setup_database.py
    print_status "Supabase database setup complete"
else
    print_info "Setting up local SQLite database..."
    python -c "
from app import create_app
from database_models import db
app = create_app()
with app.app_context():
    db.create_all()
    print('Local database created')
"
    print_status "Local database setup complete"
fi

# Ask if user wants sample data
echo ""
read -p "Would you like to generate sample data? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_info "Generating sample data..."
    if [ "$SUPABASE_CONFIGURED" = true ]; then
        python setup_database.py --sample-data
    else
        python -c "
from app import create_app
from database_models import db, DiseaseEntry
from sample_data import generate_sample_data
app = create_app()
with app.app_context():
    if DiseaseEntry.query.count() == 0:
        sample_entries = generate_sample_data(20)
        for entry_data in sample_entries:
            entry = DiseaseEntry(**entry_data)
            db.session.add(entry)
        db.session.commit()
        print('Sample data generated')
    else:
        print('Sample data already exists')
"
    fi
    print_status "Sample data generated"
fi

# Final instructions
echo ""
echo "Setup complete!"
echo ""
print_info "Next steps:"
echo "1. Start the application:"
echo "   python app.py"
echo ""
echo "2. Open your browser to:"
echo "   http://localhost:5000"
echo ""

if [ "$SUPABASE_CONFIGURED" = false ]; then
    print_warning "For production deployment:"
    echo "1. Set up a Supabase project at https://supabase.com"
    echo "2. Update your .env file with Supabase credentials"
    echo "3. Run: python setup_database.py"
    echo "4. Deploy to Railway, Render, or Heroku"
fi

echo ""
print_info "For deployment instructions, see: DEPLOYMENT_GUIDE.md"
print_info "For detailed documentation, see: README.md"

# Keep virtual environment activated
echo ""
print_status "Virtual environment is activated"
echo "To deactivate later, run: deactivate"
