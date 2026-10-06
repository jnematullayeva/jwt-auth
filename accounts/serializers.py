from rest_framework import serializers
from .models import CustomUser
from rest_framework.exceptions import ValidationError
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class  SignUpSerilazer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    confirm_password = serializers.CharField(write_only = True)
    id = serializers.CharField(read_only = True)



    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name','addres','email', 'username', 'password', 'confirm_password',]

    def validate_password(self, value):
        if len(value) < 8:
            raise ValidationError({
                "msg": "Parol kamida 8 ta belgidan iborat bo'lishi shart.",
                "status": status.HTTP_400_BAD_REQUEST
            })

        if value[0].isdigit():
            raise ValidationError({
                "msg": "Parol raqam bilan boshlanishi mumkin emas.",
                "status": status.HTTP_400_BAD_REQUEST
            })

        return value
    def validate(self, data):
       password = data.get('password')
       confirm_password = data.get('confirm_password')

       if password and confirm_password and password != confirm_password:
           raise ValidationError({
               'msg': 'parollar mos emas',
               'status':status.HTTP_400_BAD_REQUEST
                                  })
       return data
       
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        users = CustomUser.objects.create_user(**validated_data)


        return users
    
    def to_representation(self, instance):
        users =  super().to_representation(instance)

        users['status']= status.HTTP_201_CREATED
        users['msg'] = 'User muaffaqiyatli yaratildi'
        return users

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)

        if not user:
            raise ValidationError({
                "msg": "Login yoki parol xato",
                "status": status.HTTP_400_BAD_REQUEST
            })

        data["user"] = user
        return data

    def to_representation(self, instance):
        user = instance["user"]

        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
    
class PasswordChangeSerilazer(serializers.Serializer):
    old_pass = serializers.CharField(write_only = True)
    new_pass = serializers.CharField(write_only = True)
    conf_pass = serializers.CharField(write_only = True)


    def validate(self, attrs):
            old_pass = attrs.get('old_pass')
            new_pass = attrs.get('new_pass')
            conf_pass = attrs.get('conf_pass')


            if old_pass and new_pass and conf_pass and new_pass == old_pass:

                raise ValidationError({
                    'msg': "Yangi parol eskisi bilan bir xil bo'lishi mumkin emas",
                    'status': status.HTTP_400_BAD_REQUEST
                })
            
            if old_pass and new_pass and conf_pass and new_pass != conf_pass:
                    
                    raise ValidationError({
                        'msg': 'Yangi parollar mos emas',
                        'status': status.HTTP_400_BAD_REQUEST
                    })
            

            request = self.context['request']

            user = authenticate(username = request.user.username, password = old_pass)

            if not user:
                raise ValidationError({
                        'msg': 'Eski parol xato',
                        'status': status.HTTP_400_BAD_REQUEST
                    })
        
            return attrs


    def update(self, instance, validated_data):

        instance.set_password(validated_data.get('new_pass'))
        instance.save()

        return instance
    

    def to_representation(self, instance):
        return{
            'msg': "Parollar o'zgartirildi",
            'status': status.HTTP_200_OK
        }
    

        
class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'address']
    
    def validate(self, attrs):
        username = attrs.get('username')
        
        if username[0].isdigit():
            raise ValidationError({
                'msg': "Username raqam bilan boshlanishi mumkin emas!",
                'status': status.HTTP_400_BAD_REQUEST
            })
        
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError({
                'msg': "Bazada bu username mavjud!",
                'status': status.HTTP_400_BAD_REQUEST
            })
        
        
        return attrs        
        
    
    def update(self, instance, validated_data):
        
        instance.save()
        
        return instance
    
    
    def to_representation(self, instance):
        
        return {
            'msg': 'Profil yangilandi!',
            'status': status.HTTP_200_OK,
            'data': instance.validated_data
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate_refresh(self, value):
        if not value:
            raise serializers.ValidationError("Refresh token yuborilmadi.")
        return value