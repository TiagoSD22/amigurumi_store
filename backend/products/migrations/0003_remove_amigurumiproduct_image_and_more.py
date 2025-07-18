# Generated by Django 4.2.7 on 2025-07-04 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0002_alter_image_field_for_s3"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="amigurumiproduct",
            name="image",
        ),
        migrations.AddField(
            model_name="amigurumiproduct",
            name="image_s3_path",
            field=models.CharField(
                default="default.png",
                help_text="S3 path to the product image",
                max_length=500,
            ),
            preserve_default=False,
        ),
    ]
