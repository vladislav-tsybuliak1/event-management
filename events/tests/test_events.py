from datetime import datetime
from unittest import mock

from django.contrib.auth import get_user_model
from django.db.models import QuerySet, Case, When, Value, IntegerField
from django.test import TestCase
import django.utils.timezone
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from events.models import Event
from events.serializers import EventListSerializer, EventRetrieveSerializer
from events.views import EventViewSet


EVENT_URL = reverse("events:event-list")
PAGE_SIZE = EventViewSet.pagination_class.page_size
NOW_MOCKED_VALUE = django.utils.timezone.make_aware(
    datetime(2024, 12, 13, 10, 0, 0),
    django.utils.timezone.get_current_timezone(),
)


def detail_url(event_id: int) -> str:
    return reverse("events:event-detail", args=[event_id])


def annotate_priority(queryset: QuerySet, *ordering) -> QuerySet:
    if not ordering:
        ordering = ["start_time"]
    else:
        ordering = ordering
    return queryset.annotate(
        is_upcoming=Case(
            When(start_time__gte=django.utils.timezone.now(), then=Value(0)),
            default=Value(1),
            output_field=IntegerField(),
        )
    ).order_by("is_upcoming", *ordering)


class NotAuthenticatedEventApiTests(TestCase):
    fixtures = ["events/tests/fixtures/events_data.json"]

    def setUp(self) -> None:
        self.client = APIClient()
        self.payload = {
            "title": "Product Launch",
            "description": "Official launch event for the company's new product.",
            "start_time": "2026-03-30T14:00:00",
            "end_time": "2026-03-30T17:00:00",
            "location": "Main Auditorium",
        }
        self.event = Event.objects.filter(
            start_time__gt=NOW_MOCKED_VALUE
        ).first()

    @mock.patch("django.utils.timezone.now", return_value=NOW_MOCKED_VALUE)
    def test_get_events_list(self, mocked_now) -> None:
        response = self.client.get(EVENT_URL)
        events = annotate_priority(
            Event.objects.all(),
        )[:PAGE_SIZE]
        serializer = EventListSerializer(events, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    @mock.patch("django.utils.timezone.now", return_value=NOW_MOCKED_VALUE)
    def test_get_events_list_filter_by_title(self, mocked_now) -> None:
        title = "party"
        response = self.client.get(EVENT_URL, {"title": title})
        events = annotate_priority(
            Event.objects.filter(title__icontains=title)
        )[:PAGE_SIZE]
        serializer = EventListSerializer(events, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    @mock.patch("django.utils.timezone.now", return_value=NOW_MOCKED_VALUE)
    def test_get_events_list_filter_by_location(self, mocked_now) -> None:
        location = "room"
        response = self.client.get(EVENT_URL, {"location": location})
        events = annotate_priority(
            Event.objects.filter(location__icontains=location)
        )[:PAGE_SIZE]
        serializer = EventListSerializer(events, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    @mock.patch("django.utils.timezone.now", return_value=NOW_MOCKED_VALUE)
    def test_get_events_list_filter_by_start_time(self, mocked_now) -> None:
        start_date = "2024-12-13"
        response = self.client.get(EVENT_URL, {"start_date": start_date})
        events = annotate_priority(
            Event.objects.filter(start_time__date=start_date)
        )[:PAGE_SIZE]
        serializer = EventListSerializer(events, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    @mock.patch("django.utils.timezone.now", return_value=NOW_MOCKED_VALUE)
    def test_get_events_list_filter_by_organizer(self, mocked_now) -> None:
        organizer = "Digital_Dragon"
        response = self.client.get(EVENT_URL, {"organizer": organizer})
        events = annotate_priority(
            Event.objects.filter(organizer__username__icontains=organizer)
        )[:PAGE_SIZE]
        serializer = EventListSerializer(events, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    @mock.patch("django.utils.timezone.now", return_value=NOW_MOCKED_VALUE)
    def test_get_events_list_filter_by_organizing_events(
        self, mocked_now
    ) -> None:
        organizing = True
        response = self.client.get(EVENT_URL, {"organizing": organizing})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)

    @mock.patch("django.utils.timezone.now", return_value=NOW_MOCKED_VALUE)
    def test_get_events_list_filter_by_participating_events(
        self, mocked_now
    ) -> None:
        participating = True
        response = self.client.get(EVENT_URL, {"participating": participating})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)

    @mock.patch("django.utils.timezone.now", return_value=NOW_MOCKED_VALUE)
    def test_get_events_list_ordering_by_title(self, mocked_now) -> None:
        ordering_options = [
            "title",
            "-title",
            "location",
            "-location",
            "start_time",
            "-start_time",
        ]

        for ordering in ordering_options:
            with self.subTest(ordering=ordering):
                response = self.client.get(EVENT_URL, {"ordering": ordering})

                self.assertEqual(response.status_code, status.HTTP_200_OK)
                events = annotate_priority(Event.objects.all(), ordering)[
                    :PAGE_SIZE
                ]
                serializer = EventListSerializer(events, many=True)

                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(response.data["results"], serializer.data)

    def test_create_event_error(self) -> None:
        response = self.client.post(EVENT_URL, self.payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_event(self) -> None:
        response = self.client.get(detail_url(self.event.id))
        serializer = EventRetrieveSerializer(self.event)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_event_error(self) -> None:
        response = self.client.put(detail_url(self.event.id), self.payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_partially_update_event_error(self) -> None:
        response = self.client.patch(detail_url(self.event.id), self.payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_partially_destroy_event_error(self) -> None:
        response = self.client.delete(detail_url(self.event.id))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedEventApiTests(TestCase):
    fixtures = ["events/tests/fixtures/events_data.json"]

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.get(pk=1)
        self.client.force_authenticate(self.user)
        self.payload = {
            "title": "Product Launch",
            "description": "Official launch event for the company's new product.",
            "start_time": "2026-03-30 14:00",
            "end_time": "2026-03-30 17:00",
            "location": "Main Auditorium",
        }
        self.updated_payload = {
            "title": "Updated Title",
            "description": "Updated Description",
            "start_time": "2025-12-13 14:00",
            "end_time": "2025-12-13 17:00",
            "location": "Updated Location",
        }
        self.partial_updated_payload = {
            "start_time": "2025-01-13 14:00",
            "end_time": "2025-01-13 17:00",
        }
        self.own_event = Event.objects.filter(
            organizer=self.user, start_time__gt=NOW_MOCKED_VALUE
        ).first()
        self.not_own_event = (
            Event.objects.filter(start_time__gt=NOW_MOCKED_VALUE)
            .exclude(organizer=self.user)
            .first()
        )

    @mock.patch("django.utils.timezone.now", return_value=NOW_MOCKED_VALUE)
    def test_get_events_list_filter_by_organizing_events(
        self, mocked_now
    ) -> None:
        organizing = True
        response = self.client.get(EVENT_URL, {"organizing": organizing})
        events = annotate_priority(Event.objects.filter(organizer=self.user))[
            :PAGE_SIZE
        ]
        serializer = EventListSerializer(events, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    @mock.patch("django.utils.timezone.now", return_value=NOW_MOCKED_VALUE)
    def test_get_events_list_filter_by_participating_events(
        self, mocked_now
    ) -> None:
        participating = True
        response = self.client.get(EVENT_URL, {"participating": participating})
        events = annotate_priority(
            Event.objects.filter(participants=self.user)
        )[:PAGE_SIZE]
        serializer = EventListSerializer(events, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    @mock.patch("django.utils.timezone.now", return_value=NOW_MOCKED_VALUE)
    def test_create_event(self, mocked_now) -> None:
        response = self.client.post(EVENT_URL, self.payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        event = Event.objects.get(id=response.data["id"])
        self.assertEqual(self.payload["title"], event.title)
        self.assertEqual(self.payload["description"], event.description)
        self.assertEqual(self.payload["location"], event.location)
        self.assertEqual(
            self.payload["start_time"],
            event.start_time.strftime("%Y-%m-%d %H:%M"),
        )
        self.assertEqual(
            self.payload["end_time"],
            event.end_time.strftime("%Y-%m-%d %H:%M"),
        )
        self.assertEqual(self.user.id, event.organizer_id)

    @mock.patch("django.utils.timezone.now", return_value=NOW_MOCKED_VALUE)
    def test_create_event_with_empty_fields(self, mocked_now) -> None:
        response = self.client.post(EVENT_URL)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @mock.patch("django.utils.timezone.now", return_value=NOW_MOCKED_VALUE)
    def test_create_event_overlapping_time_and_location(
        self, mocked_now
    ) -> None:
        response = self.client.post(EVENT_URL, self.payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(EVENT_URL, self.payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @mock.patch("django.utils.timezone.now", return_value=NOW_MOCKED_VALUE)
    def test_create_event_in_the_past(self, mocked_now) -> None:
        self.payload["start_time"] = "2023-12-13 12:00"
        response = self.client.post(EVENT_URL, self.payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @mock.patch("django.utils.timezone.now", return_value=NOW_MOCKED_VALUE)
    def test_create_event_with_end_time_before_start_time(
        self, mocked_now
    ) -> None:
        self.payload["start_time"] = "2025-12-13 12:00"
        self.payload["end_time"] = "2025-12-13 11:00"
        response = self.client.post(EVENT_URL, self.payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @mock.patch("django.core.mail.send_mail")
    @mock.patch("django.utils.timezone.now", return_value=NOW_MOCKED_VALUE)
    def test_update_own_event_sends_email(
        self,
        mocked_now,
        mocked_send_mail,
    ) -> None:
        response = self.client.put(
            detail_url(self.own_event.id), self.updated_payload
        )
        self.own_event.refresh_from_db()

        mocked_send_mail.assert_called_once()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.updated_payload["title"], self.own_event.title)
        self.assertEqual(
            self.updated_payload["description"], self.own_event.description
        )
        self.assertEqual(self.updated_payload["location"], self.own_event.location)
        self.assertEqual(
            self.updated_payload["start_time"],
            self.own_event.start_time.strftime("%Y-%m-%d %H:%M"),
        )
        self.assertEqual(
            self.updated_payload["end_time"],
            self.own_event.end_time.strftime("%Y-%m-%d %H:%M"),
        )
        self.assertEqual(self.user.id, self.own_event.organizer_id)

    @mock.patch("django.core.mail.send_mail")
    @mock.patch("django.utils.timezone.now", return_value=NOW_MOCKED_VALUE)
    def test_update_not_own_event_forbidden(
            self,
            mocked_now,
            mocked_send_mail,
    ) -> None:
        response = self.client.put(
            detail_url(self.not_own_event.id), self.updated_payload
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @mock.patch("django.core.mail.send_mail")
    @mock.patch("django.utils.timezone.now", return_value=NOW_MOCKED_VALUE)
    def test_partially_update_own_event_sends_email(
            self,
            mocked_now,
            mocked_send_mail,
    ) -> None:
        response = self.client.patch(
            detail_url(self.own_event.id), self.partial_updated_payload
        )
        self.own_event.refresh_from_db()

        mocked_send_mail.assert_called_once()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            self.partial_updated_payload["start_time"],
            self.own_event.start_time.strftime("%Y-%m-%d %H:%M"),
        )
        self.assertEqual(
            self.partial_updated_payload["end_time"],
            self.own_event.end_time.strftime("%Y-%m-%d %H:%M"),
        )

    @mock.patch("django.core.mail.send_mail")
    @mock.patch("django.utils.timezone.now", return_value=NOW_MOCKED_VALUE)
    def test_partially_update_own_event_forbidden(
            self,
            mocked_now,
            mocked_send_mail,
    ) -> None:
        response = self.client.put(
            detail_url(self.not_own_event.id), self.partial_updated_payload
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @mock.patch("django.utils.timezone.now", return_value=NOW_MOCKED_VALUE)
    def test_delete_own_event(self, mocked_now) -> None:
        response = self.client.delete(detail_url(self.own_event.id))
        event_exists = Event.objects.filter(id=self.own_event.id).exists()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(event_exists)

    @mock.patch("django.utils.timezone.now", return_value=NOW_MOCKED_VALUE)
    def test_delete_not_own_event_forbidden(self, mocked_now) -> None:
        response = self.client.delete(detail_url(self.not_own_event.id))
        event_exists = Event.objects.filter(id=self.not_own_event.id).exists()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(event_exists)
