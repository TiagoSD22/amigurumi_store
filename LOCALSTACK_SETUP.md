# Amigurumi Store - LocalStack Setup Guide

Since Docker cannot be installed due to WSL issues, we'll use LocalStack directly with Python.

## 🚀 Quick Start Instructions

### Step 1: Start LocalStack
```bash
# Option A: Use the batch file (easiest)
start_localstack.bat

# Option B: Use PowerShell
.\start_localstack.ps1

# Option C: Manual command
.venv\Scripts\activate
python -m localstack.cli.main start
```

### Step 2: Wait for LocalStack to be Ready
- Keep the LocalStack window open
- Wait for the "Ready." message (1-2 minutes)
- LocalStack will be available at: http://localhost:4566

### Step 3: Migrate Images and Create Products
Open a **NEW** terminal/command prompt and run:
```bash
# Navigate to the project directory
cd c:\Users\dante\Documents\pocs\amigurumi_store

# Activate virtual environment
.venv\Scripts\activate

# Run the migration script
python migrate_images_to_s3.py
```

### Step 4: Start the Django Backend
```bash
cd backend
python manage.py runserver
```

### Step 5: Start the React Frontend
Open another terminal:
```bash
cd frontend
npm install  # if not done already
npm start
```

### Step 6: Visit Your Store
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api/products/
- LocalStack S3: http://localhost:4566

## 🛠️ Troubleshooting

### If LocalStack fails to start:
1. Make sure no other services are using port 4566
2. Try: `netstat -an | findstr 4566`
3. If something is using the port, kill it or use a different port

### If migration fails:
1. Make sure LocalStack is running and showing "Ready."
2. Test with: `curl http://localhost:4566/health`
3. You can also populate just the database without S3:
   ```bash
   python populate_database_only.py
   ```

### Alternative: Database-Only Mode
If LocalStack continues to have issues, you can run without S3:
```bash
python populate_database_only.py
cd backend && python manage.py runserver
cd frontend && npm start
```

## 📁 Project Structure
```
amigurumi_store/
├── backend/                # Django API
├── frontend/               # React app
├── sample_*.jpg           # Product images (11 files)
├── start_localstack.bat   # Easy LocalStack startup
├── migrate_images_to_s3.py # S3 migration script
└── populate_database_only.py # Database-only fallback
```

## 🎯 What the Migration Does
1. Starts LocalStack S3 service
2. Creates 'product-image-collection' bucket
3. Uploads all 11 sample images to S3 with organized folder structure
4. Creates/updates products in Django database with S3 image references
5. Sets up public read access for images

## 🔧 Manual Steps (if scripts fail)
1. Start LocalStack: `python -m localstack.cli.main start`
2. Create S3 bucket manually
3. Upload images manually
4. Create products in Django admin

Happy coding! 🧶✨
