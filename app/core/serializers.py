from datetime import timezone
from django.forms import ValidationError
from rest_framework import serializers
from core import models


class Categorie_EquipementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Categorie_Equipement
        fields = ('id', 'Id_admin','name', 'discription', 'created_on')

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Location
        fields = ('id', 'name', 'discription','type', 'created_on')

# hna lazmni nzid les attributes fl fields
class EquipementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Equipement
        fields = ('id', 'created_by', 'name', 'brand', 'model', 'categorie', 'reference', 'num_serie', 'condition', 'facture_number', 'date_purchase', 'Location', 'date_assignment','discription', 'image')

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Stock
        fields = ('id', 'created_by', 'name', 'brand', 'model', 'categorie', 'condition', 'facture_number', 'date_purchase', 'Location', 'date_assignment', 'quantite','discription', 'image')

class AffectationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Affectation
        fields = ('id', 'reference','Location', 'opperation', 'date_assignment')

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Inventory
        fields = ('id', 'created_by', 'name', 'brand', 'model', 'categorie', 'reference', 'num_serie', 'condition', 'facture_number', 'date_purchase', 'Location', 'date_assignment','discription', 'image')

class AllocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Allocation
        fields = ('id', 'created_by', 'name', 'brand', 'model', 'categorie', 'reference', 'num_serie', 'condition', 'facture_number', 'date_purchase', 'Location', 'date_assignment','discription', 'image')

class AllocateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Allocate
        fields = ('id', 'reference', 'start_date', 'finish_date', 'purpose')

class NotificaionStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NotificationStudent
        fields = ('id', 'message', 'reference')

class AcceptrequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Acceptrequest
        fields = ('id', 'Allocation_request', 'accept')

class NotificationManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NotificationManager
        fields =('id', 'message')

class ReservedEquipSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Allocation
        fields = ('id', 'created_by', 'name', 'brand', 'model', 'categorie', 'reference', 'num_serie', 'condition', 'facture_number', 'date_purchase', 'Location', 'date_assignment','discription', 'image')