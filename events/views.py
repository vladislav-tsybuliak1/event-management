from django.db.models import QuerySet
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)
from rest_framework.request import Request
from rest_framework.response import Response

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

    @action(
        detail=True,
        methods=["POST"],
        url_path="register",
        permission_classes=[IsAuthenticated],
    )
    def register(self, request: Request, pk: int | None = None) -> Response:
        """
        Custom action for registering a user to an event.
        """

        event = self.get_object()

        # Check if the user is organizer
        if request.user == event.organizer:
            return Response(
                {"detail": "You are the organizer of this event."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if the user is already registered
        if request.user in event.participants.all():
            return Response(
                {"detail": "You are already registered for this event."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Register the user
        event.participants.add(request.user)
        return Response(
            {"detail": "Successfully registered for the event."},
            status=status.HTTP_200_OK,
        )

    @action(
        detail=True,
        methods=["POST"],
        url_path="unregister",
        permission_classes=[IsAuthenticated],
    )
    def unregister(self, request: Request, pk: int | None = None) -> Response:
        """
        Custom action for unregistering a user from an event.
        """

        event = self.get_object()

        # Check if the user is not in event participants
        if request.user not in event.participants.all():
            return Response(
                {"detail": "You are not registered for this event."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Unregister the user
        event.participants.remove(request.user)
        return Response(
            {"detail": "Successfully unregistered from the event."},
            status=status.HTTP_200_OK,
        )
