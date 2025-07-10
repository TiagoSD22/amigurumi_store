terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region                      = "us-east-1"
  access_key                  = "test"
  secret_key                  = "test"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
  s3_use_path_style          = true

  endpoints {
    s3  = "http://localstack:4566"
    sts = "http://localstack:4566"
  }
}

# S3 bucket for product images
resource "aws_s3_bucket" "product_image_collection" {
  bucket        = "product-image-collection"
  force_destroy = true
}

# Public access configuration
resource "aws_s3_bucket_public_access_block" "product_images_pab" {
  bucket = aws_s3_bucket.product_image_collection.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

# Bucket policy for public read access
resource "aws_s3_bucket_policy" "product_images_policy" {
  bucket = aws_s3_bucket.product_image_collection.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.product_image_collection.arn}/*"
      }
    ]
  })

  depends_on = [aws_s3_bucket_public_access_block.product_images_pab]
}

# Output the bucket name
output "bucket_name" {
  value = aws_s3_bucket.product_image_collection.bucket
}

output "bucket_arn" {
  value = aws_s3_bucket.product_image_collection.arn
}
