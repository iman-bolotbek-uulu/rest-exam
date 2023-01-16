from django.shortcuts import render
from rest_framework import viewsets

from .models import Author
from .serializers import AuthorRegisterSerializer


class AuthorRegisterViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorRegisterSerializer



