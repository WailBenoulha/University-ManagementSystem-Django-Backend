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

class Categorie_EquipementViewSets(viewsets.ViewSet):
    authentication_classes = ()
    serializer_class = serializers.Categorie_EquipementSerializer
    queryset = models.Categorie_Equipement.objects.all()

    def list(self, request, pk=None):
        if pk:
            categ = models.Categorie_Equipement.objects.get(pk=pk)
            serializer = serializers.Categorie_EquipementSerializer(categ)
            return Response(serializer.data)
        else:
            categ = models.Categorie_Equipement.objects.all()
            serializer = serializers.Categorie_EquipementSerializer(categ, many=True)
            return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status = status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, pk):
        try:
            categ = models.Categorie_Equipement.objects.get(pk=pk)
        except models.Categorie_Equipement.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        categ.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk):
        try:
            categ = models.Categorie_Equipement.objects.get(pk=pk)
        except models.Categorie_Equipement.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer = serializers.Categorie_EquipementSerializer(categ, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Your categorie equipement updated succesfully', 'Updated equipement':serializer.data})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class LoacationViewSets(viewsets.ViewSet):
    queryset = models.Location.objects.all()
    serializer_class = serializers.LocationSerializer

    def list(self, request, pk=None):
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

    def create(self, request):
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

    def update(self, request, pk):
        try:
            location = models.Location.objects.get(pk=pk)
        except models.Location.DoesNotExist:
            return Response(
               {
                'message' : 'the location that you tryna access is not exist'
               },
               status=status.HTTP_404_NOT_FOUND
            )
        serializer = serializers.LocationSerializer(location, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                'message' : 'location updated successfuly',
                'location updated' : serializer.data
                },
                status=status.HTTP_202_ACCEPTED
            )
        else:
            return Response(
                {
                'message' : 'location updated failed',
                'errors': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, pk):
        try:
            location = models.Location.objects.get(pk=pk)
        except models.Location.DoesNotExist:
            return Response(
                {
                'message' : 'the location that you tryna access is not exist'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        location.delete()
        return Response(
            {
            'message' : 'location deleted successfully'
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
