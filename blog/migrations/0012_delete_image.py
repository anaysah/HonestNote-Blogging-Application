# Generated by Django 4.1.7 on 2023-07-26 05:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_image_alter_post_slug'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Image',
        ),
    ]
