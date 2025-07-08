# Generated migration to change from ImageField to CharField for S3 storage

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amigurumiproduct',
            name='image',
            field=models.CharField(max_length=500, help_text='S3 bucket path to the product image'),
        ),
    ]
