from rest_framework.routers import DefaultRouter
from .views import ArtistViewSet, RepresentationViewSet

router = DefaultRouter()
router.register(r'artists', ArtistViewSet, basename='artist')
router.register(r'representations', RepresentationViewSet, basename='representation')

urlpatterns = router.urls
