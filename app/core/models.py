from datetime import datetime, timedelta
from django.contrib.auth.models import Group
import random
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet
from django.dispatch import receiver
from django.utils import timezone
from django.conf import settings
from django.db.models.signals import post_save

from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", 'Admin'
        PRINCIPALMANAGER = "PRINCIPALMANAGER", 'Principalmanager'
        ALLOCATIONMANAGER = "ALLOCATIONMANAGER", 'Allocationmanager'
        STUDENT = "STUDENT", 'Student'
        RESEARCHER = "RESEARCHER", 'Researcher'

    base_role = Role.ADMIN
    role = models.CharField(max_length=50, choices=Role.choices)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=250)
    lastname = models.CharField(max_length=250)
    phone_regex = RegexValidator(
        regex=r'^0(6|5|7|3)\d{8}$',
        message = "Phone number must start with '06', '05', '07', or '03' and have 10 digits"
    )
    phonenumber = models.CharField(validators = [phone_regex], max_length=20)
    national_card_number = models.IntegerField()
    address = models.CharField(max_length=250)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','lastname','phonenumber','national_card_number','address']
    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.Role = self.base_role
        super().save(*args, **kwargs)
        group_name = self.role  # Group name should match the role name in lowercase
        group, created = Group.objects.get_or_create(name=group_name)
        self.groups.add(group)


class Categorie_Equipement(models.Model):
    name = models.CharField(max_length=40, unique=True)
    discription = models.CharField(max_length=250)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=250, unique=True)
    discription = models.CharField(max_length=250)
    LECTURE_HALLS  = 'lecture_halls'
    PRACTICE_ROOMS  = 'practice_rooms'
    LAB_ROOMS = 'lab_rooms'
    ADMINISTRATION = 'administration'
    RESERVATION_ROOM = 'reservation_room'
    IT_ROOM = 'it_room'
    CORRIDORS = 'corridors'
    STOCKS = 'stocks'
    TYPE_CHOICES = [
        (LECTURE_HALLS, 'lecture_halls'),
        (PRACTICE_ROOMS, 'practice_rooms'),
        (LAB_ROOMS, 'lab_rooms'),
        (ADMINISTRATION, 'administration'),
        (RESERVATION_ROOM, 'reservation_room'),
        (IT_ROOM, 'it_room'),
        (CORRIDORS, 'corridors'),
        (STOCKS, 'stocks')
    ]
    type = models.CharField(choices=TYPE_CHOICES, max_length=250)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Equipement(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=250)
    brand = models.CharField(max_length=250)
    model = models.CharField(max_length=250)
    categorie = models.ForeignKey(
        Categorie_Equipement,
        to_field='name',
        default='',
        on_delete=models.CASCADE
    )
    reference = models.CharField(max_length=10, unique=True, editable=False)
    num_serie = models.CharField(max_length=6, unique=True, editable=False)
    CONDITION_CHOICES =(
        ('new','New'),
        ('good','Good'),
        ('meduim','Meduim'),
        ('poor','Poor'),
        ('in_repair','In_repair'),
        ('stolen','Stolen'),
        ('reserve','Reserve'),
    )
    condition = models.CharField(choices=CONDITION_CHOICES, max_length=250, default='new')
    facture_number = models.IntegerField()
    date_purchase = models.DateField(default=None)
    Location = models.ForeignKey(
        Location,
        to_field='name',
        on_delete=models.CASCADE
    )
    date_assignment = models.DateField(null=True, editable=False, blank=True)
    discription = models.CharField(default='', max_length=250)
    image = models.ImageField(upload_to='images/', default='')
    is_reserved = models.BooleanField(default=False, editable=False)

    def save(self, *args, **kwargs):
        # Generate a unique reference number
        if not self.pk:
            # If the object is being created (i.e. it doesn't have a primary key yet),
            # generate the reference field based on the name field.
            prefix = self.name[:2].upper()
            while True:
                num = str(random.randint(10000, 99999)).zfill(5)
                ref = f"{prefix}-{num}"
                if not Equipement.objects.filter(reference=ref).exists():
                    break
            self.reference = ref

        # Generate a unique num_serie
        while True:
            num_serie = str(random.randint(100000, 999999))
            if not Equipement.objects.filter(num_serie=num_serie).exists():
                break

        self.num_serie = num_serie

        super().save(*args, **kwargs)

    def __str__(self):
        return self.reference

