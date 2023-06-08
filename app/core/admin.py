from django.contrib import admin

from core import models

admin.site.register(models.User)
admin.site.register(models.Categorie_Equipement)
admin.site.register(models.Location)
admin.site.register(models.Equipement)
admin.site.register(models.Stock)
admin.site.register(models.Affectation)
admin.site.register(models.Inventory)
admin.site.register(models.NotificationStudent)
admin.site.register(models.NotificationManager)
admin.site.register(models.AllocateEquipements)
admin.site.register(models.AcceptAllocationRequest)
admin.site.register(models.ReturnEquipement)
admin.site.register(models.AllocateHPC)
admin.site.register(models.ReturnEquipementhpc)