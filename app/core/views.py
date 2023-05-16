from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from core import serializers
from core import models
from django.http import Http404
from rest_framework.decorators import api_view
import genericpath
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.authentication import TokenAuthentication
from core import permissions
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsResearcher, IsAdmin, IsAllocationManager, IsPrincipalManager, IsStudent, IsAdminOrIsStudent, IsAdminOrIsAllocationManager, IsAdminOrIsPrincipalManager, IsAdminOrIsResearcher, IsAllocationManagerOrIsStudentOrIsResearcher, IsStudentOrResearcher
from rest_framework.decorators import permission_classes

from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.backends.db import SessionStore

class UserViewsets(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()

class AdminViewsets(viewsets.ModelViewSet):
    serializer_class = serializers.AdminSerializer
    queryset = models.User.objects.filter(role='Admin')
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)

class PrincipalmanagerViewsets(viewsets.ModelViewSet):
    serializer_class = serializers.PrincipalmanagerSerializer
    queryset = models.User.objects.filter(role='Principalmanager')

class AllocationmanagerViewsets(viewsets.ModelViewSet):
    serializer_class = serializers.AllocationmanagerSerializer
    queryset = models.User.objects.filter(role='Allocationmanager')

class StudentViewsets(viewsets.ModelViewSet):
    serializer_class = serializers.StudentSerializer
    queryset = models.User.objects.filter(role='Student')
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsStudent]

class ResearcherViewsets(viewsets.ModelViewSet):
    serializer_class = serializers.ResearcherSerializer
    queryset = models.User.objects.filter(role='Researcher')
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsResearcher | IsAdmin]

