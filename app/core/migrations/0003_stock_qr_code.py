# Generated by Django 4.2.1 on 2023-06-07 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_equipement_qr_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='qr_code',
            field=models.ImageField(blank=True, upload_to='qr_codes/'),
        ),
    ]