class Stock(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=250)
    brand = models.CharField(max_length=250)
    model = models.CharField(max_length=250)
    categorie = models.ForeignKey(
        Categorie_Equipement,
        to_field='name',
        on_delete=models.CASCADE
    )
    num_serie = models.CharField(max_length=6, unique=True, editable=False)
    CONDITION_CHOICES =(
        ('new','New'),
        ('good','Good'),
        ('meduim','Meduim'),
        ('poor','Poor'),
        ('in_repair','In_repair'),
        ('stolen','Stolen'),
        ('reserved','Reserved'),
    )
    condition = models.CharField(choices=CONDITION_CHOICES, max_length=250, default='new', editable=False)
    facture_number = models.IntegerField()
    date_purchase = models.DateField(default=None)
    Location = models.ForeignKey(
        Location,
        to_field='name',
        on_delete=models.CASCADE,
        editable=False
    )
    date_assignment = models.DateField(null=True, editable=False, blank=True)
    quantite = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    discription = models.CharField(default='', max_length=250)
    image = models.ImageField(upload_to='images/', default='')
    is_reserved = models.BooleanField(default=False, editable=False)

    def save(self, *args, **kwargs):

        # Generate a unique num_serie
        while True:
            num_serie = str(random.randint(100000, 999999))
            if not Stock.objects.filter(num_serie=num_serie).exists():
                break

        self.num_serie = num_serie

        location = Location.objects.get(type='stocks')
        self.Location = location

        super().save(*args, **kwargs)

        # Create the equipement objects based on the quantite field
        for i in range(self.quantite):
            equipement = Equipement(
                created_by=self.created_by,
                name=self.name,
                brand=self.brand,
                model=self.model,
                categorie=self.categorie,
                num_serie=self.num_serie,
                condition=self.condition,
                facture_number=self.facture_number,
                date_purchase=self.date_purchase,
                Location=self.Location,
                date_assignment=self.date_assignment,
                discription=self.discription,
                image=self.image,
                is_reserved=self.is_reserved
            )
            equipement.save()

    def __str__(self):
        return self.name

def validate_reference(value):
    if not value:
        raise ValidationError('Reference cannot be empty')

class Affectation(models.Model):
    reference = models.ForeignKey(
        Equipement,
        to_field='reference',
        on_delete=models.CASCADE
    )
    Location = models.ForeignKey(
        Location,
        to_field='name',
        on_delete=models.CASCADE
    )
    opperation = models.CharField(max_length=250, unique=False, editable=False)
    date_assignment = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        self.opperation = f"The equipment {self.reference.name} {self.reference.brand} {self.reference.model} {self.reference.reference} affected to the location {self.Location.name}"
        super().save(*args, **kwargs)

        if self.Location.type == 'reservation_room':
            ref = self.reference
            equipement = Equipement.objects.get(id=ref.id) #hna ta9der tbdel reference w t3awedha bl id 3la 7sab wach rah tconsulte
            inventory_equipement = Inventory(
                created_by = equipement.created_by,
                name=equipement.name,
                brand=equipement.brand,
                model=equipement.model,
                categorie=equipement.categorie,
                reference=equipement.reference,
                num_serie=equipement.num_serie,
                condition='good',
                facture_number=equipement.facture_number,
                date_purchase=equipement.date_purchase,
                Location=self.Location,
                date_assignment=self.date_assignment,
                discription=equipement.discription,
                image=equipement.image,
                is_reserved=equipement.is_reserved
            )
            allocation_equipement = Allocation(
                created_by = equipement.created_by,
                name=equipement.name,
                brand=equipement.brand,
                model=equipement.model,
                categorie=equipement.categorie,
                reference=equipement.reference,
                num_serie=equipement.num_serie,
                condition='good',
                facture_number=equipement.facture_number,
                date_purchase=equipement.date_purchase,
                Location=self.Location,
                date_assignment=self.date_assignment,
                discription=equipement.discription,
                image=equipement.image,
                is_reserved=equipement.is_reserved
            )
            allocation_equipement.save()
            inventory_equipement.save()
            equipement.delete()
        else:
            ref = self.reference
            equipement = Equipement.objects.get(id=ref.id)
            inventory_equipement2 = Inventory(
                created_by = equipement.created_by,
                name=equipement.name,
                brand=equipement.brand,
                model=equipement.model,
                categorie=equipement.categorie,
                reference=equipement.reference,
                num_serie=equipement.num_serie,
                condition='good',
                facture_number=equipement.facture_number,
                date_purchase=equipement.date_purchase,
                Location=self.Location,
                date_assignment=self.date_assignment,
                discription=equipement.discription,
                image=equipement.image,
                is_reserved=equipement.is_reserved
            )
            inventory_equipement2.save()
            equipement.delete()



