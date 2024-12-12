from django.db.models import QuerySet
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from events.models import Event
from events.permissions import IsOrganizerOrReadOnly
from events.serializers import (
    EventSerializer,
    EventListSerializer,
    EventCreateUpdateSerializer,
    EventRetrieveSerializer,
)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOrganizerOrReadOnly]

    def get_serializer_class(self) -> type[EventSerializer]:
        if self.action == "list":
            return EventListSerializer
        if self.action == "retrieve":
            return EventRetrieveSerializer
        if self.action in ["create", "update", "partial_update"]:
            return EventCreateUpdateSerializer
        return self.serializer_class

    def get_queryset(self) -> QuerySet:
        if self.action in ["list", "retrieve"]:
            self.queryset = self.queryset.select_related(
                "organizer"
            ).prefetch_related("participants")
        return self.queryset

    def perform_create(self, serializer: EventCreateUpdateSerializer):
        serializer.save(organizer=self.request.user)
