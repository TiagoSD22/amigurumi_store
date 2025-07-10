# 🧶 Amigurumi Store - Docker Deployment

A complete e-commerce platform for handmade amigurumi products with Django backend, React frontend, PostgreSQL database, and S3 storage via LocalStack.

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Database      │
│   (React)       │────│   (Django)      │────│  (PostgreSQL)   │
│   Port: 3000    │    │   Port: 8000    │    │   Port: 5432    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       
         └───────────────────────┼─────────────────────────
                                 │                       
                    ┌─────────────────┐                  
                    │   LocalStack    │                  
                    │   (S3 Storage)  │                  
                    │   Port: 4566    │                  
                    └─────────────────┘                  
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Git

### 1. Clone and Start
```bash
git clone <repository-url>
cd amigurumi_store

# Start all services
./start.sh
```

### 2. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api/products/
- **Django Admin**: http://localhost:8000/admin/ (admin/admin123)
- **Database**: localhost:5432 (postgres/postgres)
- **LocalStack**: http://localhost.localstack.cloud:4566

## 📦 Services

### 🎨 Frontend (React + Nginx)
- **Container**: `amigurumi_frontend`
- **Port**: 3000
- **Features**: Product catalog, responsive design, API integration

### ⚙️ Backend (Django + DRF)
- **Container**: `amigurumi_backend`
- **Port**: 8000
- **Features**: REST API, admin interface, S3 integration
- **Admin**: admin/admin123

### 🗄️ Database (PostgreSQL)
- **Container**: `amigurumi_db`
- **Port**: 5432
- **Credentials**: postgres/postgres
- **Database**: amigurumi_store

### ☁️ Storage (LocalStack S3)
- **Container**: `amigurumi_localstack`
- **Port**: 4566
- **Features**: S3-compatible storage, Terraform provisioning

## 🛠️ Development Commands

```bash
# View logs
docker-compose logs -f [service_name]

# Restart a service
docker-compose restart backend

# Access a container
docker-compose exec backend bash
docker-compose exec db psql -U postgres -d amigurumi_store

# Stop services
docker-compose stop

# Stop and remove everything
docker-compose down

# Full cleanup (removes volumes and images)
./cleanup.sh
```

## 📁 Project Structure

```
amigurumi_store/
├── backend/                 # Django application
│   ├── Dockerfile
│   ├── products/           # Product models & API
│   ├── requirements.txt
│   └── settings.py
├── frontend/               # React application
│   ├── Dockerfile
│   ├── src/               # React components
│   └── package.json
├── infrastructure/         # LocalStack + Terraform
│   └── Dockerfile
├── scripts/               # Setup and utility scripts
│   ├── backend-entrypoint.sh
│   ├── init-localstack.sh
│   ├── nginx.conf
│   └── wait-for-it.sh
├── terraform/             # Infrastructure as code
│   └── main.tf           # S3 bucket configuration
├── sample_*.jpg          # Product images
├── docker-compose.yml    # Service orchestration
├── start.sh             # Quick start script
└── cleanup.sh           # Cleanup script
```

## 🔧 Configuration

### Environment Variables
The application uses environment variables for configuration:

```bash
# Database
POSTGRES_DB=amigurumi_store
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db

# AWS/LocalStack
AWS_S3_ENDPOINT_URL=http://localstack:4566
AWS_ACCESS_KEY_ID=test
AWS_SECRET_ACCESS_KEY=test
```

### Volumes
- `postgres_data`: Database persistence
- `localstack_data`: S3 storage persistence
- `static_files`: Django static files
- `media_files`: Uploaded media files

## 🎯 Features

### Backend
- ✅ RESTful API for products
- ✅ Django admin interface
- ✅ PostgreSQL database
- ✅ S3 image storage
- ✅ CORS configuration
- ✅ Health checks

### Frontend
- ✅ Modern React UI
- ✅ Product catalog
- ✅ Category filtering
- ✅ Responsive design
- ✅ API integration

### Infrastructure
- ✅ LocalStack S3 service
- ✅ Terraform provisioning
- ✅ Public read bucket policy
- ✅ Automated setup

## 🐛 Troubleshooting

### Services won't start
```bash
# Check service status
docker-compose ps

# View logs
docker-compose logs -f [service_name]

# Restart problematic service
docker-compose restart [service_name]
```

### Database connection issues
```bash
# Check if database is ready
docker-compose exec db pg_isready -U postgres

# Connect to database
docker-compose exec db psql -U postgres -d amigurumi_store
```

### S3/LocalStack issues
```bash
# Check LocalStack health
curl http://localhost.localstack.cloud:4566/health

# List S3 buckets
docker-compose exec backend python -c "
import boto3
s3 = boto3.client('s3', endpoint_url='http://localstack:4566', 
                  aws_access_key_id='test', aws_secret_access_key='test')
print(s3.list_buckets())
"
```

### Reset everything
```bash
# Full cleanup and restart
./cleanup.sh
./start.sh
```

## 🚀 Production Deployment

For production deployment:

1. Update `settings.py` with production configurations
2. Use environment variables for secrets
3. Configure proper CORS origins
4. Use production-grade databases
5. Implement proper logging and monitoring
6. Use HTTPS and proper SSL certificates

## 📝 API Endpoints

- `GET /api/products/` - List all products
- `GET /api/products/{id}/` - Get product details
- `GET /admin/` - Django admin interface

## 🎉 Sample Data

The application automatically creates 11 sample products with:
- Various amigurumi categories (Animals, Characters, etc.)
- Product images stored in S3
- Realistic pricing and descriptions

---

**Happy coding! 🧶✨**
