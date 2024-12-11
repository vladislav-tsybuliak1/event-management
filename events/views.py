from rest_framework import viewsets

from events.models import Event
from events.serializers import EventSerializer, EventListSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_serializer_class(self) -> type[EventSerializer]:
        if self.action == "list":
            return EventListSerializer
        return self.serializer_class

