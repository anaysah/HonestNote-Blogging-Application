# Generated by Django 4.1.7 on 2023-04-07 07:01

import blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0026_alter_category_name_alter_post_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='icon_class_name',
            field=models.CharField(default='fa-atom', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=blog.models.path_and_rename.wrapper),
        ),
    ]