class Inventory(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        editable=False,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=250, editable=False)
    brand = models.CharField(max_length=250, editable=False)
    model = models.CharField(max_length=250, editable=False)
    categorie = models.ForeignKey(
        Categorie_Equipement,
        to_field='name',
        editable=False,
        on_delete=models.CASCADE
    )
    reference = models.CharField(max_length=10, unique=True, editable=False)
    num_serie = models.CharField(max_length=6, unique=True, editable=True)
    CONDITION_CHOICES =(
        ('new','New'),
        ('good','Good'),
        ('meduim','Meduim'),
        ('poor','Poor'),
        ('in_repair','In_repair'),
        ('stolen','Stolen'),
        ('reserve','Reserve'),
    )
    condition = models.CharField(choices=CONDITION_CHOICES, max_length=250)
    facture_number = models.IntegerField(editable=False)
    date_purchase = models.DateField(default=None, editable=False)
    Location = models.ForeignKey(
        Location,
        to_field='name',
        editable=False,
        on_delete=models.CASCADE
    )
    date_assignment = models.DateField(null=True, editable=False, blank=True)
    discription = models.CharField(default='', max_length=250)
    image = models.ImageField(upload_to='images/', default='')
    is_reserved = models.BooleanField(default=False, editable=False)

    def __srt__(self):
        return self.reference

class Allocation(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        editable=False,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=250, editable=False)
    brand = models.CharField(max_length=250, editable=False)
    model = models.CharField(max_length=250, editable=False)
    categorie = models.ForeignKey(
        Categorie_Equipement,
        to_field='name',
        editable=False,
        on_delete=models.CASCADE
    )
    reference = models.CharField(max_length=10, unique=True, editable=False)
    num_serie = models.CharField(max_length=6, unique=True, editable=False)
    CONDITION_CHOICES =(
        ('new','New'),
        ('good','Good'),
        ('meduim','Meduim'),
        ('poor','Poor'),
        ('in_repair','In_repair'),
        ('stolen','Stolen'),
        ('reserve','Reserve'),
    )
    condition = models.CharField(choices=CONDITION_CHOICES, max_length=250)
    facture_number = models.IntegerField(editable=False)
    date_purchase = models.DateField(default=None, editable=False)
    Location = models.ForeignKey(
        Location,
        to_field='name',
        editable=False,
        on_delete=models.CASCADE
    )
    date_assignment = models.DateField(null=True, editable=False, blank=True)
    discription = models.CharField(default='', max_length=250)
    image = models.ImageField(upload_to='images/', default='')
    is_reserved = models.BooleanField(default=False, editable=False)

    def __srt__(self):
        return self.reference

class Allocate(models.Model):
    reference = models.ForeignKey(
        Allocation,
        to_field='reference',
        on_delete=models.CASCADE
    )
    start_date = models.DateTimeField()
    finish_date = models.DateTimeField()
    purpose = models.CharField(max_length=250, default='')
    Message = models.CharField(editable=False, max_length=250)

    def save(self, *args, **kwargs):
        self.Message = f"the student asked to allocate the equipement {self.reference.name} {self.reference.brand} {self.reference.model} {self.reference.reference} at the startdate {self.start_date} and the finishdate {self.finish_date}"
        super().save(*args, **kwargs)

        ref = self.reference
        equipement = Allocation.objects.get(id=ref.id)
        notification_to_manager = NotificationStudent(
            message = self.Message,
            reference = equipement.reference
        )
        notification_to_manager.save()

class NotificationStudent(models.Model):
    message = models.CharField(editable=False, unique=True, max_length=250)
    reference = models.CharField(max_length=10, editable=False)

    def __str__(self):
        return self.message

class Acceptrequest(models.Model):
    Allocation_request = models.ForeignKey(
        NotificationStudent,
        on_delete=models.CASCADE
    )
    accept = models.BooleanField()
    message1 = models.CharField(editable=False, default='', max_length=250)
    message2 = models.CharField(editable=False, default='', max_length=250)

    def save(self, *args, **kwargs):
        self.message1 = f"the Admin accept your request to allocate {self.Allocation_request.reference}"
        self.message2 = f"the Admin refuse your request to allocate {self.Allocation_request.reference}"
        super().save(*args, **kwargs)

        if self.accept == True:
            try:
                notificationtd = self.Allocation_request
                allocation_ref = notificationtd.reference
                equipement = Allocation.objects.get(reference=allocation_ref)
                reserved_equipement = ReservedEquip(
                    created_by = equipement.created_by,
                    name = equipement.name,
                    brand = equipement.brand,
                    model = equipement.model,
                    categorie = equipement.categorie,
                    reference = equipement.reference,
                    num_serie = equipement.num_serie,
                    condition = equipement.condition,
                    facture_number = equipement.facture_number,
                    date_purchase = equipement.date_purchase,
                    Location = equipement.Location,
                    date_assignment =equipement.date_assignment,
                    discription = equipement.discription,
                    image = equipement.image,
                    is_reserved=equipement.is_reserved
                )
                notification = NotificationManager(
                    message = self.message1
                )
                notification.save()
                reserved_equipement.save()
                equipement.delete()
                notificationtd.delete()
            except NotificationStudent.DoesNotExist:
                pass
        else:
            try:
                notificationstd = NotificationStudent.objects.get(id=self.id)
                notification2 = NotificationManager(
                    message = self.message2
                )
                notification2.save()
                notificationstd.delete()
            except NotificationStudent.DoesNotExist:
                pass


