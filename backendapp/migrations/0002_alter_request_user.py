# Generated by Django 4.0.4 on 2022-05-11 09:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backendapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
