# Generated by Django 5.0.2 on 2024-03-12 11:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ip_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IPAddressRange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purpose', models.CharField(max_length=255)),
                ('start_ip_address', models.CharField(max_length=15)),
                ('end_ip_address', models.CharField(max_length=15)),
                ('subnet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ip_management.subnet')),
            ],
        ),
    ]
