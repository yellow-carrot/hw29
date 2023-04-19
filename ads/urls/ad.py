from rest_framework.routers import SimpleRouter

from ads.views import AdViewSet

router = SimpleRouter()
router.register('', AdViewSet)

urlpatterns = []

urlpatterns += router.urls
