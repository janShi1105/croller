from re import search
from django.shortcuts import render
from rest_framework import serializers, viewsets

from film import models

# Create your views here.

class LanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Language
        fields = '__all__'

class FilmSerializer(serializers.ModelSerializer):

    language = LanguageSerializer()

    class Meta:
        model = models.Film
        fields = '__all__'

class FilmViewSet(viewsets.ModelViewSet):
    queryset = models.Film.objects.all()

    serializer_class = FilmSerializer

    filter_fields = '__all__'
    ordering_fields = '__all__'
    search_fields = ('title', )
