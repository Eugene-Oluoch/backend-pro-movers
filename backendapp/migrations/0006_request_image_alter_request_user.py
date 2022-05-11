# Generated by Django 4.0.4 on 2022-05-11 18:25

import cloudinary.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backendapp', '0005_request_id_mover_request_id_user_alter_request_mover_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='image',
            field=cloudinary.models.CloudinaryField(max_length=255, null=True, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='request',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
