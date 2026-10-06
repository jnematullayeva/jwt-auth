from django.shortcuts import render
from .serializers import SignUpSerilazer,LoginSerializer,PasswordChangeSerilazer,ProfileUpdateSerializer, LogoutSerializer
from rest_framework.views import APIView
from rest_framework import permissions , status
from .models import CustomUser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

class SignUpView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serilazers = SignUpSerilazer(data = request.data)
        serilazers.is_valid(raise_exception=True)
        serilazers.save()

        return Response(serilazers.data)
    

class LoginView(APIView):
    def post(self, request):
        serilazers = LoginSerializer(data = request.data)
        serilazers.is_valid(raise_exception=True)
       

        return Response(serilazers.data)
    

class ProfilView(APIView):
    def get(self, request):

        user = request.user

        return Response({
            'msg': 'Profil',
            'status': status.HTTP_200_OK,
            'user':{
                'id': user.id,
                'username': user.username,
                'address': user.address,
                'first_name':user.first_name,
                'last_name':user.last_name,
                'email': user.email,


            }
        })

class PasswordChangeView(APIView):
    def patch(self, request):
        serilazers = PasswordChangeSerilazer(instance = request.user , data = request.data , partial = True, context={"request": request})
        serilazers.is_valid(raise_exception=True)
        serilazers.save()
        return Response(serilazers.data)
    


class ProfileUpdateView(APIView):
    def patch(self, request):
        serializer = ProfileUpdateSerializer(instance=request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class TokenRefresh(APIView):
    permission_classes=[permissions.AllowAny]


    def get(self, request):
        refresh = request.data.get('refresh')
        refresh_token = RefreshToken(refresh)

        return Response({
            'access_token': str(refresh_token.access_token)
        })
    



class LogoutView(APIView):

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Tizimdan muvaffaqiyatli chiqildi."},
            status=status.HTTP_200_OK
        )