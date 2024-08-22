from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializers import UserSerializer

User = get_user_model()

class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _created = Token.objects.get_or_create(user=user)
            return Response({
                'token': str(token.key),
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    authentication_classes = [TokenAuthentication]
    
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            token, _created = Token.objects.get_or_create(user=user)
            return Response({
                'token': str(token.key),
                'user': UserSerializer(user).data
            })
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        print(f"User: {user}")
        print(f"User ID: {user.id}")
        
        user_details = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_superuser': user.is_superuser,
            'is_staff': user.is_staff,
            'user_type': user.user_type,
        }
        return Response(user_details)

class VerifyTokenView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Token '):
            return Response({'valid': False}, status=status.HTTP_400_BAD_REQUEST)
        
        token = auth_header.split(' ')[1]
        try:
            Token.objects.get(key=token)
            return Response({'valid': True}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({'valid': False}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        token = request.auth
        if token:
            token.delete()
            return Response({'detail': 'Successfully logged out'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'No token to delete'}, status=status.HTTP_400_BAD_REQUEST)

