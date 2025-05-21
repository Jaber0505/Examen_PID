from rest_framework import serializers
from catalogue.models import Representation

class RepresentationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Representation
        fields = ['id', 'show', 'when', 'location', 'capacity', 'places_restantes']
        read_only_fields = ['places_restantes']
