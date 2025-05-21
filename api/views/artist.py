from rest_framework import viewsets
from catalogue.models import Artist
from api.serializers.artist import ArtistSerializer

class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
