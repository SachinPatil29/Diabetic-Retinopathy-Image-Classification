from rest_framework import serializers,validators
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Patient


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name','last_name','username','email','password')
        
        password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password')       
        
        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username=username,
            email= email, 
            password=password
        )
        user.set_password(password)
        user.save()
        return user
          
class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ('id', 'first_name', 'last_name', 'age', 'gender','phone_number','image', 'prediction')
            
            