class NotificationManager(models.Model):
    message = models.CharField(editable=False, max_length=250)

class ReservedEquip(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        editable=False,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=250, editable=False)
    brand = models.CharField(max_length=250, editable=False)
    model = models.CharField(max_length=250, editable=False)
    categorie = models.ForeignKey(
        Categorie_Equipement,
        to_field='name',
        editable=False,
        on_delete=models.CASCADE
    )
    reference = models.CharField(max_length=10, unique=True, editable=False)
    num_serie = models.CharField(max_length=6, unique=True, editable=False)
    CONDITION_CHOICES =(
        ('new','New'),
        ('good','Good'),
        ('meduim','Meduim'),
        ('poor','Poor'),
        ('in_repair','In_repair'),
        ('stolen','Stolen'),
        ('reserve','Reserve'),
    )
    condition = models.CharField(choices=CONDITION_CHOICES, max_length=250)
    facture_number = models.IntegerField(editable=False)
    date_purchase = models.DateField(default=None, editable=False)
    Location = models.ForeignKey(
        Location,
        to_field='name',
        editable=False,
        on_delete=models.CASCADE
    )
    date_assignment = models.DateField(null=True, editable=False, blank=True)
    discription = models.CharField(default='', max_length=250)
    image = models.ImageField(upload_to='images/', default='')
    is_reserved = models.BooleanField(default=True, editable=False)

    def __srt__(self):
        return self.reference

class ReturnEquipement(models.Model):
    Equipement = models.OneToOneField(
        ReservedEquip,
        to_field='reference',
        on_delete=models.CASCADE,
        verbose_name="Equipment"
    )

    def save(self, *args, **kwargs):
        ref = self.Equipement
        equipement = ReservedEquip.objects.get(reference=ref)
        reserved_equipement = Allocation(
            created_by = equipement.created_by,
            name = equipement.name,
            brand = equipement.brand,
            model = equipement.model,
            categorie = equipement.categorie,
            reference = equipement.reference,
            num_serie = equipement.num_serie,
            condition = equipement.condition,
            facture_number = equipement.facture_number,
            date_purchase = equipement.date_purchase,
            Location = equipement.Location,
            date_assignment =equipement.date_assignment,
            discription = equipement.discription,
            image = equipement.image,
            is_reserved=equipement.is_reserved
        )
        reserved_equipement.save()
        equipement.delete()

# class AllocateEquipements(models.Model):
#     Reserved_by = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         editable=False,
#         on_delete=models.CASCADE
#     )
#     equipement = models.ForeignKey(
#         Inventory,
#         on_delete=models.CASCADE,
#         limit_choices_to={'Location__type':'reservation_room'},
#         to_field='reference'
#     )
#     CHOICES = (
#         (datetime.now(), datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
#         (datetime.now() + timedelta(days=1), (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")),
#         (datetime.now() + timedelta(days=2), (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S")),
#         (datetime.now() + timedelta(days=3), (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S")),
#         (datetime.now() + timedelta(days=4), (datetime.now() + timedelta(days=4)).strftime("%Y-%m-%d %H:%M:%S")),
#         (datetime.now() + timedelta(days=5), (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d %H:%M:%S")),
#         (datetime.now() + timedelta(days=6), (datetime.now() + timedelta(days=6)).strftime("%Y-%m-%d %H:%M:%S")),
#         (datetime.now() + timedelta(days=7), (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")),
#     )
#     start_date = models.DateField(choices=CHOICES, validators=[MinValueValidator(datetime.now())])
#     finish_date = models.DateField(editable=False, null=True)
#     purpose = models.CharField(max_length=250, default='')
#     Message = models.CharField(editable=False, max_length=250)

#     def save(self, *args, **kwargs):
#         if not self.pk:  # only set finish_date if object is being created for the first time
#             self.finish_date = self.start_date.date() + timezone.timedelta(days=7)
#         super(AllocateEquipements, self).save(*args, **kwargs)





# HPC
# class allocatehpc(models.Model):
#     reference = models.ForeignKey(
#         Inventory,
#         to_field='reference',
#         on_delete=models.CASCADE,
#         limit_choices_to={
#             'Location__type': 'it_room',
#             'is_reserved' : 'False'
#         }
#     )
#     allocator = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         editable=False,
#         related_name='allocater',
#         on_delete=models.CASCADE
#     )
#     purpose = models.CharField(max_length=250, default='')

