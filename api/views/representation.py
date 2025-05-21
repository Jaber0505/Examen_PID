from rest_framework import viewsets
from catalogue.models import Representation
from api.serializers.representation import RepresentationSerializer

class RepresentationViewSet(viewsets.ModelViewSet):
    queryset = Representation.objects.select_related('show', 'location')
    serializer_class = RepresentationSerializer
