from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from core import serializers
from core import models
from django.http import Http404
from rest_framework.decorators import api_view
import genericpath
from rest_framework import generics

class Categorie_EquipementApiView(APIView):
    serializer_class = serializers.Categorie_EquipementSerializer
    queryset = models.Categorie_Equipement.objects.all()

    def get(self, request, pk=None):
        if pk:
            try:
                categorie = models.Categorie_Equipement.objects.get(pk=pk)
            except models.Categorie_Equipement.DoesNotExist:
                return Response(
                    {
                    'message' : 'the categorie that you tryna access is not exist'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = serializers.Categorie_EquipementSerializer(categorie)
            return Response(serializer.data)
        else:
            categorie = models.Categorie_Equipement.objects.all()
            serializer = serializers.Categorie_EquipementSerializer(categorie, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                'message' : 'categorie created successfully',
                'the new categorie' : serializer.data
                },
                status= status.HTTP_201_CREATED
            )
        else:
            return Response(
                {
                'message' : 'categorie created failed! check your informations',
                'errors' : serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, pk=None):
        if pk:
            try:
                categorie = models.Categorie_Equipement.objects.get(pk=pk)
            except models.Categorie_Equipement.DoesNotExist:
                return Response(
                    {
                    'message' : 'the categorie that you tryna access is not found'
                    },
                    status=status.HTTP_204_NO_CONTENT
                )

            serializer = serializers.Categorie_EquipementSerializer(categorie, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                    'message': 'the categorie updated successfully',
                    'data': serializer.data
                    },
                    status=status.HTTP_202_ACCEPTED
                )
            else:
                return Response(
                    {
                    'message': 'categorie failed updated! check your updated informations',
                    'errors': serializer.errors
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {
                    'message' : 'You must provide the id number to update a loation'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, pk=None):
        if pk:
            try:
                categorie = models.Categorie_Equipement.objects.get(pk=pk)
            except models.Categorie_Equipement.DoesNotExist:
                return Response(
                    {
                    'message' : 'the categorie that you tryna access is not exist'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            categorie.delete()
            return Response(
                {
                'message' : 'the categorie deleted successfuly'
                },
                status=status.HTTP_204_NO_CONTENT
            )
        else:
            categorie = models.Categorie_Equipement.objects.all()
            categorie.delete()
            return Response(
                {
                'message' : 'all the categories deleted successfully'
                },
                status=status.HTTP_204_NO_CONTENT
            )

class LoacationApiView(APIView):
    queryset = models.Location.objects.all()
    serializer_class = serializers.LocationSerializer

    def get(self, request, pk=None):
        if pk:
            try:
                location = models.Location.objects.get(pk=pk)
            except models.Location.DoesNotExist:
                return Response(
                    {
                    'message' : 'the location that you tryna access is not exist'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = serializers.LocationSerializer(location)
            return Response(serializer.data)
        else:
            location = models.Location.objects.all()
            serializer = serializers.LocationSerializer(location, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                'message' : 'location created successfully',
                'the new location' : serializer.data
                },
                status= status.HTTP_201_CREATED
            )
        else:
            return Response(
                {
                'message' : 'location created failed! check your informations',
                'errors' : serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, pk=None):
        if pk:
            try:
                location = models.Location.objects.get(pk=pk)
            except models.Location.DoesNotExist:
                return Response(
                    {
                    'message' : 'the Location that you tryna access is not found'
                    },
                    status=status.HTTP_204_NO_CONTENT
                )

            serializer = serializers.LocationSerializer(location, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                    'message': 'the location updated successfully',
                    'data': serializer.data
                    },
                    status=status.HTTP_202_ACCEPTED
                )
            else:
                return Response(
                    {
                    'message': 'location failed updated! check your updated informations',
                    'errors': serializer.errors
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {
                    'message' : 'You must provide the id number to update a loation'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, pk=None):
        if pk:
            try:
                location = models.Location.objects.get(pk=pk)
            except models.Location.DoesNotExist:
                return Response(
                    {
                    'message' : 'the Location that you tryna access is not exist'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            location.delete()
            return Response(
                {
                'message' : 'the location deleted successfuly'
                },
                status=status.HTTP_204_NO_CONTENT
            )
        else:
            location = models.Location.objects.all()
            location.delete()
            return Response(
                {
                'message' : 'all the locations deleted successfully'
                },
                status=status.HTTP_204_NO_CONTENT
            )


class EquipementApiview(APIView):
    queryset = models.Equipement.objects.all()
    serializer_class = serializers.EquipementSerializer

    def get(self, request, pk=None):
        if pk:
            try:
                equipement = models.Equipement.objects.get(pk=pk)
            except models.Equipement.DoesNotExist:
                return Response(
                    {
                    'message' : 'the equipement that you tryna access is not exist'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = serializers.EquipementSerializer(equipement)
            return Response(serializer.data)
        else:
            equipement = models.Equipement.objects.all()
            serializer = serializers.EquipementSerializer(equipement, many=True)
            return Response(serializer.data)

    def delete(self, request, pk=None):
        if pk:
            try:
                equipement = models.Equipement.objects.get(pk=pk)
            except models.Stock.DoesNotExist:
                return Response(
                    {
                    'message' : 'the equipement that you tryna access is not exist'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            equipement.delete()
            return Response(
                {
                'message' : 'the equipement deleted successfuly'
                },
                status=status.HTTP_204_NO_CONTENT
            )
        else:
            equipement = models.Equipement.objects.all()
            equipement.delete()
            return Response(
                {
                'message' : 'all the equipements deleted successfully'
                },
                status=status.HTTP_204_NO_CONTENT
            )

    def put(self, request, pk=None):
        if pk:
            try:
                equipement = models.Equipement.objects.get(pk=pk)
            except models.Equipement.DoesNotExist:
                return Response(
                    {
                    'message' : 'the equipement that you tryna access is not found'
                    },
                    status=status.HTTP_204_NO_CONTENT
                )

            serializer = serializers.EquipementSerializer(equipement, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                    'message': 'the equipement updated successfully',
                    'data': serializer.data
                    },
                    status=status.HTTP_202_ACCEPTED
                )
            else:
                return Response(
                    {
                    'message': 'equipement field update! check your updated informations',
                    'errors': serializer.errors
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {
                    'message' : 'You must provide the id number to update an equipment'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

class StockApiView(APIView):
    queryset = models.Stock.objects.all()
    serializer_class = serializers.StockSerializer

    def get(self, request, pk=None):
        if pk:
            try:
                stock = models.Stock.objects.get(pk=pk)
            except models.Stock.DoesNotExist:
                return Response(
                    {
                    'message' : 'the equipement that you tryna access is not exist'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = serializers.StockSerializer(stock)
            return Response(serializer.data)
        else:
            stock = models.Stock.objects.all()
            serializer = serializers.StockSerializer(stock, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = serializers.StockSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                'messge' : 'new equipement created successfuly',
                'new equipement' : serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {
                'message' : 'Equipement field created',
                'errors' : serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, pk=None):
        if pk:
            try:
                stock = models.Stock.objects.get(pk=pk)
            except models.Stock.DoesNotExist:
                return Response(
                    {
                    'message' : 'the equipement that you tryna access is not exist'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            stock.delete()
            return Response(
                {
                'message' : 'the equipement deleted successfuly'
                },
                status=status.HTTP_204_NO_CONTENT
            )
        else:
            stock = models.Stock.objects.all()
            stock.delete()
            return Response(
                {
                'message' : 'all the equipements deleted successfully'
                },
                status=status.HTTP_204_NO_CONTENT
            )


class AffectationApiView(APIView):
    queryset = models.Affectation.objects.all()
    serializer_class = serializers.AffectationSerializer

    def get(self, request, pk=None):
        if pk:
            try:
                affect = models.Affectation.objects.get(pk=pk)
            except models.Affectation.DoesNotExist:
                return Response(
                    {
                    'message' : 'the affectation opperation that you tryna access is not exist'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = serializers.AffectationSerializer(affect)
            return Response(serializer.data)
        else:
            affect = models.Affectation.objects.all()
            serializer = serializers.AffectationSerializer(affect, many=True)
            return Response(serializer.data)

    def post(self, request):
        location_name =request.data.get('Location')
        if location_name.lower() in ['stock1','stock2','stock3','stock','stock4','stock5','stock6','stock7','stock8']:
            return Response(
                {
                    'message' : 'the equipement is usually on stock you should choose anouther location to run the affectation to !'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = serializers.AffectationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                'messge' : 'new affectation opperation run successfuly',
                'new affectation' : serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {
                'message' : 'affectation run failed',
                'errors' : serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, pk=None):
        if pk:
            try:
                affect = models.Affectation.objects.get(pk=pk)
            except models.Affectation.DoesNotExist:
                return Response(
                    {
                    'message' : 'the affectation that you tryna access is not exist'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            affect.delete()
            return Response(
                {
                'message' : 'the affectation deleted successfuly'
                },
                status=status.HTTP_204_NO_CONTENT
            )
        else:
            affect = models.Affectation.objects.all()
            affect.delete()
            return Response(
                {
                'message' : 'all the affectation deleted successfully'
                },
                status=status.HTTP_204_NO_CONTENT
            )

class InventoryApiView(APIView):
    queryset = models.Inventory.objects.all()
    serializer_class = serializers.InventorySerializer

    def get(self, request, pk=None):
        if pk:
            try:
                inventory = models.Inventory.objects.get(pk=pk)
            except models.Inventory.DoesNotExist:
                return Response(
                    {
                    'message' : 'the equipement that you tryna access is not exist'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = serializers.InventorySerializer(inventory)
            return Response(serializer.data)
        else:
            inventory = models.Inventory.objects.all()
            serializer = serializers.InventorySerializer(inventory, many=True)
            return Response(serializer.data)

    def delete(self, request, pk=None):
        if pk:
            try:
                inventory = models.Inventory.objects.get(pk=pk)
            except models.Inventory.DoesNotExist:
                return Response(
                    {
                    'message' : 'the equipement that you tryna access is not exist'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            inventory.delete()
            return Response(
                {
                'message' : 'the equipement deleted successfuly in the Inventory'
                },
                status=status.HTTP_204_NO_CONTENT
            )
        else:
            inventory = models.Inventory.objects.all()
            inventory.delete()
            return Response(
                {
                'message' : 'all the equipements deleted successfully in the Inventory'
                },
                status=status.HTTP_204_NO_CONTENT
            )

    def put(self, request, pk=None):
        if pk:
            try:
                equipement = models.Inventory.objects.get(pk=pk)
            except models.Inventory.DoesNotExist:
                return Response(
                    {
                        'message' : 'the equipement that you tryna access is not found'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = serializers.InventorySerializer(equipement, data=request.data, partial=True)
            if serializer.is_valid():
                # Update only the condition field
                equipement.condition = serializer.validated_data['condition']
                equipement.save()
                return Response(
                    {
                        'message': 'the equipement updated successfully'
                    },
                    status=status.HTTP_202_ACCEPTED
                )
            else:
                return Response(
                    {
                        'message': 'equipement field update! check your updated informations'
                    },
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {
                    'message' : 'You must provide the id number to update an equipment'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

class AllocationApiView(APIView):
    queryset = models.Allocation.objects.all()
    serializer_class = serializers.AllocationSerializer

    def get(self, request, pk=None):
        if pk:
            try:
                allocation = models.Allocation.objects.get(pk=pk)
            except models.Allocation.DoesNotExist:
                return Response(
                    {
                    'message' : 'the equipement that you tryna access is not exist'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = serializers.AllocationSerializer(allocation)
            return Response(serializer.data)
        else:
            allocation = models.Allocation.objects.all()
            serializer = serializers.AllocationSerializer(allocation, many=True)
            return Response(serializer.data)

    def delete(self, request, pk=None):
        if pk:
            try:
                allocation = models.Allocation.objects.get(pk=pk)
            except models.Allocation.DoesNotExist:
                return Response(
                    {
                    'message' : 'the equipement that you tryna access is not exist'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            allocation.delete()
            return Response(
                {
                'message' : 'the equipement deleted successfuly in the ITroom'
                },
                status=status.HTTP_204_NO_CONTENT
            )
        else:
            allocation = models.Allocation.objects.all()
            allocation.delete()
            return Response(
                {
                'message' : 'all the equipements deleted successfully in the ITroom'
                },
                status=status.HTTP_204_NO_CONTENT
            )

class AllocateApiView(APIView):
    queryset = models.Allocate.objects.all()
    serializer_class = serializers.AllocateSerializer

    def get(self, request, pk=None):
        if pk:
            try:
                allocate = models.Allocate.objects.get(pk=pk)
            except models.Allocate.DoesNotExist:
                return Response(
                    {
                    'message' : 'the allocation opperation that you tryna access is not exist'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = serializers.AllocateSerializer(allocate)
            return Response(serializer.data)
        else:
            allocate = models.Allocate.objects.all()
            serializer = serializers.AllocateSerializer(allocate, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = serializers.AllocateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                'messge' : 'new allocation request created successfuly wait until the admin accept',
                'new_request_allocation' : serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {
                'message' : 'Allocation request failed',
                'errors' : serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, pk=None):
        if pk:
            try:
                allocation = models.Allocate.objects.get(pk=pk)
            except models.Allocate.DoesNotExist:
                return Response(
                    {
                    'message' : 'the allocation request that you tryna access is not exist'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            allocation.delete()
            return Response(
                {
                'message' : 'the allocation request deleted successfuly'
                },
                status=status.HTTP_204_NO_CONTENT
            )
        else:
            allocation = models.Allocate.objects.all()
            allocation.delete()
            return Response(
                {
                'message' : 'all the allocations requestes deleted successfully'
                },
                status=status.HTTP_204_NO_CONTENT
            )

class NotificationStudentApiView(APIView):
    queryset = models.NotificationStudent.objects.all()
    serializer_class = serializers.NotificaionStudentSerializer

    def get(self, request, pk=None):
        if pk:
            try:
                notif = models.NotificationStudent.objects.get(pk=pk)
            except models.NotificationStudent.DoesNotExist:
                return Response(
                    {
                    'message' : 'the notification that you tryna access is not exist'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = serializers.NotificaionStudentSerializer(notif)
            return Response(serializer.data)
        else:
            notif = models.NotificationStudent.objects.all()
            serializer = serializers.NotificaionStudentSerializer(notif, many=True)
            return Response(serializer.data)

    def delete(self, request, pk=None):
        if pk:
            try:
                notif = models.NotificationStudent.objects.get(pk=pk)
            except models.Allocate.DoesNotExist:
                return Response(
                    {
                    'message' : 'the notification that you tryna access is not exist'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            notif.delete()
            return Response(
                {
                'message' : 'the notification deleted successfuly'
                },
                status=status.HTTP_204_NO_CONTENT
            )
        else:
            notif = models.NotificationStudent.objects.all()
            notif.delete()
            return Response(
                {
                'message' : 'all the notifications deleted successfully'
                },
                status=status.HTTP_204_NO_CONTENT
            )

class AcceptrequestApiView(APIView):
    queryset = models.Acceptrequest.objects.all()
    serializer_class = serializers.AcceptrequestSerializer

    def get(self, request, pk=None):
        if pk:
            try:
                notif = models.Acceptrequest.objects.get(pk=pk)
            except models.Acceptrequest.DoesNotExist:
                return Response(
                    {
                    'message' : 'the request that you tryna access is not exist'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = serializers.AcceptrequestSerializer(notif)
            return Response(serializer.data)
        else:
            notif = models.Acceptrequest.objects.all()
            serializer = serializers.AcceptrequestSerializer(notif, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = serializers.AcceptrequestSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                'message' : 'opperation succed',
                'data' : serializer.data
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                'message' : 'check your invalid information'
                },
                serializer.errors
            )

    def delete(self, request, pk=None):
        if pk:
            try:
                notif = models.Acceptrequest.objects.get(pk=pk)
            except models.Acceptrequest.DoesNotExist:
                return Response(
                    {
                    'message' : 'the opperation that you tryna access is not exist'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            notif.delete()
            return Response(
                {
                'message' : 'the opperation deleted successfuly'
                },
                status=status.HTTP_204_NO_CONTENT
            )
        else:
            notif = models.Acceptrequest.objects.all()
            notif.delete()
            return Response(
                {
                'message' : 'all the opperation deleted successfully'
                },
                status=status.HTTP_204_NO_CONTENT
            )

class NotificationManagerApiView(APIView):
    queryset = models.NotificationManager.objects.all()
    serializer_class = serializers.NotificationManagerSerializer

    def get(self, request, pk=None):
        if pk:
            try:
                notif = models.NotificationManager.objects.get(pk=pk)
            except models.NotificationManager.DoesNotExist:
                return Response(
                    {
                    'message' : 'the notification that you tryna access is not exist'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = serializers.NotificationManagerSerializer(notif)
            return Response(serializer.data)
        else:
            notif = models.NotificationManager.objects.all()
            serializer = serializers.NotificationManagerSerializer(notif, many=True)
            return Response(serializer.data)

    def delete(self, request, pk=None):
        if pk:
            try:
                notif = models.NotificationManager.objects.get(pk=pk)
            except models.NotificationManager.DoesNotExist:
                return Response(
                    {
                    'message' : 'the notification that you tryna access is not exist'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            notif.delete()
            return Response(
                {
                'message' : 'the notification deleted successfuly'
                },
                status=status.HTTP_204_NO_CONTENT
            )
        else:
            notif = models.NotificationManager.objects.all()
            notif.delete()
            return Response(
                {
                'message' : 'all the notifications deleted successfully'
                },
                status=status.HTTP_204_NO_CONTENT
            )

class ReservedEquipApiView(APIView):
    queryset = models.ReservedEquip.objects.all()
    serializer_class = serializers.ReservedEquipSerializer

    def get(self, request, pk=None):
        if pk:
            try:
                allocation = models.ReservedEquip.objects.get(pk=pk)
            except models.ReservedEquip.DoesNotExist:
                return Response(
                    {
                    'message' : 'the equipement that you tryna access is not exist'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = serializers.ReservedEquipSerializer(allocation)
            return Response(serializer.data)
        else:
            allocation = models.ReservedEquip.objects.all()
            serializer = serializers.ReservedEquipSerializer(allocation, many=True)
            return Response(serializer.data)

    def delete(self, request, pk=None):
        if pk:
            try:
                allocation = models.ReservedEquip.objects.get(pk=pk)
            except models.ReservedEquip.DoesNotExist:
                return Response(
                    {
                    'message' : 'the equipement that you tryna access is not exist'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            allocation.delete()
            return Response(
                {
                'message' : 'the equipement deleted successfuly in the ITroom'
                },
                status=status.HTTP_204_NO_CONTENT
            )
        else:
            allocation = models.ReservedEquip.objects.all()
            allocation.delete()
            return Response(
                {
                'message' : 'all the equipements deleted successfully in the ITroom'
                },
                status=status.HTTP_204_NO_CONTENT
            )