from rest_framework import routers
from .views import UserViewset

router = routers.SimpleRouter()
router.register(r'', UserViewset)
urlpatterns = router.urls
