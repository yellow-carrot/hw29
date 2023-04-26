from rest_framework.routers import SimpleRouter

from ads.views import CompilationViewSet

router = SimpleRouter()
router.register('', CompilationViewSet)

urlpatterns = []

urlpatterns += router.urls