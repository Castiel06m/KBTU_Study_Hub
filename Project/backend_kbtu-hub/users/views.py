from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegisterSerializer
from api.serializers import UserSerializer

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny]) 
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    """Возвращает данные текущего авторизованного пользователя"""
    # Мы используем UserSerializer, чтобы отдать id, username и role
    from api.serializers import UserSerializer 
    serializer = UserSerializer(request.user)
    return Response(serializer.data)