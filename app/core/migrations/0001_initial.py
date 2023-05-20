# Generated by Django 4.2.1 on 2023-05-19 18:37

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('role', models.CharField(choices=[('ADMIN', 'Admin'), ('PRINCIPALMANAGER', 'Principalmanager'), ('ALLOCATIONMANAGER', 'Allocationmanager'), ('STUDENT', 'Student'), ('RESEARCHER', 'Researcher')], max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(max_length=250)),
                ('lastname', models.CharField(max_length=250)),
                ('phonenumber', models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(message="Phone number must start with '06', '05', '07', or '03' and have 10 digits", regex='^0(6|5|7|3)\\d{8}$')])),
                ('national_card_number', models.IntegerField()),
                ('address', models.CharField(max_length=250)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Categorie_Equipement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, unique=True)),
                ('discription', models.CharField(max_length=250)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True)),
                ('discription', models.CharField(max_length=250)),
                ('type', models.CharField(choices=[('lecture_halls', 'lecture_halls'), ('practice_rooms', 'practice_rooms'), ('lab_rooms', 'lab_rooms'), ('administration', 'administration'), ('reservation_room', 'reservation_room'), ('it_room', 'it_room'), ('corridors', 'corridors'), ('stocks', 'stocks')], max_length=250)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='NotificationManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(editable=False, max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='NotificationStudent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(editable=False, max_length=250)),
                ('reference', models.CharField(editable=False, max_length=10)),
                ('send_by', models.CharField(default='', editable=False, max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('brand', models.CharField(max_length=250)),
                ('model', models.CharField(max_length=250)),
                ('num_serie', models.CharField(editable=False, max_length=6, unique=True)),
                ('condition', models.CharField(choices=[('new', 'New'), ('good', 'Good'), ('meduim', 'Meduim'), ('poor', 'Poor'), ('in_repair', 'In_repair'), ('stolen', 'Stolen'), ('reserved', 'Reserved')], default='new', editable=False, max_length=250)),
                ('facture_number', models.IntegerField()),
                ('date_purchase', models.DateField(default=None)),
                ('date_assignment', models.DateField(blank=True, editable=False, null=True)),
                ('quantite', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('discription', models.CharField(default='', max_length=250)),
                ('image', models.ImageField(default='', upload_to='images/')),
                ('is_reserved', models.BooleanField(default=False, editable=False)),
                ('Location', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='core.location', to_field='name')),
                ('categorie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.categorie_equipement', to_field='name')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(editable=False, max_length=250)),
                ('brand', models.CharField(editable=False, max_length=250)),
                ('model', models.CharField(editable=False, max_length=250)),
                ('reference', models.CharField(editable=False, max_length=10, unique=True)),
                ('num_serie', models.CharField(max_length=6, unique=True)),
                ('condition', models.CharField(choices=[('new', 'New'), ('good', 'Good'), ('meduim', 'Meduim'), ('poor', 'Poor'), ('in_repair', 'In_repair'), ('stolen', 'Stolen'), ('reserve', 'Reserve')], max_length=250)),
                ('facture_number', models.IntegerField(editable=False)),
                ('date_purchase', models.DateField(default=None, editable=False)),
                ('date_assignment', models.DateField(blank=True, editable=False, null=True)),
                ('discription', models.CharField(default='', max_length=250)),
                ('image', models.ImageField(default='', upload_to='images/')),
                ('is_reserved', models.BooleanField(default=False, editable=False)),
                ('Location', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='core.location', to_field='name')),
                ('categorie', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='core.categorie_equipement', to_field='name')),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Equipement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('brand', models.CharField(max_length=250)),
                ('model', models.CharField(max_length=250)),
                ('reference', models.CharField(editable=False, max_length=10, unique=True)),
                ('num_serie', models.CharField(editable=False, max_length=6, unique=True)),
                ('condition', models.CharField(choices=[('new', 'New'), ('good', 'Good'), ('meduim', 'Meduim'), ('poor', 'Poor'), ('in_repair', 'In_repair'), ('stolen', 'Stolen'), ('reserve', 'Reserve')], default='new', max_length=250)),
                ('facture_number', models.IntegerField()),
                ('date_purchase', models.DateField(default=None)),
                ('date_assignment', models.DateField(blank=True, editable=False, null=True)),
                ('discription', models.CharField(default='', max_length=250)),
                ('image', models.ImageField(default='', upload_to='images/')),
                ('is_reserved', models.BooleanField(default=False, editable=False)),
                ('Location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.location', to_field='name')),
                ('categorie', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='core.categorie_equipement', to_field='name')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AllocateEquipements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('finish_date', models.DateField()),
                ('purpose', models.CharField(default='', max_length=250)),
                ('Message', models.CharField(editable=False, max_length=250)),
                ('Reserved_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('reference', models.ForeignKey(limit_choices_to={'Location__type': 'reservation_room', 'is_reserved': False}, on_delete=django.db.models.deletion.CASCADE, to='core.inventory', to_field='reference')),
            ],
        ),
        migrations.CreateModel(
            name='Affectation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opperation', models.CharField(editable=False, max_length=250)),
                ('date_assignment', models.DateTimeField(auto_now_add=True)),
                ('Location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.location', to_field='name')),
                ('reference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.equipement', to_field='reference')),
            ],
        ),
        migrations.CreateModel(
            name='AcceptAllocationRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accept', models.BooleanField()),
                ('message1', models.CharField(default='', editable=False, max_length=250)),
                ('message2', models.CharField(default='', editable=False, max_length=250)),
                ('Allocation_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.notificationstudent')),
            ],
        ),
    ]
