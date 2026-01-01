from django.shortcuts import render
from . serializers import RegisterUserSerializer
from rest_framework import generics

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterUserSerializer
    # permission_classes = []

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {"message": "User registered successfully"}
        return response