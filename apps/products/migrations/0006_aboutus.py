# Generated by Django 5.1.6 on 2025-03-21 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_product_accessory_color_alter_product_category_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('team_image', models.ImageField(blank=True, null=True, upload_to='about_us_images/')),
            ],
        ),
    ]
