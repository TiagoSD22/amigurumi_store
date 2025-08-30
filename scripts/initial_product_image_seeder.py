#!/usr/bin/env python3
"""
Batch upload script for product images to S3.
Uploads sample images for products 1-11 using the upload_product_images_to_s3.py script.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_upload_for_product(product_id: int, stack: str = "local") -> bool:
    """
    Run the upload script for a specific product ID.
    
    Args:
        product_id: Product ID (1-11)
        stack: Target stack environment
        
    Returns:
        bool: True if upload was successful, False otherwise
    """
    # Define the image path for this product
    image_path = f"images/sample_{product_id}.png"
    
    # Check if image file exists
    if not os.path.exists(image_path):
        print(f"⚠️  Warning: Image file {image_path} does not exist, skipping product {product_id}")
        return False
    
    # Define the command to run
    script_path = "scripts/upload_product_images_to_s3.py"
    cmd = [
        "python",
        script_path,
        "--stack", stack,
        "--product_id", str(product_id),
        "--images", image_path
    ]
    
    print(f"🚀 Uploading image for Product {product_id}: {image_path}")
    print(f"   Command: {' '.join(cmd)}")
    
    try:
        # Run the upload script
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        
        print(f"✅ Successfully uploaded image for Product {product_id}")
        if result.stdout:
            # Print any output from the upload script (indented for readability)
            for line in result.stdout.strip().split('\n'):
                print(f"   {line}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to upload image for Product {product_id}")
        print(f"   Error code: {e.returncode}")
        if e.stdout:
            print(f"   Stdout: {e.stdout}")
        if e.stderr:
            print(f"   Stderr: {e.stderr}")
        return False
    
    except Exception as e:
        print(f"❌ Unexpected error uploading image for Product {product_id}: {str(e)}")
        return False

def main():
    """Main function to batch upload all product images."""
    
    import argparse
    
    parser = argparse.ArgumentParser(description='Batch upload product images to S3')
    parser.add_argument('--stack', 
                       choices=['local', 'demo', 'stage', 'prod'],
                       default='local',
                       help='Stack environment (default: local)')
    parser.add_argument('--products',
                       type=str,
                       default='1,2,3,4,5,6,7,8,9,10,11',
                       help='Comma-separated list of product IDs (default: 1,2,3,4,5,6,7,8,9,10,11)')
    parser.add_argument('--continue-on-error',
                       action='store_true',
                       help='Continue uploading even if some products fail')
    
    args = parser.parse_args()
    
    # Parse product IDs
    try:
        product_ids = [int(pid.strip()) for pid in args.products.split(',')]
    except ValueError as e:
        print(f"❌ Error parsing product IDs: {e}")
        sys.exit(1)
    
    print("=" * 60)
    print("🎯 BATCH PRODUCT IMAGE UPLOAD")
    print("=" * 60)
    print(f"📦 Target Stack: {args.stack}")
    print(f"🛍️  Products: {product_ids}")
    print(f"🔄 Continue on error: {args.continue_on_error}")
    print("=" * 60)
    
    # Check if upload script exists
    script_path = "scripts/upload_product_images_to_s3.py"
    if not os.path.exists(script_path):
        print(f"❌ Upload script not found: {script_path}")
        print("   Make sure you're running this from the project root directory")
        sys.exit(1)
    
    # Check if images directory exists
    if not os.path.exists("images"):
        print("❌ Images directory not found: images/")
        print("   Make sure the images/ directory exists with sample_*.png files")
        sys.exit(1)
    
    # Track results
    successful_uploads = 0
    failed_uploads = 0
    skipped_uploads = 0
    
    # Upload images for each product
    for product_id in product_ids:
        print(f"\n📸 Processing Product {product_id}...")
        
        # Check if image exists before attempting upload
        image_path = f"images/sample_{product_id}.png"
        if not os.path.exists(image_path):
            print(f"⏭️  Skipping Product {product_id}: Image {image_path} not found")
            skipped_uploads += 1
            continue
        
        success = run_upload_for_product(product_id, args.stack)
        
        if success:
            successful_uploads += 1
        else:
            failed_uploads += 1
            
            if not args.continue_on_error:
                print(f"\n💥 Stopping batch upload due to failure on Product {product_id}")
                print("   Use --continue-on-error to skip failed uploads and continue")
                break
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 BATCH UPLOAD SUMMARY")
    print("=" * 60)
    print(f"✅ Successful uploads: {successful_uploads}")
    print(f"❌ Failed uploads: {failed_uploads}")
    print(f"⏭️  Skipped uploads: {skipped_uploads}")
    print(f"📝 Total processed: {successful_uploads + failed_uploads + skipped_uploads}")
    
    if failed_uploads > 0:
        print(f"\n⚠️  {failed_uploads} uploads failed. Check the logs above for details.")
        sys.exit(1)
    elif skipped_uploads > 0:
        print(f"\n⚠️  {skipped_uploads} uploads were skipped due to missing image files.")
    else:
        print(f"\n🎉 All uploads completed successfully!")

if __name__ == "__main__":
    main()