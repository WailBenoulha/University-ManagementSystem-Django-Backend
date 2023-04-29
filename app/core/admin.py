from django.contrib import admin

from core import models

admin.site.register(models.AdminProfile)
admin.site.register(models.Categorie_Equipement)
admin.site.register(models.Location)
admin.site.register(models.Equipement)
admin.site.register(models.Stock)
admin.site.register(models.Affectation)
admin.site.register(models.Inventory)