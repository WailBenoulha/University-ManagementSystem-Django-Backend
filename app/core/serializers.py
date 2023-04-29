from rest_framework import serializers
from core import models


class Categorie_EquipementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Categorie_Equipement
        fields = ('id', 'Id_admin','name', 'discription', 'created_on')

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Location
        fields = ('id', 'Id_admin', 'name', 'discription','type', 'created_on')

# hna lazmni nzid les attributes fl fields
class EquipementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Equipement
        fields = ('id', 'created_by', 'name', 'brand', 'model', 'categorie', 'reference', 'num_serie', 'condition', 'facture_number', 'date_purchase', 'Location', 'date_assignment','discription', 'image')

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Stock
        fields = ('id', 'created_by', 'name', 'brand', 'model', 'categorie', 'num_serie', 'condition', 'facture_number', 'date_purchase', 'Location', 'date_assignment', 'quantite','discription', 'image')

class AffectationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Affectation
        fields = ('id', 'reference','Location', 'opperation', 'date_assignment')

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Inventory
        fields = ('id', 'created_by', 'name', 'brand', 'model', 'categorie', 'reference', 'num_serie', 'condition', 'facture_number', 'date_purchase', 'Location', 'date_assignment','discription', 'image')
