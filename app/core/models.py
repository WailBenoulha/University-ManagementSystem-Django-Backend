import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings
import random
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


from django.core.validators import RegexValidator


class AdminProfileManager(BaseUserManager):
    def create_user(self, email, name, lastname, phonenumber, national_card_number, address, role, password=None):
        if not email:
            raise ValueError('User Must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, lastname=lastname, phonenumber=phonenumber, national_card_number=national_card_number, address=address, role=role)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, lastname, phonenumber, national_card_number, address, role, password):
        user = self.create_user(email, name, lastname, phonenumber, national_card_number, address, role, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user

class AdminProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    phone_regex = RegexValidator(
        regex=r'^0(6|5|7|3)\d{8}$',
        message = "Phone number must start with '06', '05', '07', or '03' and have 10 digits"
    )
    phonenumber = models.CharField(validators = [phone_regex], max_length=20)
    national_card_number = models.IntegerField()
    address = models.CharField(max_length=255)
    ROLE_CHOICES = (
        ('admin', 'Admin'),
    )
    role = models.CharField(choices=ROLE_CHOICES ,max_length=255, default='admin')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = AdminProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','lastname','phonenumber','national_card_number','address','role']

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.email

class Categorie_Equipement(models.Model):
    Id_admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='Categorie',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=40, unique=True)
    discription = models.TextField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Location(models.Model):
    Id_admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255, unique=True)
    discription = models.TextField()
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
    type = models.CharField(choices=TYPE_CHOICES, max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Equipement(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    categorie = models.ForeignKey(
        Categorie_Equipement,
        to_field='name',
        default='',
        on_delete=models.CASCADE
    )
    reference = models.CharField(max_length=7, unique=True, editable=False)
    num_serie = models.CharField(max_length=6, unique=True, editable=False)
    CONDITION_CHOICES =(
        ('new','New'),
        ('meduim','Meduim'),
        ('poor','Poor'),
        ('in_repair','In_repair'),
        ('stolen','Stolen'),
        ('reserve','Reserve'),
    )
    condition = models.CharField(choices=CONDITION_CHOICES, max_length=255, default='new')
    facture_number = models.IntegerField()
    date_purchase = models.DateField(default=None)
    Location = models.ForeignKey(
        Location,
        to_field='name',
        on_delete=models.CASCADE
    )
    date_assignment = models.DateField(null=True, editable=False, blank=True)
    discription = models.TextField(default='')
    image = models.ImageField(upload_to='images/', default='')

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
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    categorie = models.ForeignKey(
        Categorie_Equipement,
        to_field='name',
        on_delete=models.CASCADE
    )
    num_serie = models.CharField(max_length=6, unique=True, editable=False)
    CONDITION_CHOICES =(
        ('new','New'),
        ('meduim','Meduim'),
        ('poor','Poor'),
        ('in_repair','In_repair'),
        ('stolen','Stolen'),
        ('reserved','Reserved'),
    )
    condition = models.CharField(choices=CONDITION_CHOICES, max_length=255, default='new', editable=False)
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
    discription = models.TextField(default='')
    image = models.ImageField(upload_to='images/', default='')

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
                image=self.image
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
    opperation = models.TextField(max_length=255, unique=False, editable=False)
    date_assignment = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        self.opperation = f"The equipment {self.reference.name} {self.reference.brand} {self.reference.model} {self.reference.reference} affected to the location {self.Location.name}"
        super().save(*args, **kwargs)

        if self.Location.type == 'it_room':
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
                condition=equipement.condition,
                facture_number=equipement.facture_number,
                date_purchase=equipement.date_purchase,
                Location=self.Location,
                date_assignment=self.date_assignment,
                discription=equipement.discription,
                image=equipement.image
            )
            allocation_equipement = Allocation(
                created_by = equipement.created_by,
                name=equipement.name,
                brand=equipement.brand,
                model=equipement.model,
                categorie=equipement.categorie,
                reference=equipement.reference,
                num_serie=equipement.num_serie,
                condition=equipement.condition,
                facture_number=equipement.facture_number,
                date_purchase=equipement.date_purchase,
                Location=self.Location,
                date_assignment=self.date_assignment,
                discription=equipement.discription,
                image=equipement.image
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
                condition=equipement.condition,
                facture_number=equipement.facture_number,
                date_purchase=equipement.date_purchase,
                Location=self.Location,
                date_assignment=self.date_assignment,
                discription=equipement.discription,
                image=equipement.image
            )
            inventory_equipement2.save()
            equipement.delete()



class Inventory(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        editable=False,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255, editable=False)
    brand = models.CharField(max_length=255, editable=False)
    model = models.CharField(max_length=255, editable=False)
    categorie = models.ForeignKey(
        Categorie_Equipement,
        to_field='name',
        editable=False,
        on_delete=models.CASCADE
    )
    reference = models.CharField(max_length=7, unique=True, editable=False)
    num_serie = models.CharField(max_length=6, unique=True, editable=False)
    CONDITION_CHOICES =(
        ('new','New'),
        ('meduim','Meduim'),
        ('poor','Poor'),
        ('in_repair','In_repair'),
        ('stolen','Stolen'),
        ('reserve','Reserve'),
    )
    condition = models.CharField(choices=CONDITION_CHOICES, max_length=255)
    facture_number = models.IntegerField(editable=False)
    date_purchase = models.DateField(default=None, editable=False)
    Location = models.ForeignKey(
        Location,
        to_field='name',
        editable=False,
        on_delete=models.CASCADE
    )
    date_assignment = models.DateField(null=True, editable=False, blank=True)
    discription = models.TextField(default='')
    image = models.ImageField(upload_to='images/', default='')

    def __srt__(self):
        return self.reference

class Allocation(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        editable=False,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255, editable=False)
    brand = models.CharField(max_length=255, editable=False)
    model = models.CharField(max_length=255, editable=False)
    categorie = models.ForeignKey(
        Categorie_Equipement,
        to_field='name',
        editable=False,
        on_delete=models.CASCADE
    )
    reference = models.CharField(max_length=7, unique=True, editable=False)
    num_serie = models.CharField(max_length=6, unique=True, editable=False)
    CONDITION_CHOICES =(
        ('new','New'),
        ('meduim','Meduim'),
        ('poor','Poor'),
        ('in_repair','In_repair'),
        ('stolen','Stolen'),
        ('reserve','Reserve'),
    )
    condition = models.CharField(choices=CONDITION_CHOICES, max_length=255)
    facture_number = models.IntegerField(editable=False)
    date_purchase = models.DateField(default=None, editable=False)
    Location = models.ForeignKey(
        Location,
        to_field='name',
        editable=False,
        on_delete=models.CASCADE
    )
    date_assignment = models.DateField(null=True, editable=False, blank=True)
    discription = models.TextField(default='')
    image = models.ImageField(upload_to='images/', default='')

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
    purpose = models.TextField(max_length=255, default='')
    Message = models.TextField(editable=False)

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
    message = models.TextField(editable=False, unique=True)
    reference = models.CharField(max_length=7, editable=False)

    def __str__(self):
        return self.message

class Acceptrequest(models.Model):
    Allocation_request = models.ForeignKey(
        NotificationStudent,
        on_delete=models.CASCADE
    )
    accept = models.BooleanField()
    message1 = models.TextField(editable=False, default='')
    message2 = models.TextField(editable=False, default='')

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
                    image = equipement.image
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
    message = models.TextField(editable=False)

class ReservedEquip(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        editable=False,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255, editable=False)
    brand = models.CharField(max_length=255, editable=False)
    model = models.CharField(max_length=255, editable=False)
    categorie = models.ForeignKey(
        Categorie_Equipement,
        to_field='name',
        editable=False,
        on_delete=models.CASCADE
    )
    reference = models.CharField(max_length=7, unique=True, editable=False)
    num_serie = models.CharField(max_length=6, unique=True, editable=False)
    CONDITION_CHOICES =(
        ('new','New'),
        ('meduim','Meduim'),
        ('poor','Poor'),
        ('in_repair','In_repair'),
        ('stolen','Stolen'),
        ('reserve','Reserve'),
    )
    condition = models.CharField(choices=CONDITION_CHOICES, max_length=255)
    facture_number = models.IntegerField(editable=False)
    date_purchase = models.DateField(default=None, editable=False)
    Location = models.ForeignKey(
        Location,
        to_field='name',
        editable=False,
        on_delete=models.CASCADE
    )
    date_assignment = models.DateField(null=True, editable=False, blank=True)
    discription = models.TextField(default='')
    image = models.ImageField(upload_to='images/', default='')

    def __srt__(self):
        return self.reference