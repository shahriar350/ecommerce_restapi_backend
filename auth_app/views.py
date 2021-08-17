from django.contrib.auth import authenticate, login, logout

# Create your views here.
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from auth_app.serializers import UserSerializer, SellerRequestSerializer, SingleUserSerializer


@api_view(['GET', 'POST'])
def seller_request(request):
    if request.method == 'POST':
        serializer = SellerRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)


@api_view(['POST'])
def seller_login(request):
    if request.method == 'POST':
        serializer = SingleUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        number = serializer.validated_data['phone_number']
        password = serializer.validated_data['password']
        user = authenticate(username=number, password=password)
        if user and user.is_seller:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        else:
            raise ValidationError('Please provide correct credential')


@api_view(['GET'])
def get_user(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_now(request):
    if request.method == 'POST':
        logout(request)
        return Response(status=status.HTTP_200_OK)


@ensure_csrf_cookie
@api_view(['GET'])
def login_set_cookie(request):
    if request.method == 'GET':
        return Response(status=status.HTTP_200_OK)
