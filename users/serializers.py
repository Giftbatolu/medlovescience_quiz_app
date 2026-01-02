from rest_framework import serializers
from . models import CustomUser

class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('username','email', 'role', 'password')

    def create(self, validated_data):
      user = CustomUser.objects.create_user(
          username=validated_data['username'],
          email=validated_data['email'],
          password=validated_data['password'],
          role=validated_data.get('role', 'student')
      )
      return user