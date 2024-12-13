import django.utils.timezone
import django.core.mail
from django.conf import settings
from django.db.models import QuerySet
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)
from rest_framework.request import Request
from rest_framework.response import Response

from email_templates.event_registration_template import (
    REGISTRATION_HTML_CONTENT,
)
from email_templates.event_cancel_registration_template import (
    CANCEL_REGISTRATION_HTML_CONTENT,
)
from email_templates.event_update_template import UPDATE_HTML_CONTENT
from events.filters import EventFilter
from events.models import Event
from events.permissions import IsOrganizerOrReadOnly
from events.schemas.events import event_schema
from events.serializers import (
    EventSerializer,
    EventListSerializer,
    EventCreateUpdateSerializer,
    EventRetrieveSerializer,
)


@event_schema
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOrganizerOrReadOnly]
    filterset_class = EventFilter

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

    def perform_update(self, serializer: EventCreateUpdateSerializer):
        event = self.get_object()
        updated_event = serializer.save()

        # Check if start_time, end_time, or location have changed
        if (
            updated_event.start_time != event.start_time
            or updated_event.end_time != event.end_time
            or updated_event.location != event.location
        ):
            # Sending email about update
            subject = f"Event {event.title} was updated"
            message = UPDATE_HTML_CONTENT.format(
                event=updated_event.title,
                start_time=updated_event.start_time.strftime("%d %b %Y %H:%M"),
                end_time=updated_event.end_time.strftime("%d %b %Y %H:%M"),
                location=updated_event.location,
                organizer_email=updated_event.organizer.email,
            )
            participant_emails = updated_event.participants.values_list(
                "email",
                flat=True,
            )
            django.core.mail.send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=participant_emails,
                fail_silently=True,
                html_message=message,
            )

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
        if event.participants.filter(id=request.user.id).exists():
            return Response(
                {"detail": "You are already registered for this event."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if the event started or is in the past
        if event.start_time < django.utils.timezone.now():
            return Response(
                {
                    "detail": "You cannot register for the event that have already started or is finished"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Sending email about successful registration
        subject = f"You are registered at {event.title}"
        message = REGISTRATION_HTML_CONTENT.format(
            username=request.user.username,
            event=event.title,
            start_time=event.start_time.strftime("%d %b %Y %H:%M"),
            end_time=event.end_time.strftime("%d %b %Y %H:%M"),
            location=event.location,
            organizer_email=event.organizer.email,
        )
        django.core.mail.send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[request.user.email],
            fail_silently=True,
            html_message=message,
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
        if not event.participants.filter(id=request.user.id).exists():
            return Response(
                {"detail": "You are not registered for this event."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Sending email about successful canceling of the registration
        subject = f"You've canceled you registration at {event.title}"
        message = CANCEL_REGISTRATION_HTML_CONTENT.format(
            username=request.user.username,
            event=event.title,
        )
        django.core.mail.send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[request.user.email],
            fail_silently=True,
            html_message=message,
        )

        # Unregister the user
        event.participants.remove(request.user)
        return Response(
            {"detail": "Successfully unregistered from the event."},
            status=status.HTTP_200_OK,
        )
