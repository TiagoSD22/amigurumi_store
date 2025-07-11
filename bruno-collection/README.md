# Amigurumi Store API - Bruno Collection

This Bruno collection provides comprehensive API testing for the Amigurumi Store backend service.

## Collection Structure

```
bruno-collection/
├── bruno.json                          # Collection configuration
├── environments/
│   └── bruno.json                      # Environment variables
├── Products/                           # Core product operations
│   ├── Get All Products.bru
│   ├── Get Product by ID.bru
│   ├── Get Featured Products.bru
│   └── Get Products by Category.bru
├── Admin/                              # Administrative operations
│   ├── Create Product.bru
│   ├── Update Product (PUT).bru
│   ├── Partial Update Product (PATCH).bru
│   └── Delete Product.bru
├── Testing/                            # Specialized test cases
│   ├── Test Product Images S3 Integration.bru
│   ├── Test Category Filtering.bru
│   └── Test Featured Products.bru
└── README.md                           # This file
```

## Available Environments

- **Local Development**: `http://localhost:8000`
- **Docker Development**: `http://localhost:8000`
- **Demo Environment**: `https://demo-api.amigurumi-store.com`
- **Production**: `https://api.amigurumi-store.com`

## API Endpoints

### Public Endpoints (Products folder)

1. **GET /api/products/** - Get all products
2. **GET /api/products/{id}/** - Get product by ID
3. **GET /api/products/featured/** - Get featured products
4. **GET /api/products/category/{category}/** - Get products by category

### Admin Endpoints (Admin folder)

1. **POST /api/products/** - Create new product
2. **PUT /api/products/{id}/** - Update product (complete)
3. **PATCH /api/products/{id}/** - Update product (partial)
4. **DELETE /api/products/{id}/** - Delete product

### Force Refresh Parameter

All GET endpoints support an optional `force_refresh` query parameter:

```
GET /api/products/?force_refresh=true
GET /api/products/1/?force_refresh=true
GET /api/products/featured/?force_refresh=true
GET /api/products/category/ANIMAL/?force_refresh=true
```

**Accepted values**: `true`, `1`, `yes` (case-insensitive)

**Purpose**: 
- Bypasses image cache and fetches fresh data from S3
- Useful after uploading new images
- Ensures you see the latest images immediately
- Required when cache hasn't expired but images have been updated

## Environment Variables

The collection uses these variables (configurable per environment):

- `baseUrl`: API base URL
- `productId`: Default product ID for testing (1)
- `category`: Default category for testing (ANIMAL)

## Product Categories

- **ANIMAL**: Animal-themed amigurumi (bears, cats, dogs, etc.)
- **DOLL**: Doll-style amigurumi (people, characters with human features)
- **CHARACTER**: Character-based amigurumi (cartoon characters, fantasy creatures)
- **ACCESSORIES**: Amigurumi accessories (bags, hats, decorative items)
- **SEASONAL**: Seasonal/holiday themed (Christmas, Halloween, Easter, etc.)

## S3 Image Integration

The API integrates with S3 for image storage:

- **Product Images**: Stored at `s3://product-image-collection/{productId}/`
- **Default Image**: `s3://product-image-collection/image_not_found.png`
- **Presigned URLs**: Generated with 1-hour expiration
- **Caching**: Images cached for 1 hour, default images for 5 minutes

### Image Response Structure

```json
{
  "images": [
    {
      "url": "https://s3.../presigned-url",
      "filename": "image1.jpg",
      "key": "1/image1.jpg",
      "expires_at": "2025-07-10T15:30:00Z",
      "is_default": false
    }
  ],
  "primary_image": { /* First image object */ }
}
```

## Running Tests

### Prerequisites

1. Ensure your backend is running:
   ```bash
   # Local development
   python manage.py runserver
   
   # Or with Docker
   docker-compose up backend
   ```

2. Ensure LocalStack is running for S3 integration:
   ```bash
   docker-compose up localstack
   ```

### Test Execution Order

1. **Start with Products folder**: Test basic CRUD operations
2. **Run Admin folder**: Test administrative functions
3. **Execute Testing folder**: Validate specialized features

### Expected Test Results

- All GET requests should return 200 status
- POST requests should return 201 with created product
- PUT/PATCH requests should return 200 with updated data
- DELETE requests should return 204 (No Content)
- All products should have images array (even if using default image)

## Troubleshooting

### Common Issues

1. **Connection refused**: Ensure backend server is running
2. **Empty images array**: Check S3/LocalStack connectivity
3. **Invalid presigned URLs**: Verify AWS credentials and endpoint
4. **404 errors**: Check product ID exists in database

### Debug Commands

```bash
# Check backend logs
docker-compose logs backend

# Check LocalStack S3
aws --endpoint-url=http://localhost:4566 s3 ls s3://product-image-collection/

# Test API directly
curl http://localhost:8000/api/products/
```

## Image Upload Workflow

After creating products via API, upload images using the provided script:

```bash
# Upload images for a product
python upload_product_images_to_s3.py --product_id=1 --images="sample1.jpg sample2.jpg"

# Or via Django management command
python manage.py upload_images --product-id=1 --image-dir="./images/"
```

## Notes

- All endpoints support JSON format
- Images are managed separately from product data
- Default images ensure all products display correctly
- Presigned URLs provide secure, temporary access to S3 objects
- Cache invalidation happens automatically when images are uploaded/deleted
