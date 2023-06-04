# Generated by Django 4.2.1 on 2023-06-02 14:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_returnequipement'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllocateHPC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('finish_time', models.DateTimeField(editable=False)),
                ('purpose', models.CharField(default='', max_length=250)),
                ('Message', models.CharField(editable=False, max_length=250)),
                ('Reserved_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('reference', models.ForeignKey(limit_choices_to={'Location__type': 'it_room', 'is_requested': False, 'is_reserved': False}, on_delete=django.db.models.deletion.CASCADE, to='core.inventory', to_field='reference')),
            ],
        ),
    ]