class UserLoginApiView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    @method_decorator(csrf_exempt)  # Disable CSRF protection for this view
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = response.data['token']
        user = self.get_user(request, token)

        if user:
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            session = self.create_session(request, user)
            response.set_cookie('sessionid', session.session_key)

            data = {
                'token': token,
                'role': user.role,
                'name': user.name,
                'email': user.email,
                'lastname': user.lastname,
                'phonenumber': user.phonenumber,
                'national_card_number': user.national_card_number,
                'address': user.address,
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    def get_user(self, request, token):
        # Implement your logic to retrieve the user based on the token
        try:
            token_obj = Token.objects.get(key=token)
            user = token_obj.user
            return user
        except Token.DoesNotExist:
            return None

    def create_session(self, request, user):
        session = SessionStore()
        session.create()
        session['user_id'] = user.id
        session['role'] = user.role
        session.save()
        return session


class Categorie_EquipementApiView(APIView):
    serializer_class = serializers.Categorie_EquipementSerializer
    queryset = models.Categorie_Equipement.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAdmin()]
        elif self.request.method == 'POST':
            return [IsAdmin()]
        elif self.request.method == 'PUT':
            return [IsAdmin()]
        elif self.request.method == 'DELETE':
            return [IsAdmin()]
        else:
            return []

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

    def post(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)
        if pk:
            return Response(
                {
                    'message' : 'you cant add a new categorie inside this categorie you gotta move to the general page'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
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

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAdmin()]
        elif self.request.method == 'POST':
            return [IsAdmin()]
        elif self.request.method == 'PUT':
            return [IsAdmin()]
        elif self.request.method == 'DELETE':
            return [IsAdmin()]
        else:
            return []

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

    def post(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)

        if pk:
            return Response(
                {
                    'message' : 'you cant add a new location inside this existing location you gotta move to the general page'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
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
                    'message': 'location fail to update! check your updated informations',
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

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsPrincipalManager()]
        elif self.request.method == 'PUT':
            return [IsPrincipalManager()]
        elif self.request.method == 'DELETE':
            return [IsPrincipalManager()]
        else:
            return []

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

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsPrincipalManager()]
        elif self.request.method == 'POST':
            return [IsPrincipalManager()]
        elif self.request.method == 'DELETE':
            return [IsPrincipalManager()]
        else:
            return []

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

    def post(self, request, pk=None):
        serializer = serializers.StockSerializer(data=request.data)
        if pk:
            return Response(
                {
                    'message' : 'you cannot create a new equipement inside an existing equipement'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            if models.Location.objects.filter(type='stocks').exists():
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
            else:
                return Response(
                    {
                        'message' : 'there is no stock in locations wait until the admin create it'
                    },
                    status=status.HTTP_404_NOT_FOUND
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

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsPrincipalManager()]
        elif self.request.method == 'POST':
            return [IsPrincipalManager()]
        elif self.request.method == 'DELETE':
            return [IsPrincipalManager()]
        else:
            return []

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

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAdminOrIsPrincipalManager()]
        elif self.request.method == 'PUT':
            return [IsPrincipalManager()]
        elif self.request.method == 'DELETE':
            return [IsPrincipalManager()]
        else:
            return []

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
            condition = request.data.get('condition')
            if condition == 'new':
                return Response(
                    {
                        'message' : 'You cant update the condition to <new>! the condition <new> only defined automatically on stock'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
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

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAllocationManagerOrIsStudentOrIsResearcher()]
        elif self.request.method == 'DELETE':
            return [IsAllocationManager()]
        else:
            return []

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

    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [IsStudentOrResearcher()]
    #     elif self.request.method == 'POST':
    #         return [IsStudentOrResearcher()]
    #     elif self.request.method == 'DELETE':
    #         return [IsStudentOrResearcher()]
    #     else:
    #         return []

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

        if request.data.get('reference') is None:
            return Response(
                {
                    'meassage' : 'there is no equipement to allocate'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
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

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAllocationManager()]
        elif self.request.method == 'DELETE':
            return [IsAllocationManager()]
        else:
            return []

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

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAllocationManager()]
        elif self.request.method == 'POST':
            return [IsAllocationManager()]
        elif self.request.method == 'DELETE':
            return [IsAllocationManager()]
        else:
            return []

    def get(self, request, pk=None):
        if pk:
            try:
                notif = models.Acceptrequest.objects.get(pk=pk)
            except models.Acceptrequest.DoesNotExist:
                return Response(
                    {
                    'message' : 'the request that you tryna access does not exist'
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
                'message' : 'you dont have any allocation request to accept or refuse wait til someone request an allocation',
                'error' : serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
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

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsStudentOrResearcher()]
        elif self.request.method == 'DELETE':
            return [IsStudentOrResearcher()]
        else:
            return []

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

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAllocationManagerOrIsStudentOrIsResearcher()]
        elif self.request.method == 'DELETE':
            return [IsAllocationManagerOrIsStudentOrIsResearcher()]
        else:
            return []

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

class ReturnEquipementApiview(APIView):
    queryset = models.ReturnEquipement.objects.all()
    serializer_class = serializers.ReturnEquipementSerializer

    def get(self, request, pk=None):
        if pk:
            try:
                equip = models.ReturnEquipement.objects.get(pk=pk)
            except models.ReturnEquipement.DoesNotExist:
                return Response(
                    {
                    'message' : 'the opperation that you tryna access is not exist'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = serializers.ReturnEquipementSerializer(equip)
            return Response(serializer.data)
        else:
            equip = models.ReturnEquipement.objects.all()
            serializer = serializers.ReturnEquipementSerializer(equip, many=True)
            return Response(serializer.data)

    def post(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)
        if pk: return Response(
                {
                    'message' : 'opperation invalid'
                },
                status=status.HTTP_400_BAD_REQUEST
        )
        else:
            if request.data.get('Equipement') is None:
                return Response(
                {
                    'meassage' : 'there is no reserved equipement to return'
                },
                status=status.HTTP_400_BAD_REQUEST
                )
            else:
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        {
                        'message' : 'Reserved Equipement returned successfully to ITroom',
                        'opperation' : serializer.data
                        },
                        status= status.HTTP_201_CREATED
                    )
                else:
                    return Response(
                        {
                        'message' : 'opperation invalid',
                        'errors' : serializer.errors
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

class AllocationEquipementsApiView(APIView):
    serializer_class = serializers.InventorySerializer

    def get(self, request, pk=None):
        if pk:
            try:
                typelocation = models.Location.objects.get(type='reservation_room')
                equip = models.Inventory.objects.get(Location=typelocation, pk=pk)
            except models.Inventory.DoesNotExist:
                return Response(
                    {
                    'message' : 'the equipement that you tryna access is not exist'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = serializers.InventorySerializer(equip)
            return Response(serializer.data)
        else:
            typelocation = models.Location.objects.filter(type='reservation_room')
            equip = models.Inventory.objects.filter(Location__in=typelocation)
            serializer = serializers.InventorySerializer(equip, many=True)
            return Response(serializer.data)

# class AllocateEquipementsApiView(APIView):
#     queryset = models.AllocateEquipements.objects.all()
#     serializer_class = serializers.AllocateEquipementsSerializer

#     def get(self, request, pk=None):
#         if pk:
#             try:
#                 allocate = models.AllocateEquipements.objects.get(pk=pk)
#             except models.Allocate.DoesNotExist:
#                 return Response(
#                     {
#                     'message' : 'the allocation opperation that you tryna access is not exist'
#                     },
#                     status=status.HTTP_404_NOT_FOUND
#                 )
#             serializer = serializers.AllocateEquipementsSerializer(allocate)
#             return Response(serializer.data)
#         else:
#             allocate = models.AllocateEquipements.objects.all()
#             serializer = serializers.AllocateEquipementsSerializer(allocate, many=True)
#             return Response(serializer.data)

#     def post(self, request):
#         serializer = serializers.AllocateEquipementsSerializer(data=request.data)

#         # if request.data.get('reference') is None:
#         #     return Response(
#         #         {
#         #             'meassage' : 'there is no equipement to allocate'
#         #         },
#         #         status=status.HTTP_400_BAD_REQUEST
#         #     )
#         # else:
#         if serializer.is_valid():
#                 serializer.save()
#                 return Response(
#                     {
#                     'messge' : 'new allocation request created successfuly wait until the admin accept',
#                     'new_request_allocation' : serializer.data
#                     },
#                     status=status.HTTP_201_CREATED
#                 )
#         else:
#                 return Response(
#                     {
#                     'message' : 'Allocation request failed',
#                     'errors' : serializer.errors
#                     },
#                     status=status.HTTP_400_BAD_REQUEST
#                 )