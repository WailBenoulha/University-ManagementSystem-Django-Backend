# Generated by Django 4.2.1 on 2023-05-21 23:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_remove_acceptallocationrequest_allocation_request_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acceptallocationrequest',
            name='request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.allocateequipements'),
        ),
    ]