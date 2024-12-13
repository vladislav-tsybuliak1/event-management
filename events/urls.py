from rest_framework import routers

from events.views import EventViewSet


router = routers.DefaultRouter()
router.register(prefix="", viewset=EventViewSet, basename="event")

urlpatterns = router.urls

app_name = "events"
